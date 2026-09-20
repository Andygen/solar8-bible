/* Reading navigation: native anchors work without JavaScript. */
(() => {
  'use strict';
  const tree = document.querySelector('.scenario-tree');
  const groups = [...tree.querySelectorAll('.chapter-tree')];
  document.querySelectorAll('[data-tree]').forEach(button => button.addEventListener('click', () => {
    groups.forEach(group => { group.open = button.dataset.tree === 'open'; });
  }));
  document.querySelector('.open-contents').addEventListener('click', () => {
    if (innerWidth <= 960) document.querySelector('#menu').click();
    else {groups[0].open = true; tree.querySelector('a').focus();}
  });
  function revealHash() {
    const hash = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(hash);
    const chapter = target?.dataset.chapter || (target?.classList.contains('chapter-reader') ? target.id : null);
    const group = groups.find(g => g.dataset.chapter === chapter);
    if (group) group.open = true;
  }
  addEventListener('hashchange', revealHash); revealHash();
  const key = 'solar8-scenario-position-v1';
  const steps = [...document.querySelectorAll('#overview, .reader-mission, #solar-crown')];
  const resume = document.querySelector('.resume-reading');
  try {
    const saved = localStorage.getItem(key);
    const target = steps.find(s => s.id === saved);
    if (target && saved !== 'overview') {
      const heading = target.querySelector('h2,h3');
      resume.hidden = false; resume.textContent = 'Продолжить: ' + (saved === 'solar-crown' ? 'Solar Crown' : saved.replace('mission-','')) + ' →';
      resume.title = heading?.textContent || 'Продолжить чтение';
      resume.addEventListener('click', () => { location.hash = saved; });
    }
  } catch (_) { /* Private browsing may disable storage; reading remains available. */ }
  let queued = false, last = '';
  function updatePosition() {
    queued = false;
    let current = steps[0];
    for (const step of steps) {if (step.getBoundingClientRect().top <= 150) current = step; else break;}
    if (current.id === last) return; last = current.id;
    try {localStorage.setItem(key, last);} catch (_) {}
  }
  addEventListener('scroll', () => {if (!queued) {queued = true; requestAnimationFrame(updatePosition);}}, {passive:true});
})();
