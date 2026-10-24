# Metafields et metaobjets — marche à suivre

Les clés ci-dessous sont lues telles quelles par les sections `iz-*`.
**Une clé mal orthographiée = un champ qui ne s'affichera jamais**, sans message
d'erreur. Recopie-les exactement, en minuscules et sans accent.

Espace de noms partout : `custom`

---

## Étape 1 — Les champs simples

Les plus rentables : ils remplissent le haut de la fiche, là où se joue la
décision d'achat. Commence par eux.

**Où** : Paramètres → Données personnalisées → **Produits** → Ajouter une
définition.

| Nom à afficher | Clé | Type |
|---|---|---|
| Format | `format` | Texte · Une ligne |
| Promesse | `promesse` | Texte · Une ligne |
| Bénéfices | `benefices` | Texte · Une ligne · **cocher « Liste de valeurs »** |
| Liste INCI | `inci` | Texte · Multiligne |
| Titre de la texture | `texture_titre` | Texte · Une ligne |
| Texte de la texture | `texture_texte` | **Texte enrichi** |
| Image de la texture | `texture_image` | Fichier · Image |

> **Attention à `benefices`** : c'est un texte *une ligne* avec l'option
> « liste » activée, pas un multiligne. Sans la liste, la section n'affichera
> rien.
>
> **Et à `texture_texte`** : en texte enrichi, tes paragraphes s'afficheront
> correctement. En multiligne, tout sera collé en un bloc.

Une fois créés, va dans chaque produit → section **Metafields** en bas de page,
et remplis-les avec le contenu de `contenu-fiches-produit.md`.

**À ce stade, la fiche est déjà vendeuse** : sur-titre, promesse, bénéfices,
composition et section texture s'affichent.

---

## Étape 2 — Les metaobjets

Trois types à créer, pour le rituel, les actifs et la FAQ.

**Où** : Paramètres → Données personnalisées → **Metaobjets** → Ajouter une
définition.

### `etape_rituel`

| Champ | Clé | Type |
|---|---|---|
| Titre | `titre` | Texte · Une ligne |
| Description | `description` | Texte · Multiligne |
| Image | `image` | Fichier · Image |

### `actif`

| Champ | Clé | Type |
|---|---|---|
| Nom | `nom` | Texte · Une ligne |
| Description | `description` | Texte · Multiligne |

### `question_faq`

| Champ | Clé | Type |
|---|---|---|
| Question | `question` | Texte · Une ligne |
| Réponse | `reponse` | **Texte enrichi** |

Puis, de retour dans **Produits**, trois définitions de plus :

| Nom à afficher | Clé | Type |
|---|---|---|
| Étapes du rituel | `etapes` | Référence à un metaobjet · `etape_rituel` · **liste** |
| Actifs | `actifs` | Référence à un metaobjet · `actif` · **liste** |
| FAQ | `faq` | Référence à un metaobjet · `question_faq` · **liste** |

> Crée d'abord les **définitions de metaobjets**, puis les champs produit qui
> les référencent — l'inverse n'est pas possible.

---

## Étape 3 — Plus tard

Rien ne presse : ces sections resteront simplement masquées.

### Le choix du format (quand Le Rituel et Le Coffret existeront)

Sur **Produits** :

| Nom à afficher | Clé | Type |
|---|---|---|
| Offres | `offres` | Référence à un produit · **liste** |
| Libellé d'offre | `offre_libelle` | Texte · Une ligne |
| Sous-titre d'offre | `offre_sous_titre` | Texte · Une ligne |
| Badge d'offre | `offre_badge` | Texte · Une ligne |

`offres` se remplit sur **chaque** produit : sur le Masque, tu listes Le Rituel
et Le Coffret. Les trois autres se remplissent sur le produit **cible** — c'est
lui qui porte son propre libellé.

### Produits complémentaires

| Nom à afficher | Clé | Type |
|---|---|---|
| Produits complémentaires | `complementaires` | Référence à un produit · **liste** |

### Vidéos créateurs

Metaobjet `video_ugc` :

| Champ | Clé | Type |
|---|---|---|
| Vidéo | `video` | Fichier · Vidéo |
| Pseudo | `pseudo` | Texte · Une ligne |
| Accroche | `accroche` | Texte · Une ligne |

Puis sur Produits : `videos_ugc`, référence metaobjet `video_ugc`, **liste**.

### Résultats chiffrés — seulement avec une vraie étude

Metaobjet `resultat` :

| Champ | Clé | Type |
|---|---|---|
| Chiffre | `chiffre` | Texte · Une ligne |
| Libellé | `libelle` | Texte · Une ligne |

Puis sur Produits :

| Nom à afficher | Clé | Type |
|---|---|---|
| Résultats | `resultats` | Référence metaobjet · `resultat` · **liste** |
| Source des résultats | `resultats_source` | Texte · Multiligne |

> **Sans `resultats_source`, la section ne s'affichera pas**, même avec des
> chiffres. C'est délibéré : un pourcentage sans source est une allégation non
> étayée.

---

## Vérifier que ça marche

Après l'étape 1, ouvre la fiche du Masque sur la préprod. Tu dois voir
apparaître le sur-titre, la promesse, les bénéfices cochés, l'accordéon
composition et la section texture.

Si un élément manque, c'est presque toujours la clé : un accent, une
majuscule, un `s` oublié. Shopify ne signale rien, il renvoie simplement du
vide.

Dis-le-moi et je vérifie — je peux lire ce que le thème reçoit réellement.
