# Journal de développement — Boutique Shopify

Log daté des décisions prises et de ce qui a été fait, au fil du dev.
Objectif : ne pas perdre le "pourquoi" derrière un choix technique une fois
qu'on est trois semaines plus loin.

Une entrée = une date + ce qui a été fait/décidé + pourquoi si c'est un choix
non évident. Pas besoin de détailler chaque ligne de code — l'historique git
s'en charge déjà, ce journal est pour le contexte que le code ne montre pas.

---

## 2026-08-31

- Environnement de dev en place : Shopify CLI installé (via npm, préfixe
  utilisateur `~/.npm-global` pour éviter les soucis de permissions),
  thème scaffoldé depuis Dawn (fork, pas de rebuild from scratch — voir
  [README](../README.md) pour le pourquoi).
- Dépôt git initialisé à la racine de `shopify/` (thème + docs + roadmap
  dans le même repo). Historique de Dawn retiré avant le premier commit.
- Boutique Shopify existante identifiée : `0nz0p1-61.myshopify.com`
  (domaine personnalisé connecté : irizee.com).
- `shopify theme dev --store=0nz0p1-61.myshopify.com` connecté et
  fonctionnel (preview sur `localhost:9292`, confirmé OK).
- Pas encore de décision sur la charte visuelle (couleurs/logo/typo) —
  en attente.

## 2026-08-31 (suite)

- Charte visuelle : le bleu générique utilisé au départ (repris de l'UI
  interne Brand OS/Finance) a été écarté — il ne représente pas vraiment la
  marque. Nouveau choix : **bleu nila `#214975`**, extrait directement d'une
  photo de poudre de nila (indigo naturel, ingrédient traditionnel
  marocain/berbère utilisé dans la formule — éclaircissant, purifiant).
  Ancré dans un vrai actif plutôt que choisi arbitrairement.
- Palette testée dans `theme/config/settings_data.json` (scheme-1) : fond
  crème `#FBFAF8`, texte quasi-noir `#1A1A1A`, bleu nila en bouton/accent.
  Facilement réversible (une entrée JSON).
- Inspiration concurrents passée en revue (Typology, Respire, rhode,
  La Rosée) : aucun n'utilise sa couleur signature en aplat massif — toujours
  posée sur un fond neutre clair. On suit le même principe.
- Ajout d'un module **Conversion** au roadmap (SH-28 à SH-34) : proposition
  de valeur home, bouton panier sticky mobile, réassurance fiche produit,
  capture email, avis clients, wallets de paiement express (Shop Pay/Apple
  Pay/PayPal), stratégie contenu blog SEO. Objectif : penser le parcours
  utilisateur et la conversion dès le dev, pas après coup.

## 2026-10-15

- Corrections de la home : marges verticales réglables sur le menu (le
  réglage existant n'agissait que sur l'horizontal), allègement du bandeau
  de réassurance (filets et numéros retirés, devenus optionnels, marges
  extérieures ajoutées), footer passé en pleine largeur — il était la
  seule section du thème sans la classe `full-width`, d'où les bandes de
  fond sur les côtés. Ajout de la flèche de retour sur le carrousel
  produits, qui n'avait qu'un bouton « suivant ». Suppression de la bulle
  « swipe » des cartes produit : elle était enfermée dans un
  `@media (hover: hover)` et n'apparaissait donc que sur ordinateur, là
  où on ne swipe pas.
- **Incident à retenir** : un `shopify theme push` nu renvoie les copies
  locales des fichiers JSON (`templates/*.json`,
  `config/settings_data.json`, `sections/*-group.json`) et écrase donc ce
  qui a été réglé dans l'éditeur Shopify depuis le dernier pull. C'est
  arrivé en début de session. Des scripts de synchronisation ont d'abord
  été écrits pour l'éviter, puis retirés au profit de la solution de fond.
- **Décision : intégration GitHub de Shopify.** Le thème sera connecté à
  une branche du dépôt, avec synchronisation dans les deux sens — les
  enregistrements de l'éditeur sont commités automatiquement, les push
  déploient automatiquement. Cela supprime la divergence entre le dépôt et
  la boutique au lieu de la gérer à la main.
- **Conséquence sur la structure du dépôt** : l'intégration exige les
  dossiers du thème (`assets/`, `sections/`, `templates/`…) à la racine de
  la branche, sans possibilité d'indiquer un sous-dossier. Le contenu de
  `theme/` a donc été remonté d'un cran. `docs/`, `README.md` et
  `roadmap.html` restent à la racine à côté — Shopify les ignore, c'est la
  structure du thème Dawn officiel.
- Branche `preprod` créée pour porter cette connexion. Elle est permanente :
  la supprimer casserait le lien avec le thème.

## 2026-10-15 (suite)

- **Panne de la journée, et sa leçon.** Un réglage `range` déclaré en 0–999 avec
  un pas de 1 (soit 999 crans, contre 101 autorisés par Shopify) a fait rejeter
  7 fichiers. Shopify ne signale rien : le fichier n'arrive simplement jamais sur
  la boutique. L'absence de `templates/index.json` a mis la page d'accueil en 404.
  `shopify theme check` ne détecte pas cette règle et affichait zéro défaut.
- **Deuxième leçon** : un symptôme visuel se vérifie sur la page rendue, jamais
  sur le constat qu'un fichier est déployé. Le header n'occupait pas toute la
  largeur à cause d'un `max-width: var(--page-width)` dans `.header--overlay` —
  invisible en dessous de 1440 px de large. Trois corrections ont été annoncées
  à tort avant de mesurer la page réelle avec `shopify theme dev`.
- **Mise en place d'une barrière qualité sur les PR** (`.github/workflows/qualite.yml`) :
  `shopify theme check` d'une part, et `scripts/valider-theme.py` d'autre part,
  qui porte les règles que le linter ne couvre pas — les 101 crans des `range`,
  les réglages utilisés sans être déclarés, les valeurs de template hors bornes,
  les identifiants dupliqués. Chaque règle correspond à une erreur réellement
  rencontrée. Reste à cocher ces deux contrôles comme obligatoires dans les
  protections de branche du dépôt.

## 2026-10-20

- Fiche produit construite d'après la maquette : snippet de tokens, section
  d'achat (galerie, bloc d'achat, choix du format, jauge, accordéons), barre
  d'achat fixe sur mobile, puis texture, résultats, vidéos, rituel, formule,
  routine, FAQ et marque. Le bandeau d'engagements réutilise la section de
  réassurance de l'accueil, sans la modifier.
- **Trois règles Shopify non documentées par le linter**, chacune ayant fait
  disparaître un fichier en silence : un `range` limité à 101 crans, un `name`
  de section ou de bloc limité à 25 caractères, et le rejet du fichier entier
  dès qu'une de ces règles est violée. Les deux premières sont désormais
  contrôlées par `scripts/valider-theme.py`.
- **Leçon de méthode** : un symptôme visuel se mesure sur la page rendue. Le
  header plafonné à 1440 px, le bandeau décalé de 64 puis 28 px, la
  compensation de hauteur figée à une valeur périmée — aucun de ces défauts
  n'était visible dans le code, tous l'étaient en deux mesures.
- Les sections 6 à 13 dépendent de metafields et de metaobjets qui n'existent
  pas encore : elles sont en place mais restent masquées, conformément à la
  règle d'état vide. La section d'avis (étape 11) attend l'installation d'une
  app d'avis.

## 2026-10-24

- **Metafields, metaobjets et contenu créés directement dans l'admin** : les
  dix définitions de champ produit, les trois définitions de metaobjets, les
  24 entrées (6 étapes de rituel, 8 actifs, 10 questions) et le remplissage
  complet de la fiche du Masque. Chaque clé a été vérifiée à l'écran avant
  enregistrement — Shopify fabrique la clé à partir du nom affiché, et une
  clé fausse ne renvoie rien et ne signale rien.
- **Le texte enrichi sortait en JSON brut sur la page rendue.** Shopify
  convertit un metafield `rich_text` quand on le sort directement, mais pas
  dans deux cas : quand la valeur passe par un filtre (`iz-texture` utilisait
  `| default:`) et quand elle vient d'un champ de metaobjet (`iz-faq` lisait
  `q.reponse`). Dans le second cas l'arbre n'est même accessible que derrière
  `.value`. D'où `snippets/iz-richtext.liquid`, qui fait la conversion à la
  main et laisse passer intact ce qui est déjà du HTML.
- **La leçon du 20 octobre a resservi le jour même** : les deux défauts
  ci-dessus étaient invisibles dans le code et dans l'admin — l'admin
  affichait un joli texte formaté. Ils n'apparaissent qu'en lisant le HTML de
  la page rendue. Le premier correctif n'a d'ailleurs réparé que la section
  texture ; c'est la mesure suivante qui a montré que la FAQ, elle, tenait à
  une autre cause.
- Le contenu de démonstration du gabarit (vidéos, rituel, actifs, FAQ) a été
  retiré. L'une des accroches annonçait « Avant / après 4 semaines », un
  résultat daté que rien n'étaye.

## 2026-10-26

- **Le plein cadre rendait le texte des cartes d'accueil illisible.** Le
  réglage existait, le voile aussi, mais la page d'accueil n'en portait
  aucun : `overlay_strength` et `text_color_hover` étaient absents de
  `templates/index.json`, donc nuls. Un réglage qu'aucun gabarit ne porte ne
  sert à rien.
- **Le voile était quand même le mauvais outil.** Il réglait le contraste en
  abîmant ce qu'il protégeait : il ternissait la photo lifestyle, et en haut
  de carte il assombrissait toute une bande pour un seul mot. Remplacé par une
  ombre portée sur le texte, qui ne touche pas l'image. Elle s'oppose toujours
  à l'encre choisie, noire sous un texte clair et blanche sous un texte foncé,
  déduite en Liquid de `color_extract: 'lightness'`. Le voile subsiste en
  option, en bas seulement, à zéro par défaut.
- La vraie réponse au contraste était déjà là : les packshots sont clairs,
  donc encre foncée au repos ; la photo lifestyle est bleu profond, donc
  blanc au survol. Les deux réglages de couleur existaient, ils étaient tous
  les deux sur blanc.
- L'accroche et le prix de la carte suivent maintenant la couleur du nom.
  Laisser l'accroche en gris fixe pendant qu'on choisissait du blanc pour le
  titre garantissait qu'une des deux lignes resterait illisible.
- **Le changement d'encre au survol valait aussi au doigt.** La règle vivait
  sous `@media (hover: hover)` : sur mobile, la carte « swipée » montrait la
  photo lifestyle avec l'encre du packshot. Le sélecteur `.product-card--swiped`
  a été ajouté.
- Nouveau champ `custom.carte_accroche`. Sans lui, la vignette affichait les
  soixante premiers caractères de la description, soit « Appliqué une à deux
  fois par semaine, ce masque absorbe l… ». Les deux produits ont leur
  accroche.
- **Les descriptions des deux produits ont été réécrites** : elles ouvraient
  sur le mode d'emploi, elles ouvrent sur le problème. Le Sérum ne nommait
  aucun actif, ce qui le privait de tout référencement sur « vitamine C » et
  « alpha-arbutine ».
- **Le volume du Sérum est réglé** : 30 ml, lu sur le flacon dans le packshot,
  pas sur la fiche technique qui ne le porte toujours pas. La mention
  obligatoire est en ligne.
