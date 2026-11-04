# Les trois e-mails de panier abandonné

Montés dans Klaviyo le 04/11/2026, **laissés en brouillon**. L'activation
déclenche de vrais envois : elle revient au propriétaire du compte.

## Pourquoi Klaviyo et pas Shopify

Shopify avait sa propre relance active — automatisation « Récupérer le
paiement abandonné », 1 e-mail envoyé, 0 clic, 0 commande. Elle a été
**désactivée** (et non supprimée : elle se rallume en un clic).

Les deux outils peuvent relancer un panier, mais pas en même temps, sinon le
client reçoit deux e-mails pour le même panier. Klaviyo l'emporte parce qu'il
permet une séquence, un design à la marque et la mesure du chiffre d'affaires
récupéré ; l'e-mail natif de Shopify est unique et générique.

## Le scénario

| Étape | Délai cumulé | Message |
|---|---|---|
| Déclencheur | — | Indicateur **Commande Débutée** (Started Checkout, via l'intégration Shopify) |
| Attente | 4 h | |
| E-mail 1 | 4 h | « Votre panier vous attend » |
| Attente | +20 h | |
| E-mail 2 | 24 h | « Votre panier n'a pas bougé » |
| Attente | +1 jour | |
| E-mail 3 | 48 h | « Dernier rappel pour votre panier » |

**Filtre de profil** : `Commande Passée` **zéro fois depuis le début de ce
flux**. C'est la pièce qui empêche de relancer quelqu'un qui vient d'acheter :
dès que la commande arrive, la personne sort du scénario et ne reçoit pas les
e-mails suivants.

**Réintégration** : autorisée après **7 jours**. Quelqu'un qui abandonne deux
paniers dans la même semaine n'est relancé qu'une fois.

**Pas de remise.** Au lancement, une remise systématique apprend aux clients à
abandonner leur panier pour l'obtenir. Les trois e-mails relancent sur le
produit et sur la livraison offerte dès 39 €.

## Le contenu

Même règle que pour les e-mails du diagnostic : pas d'objet en majuscules, pas
d'émoji, pas de compte à rebours, aucune urgence inventée. Le panier Shopify ne
réserve pas de stock — on ne prétend donc pas qu'il « expire ».

### E-mail 1 — 4 h

**Objet** : Votre panier vous attend
**Aperçu** : Rien n'est perdu, vous pouvez reprendre où vous en étiez.

> Bonjour,
>
> Vous avez commencé une commande sur irizee.com sans la terminer. Votre panier
> est toujours là, rien n'est perdu.
>
> [articles du panier]
> [Reprendre ma commande]
>
> Livraison offerte dès 39 € d'achat en France. Retours acceptés sous 14 jours.
>
> Une question avant de commander ? Répondez à cet e-mail, nous lisons tout.
>
> À bientôt,
> Irizée

### E-mail 2 — 24 h

**Objet** : Votre panier n'a pas bougé
**Aperçu** : Si quelque chose vous a fait hésiter, dites-le-nous.

> Bonjour,
>
> Votre panier vous attend toujours. Si quelque chose vous a fait hésiter — le
> choix du soin, une question sur la formule, le délai de livraison —
> dites-le-nous.
>
> Chez Irizée, les formules sont courtes : un actif par besoin, et la raison
> pour laquelle il est là. Si vous hésitez entre deux soins, nous vous aidons à
> choisir.
>
> [articles du panier]
> [Reprendre ma commande]

### E-mail 3 — 48 h

**Objet** : Dernier rappel pour votre panier
**Aperçu** : On vous le garde encore un peu.

> Bonjour,
>
> C'est le dernier message que nous vous envoyons au sujet de ce panier.
>
> Il reste accessible : si vous souhaitez le reprendre, c'est en un clic.
> Sinon, nous n'en reparlerons plus.
>
> [articles du panier]
> [Reprendre ma commande]

## Comment c'est fabriqué

Les trois e-mails sont des **modèles HTML** importés dans Klaviyo, pas des
montages glisser-déposer. Les sources sont ici :

- `docs/emails/generer-panier-abandonne.py` — le gabarit commun et les trois
  textes. C'est le seul fichier à modifier.
- `docs/emails/panier-abandonne-{1,2,3}.html` — ce que le script produit, et ce
  qui est importé dans Klaviyo.

Pour changer un texte : modifier le script, le relancer (`python3
docs/emails/generer-panier-abandonne.py`), puis réimporter le HTML dans Klaviyo
(Contenu → Modèles → Créer → Importer un modèle d'e-mail) et le réaffecter au
message du flux. Le contenu d'un message peut aussi s'éditer directement dans
l'éditeur de code de Klaviyo, mais alors les deux versions divergent.

### Le piège de la boucle dans un tableau

La boucle des articles s'écrit **autour** du `<table>`, à l'intérieur d'un
`<td>` :

```html
<td>
  {% for item in event.extra.line_items %}
  <table>…une ligne produit…</table>
  {% endfor %}
</td>
```

Écrite **entre** `<table>` et `<tr>`, elle est éjectée hors du tableau par le
parseur HTML (*foster parenting*) et n'entoure plus rien : un seul article
s'affiche quoi qu'il arrive. C'est arrivé au premier import, c'est visible dans
l'aperçu du modèle (les balises se retrouvent au-dessus du tableau).

### Variables utilisées

| Variable | Rôle |
|---|---|
| `event.extra.line_items` | la liste des articles du panier |
| `item.product.title` | le nom du produit |
| `item.product.images.0.src` | la vignette |
| `item.quantity\|floatformat:0` | la quantité |
| `item.line_price\|floatformat:2` | le prix de la ligne |
| `event.extra.checkout_url` | le lien qui ramène au paiement |
| `{% unsubscribe %}` | le lien de désabonnement, obligatoire |

Le logo pointe sur `https://irizee.com/cdn/shop/t/9/assets/irizee-logo.png`.
**Cette URL contient l'identifiant du thème** (`t/9`). Si un jour un autre
thème est publié, l'identifiant change et le logo casse dans les e-mails. Le
geste définitif serait de téléverser le logo dans la bibliothèque de médias de
Klaviyo et de pointer dessus.

## Ce qui reste à faire

1. **Valider le rendu avec de vraies données.** Klaviyo répond « il n'y a aucun
   événement à prévisualiser » : la boutique n'a pas encore de `Commande
   Débutée` dans Klaviyo. Tant qu'un vrai panier abandonné n'a pas eu lieu, on
   ne peut pas vérifier que les articles, les prix et le lien de paiement
   s'affichent. Le moyen de le provoquer : ajouter un produit au panier sur
   irizee.com, commencer le paiement en saisissant une adresse e-mail, puis
   quitter la page.
2. **Passer les trois messages de « Brouillon » à « Actif ».** Un message en
   brouillon est ignoré même quand le scénario tourne.
3. **Activer le scénario** (« Vérifier et activer »).

Tant que 2 et 3 ne sont pas faits, aucun e-mail ne part — et comme la relance
de Shopify est désactivée, **il n'y a aujourd'hui plus aucune relance de panier
abandonné en service**. C'est l'état voulu le temps de la vérification, mais ce
n'est pas un état où rester.

## Expéditeur

`Irizée <contact@irizee.com>`, avec réponse sur la même adresse. Le domaine
d'envoi reste le domaine partagé de Klaviyo : un domaine dédié demanderait des
enregistrements NS que la zone DNS de Shopify n'accepte pas.
