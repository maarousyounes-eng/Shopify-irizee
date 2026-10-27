# Les trois emails du diagnostic

Prêts à coller dans Klaviyo. Un email par résultat, déclenché sur l'étiquette
que le diagnostic pose sur la cliente.

| Étiquette Shopify | Email | Produit |
|---|---|---|
| `diagnostic-masque` | 1 | Masque Rituel Nila, 25,00 € |
| `diagnostic-serum` | 2 | Sérum Correcteur & Éclat, 24,90 € |
| `diagnostic-routine` | 3 | La Routine, 45,00 € au lieu de 49,90 € |

**Règle tenue partout** : aucune allégation qui ne soit déjà sur la fiche
produit, aucun terme médical, aucun chiffre de résultat. Ce sont les mêmes
promesses que la boutique, pas des promesses d'email.

Pas d'objet en majuscules, pas d'émoji, pas de compte à rebours. La marque
n'est pas celle-là.

---

## Email 1 — le Masque

**Objet** : Par où commencer pour votre peau
**Préheader** : Vos réponses pointent vers le sébum et les impuretés. Voici le geste à poser en premier.

> Bonjour,
>
> Vous venez de faire le diagnostic, et vos réponses décrivent une peau qui
> produit du sébum et dont le grain s'irrégularise. C'est ce qu'il faut
> traiter en premier : un sérum posé sur une peau encombrée travaille moins
> bien.
>
> **Le Masque Rituel Nila**, c'est le geste qui désencombre. La poudre de nila
> et les argiles absorbent l'excès de sébum et les impuretés, pendant que
> l'huile d'argan et le beurre de karité gardent la peau souple tout au long
> de la pose.
>
> **Votre routine**
> Le matin : nettoyant doux, puis votre crème habituelle.
> Le soir : une à deux fois par semaine, le masque pendant dix à quinze
> minutes, puis votre crème.
>
> [Découvrir le Masque Rituel Nila, 25,00 €]
>
> Une question sur son utilisation ? Répondez à cet email, nous lisons tout.
>
> À bientôt,
> Irizée

**Lien** : `https://irizee.com/products/masque-rituel-nila`

---

## Email 2 — le Sérum

**Objet** : Par où commencer pour votre teint
**Préheader** : Vos réponses pointent vers les taches et le manque d'éclat. C'est un travail quotidien.

> Bonjour,
>
> Vous venez de faire le diagnostic, et vos réponses décrivent des taches, des
> marques ou un teint qui manque d'uniformité. C'est un travail de fond :
> il demande des actifs appliqués tous les jours, pas un soin hebdomadaire.
>
> **Le Sérum Correcteur & Éclat** réunit trois actifs dans la même formule.
> La vitamine C ravive la luminosité, l'alpha-arbutine cible les taches et les
> marques, l'acide hyaluronique garde la peau hydratée.
>
> **Votre routine**
> Le matin : quelques gouttes sur peau propre, puis la crème et une protection
> solaire.
> Le soir : quelques gouttes sur peau propre, puis la crème.
>
> La protection solaire n'est pas une formalité. Sur un teint qu'on cherche à
> unifier, c'est elle qui empêche le travail de se défaire.
>
> [Découvrir le Sérum Correcteur & Éclat, 24,90 €]
>
> Une question ? Répondez à cet email, nous lisons tout.
>
> À bientôt,
> Irizée

**Lien** : `https://irizee.com/products/serum-correcteur-eclat`

---

## Email 3 — La Routine

**Objet** : Vos deux besoins arrivent ensemble
**Préheader** : Le masque prépare la peau, le sérum prend le relais. Et les deux coûtent moins cher ensemble.

> Bonjour,
>
> Vous venez de faire le diagnostic, et vos réponses pointent autant vers le
> sébum et les impuretés que vers les taches et le manque d'éclat.
>
> Les traiter l'un après l'autre ferait perdre des semaines. Les deux soins ne
> jouent pas sur le même terrain et ne se gênent pas : le masque prépare la
> peau une à deux fois par semaine, le sérum prend le relais au quotidien.
>
> **Votre routine**
> Le matin : le sérum sur peau propre, puis la crème et une protection
> solaire.
> Le soir : le sérum tous les soirs. Une à deux fois par semaine, le masque
> avant le sérum.
>
> **La Routine** réunit les deux pour 45,00 €, contre 49,90 € achetés
> séparément.
>
> [Découvrir La Routine, 45,00 €]
>
> Une question ? Répondez à cet email, nous lisons tout.
>
> À bientôt,
> Irizée

**Lien** : `https://irizee.com/products/la-routine`

---

## État du scénario dans Klaviyo

Monté le 27/10/2026, **laissé en brouillon**. L'activation déclenche de vrais
envois : elle revient au propriétaire du compte.

- **Segment** « Diagnostic de peau » : `Shopify Tags` contient `diagnostic`.
- **Scénario** « Diagnostic de peau — résultat », déclencheur *Ajout au
  segment*, sans réintégration.
- **Fractionnement** « Résultat du diagnostic », trois chemins :
  `diagnostic-serum`, `diagnostic-masque`, puis tous les autres.
- **Trois emails** nommés, avec objet et texte d'aperçu, chacun sur sa branche.

Les **trois emails sont écrits** dans Klaviyo : objet, texte d'aperçu et
contenu. L'expéditeur est provisoirement `maarous.younes@gmail.com`, celui du
compte.

Ce qui reste à faire dans Klaviyo :

1. **Vérifier un domaine d'envoi** et basculer l'expéditeur dessus. Partir
   d'une adresse gmail.com fait tomber les messages en indésirables : c'est
   le point le plus coûteux à négliger.
2. **Activer le scénario.**

**Piège à connaître pour tester.** Le déclencheur est l'entrée dans le
segment, et la réintégration est désactivée. Une adresse déjà étiquetée
`diagnostic` ne déclenchera donc rien, même après activation : elle n'a jamais
quitté le segment. Pour un test de bout en bout, il faut une adresse neuve, ou
retirer les étiquettes `diagnostic` de la cliente dans Shopify avant de
recommencer.

**La propriété des étiquettes s'appelle `Shopify Tags`** et contient un
tableau, par exemple `["diagnostic","diagnostic-serum"]`. C'est lu sur un
profil synchronisé, pas deviné.

**Une limite assumée** : sans réintégration, une personne qui refait le
diagnostic plus tard ne recevra pas de second email, puisqu'elle n'a jamais
quitté le segment. C'est le prix à payer pour ne pas réexpédier en boucle.

## Le scénario dans Klaviyo

Un seul scénario, trois embranchements, plutôt que trois scénarios : la
condition d'entrée est la même pour tout le monde et le contenu seul change.

1. **Déclencheur** : ajout à la liste des abonnés Shopify.
2. **Filtre d'entrée** : la cliente porte l'étiquette `diagnostic`. Sans ce
   filtre, toutes les inscriptions à la newsletter recevraient une routine
   qu'elles n'ont pas demandée.
3. **Attente** : quelques minutes, le temps que Klaviyo ait fini de
   synchroniser les étiquettes depuis Shopify. Sans cette attente, le profil
   peut arriver avant son étiquette et partir dans la mauvaise branche.
4. **Embranchement conditionnel** sur l'étiquette : `diagnostic-masque`,
   `diagnostic-serum`, sinon `diagnostic-routine`.
5. Un email par branche.

**À vérifier au moment de le monter** : le nom exact de la propriété où
Klaviyo range les étiquettes Shopify. Il se lit sur un profil déjà
synchronisé, pas dans la documentation.
