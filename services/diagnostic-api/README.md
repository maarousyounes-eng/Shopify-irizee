# Analyse photo du diagnostic

Une seule fonction, `api/analyse.js`. Elle existe parce que la clé d'API ne
peut pas vivre dans le thème Shopify, qui est public.

## État

Déployé le 26/10/2026 sur le projet Vercel `irizee-diagnostic` :
`https://irizee-diagnostic.vercel.app/api/analyse`

`ORIGINES_AUTORISEES` et `MODELE` sont posées. Il manque `ANTHROPIC_API_KEY`,
que le propriétaire du compte pose lui-même : une clé ne se colle pas dans une
conversation ni dans un dépôt.

## Mise en service

1. Créer une clé sur console.anthropic.com.
2. Déployer ce dossier sur Vercel comme un projet à part.
3. Poser trois variables d'environnement **dans Vercel**, jamais dans le dépôt :

   | Nom | Valeur |
   |---|---|
   | `ANTHROPIC_API_KEY` | la clé |
   | `ORIGINES_AUTORISEES` | `https://irizee.com,https://0nz0p1-61.myshopify.com` |
   | `MODELE` | facultatif, `claude-sonnet-5-5` par défaut |

4. Reporter l'URL de la fonction dans le réglage « Adresse de l'analyse » de
   la section Diagnostic, et cocher « Proposer la photo ».

`ORIGINES_AUTORISEES` n'est pas une formalité : sans elle la fonction refuse
tout. Une fonction ouverte est une fonction que n'importe qui fait payer au
propriétaire de la clé.

## Ce que la fonction ne fait pas

La photo n'est écrite nulle part : ni disque, ni base, ni journal. Elle
traverse la mémoire du temps de l'appel, et c'est tout. La réponse ne contient
que trois notes de 0 à 3 et une phrase d'observation.

Le modèle a pour consigne de ne poser aucun diagnostic médical et de ne nommer
aucune pathologie. Les notes sont bornées côté serveur : même si le modèle
renvoie n'importe quoi, rien ne sort de l'intervalle 0 à 3.

## Coût

Un appel, c'est une image et quelques centaines de jetons. L'ordre de grandeur
est le centime par analyse, donc quelques euros par mois pour un millier de
diagnostics. À surveiller quand même : c'est un point de dépense ouvert sur
Internet, d'où la liste d'origines.
