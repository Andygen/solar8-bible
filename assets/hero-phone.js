/* Autoplay when visible, with a manual home-button pause and reduced-motion support. */
(() => {
  const video=document.querySelector('.phone-screen video');
  const button=document.querySelector('.phone-toggle');
  if(!video || !button)return;
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  let wantsPlayback=!motion.matches,visible=true;
  video.muted=true;
  function state(){
    button.setAttribute('aria-pressed',String(!video.paused));
    button.setAttribute('aria-label',video.paused?'Воспроизвести видео':'Приостановить видео');
  }
  function sync(){
    if(wantsPlayback && visible && !document.hidden)video.play().catch(state);
    else video.pause();
    state();
  }
  button.addEventListener('click',()=>{wantsPlayback=video.paused;sync();});
  video.addEventListener('play',state);video.addEventListener('pause',state);
  document.addEventListener('visibilitychange',sync);
  motion.addEventListener('change',()=>{wantsPlayback=!motion.matches;sync();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();},{threshold:0.1}).observe(video);
  sync();
})();
