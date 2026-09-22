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
