# Arborescence du site — Boutique Shopify

Statut : brouillon de travail (tâche SH-03). À affiner une fois la gamme
produits et le positionnement de marque validés.

## Navigation principale

- **Accueil** (`/`)
- **Boutique** (`/collections/all`)
  - Collection(s) par catégorie — _à définir selon la gamme de produits
    (ex : soin visage, soin corps, best-sellers, nouveautés)_
- **Fiche produit** (`/products/[handle]`)
- **À propos** (`/pages/a-propos`) — histoire de la marque, valeurs
- **Journal / Blog** (`/blogs/journal`) — optionnel, utile pour le SEO
  éditorial si contenu régulier prévu
- **Contact** (`/pages/contact`)
- **Panier / Checkout** — géré nativement par Shopify

## Pages secondaires (footer)

- FAQ (`/pages/faq`)
- Livraison & délais (`/pages/livraison`)
- Retours & remboursements (`/pages/retours`)
- CGV (`/pages/cgv`)
- Mentions légales (`/pages/mentions-legales`)
- Politique de confidentialité (`/pages/confidentialite`)

## Fiche produit — structure type

- Nom du produit
- Prix
- Galerie photos (packshot + contexte + texture/zoom)
- Description courte (accroche)
- Description longue (ingrédients, bénéfices, usage)
- Composition / liste INCI (si cosmétique)
- Avis clients (si app reviews légère retenue)
- Produits complémentaires / cross-sell

## Notes

- Garder la profondeur de navigation à 2 clics max depuis l'accueil.
- Les URLs `/products/` et `/collections/` sont imposées par Shopify (non
  modifiables sans app tierce) — ne pas prévoir de structure d'URL custom.
- Si un blog éditorial est prévu à terme (stratégie SEO de contenu), le
  prévoir dès la structure de navigation pour éviter une refonte du menu.
