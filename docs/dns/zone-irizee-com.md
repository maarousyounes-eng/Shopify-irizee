# Zone DNS d'irizee.com

Relevé le 17/11/2026 dans Shopify (Paramètres > Domaines > irizee.com >
Paramètres DNS), recoupé avec `dig`. C'est la référence pour toute migration
du DNS : chaque ligne doit exister à l'identique chez le nouvel hébergeur
**avant** de changer les serveurs de noms.

- Domaine acheté via Shopify (registrar Tucows), créé le 24/08/2026,
  renouvellement automatique le 10/08/2027 (17 USD).
- Serveurs de noms actuels : ceux de Shopify (`ns-cloud-b1..b4.googledomains.com`).
- Shopify accepte A, AAAA, CNAME, MX, TXT, SRV, **pas NS**. Les serveurs de
  noms sont modifiables (bouton « Changer »), sans transfert du domaine.

## Enregistrements

| Type | Nom | Valeur | Rôle |
|---|---|---|---|
| A | @ | 23.227.38.67 | Boutique Shopify |
| AAAA | @ | 2620:127:f00f:7:: | Boutique Shopify |
| CNAME | www | shops.myshopify.com | Boutique Shopify |
| CNAME | account | shops.myshopify.com | Compte client |
| CNAME | mailersp2 | bd8a46abb529.p800.email.myshopify.com | E-mails Shopify (domaine d'envoi) |
| CNAME | mailery9d | e5cb8d8b510.p798.email.myshopify.com | E-mails Shopify (domaine d'envoi) |
| CNAME | pdk1._domainkey.mailersp2 | dkim3.bd8a46abb529.p800.email.myshopify.com | DKIM Shopify |
| CNAME | pdk2._domainkey.mailersp2 | dkim4.bd8a46abb529.p800.email.myshopify.com | DKIM Shopify |
| CNAME | y9d._domainkey | dkim1.e5cb8d8b510.p798.email.myshopify.com | DKIM Shopify |
| CNAME | y9d2._domainkey | dkim2.e5cb8d8b510.p798.email.myshopify.com | DKIM Shopify |
| MX | @ | smtp.google.com (priorité 1) | Boîte contact@ (Google Workspace) |
| TXT | @ | google-site-verification=KMZEcxzuGdAMXcobfAPY8PFXNbJlVVR3FtCeh_HlBWo | Search Console / Workspace |
| TXT | @ | v=spf1 include:_spf.google.com ~all | SPF Google |
| TXT | _dmarc | v=DMARC1; p=none | DMARC |
| TXT | _provider | shopify | Marqueur Shopify |
| TXT | google._domainkey | v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCPCMNlg5Pv7ttjMTeZdDpRbf/LInJZRvkCtxCo0ih2YLLzuNxg7Q5BCsUpO4YhSOfDgMBqg4yGPtokrW7ISJRciCG1f9F95aQD7t2OtkDjXA4cmffRodaFORwrTER4e6559tm4V49F81IwB+OfPL8S0Pg2zjAqERGH+sZQ1Z3eeQIDAQAB | DKIM Google |

## À ajouter pour Klaviyo (domaine d'envoi dédié envoi.irizee.com)

| Type | Nom | Valeur |
|---|---|---|
| NS | envoi | ns1.klaviyo.com |
| NS | envoi | ns2.klaviyo.com |
| NS | envoi | ns3.klaviyo.com |
| NS | envoi | ns4.klaviyo.com |
| TXT | @ | klaviyo-site-verification=RWDA3W |

Les NS sont la raison du déménagement : Shopify ne les accepte pas.

## Migration vers Cloudflare (17/11/2026)

- Compte Cloudflare (offre Free), zone irizee.com créée. Serveurs de noms
  attribués : `faye.ns.cloudflare.com`, `valentin.ns.cloudflare.com`.
- Tous les enregistrements en **DNS only** (nuage gris) : Shopify refuse le
  proxy Cloudflare devant la boutique. « Bot Preference Sync » désactivé (il
  réécrirait le robots.txt).
- Le scan automatique n'avait repris que 9 enregistrements sur 16 : les 6
  CNAME d'e-mail Shopify et `_provider` ont été ajoutés par import d'un
  fichier de zone, avec les 4 NS `envoi` et le TXT de vérification Klaviyo.
- Contrôle `dig` sur `faye.ns.cloudflare.com` contre l'ancien serveur
  Shopify : 15 réponses identiques ; seule différence, le TXT Klaviyo ajouté.
  Pas de DNSSEC (aucun DS).
- **Retour arrière** : dans Shopify, remettre les serveurs de noms par défaut
  de Shopify. La zone Shopify n'est pas supprimée.
- **Bascule faite le 17/11/2026 vers 15:50** dans Shopify (serveurs de noms
  personnalisés : faye / valentin.ns.cloudflare.com). Shopify annonce jusqu'à
  24 h pour la prise en compte au registre. Bouton de retour arrière :
  « Restaurer les serveurs de nom de Shopify » (Paramètres > Domaines >
  irizee.com > Paramètres DNS).
- Désormais, **toute modification DNS se fait dans Cloudflare**, plus dans
  Shopify.
- Reste à faire après propagation : valider `envoi.irizee.com` dans Klaviyo
  (Paramètres > Domaines), puis l'utiliser comme domaine d'envoi.
