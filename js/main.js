// Navegação mobile: toggle acessível, fecha com Esc e ao navegar.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (!toggle || !nav) return;

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    toggle.querySelector('use').setAttribute('href', open ? '#i-x' : '#i-menu');
  }

  toggle.addEventListener('click', function () { setOpen(!nav.classList.contains('is-open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
  });
})();

// E-mail montado em runtime (evita scraping simples). Sem JS, o texto "[arroba]" permanece sem link.
(function () {
  document.querySelectorAll('[data-email-user]').forEach(function (a) {
    var addr = a.dataset.emailUser + '@' + a.dataset.emailDomain;
    a.href = 'mailto:' + addr;
    var meta = a.closest('.social') && a.closest('.social').querySelector('[data-email-text]');
    if (meta) meta.textContent = addr;
  });
})();
