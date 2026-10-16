(function () {
  'use strict';
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('video[data-lazy-video]').forEach(function (video) {
    var userPlayback = video.hasAttribute('data-user-playback');
    video.preload = 'none';
    function load() {
      var changed = false;
      video.querySelectorAll('source[data-src]').forEach(function (source) {
        source.src = source.dataset.src;
        source.removeAttribute('data-src');
        changed = true;
      });
      if (changed) video.load();
    }
    function enter() {
      load();
      if (!userPlayback && !motion.matches) video.play().catch(function () {});
    }
    var playButton = video.parentElement.querySelector('[data-video-play]');
    if (playButton) {
      playButton.addEventListener('click', function () {
        load();
        video.play().catch(function () { playButton.hidden = false; });
      });
      video.addEventListener('playing', function () { playButton.hidden = true; });
      video.addEventListener('pause', function () { playButton.hidden = false; });
      video.addEventListener('ended', function () { playButton.hidden = false; });
    }
    video.addEventListener('pointerdown', load, { once: true });
    video.addEventListener('focus', load, { once: true });
    motion.addEventListener('change', function () {
      if (motion.matches && !userPlayback) video.pause();
    });
    if (!('IntersectionObserver' in window)) { load(); return; }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) enter();
        else video.pause();
      });
    }, { threshold: 0.25, rootMargin: '120px' });
    observer.observe(video);
  });
})();
