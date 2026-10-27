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

- **Le texte est passé sous la photo, et c'était ça le vrai correctif.** Le
  nom et le prix ne manquaient pas de contraste : ils tombaient sur le tube,
  au milieu du cadre. Trois tentatives successives ont traité le symptôme
  (encre, voile, ombre portée) avant qu'une maquette comparative ne montre
  que le défaut était géométrique, pas chromatique.
- Le cadre 4:5 est donc descendu de `.product-card` vers
  `.product-card__media`, et le bloc de texte vit sur le fond de la page.
  Trois réglages disparaissent avec le problème : l'encre de survol, l'ombre
  portée et le voile. Seuls le badge et le bandeau d'achat restent sur la
  photo, et ils ont leur propre fond.
- **Le gabarit `templates/index.json` ne redescend pas de GitHub vers
  Shopify** quand l'éditeur de thème tient ce fichier : le Liquid et le CSS
  se synchronisent en secondes, la valeur du réglage non. Contourné en
  renommant l'identifiant (`category_size` → `eyebrow_size`) : la valeur
  stockée devient orpheline et le défaut du schéma s'applique. À retenir pour
  tout changement de réglage par défaut.
- **Le lot s'appelle « La Routine », et le pinceau en sort.** Renommage
  complet : titre, libellé et sous-titre d'offre, promesse, bénéfices, format,
  description, titre et description de référencement, et le handle. Shopify a
  créé la redirection `le-rituel` → `la-routine` tout seul, case cochée par
  défaut. Le troisième bénéfice ne pouvait pas rester vide : il annonce
  maintenant l'économie, vérifiable au centime (49,90 € contre 45,00 €).
- **Les flèches du carrousel ne disparaissaient jamais.** Le script les
  marquait bien `hidden`, mais `.featured-products__arrow` pose
  `display: flex`, et un sélecteur de classe bat le `[hidden] { display: none }`
  du navigateur, qui n'est qu'un sélecteur d'attribut. Le symptôme ressemblait
  à une erreur de logique, c'était une question de spécificité.

## 2026-10-26 (suite) — Diagnostic de peau

- **La section d'accueil était une vitrine sans rien derrière** : elle
  promettait une analyse photo et son bouton pointait sur une ancre vide.
  Remplacée par un vrai questionnaire, `sections/iz-diagnostic.liquid`, servi
  par `templates/page.diagnostic.json` sur `/pages/diagnostic`.
- **Pas d'analyse photo, et c'est un choix.** Avec deux soins au catalogue, ce
  qui décide la recommandation tient en cinq questions. Une photo de visage
  est une donnée personnelle : la collecter demanderait un service externe
  pour la clé d'API, un budget par analyse, un consentement et une durée de
  conservation, pour un gain nul sur un catalogue de deux produits.
- **Le moteur est séparé de la collecte**, exprès. Chaque réponse n'ajoute que
  des points à `score.masque` et `score.serum`, et `choisirCible()` tranche.
  Une analyse photo, plus tard, alimentera le même objet : rien de ce qui est
  écrit ne sera à jeter. À égalité, c'est la routine qui sort, parce que les
  deux besoins sont alors réellement présents.
- **Shopify ne reprend un gabarit JSON de GitHub qu'à sa création.** Les
  trois produits des résultats, ajoutés au JSON après coup, ne sont jamais
  arrivés, et le `templates/index.json` de l'accueil était figé depuis des
  heures. Pire : Shopify a ensuite réécrit `page.diagnostic.json` dans le
  dépôt en vidant les trois valeurs. Sa copie fait foi, point final.
- **Deux parades, selon la nature du réglage.** Pour un réglage technique, un
  identifiant neuf dans le schéma : la clé absente du JSON stocké fait
  s'appliquer la valeur par défaut (`eyebrow_size`, puis `handle_masque`,
  `handle_serum`, `handle_routine`). Pour du contenu, il n'y a pas de
  raccourci : il faut l'écrire dans l'éditeur de thème, qui écrit côté
  Shopify et le renvoie ensuite dans le dépôt.
- **Le sélecteur de gabarit d'une page ne liste que les gabarits du thème
  publié.** `page.diagnostic` n'y apparaîtra donc qu'après la publication de
  preprod. En attendant, le gabarit se teste avec `?view=diagnostic`.
- Le header se posait aussi sur le texte des pages de contenu : la fiche
  produit avait son exception, la condition couvre maintenant les deux.
- **Trois questions d'hygiène de vie** ajoutées au diagnostic : sommeil,
  exposition au soleil, alimentation. Le manque de sommeil et le soleil tirent
  vers le sérum, l'alimentation vers le masque. Huit questions au total.
- **Le contenu du diagnostic vit dans le préréglage de la section**, pas dans
  le gabarit. C'est la conséquence directe de la règle ci-dessus : Shopify ne
  reprend pas un gabarit JSON déjà créé, mais il reprend le Liquid. Pour
  changer les questions, on modifie le préréglage, on retire la section dans
  l'éditeur et on la réinsère : les huit questions arrivent d'un coup.
- **L'analyse photo est branchée.** Le moteur était prévu pour : la photo
  ajoute ses points au même objet `score`, trois au maximum de chaque côté
  contre huit pour les réponses. Elle pèse sans décider à la place du
  questionnaire, et si elle échoue le diagnostic continue sans elle.
- La clé d'API ne peut pas vivre dans un thème public : l'appel passe par
  `services/diagnostic-api`, une fonction Vercel qui ne conserve la photo
  nulle part, borne les notes du modèle et refuse toute origine non déclarée.
  Ce dernier point n'est pas une formalité : une fonction ouverte est une
  fonction que n'importe qui fait payer au propriétaire de la clé.

## 2026-10-27 — L'analyse photo en service

- **Deux symptômes, deux causes sans rapport.** L'étape photo n'apparaissait
  pas parce que son réglage était à non par défaut ; l'email ne « marchait
  pas » parce que rien n'envoyait d'email. Chercher une cause unique aurait
  fait perdre du temps.
- **La réponse du modèle arrivait tronquée.** `max_tokens` à 400 coupait le
  JSON avant l'accolade fermante, et le parseur rendait « reponse_illisible ».
  Le code ne disait rien de ce qui se passait : c'est en journalisant la
  raison d'arrêt, la longueur et la fin du texte qu'on l'a vu en une lecture.
  Porté à 1024. **Leçon : devant un format de sortie, journaliser le texte
  brut avant de spéculer.**
- **Le formulaire inscrit, il n'expédie pas.** `{% form 'customer' %}` crée
  une cliente marquée `diagnostic`, rien de plus. Le texte promettait l'envoi
  de la routine : il a été corrigé. L'étiquette du résultat part désormais
  avec l'inscription (`diagnostic-masque`, `diagnostic-serum`,
  `diagnostic-routine`) pour qu'un outil d'emailing puisse viser la bonne
  routine le jour où il y en aura un.
- Un refus de Shopify (adresse invalide, 400) était avalé : le résultat
  s'affichait comme si l'inscription avait eu lieu. Corrigé.
- **Les réglages d'une section insérée depuis un préréglage sont écrits en
  dur dans le gabarit.** Changer la valeur par défaut du schéma n'a alors plus
  aucun effet : il faut passer par l'éditeur. Seuls les réglages ajoutés
  *après* l'insertion retombent sur leur défaut, ce qui a permis d'activer
  l'étape photo sans toucher à l'éditeur.
- Parcours vérifié de bout en bout avec une vraie photo : analyse, points
  ajoutés au score, phrase d'observation affichée au-dessus du résultat,
  produit et bouton d'achat.
- **`/pages/diagnostic` fonctionne enfin sans paramètre.** Le gabarit
  `page.diagnostic` ne peut pas être attaché à la page avant la publication,
  et obliger à ouvrir `?view=diagnostic` à chaque essai n'était pas une
  réponse tenable pour une page qu'on teste tous les jours. La section est
  donc posée dans le gabarit de page ordinaire, avec un garde-fou sur
  l'identifiant de la page : elle ne se montre que sur `diagnostic` et reste
  muette ailleurs. Vérifié sur `/pages/contact`, qui n'en rend rien.
- À la publication, deux options : attacher `page.diagnostic` à la page et
  retirer la section du gabarit ordinaire, ou ne rien changer. Les deux
  tiennent, la première est plus propre.

## SEO, ordre de l'accueil, précommande (27 octobre 2026)

### Les alternatives d'images étaient toutes vides

`{{ image | image_url: width: 900 | image_tag }}` ne sort **aucun** alt.
`image_url` rend une chaîne de caractères : `image_tag` n'a plus d'objet image
où lire l'alternative, et il n'invente rien. Toutes les cartes produit, le
hero, le collage de la marque, le teaser du diagnostic et les visuels du blog
étaient concernés, c'est-à-dire presque chaque image de l'accueil.

**Leçon : dès qu'on passe par `image_url`, l'alt se passe à la main**
(`image_tag: alt: mon_alt`). Les balises `<img>` écrites à la main, elles,
étaient correctes depuis le début.

Attention au piège de la boucle : patcher trois lignes identiques avec
`str.find` a collé deux alternatives sur la même image et aucune sur la
troisième. Vérifier le résultat ligne par ligne, pas le compte de
remplacements.

### Le texte alternatif vit sur le fichier, pas sur le produit

Les trente médias des trois produits ont reçu leur alternative dans l'admin.
Les fichiers partagés entre produits (La Routine réutilise des photos du
masque et du sérum) portent **une seule** alternative : renseignée une fois,
elle vaut partout. Neuf des médias de La Routine étaient donc déjà couverts.

Dans l'éditeur de fichiers, la flèche « suivant » ne répond pas tant qu'une
modification n'est pas enregistrée, et un clic par coordonnées sur
« Enregistrer » rate si on n'attend pas que React ait pris la saisie. Le
rythme qui marche : saisir, attendre deux secondes, enregistrer, attendre,
passer au suivant.

### La boutique ne s'appelle pas comme son domaine

L'admin répondait « un problème technique lié à Shopify » sur toutes les URL
en `/store/atelier-irizee/`. Ce n'était pas une panne : la boutique s'appelle
`0nz0p1-61`. **Leçon : lire le handle dans l'URL de l'admin avant de conclure
à une panne de Shopify.**

### Un préréglage peut livrer ses blocs déjà remplis

La section FAQ tire ses questions du metafield du produit ; sur l'accueil il
n'y a pas de produit, et son préréglage arrive vide. Plutôt que saisir cinq
questions à l'écran, un second préréglage « FAQ boutique » porte les questions
dans le schéma : Shopify crée les blocs d'un préréglage à l'insertion, donc la
section arrive remplie.

**Leçon : pour poser du contenu répétitif dans l'éditeur, le faire passer par
un préréglage plutôt que par la saisie.**

### Ce qui bloque encore sur la publication

Le thème publié est toujours celui de Shopify par défaut ; `preprod` est un
brouillon. C'est pour cette raison que le sélecteur de modèle d'une page ne
propose que `contact` : il ne liste que les modèles du thème publié. Le
modèle `page.diagnostic` reste donc inattachable jusqu'à la publication.

### Corrections de fond

- **« Vous n'êtes débité qu'aujourd'hui »** : la tournure restrictive disait
  « uniquement aujourd'hui » et transformait une information de paiement en
  énigme. Remplacée par « Le paiement est encaissé à la commande. »
- **Pastille « Best »** sur la photo principale : la boutique n'a pas vendu un
  article, l'argument n'était soutenu par rien, et il était en anglais.
  Devient « Nouveau ».
- **Format monétaire** : les prix sortaient en `€24,90`. Passés en
  `24,90 €` dans les quatre champs (HTML et e-mail, avec et sans devise).
- **Collection « Les soins »** créée (`/collections/les-soins`) avec les trois
  produits : il n'existait qu'une collection « Page d'accueil » à un produit.

## Le pack prend un nom, et l'en-tête rend sa place (27 octobre 2026)

### « Votre panier » était coupé en deux

`is_overlay` ne regardait pas la page : le header passait en
`position: fixed` **partout**. Il sortait donc du flux et chaque page
démarrait derrière lui. L'accueil n'y voyait rien parce que son hero est
justement fait pour passer dessous ; le panier, lui, perdait le haut de son
titre malgré ses 72 px de marge.

**Leçon : un réglage qui change le mode de positionnement doit porter sa
condition de page, pas seulement les styles qui l'accompagnent.** La
correction précédente (`reglages_pdp`) ne gouvernait que les couleurs.

### La typo du menu n'était pas la bonne police

Le menu était réglé sur **Helvetica** quand tout le reste du site est en Work
Sans. L'œil attrape la rupture sans pouvoir la nommer. Repassé en Work Sans.

**Leçon : avant de retoucher taille, graisse et espacement, vérifier que
c'est bien la même famille que le reste.**

### Le pack s'appelle Routine Anti-Taches & Éclat

Le nom est passé du descriptif (« La Routine ») au problème qu'il règle.
L'identifiant d'URL reste `la-routine` : le diagnostic le référence par
`handle_routine`, le changer casserait le résultat « les deux ». Mis à jour :
titre, `offre_libelle`, balise SEO, accroche de carte, hero de l'accueil.

Note : « anti-taches » est une allégation cosmétique. Le choix est assumé
côté marque, mais il demande un dossier qui le justifie, pas seulement la
présence d'alpha-arbutine dans la formule.

### Autres corrections

- **« Fabriqué en France »** retiré du bandeau de réassurance : la production
  n'est pas française. Le bandeau passe de cinq à quatre colonnes, sinon il
  gardait une case vide.
- **« Débit aujourd'hui, expédition en décembre »** menait par le débit, la
  partie la moins engageante. Devient « Commande réservée, expédition en
  décembre » ; le détail du paiement reste sous le bouton d'achat.
- **Le bloc d'achat de la fiche** a son propre fond, blanc, pour se détacher
  du beige du reste du site. Réglage neuf, donc le défaut s'applique sans
  passer par l'éditeur.
- **La date d'expédition** disparaît du catalogue : déjà portée par le bouton
  de chaque carte et par la fiche.
- **La newsletter** promet maintenant du contenu, pas une alerte de
  lancement, et elle existe aussi en bas de la fiche produit.
