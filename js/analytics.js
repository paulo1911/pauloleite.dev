// Eventos de conversão. Delegado: lê data-event + data-* dos elementos.
// Sempre empilha em window.dataLayer (sem rede). O GA4 só carrega se houver ID
// (atributo data-ga4-id neste <script>, vindo de data/site.json "ga4_id").
(function () {
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  var self = document.currentScript;
  var id = self && self.dataset.ga4Id;
  if (id) {
    // Antes de definir um ID: adicionar aviso de cookies (LGPD) — ver docs/ANALYTICS.md.
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', id, { anonymize_ip: true });
  }

  function snake(k) { return k.replace(/[A-Z]/g, function (c) { return '_' + c.toLowerCase(); }); }

  document.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-event]');
    if (!el) return;
    var params = { page_path: location.pathname };
    Object.keys(el.dataset).forEach(function (k) {
      if (k === 'event' || k.indexOf('email') === 0) return; // nunca envia o e-mail
      params[snake(k)] = el.dataset[k];
    });
    window.dataLayer.push({ event: el.dataset.event, params: params });
    if (id) gtag('event', el.dataset.event, params);
  }, true);
})();
