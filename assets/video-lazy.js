(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var videos = document.querySelectorAll('video[data-lazy-video]');
  if (!videos.length) return;

  videos.forEach(function (video) {
    video.preload = 'none';
    if (reducedMotion) {
      video.removeAttribute('autoplay');
      return;
    }

    if (!('IntersectionObserver' in window)) {
      video.play().catch(function () {});
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          video.play().catch(function () {});
        } else {
          video.pause();
        }
      });
    }, { threshold: 0.25 });

    observer.observe(video);
  });
})();
