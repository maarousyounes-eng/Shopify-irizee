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
