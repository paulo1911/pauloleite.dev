// Consentimento de cookies (LGPD) + carregamento do Google Tag Manager SOMENTE após aceite.
// Sem aceite: nenhum script do Google é carregado e nenhum evento é registrado.
(function () {
  var self = document.currentScript;
  var gtm = self && self.dataset.gtmId;
  var KEY = 'pl_consent';
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.__plConsent = null;
  if (!gtm) return;

  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function write(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function clearCookies() {
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (n === '_ga' || n.indexOf('_ga_') === 0 || n === '_gid' || n.indexOf('_gat') === 0) {
        [location.hostname, '.' + location.hostname.replace(/^www\./, ''), ''].forEach(function (d) {
          document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
        });
      }
    });
  }

  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });

  var loaded = false;
  function load() {
    if (loaded) return;
    loaded = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(gtm);
    document.head.appendChild(s);
    document.dispatchEvent(new Event('pl:consent'));
  }

  document.addEventListener('DOMContentLoaded', function () {
    var box = document.getElementById('consent');
    var openBtn = document.getElementById('consent-open');
    if (!box) return;
    var last = null;
    function show(from) { last = from || null; box.hidden = false; if (from) { var b = box.querySelector('[data-consent]'); if (b) b.focus(); } }
    function hide() { box.hidden = true; if (last) { last.focus(); last = null; } }
    function choose(v) {
      var prev = read();
      write(v);
      window.__plConsent = v;
      if (v === 'granted') { load(); hide(); }
      else { clearCookies(); hide(); if (prev === 'granted') location.reload(); }
    }
    box.addEventListener('click', function (e) { var b = e.target.closest('[data-consent]'); if (b) choose(b.dataset.consent); });
    box.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
    if (openBtn) openBtn.addEventListener('click', function () { show(openBtn); });
    var cur = read();
    window.__plConsent = cur;
    if (cur === 'granted') load(); else if (cur !== 'denied') show();
  });
})();
