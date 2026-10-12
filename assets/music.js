'use strict';
document.addEventListener('play', event => {
  if (!(event.target instanceof HTMLAudioElement)) return;
  document.querySelectorAll('audio').forEach(player => {
    if (player !== event.target) player.pause();
  });
}, true);
