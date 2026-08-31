# Boutique Shopify — Atelier Irizée

## Objectif

Lancer le site e-commerce de la marque sur Shopify. Ce dossier centralise la
documentation et le suivi du projet, séparément de Brand OS (outil interne de
pilotage de contenu/UGC/veille, situé dans `/Desktop/brand-os/`).

## État actuel (2026-08-24)

- Compte Shopify : **déjà créé** — on part de là, pas de zéro complet.
- Produits : **prêts** (gamme définie), mais **pas encore de photos** —
  c'est le point bloquant principal avant la mise en ligne (SH-06).
- Thème : **dev maison**, pas d'achat de thème premium.

## Décisions techniques

- **Plateforme** : Shopify hébergé (pas de headless) — le meilleur rapport
  vitesse de lancement / effort pour un premier site e-commerce.
- **Thème** : développé nous-mêmes (Shopify CLI, Liquid), pas de thème
  premium acheté. Départ probable sur une base Dawn vierge (gratuite,
  conforme Online Store 2.0) plutôt que from scratch, à trancher en SH-05.
- **Apps** : minimalisme strict. Chaque app ajoute du JS qui dégrade les
  Core Web Vitals (facteur de ranking SEO direct) — on n'installe que ce qui
  est indispensable. Le dev maison donne un contrôle direct là-dessus.
- **Pourquoi pas headless (Hydrogen/Next.js)** : plus de contrôle mais
  maintenance continue qui ne se justifie pas ici — le dev de thème custom
  sur Shopify hébergé donne déjà l'essentiel du contrôle recherché sans
  cette charge en plus.

## Suivi du projet

Voir [`roadmap.html`](roadmap.html) — tracker interactif des tâches (ouvrir
dans un navigateur), même logique que le suivi Brand OS. 27 tâches réparties
sur 5 phases : Cadrage & compte, Produits, Dev du thème, SEO & Perf, Tests &
lancement. Une zone "Idées à explorer" en bas de page permet de noter des
pistes en vrac sans les transformer tout de suite en tâches.

## Structure du site

Voir [`docs/sitemap.md`](docs/sitemap.md) pour l'arborescence des pages,
collections et navigation.

## Checklists

- [`docs/seo-perf-checklist.md`](docs/seo-perf-checklist.md) — points à
  vérifier avant lancement pour la performance et le SEO.

## Liens utiles

- Admin Shopify : _à compléter_
- Nom de domaine : _à compléter (SH-02)_
- Dépôt du thème (git) : _à compléter (SH-04)_
- Brand assets (logos, packshots, couleurs) : voir Brand OS / Content Studio
