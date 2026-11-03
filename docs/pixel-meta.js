/*
  Pixel Meta — pixel personnalisé Shopify
  Copie de référence. L'original vit dans Shopify : Paramètres →
  Événements client → « Pixel Meta ».

  Pourquoi écrit à la main plutôt que posé par le canal Facebook &
  Instagram : le parcours de ce canal se termine par la création d'une
  Boutique Facebook, que Meta a fermée en Europe. L'étape échoue, et tout
  le parcours se réinitialise à chaque passage — catalogue et pixel
  compris. Le canal ne peut donc pas activer le pixel ici.

  Conséquence à connaître : ce pixel est côté navigateur uniquement. Il n'y
  a pas d'API Conversions, donc les événements bloqués par les bloqueurs de
  publicité et par iOS sont perdus — de l'ordre d'un tiers. À compléter via
  le Gestionnaire d'événements Meta quand ce sera possible.
*/

const ID_PIXEL = '1136352515424838';

// Un article au format attendu par Meta.
const contenu = (v, quantite) => ({
  id: v?.sku || v?.id,
  quantity: quantite || 1,
  item_price: v?.price?.amount,
});

(async () => {
  const balise = document.createElement('script');
  balise.async = true;
  balise.src = 'https://connect.facebook.net/en_US/fbevents.js';
  document.head.appendChild(balise);

  window.fbq = window.fbq || function () {
    (window.fbq.queue = window.fbq.queue || []).push(arguments);
  };
  window._fbq = window.fbq;
  window.fbq.push = window.fbq;
  window.fbq.loaded = true;
  window.fbq.version = '2.0';
  window.fbq.queue = window.fbq.queue || [];

  fbq('init', ID_PIXEL);

  analytics.subscribe('page_viewed', () => {
    fbq('track', 'PageView');
  });

  analytics.subscribe('product_viewed', (e) => {
    const v = e.data.productVariant;
    fbq('track', 'ViewContent', {
      content_type: 'product',
      content_ids: [v?.sku || v?.id],
      content_name: v?.product?.title,
      value: v?.price?.amount,
      currency: v?.price?.currencyCode,
    });
  });

  analytics.subscribe('product_added_to_cart', (e) => {
    const l = e.data.cartLine;
    fbq('track', 'AddToCart', {
      content_type: 'product',
      contents: [contenu(l?.merchandise, l?.quantity)],
      value: l?.cost?.totalAmount?.amount,
      currency: l?.cost?.totalAmount?.currencyCode,
    });
  });

  analytics.subscribe('checkout_started', (e) => {
    const c = e.data.checkout;
    fbq('track', 'InitiateCheckout', {
      content_type: 'product',
      contents: (c?.lineItems || []).map((l) => contenu(l?.variant, l?.quantity)),
      num_items: (c?.lineItems || []).length,
      value: c?.totalPrice?.amount,
      currency: c?.currencyCode,
    });
  });

  analytics.subscribe('checkout_completed', (e) => {
    const c = e.data.checkout;
    fbq('track', 'Purchase', {
      content_type: 'product',
      contents: (c?.lineItems || []).map((l) => contenu(l?.variant, l?.quantity)),
      value: c?.totalPrice?.amount,
      currency: c?.currencyCode,
    });
  });

  analytics.subscribe('search_submitted', (e) => {
    fbq('track', 'Search', { search_string: e.data.searchResult?.query });
  });
})();
