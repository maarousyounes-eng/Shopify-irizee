/*
  Google Analytics 4 — pixel personnalisé Shopify
  Copie de référence. L'original vit dans Shopify : Paramètres →
  Événements client → « Google Analytics 4 ». Modifier ici ne change rien
  en ligne ; il faut recopier dans l'admin.

  Pourquoi un pixel écrit à la main plutôt que l'intégration native du
  canal Google & YouTube : cette dernière est verrouillée derrière la
  création d'un compte Merchant Center, que Google suspend quand le site
  n'a pas encore ses pages légales. À remplacer par l'intégration native
  dès que les CGV, la politique de retour et les mentions légales sont en
  ligne — et supprimer ce pixel à ce moment-là, pour ne pas compter deux
  fois.
*/

const ID_MESURE = 'G-ZCMPW1MWF0';
const NOM_COOKIE = '_iz_cid';

// GA4 identifie un visiteur par un `client_id` qu'il garde d'ordinaire dans
// son propre cookie. Ici impossible : un pixel personnalisé s'exécute dans
// un bac à sable, sur une autre origine que la boutique, et ce cookie-là ne
// survivrait pas d'une page à l'autre — chaque page compterait un nouveau
// visiteur. On tient donc l'identifiant nous-mêmes, dans un cookie du site,
// via l'API que Shopify expose pour ça.
const fabriquerIdentifiant = () =>
  Math.floor(Math.random() * 1e9) + '.' + Math.floor(Date.now() / 1000);

// Une ligne d'article au format attendu par GA4.
const article = (v, quantite) => ({
  item_id: v?.sku || v?.id,
  item_name: v?.product?.title,
  item_variant: v?.title,
  item_brand: v?.product?.vendor,
  price: v?.price?.amount,
  quantity: quantite || 1,
});

(async () => {
  // L'identifiant client ne doit JAMAIS bloquer la mesure. `browser.cookie`
  // peut être indisponible — API absente, consentement « préférences »
  // refusé — et une promesse qui ne se résout pas emporterait tout ce qui
  // suit, y compris le chargement de la balise. On part donc d'un
  // identifiant de session, et le cookie ne fait que le rendre durable
  // quand il répond.
  let cid = fabriquerIdentifiant();
  try {
    const delai = new Promise((r) => setTimeout(() => r(undefined), 1000));
    const lu = await Promise.race([browser.cookie.get(NOM_COOKIE), delai]);
    if (lu) cid = lu;
    else browser.cookie.set(NOM_COOKIE, cid);
  } catch (e) {
    // Tant pis : l'identifiant de session suffit à mesurer la visite.
  }

  const balise = document.createElement('script');
  balise.async = true;
  balise.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID_MESURE;
  document.head.appendChild(balise);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  gtag('js', new Date());
  gtag('config', ID_MESURE, {
    client_id: cid,
    // Shopify nous prévient lui-même de chaque page vue : laisser gtag en
    // envoyer une de son côté les compterait en double.
    send_page_view: false,
    transport_type: 'beacon',
  });

  analytics.subscribe('page_viewed', (e) => {
    gtag('event', 'page_view', {
      page_location: e.context.document.location.href,
      page_title: e.context.document.title,
      page_referrer: e.context.document.referrer,
    });
  });

  analytics.subscribe('product_viewed', (e) => {
    const v = e.data.productVariant;
    gtag('event', 'view_item', {
      currency: v?.price?.currencyCode,
      value: v?.price?.amount,
      items: [article(v, 1)],
    });
  });

  analytics.subscribe('product_added_to_cart', (e) => {
    const l = e.data.cartLine;
    gtag('event', 'add_to_cart', {
      currency: l?.cost?.totalAmount?.currencyCode,
      value: l?.cost?.totalAmount?.amount,
      items: [article(l?.merchandise, l?.quantity)],
    });
  });

  analytics.subscribe('checkout_started', (e) => {
    const c = e.data.checkout;
    gtag('event', 'begin_checkout', {
      currency: c?.currencyCode,
      value: c?.totalPrice?.amount,
      items: (c?.lineItems || []).map((l) => article(l?.variant, l?.quantity)),
    });
  });

  analytics.subscribe('checkout_completed', (e) => {
    const c = e.data.checkout;
    gtag('event', 'purchase', {
      transaction_id: c?.order?.id || c?.token,
      currency: c?.currencyCode,
      value: c?.totalPrice?.amount,
      tax: c?.totalTax?.amount,
      shipping: c?.shippingLine?.price?.amount,
      items: (c?.lineItems || []).map((l) => article(l?.variant, l?.quantity)),
    });
  });

  analytics.subscribe('search_submitted', (e) => {
    gtag('event', 'search', { search_term: e.data.searchResult?.query });
  });
})();
