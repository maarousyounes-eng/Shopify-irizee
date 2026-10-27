/**
 * Analyse d'une photo de peau pour le diagnostic Irizée.
 *
 * Pourquoi cette fonction existe : la clé d'API ne peut pas vivre dans le
 * thème, qui est public. Tout ce qui touche à la clé passe donc ici.
 *
 * Ce qu'elle ne fait pas, volontairement :
 *   - elle n'écrit la photo nulle part, ni disque ni base ni journal ;
 *   - elle ne renvoie aucune description de la personne, seulement trois
 *     notes sur ce qui est visible ;
 *   - elle ne pose pas de diagnostic médical et le modèle a pour consigne
 *     de refuser si la demande glisse vers là.
 *
 * Variables d'environnement attendues :
 *   ANTHROPIC_API_KEY     la clé, posée dans Vercel, jamais dans le dépôt
 *   ORIGINES_AUTORISEES   domaines séparés par des virgules
 *   MODELE                facultatif, par défaut claude-sonnet-5-5
 */

const MODELE_PAR_DEFAUT = 'claude-sonnet-5-5';
const TYPES_ACCEPTES = ['image/jpeg', 'image/png', 'image/webp'];
const TAILLE_MAX = 4 * 1024 * 1024; // 4 Mo une fois décodé

const CONSIGNE = `Tu observes une photo de visage pour une boutique de cosmétiques.

Tu ne poses aucun diagnostic médical et tu ne nommes aucune pathologie. Tu
décris uniquement ce qui est visible à l'œil, comme le ferait un conseiller en
boutique, et seulement sur trois axes.

Réponds par un objet JSON et rien d'autre, sans texte autour, de la forme :

{"sebum": 0, "taches": 0, "eclat": 0, "utilisable": true, "remarque": ""}

- sebum   : 0 à 3, brillances et pores visibles.
- taches  : 0 à 3, taches, marques, irrégularités de pigmentation.
- eclat   : 0 à 3, à quel point le teint paraît terne. 0 = teint lumineux.
- utilisable : false si la photo est trop sombre, floue, trop loin, si le
  visage n'est pas visible, ou si ce n'est pas un visage.
- remarque : une phrase courte en français, ce que tu observes, sans jamais
  juger la personne et sans aucun terme médical. Vide si utilisable est false.

Si tu hésites, baisse la note plutôt que de l'inventer.`;

function definirCors(req, res, origines) {
  const origine = req.headers.origin;
  if (origine && origines.includes(origine)) {
    res.setHeader('Access-Control-Allow-Origin', origine);
  }
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Max-Age', '86400');
  return origine;
}

export default async function handler(req, res) {
  const origines = (process.env.ORIGINES_AUTORISEES || '')
    .split(',')
    .map((o) => o.trim())
    .filter(Boolean);

  const origine = definirCors(req, res, origines);

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ erreur: 'methode' });

  // Sans liste d'origines, on refuse tout : une fonction ouverte est une
  // fonction que n'importe qui fait payer au propriétaire de la clé.
  if (!origines.length || !origines.includes(origine)) {
    return res.status(403).json({ erreur: 'origine' });
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return res.status(500).json({ erreur: 'cle_absente' });
  }

  const { image, type } = req.body || {};

  if (typeof image !== 'string' || !image) {
    return res.status(400).json({ erreur: 'image_absente' });
  }
  if (!TYPES_ACCEPTES.includes(type)) {
    return res.status(400).json({ erreur: 'type_refuse' });
  }
  // base64 pèse environ 4/3 de l'octet source.
  if (image.length * 0.75 > TAILLE_MAX) {
    return res.status(413).json({ erreur: 'image_trop_lourde' });
  }

  try {
    const reponse = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: process.env.MODELE || MODELE_PAR_DEFAUT,
        max_tokens: 1024,
        system: CONSIGNE,
        messages: [
          {
            role: 'user',
            content: [
              { type: 'image', source: { type: 'base64', media_type: type, data: image } },
              { type: 'text', text: 'Analyse cette photo et réponds en JSON.' },
            ],
          },
        ],
      }),
    });

    if (!reponse.ok) {
      // On ne renvoie pas le détail au navigateur : il pourrait contenir des
      // informations sur la clé ou le compte.
      console.error('Anthropic a répondu', reponse.status);
      return res.status(502).json({ erreur: 'analyse_indisponible' });
    }

    const donnees = await reponse.json();
    const texte = (donnees.content || [])
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('')
      .trim()
      // Le modèle enrobe parfois sa réponse dans une clôture Markdown.
      .replace(/^```(?:json)?/i, '')
      .replace(/```$/, '')
      .trim();

    // Le modèle a pour consigne de ne renvoyer que du JSON, mais on ne lui
    // fait pas confiance aveuglément : on isole le premier objet.
    const debut = texte.indexOf('{');
    const fin = texte.lastIndexOf('}');
    if (debut === -1 || fin === -1) {
      // Le texte part dans les journaux, jamais dans la réponse HTTP : c'est
      // le seul endroit où on peut comprendre un refus du modèle.
      console.error(
        'Pas de JSON. arret=' + donnees.stop_reason +
        ' longueur=' + texte.length +
        ' fin=' + JSON.stringify(texte.slice(-80))
      );
      return res.status(502).json({ erreur: 'reponse_illisible' });
    }

    let brut;
    try {
      brut = JSON.parse(texte.slice(debut, fin + 1));
    } catch (e) {
      console.error(
        'JSON invalide. arret=' + donnees.stop_reason +
        ' longueur=' + texte.length +
        ' fin=' + JSON.stringify(texte.slice(-80))
      );
      return res.status(502).json({ erreur: 'reponse_illisible' });
    }

    const borne = (v) => {
      const n = Number(v);
      if (!Number.isFinite(n)) return 0;
      return Math.max(0, Math.min(3, Math.round(n)));
    };

    return res.status(200).json({
      sebum: borne(brut.sebum),
      taches: borne(brut.taches),
      eclat: borne(brut.eclat),
      utilisable: brut.utilisable !== false,
      remarque: typeof brut.remarque === 'string' ? brut.remarque.slice(0, 300) : '',
    });
  } catch (e) {
    console.error('Échec de l analyse', e && e.message);
    return res.status(502).json({ erreur: 'analyse_indisponible' });
  }
}

export const config = {
  api: { bodyParser: { sizeLimit: '6mb' } },
};
