// Eventos de engajamento. Tudo é empilhado em window.dataLayer (o GTM lê de lá).
// REGRA LGPD: sem consentimento (window.__plConsent === 'granted', definido em consent.js) nada é registrado.
// Formato: dataLayer.push({ event: '<nome>', <parametros planos> }). Nome e parâmetros em snake_case.
(function () {
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  // GA4 direto (legado, sem aviso de cookies): só se data-ga4-id existir. Prefira o GTM.
  var self = document.currentScript;
  var id = self && self.dataset.ga4Id;
  if (id) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', id, { anonymize_ip: true });
  }

  var granted = function () { return window.__plConsent === 'granted'; };
  function snake(k) { return k.replace(/[A-Z]/g, function (c) { return '_' + c.toLowerCase(); }); }
  function clip(v, n) { v = String(v == null ? '' : v).replace(/\s+/g, ' ').trim(); return v.length > n ? v.slice(0, n - 1) + '…' : v; }

  function slug(t) {
    return String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
  }
  function labelOf(sec) { // nome legível da seção: data-section, título (h1/h2) ou aria-label
    if (sec.dataset.section) return sec.dataset.section;
    var lb = sec.getAttribute('aria-labelledby'), h = lb && document.getElementById(lb);
    return slug(h ? h.textContent : (sec.getAttribute('aria-label') || sec.id || sec.tagName));
  }
  function sectionOf(el) {
    var sec = el.closest('main section, header, footer, nav');
    return sec ? labelOf(sec) : '';
  }
  function textOf(el) { // texto visível, sem o aviso "(abre em nova aba)" dos leitores de tela
    var c = el.cloneNode(true);
    c.querySelectorAll('.visually-hidden, svg').forEach(function (n) { n.remove(); });
    return c.textContent;
  }

  function track(name, params) {
    if (!granted()) return false;
    var o = { event: name, page_path: location.pathname };
    Object.keys(params || {}).forEach(function (k) { if (params[k] !== '' && params[k] != null) o[k] = clip(params[k], 100); });
    window.dataLayer.push(o);
    return true;
  }

  // ---- Cliques ----
  document.addEventListener('click', function (ev) {
    if (!granted()) return;
    var el = ev.target.closest('[data-event]');
    var link = ev.target.closest('a[href]');
    var params = {};
    var name;
    if (el) {
      name = el.dataset.event;
      Object.keys(el.dataset).forEach(function (k) {
        if (k === 'event' || k.indexOf('email') === 0) return; // nunca envia o e-mail
        params[snake(k)] = el.dataset[k];
      });
      if (name === 'menu_toggle') params.state = el.getAttribute('aria-expanded') === 'true' ? 'close' : 'open';
    } else if (link && /^https?:/i.test(link.href) && link.hostname !== location.hostname) {
      name = 'outbound_click'; // qualquer link externo sem data-event
      el = link;
    } else {
      return;
    }
    var a = el.closest('a[href]') || (el.tagName === 'A' ? el : null);
    if (a && /^https?:/i.test(a.href)) {
      params.link_domain = a.hostname;
      params.link_url = a.hostname === location.hostname ? a.pathname : a.origin + a.pathname;
    }
    if (a || el.tagName === 'BUTTON') params.link_text = textOf(el);
    params.section_id = sectionOf(el);
    track(name, params);
  }, true);

  // ---- Abrir/fechar <details> (FAQ, "ver mais" das recomendações) ----
  document.addEventListener('toggle', function (ev) {
    var d = ev.target;
    if (!d.open || d.tagName !== 'DETAILS') return;
    var q = d.querySelector('summary');
    if (d.classList.contains('faq')) track('faq_toggle', { question: q && textOf(q), section_id: sectionOf(d) });
    else if (d.classList.contains('reco__more')) {
      var card = d.closest('.card'), h = card && card.querySelector('.card__title');
      track('reco_expand', { category: h && textOf(h), section_id: sectionOf(d) });
    }
  }, true);

  // ---- Carrossel de depoimentos (primeira rolagem horizontal) ----
  var scrolled = new WeakSet();
  document.addEventListener('scroll', function (ev) {
    var t = ev.target;
    if (!t || !t.classList || !t.classList.contains('quotes') || scrolled.has(t)) return;
    if (track('carousel_scroll', { section_id: sectionOf(t) })) scrolled.add(t);
  }, true);

  // ---- Profundidade de rolagem (25/50/75/100) ----
  var fired = {}, ticking = false;
  function depth() {
    ticking = false;
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (max <= 0) return;
    var pct = (window.scrollY / max) * 100;
    [25, 50, 75, 100].forEach(function (t) {
      if (pct >= t - (t === 100 ? 2 : 0) && !fired[t] && track('scroll_depth', { depth: t })) fired[t] = true;
    });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(depth); } }, { passive: true });

  // ---- Seções vistas (uma vez por página, quando cruzam o centro da tela) ----
  var seen = new WeakSet(), io = null;
  function observeSections() {
    if (!('IntersectionObserver' in window)) return;
    if (io) io.disconnect();
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting || seen.has(en.target)) return;
        var sec = en.target;
        if (track('section_view', { section_id: labelOf(sec) })) {
          seen.add(sec); io.unobserve(sec);
        }
      });
    }, { rootMargin: '-35% 0px -35% 0px', threshold: 0 });
    document.querySelectorAll('main section[aria-labelledby], main section[id]').forEach(function (sec) { if (!seen.has(sec)) io.observe(sec); });
  }
  var nf = false;
  function notFound() { if (!nf && document.body.dataset.page === '404' && track('page_not_found', { missing_path: location.pathname })) nf = true; }
  document.addEventListener('DOMContentLoaded', function () { observeSections(); notFound(); });
  // Quando o consentimento é dado depois do carregamento, recomeça a observar o que já está na tela.
  document.addEventListener('pl:consent', function () {
    observeSections(); depth(); notFound();
  });
})();
