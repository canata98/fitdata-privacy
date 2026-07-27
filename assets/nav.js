(function () {
  'use strict';

  document.documentElement.classList.remove('no-js');

  var nav = document.querySelector('nav');
  if (!nav) return;

  var links = nav.querySelector('.nav-links');
  if (!links) return;

  var toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'nav-toggle';
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-controls', 'nav-menu');
  toggle.setAttribute('aria-label', 'Open menu');
  toggle.innerHTML = '<span></span><span></span><span></span>';

  links.id = 'nav-menu';
  nav.insertBefore(toggle, links);

  var focusableSelector = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

  function setOpen(open) {
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    links.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      var first = links.querySelector(focusableSelector);
      if (first) first.focus();
    }
  }

  function closeMenu() { setOpen(false); }

  toggle.addEventListener('click', function () {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });

  document.addEventListener('click', function (e) {
    if (toggle.getAttribute('aria-expanded') === 'true' &&
        !links.contains(e.target) && !toggle.contains(e.target)) {
      closeMenu();
    }
  });

  links.querySelectorAll('a').forEach(function (anchor) {
    anchor.addEventListener('click', closeMenu);
  });

  links.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab' || toggle.getAttribute('aria-expanded') !== 'true') return;
    var focusable = Array.prototype.slice.call(links.querySelectorAll(focusableSelector));
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 600) closeMenu();
  });

  document.querySelectorAll('.nav-lang a[data-alt-href]').forEach(function (langLink) {
    var alt = langLink.getAttribute('data-alt-href');
    if (alt) langLink.setAttribute('href', alt);
  });
})();
