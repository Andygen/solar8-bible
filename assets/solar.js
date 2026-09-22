/* Shared, dependency-free archive navigation and accessible dialogs. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  // Preserve old direct links after moving ship cards into the fleet catalogue.
  function revealHashTarget() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target?.dataset.fleetTarget) { location.replace(target.dataset.fleetTarget); return; }
    const disclosure = target?.closest('.fleet-archive details');
    if (disclosure && !disclosure.open) { disclosure.open = true; target.scrollIntoView(); }
  }
  revealHashTarget();
  addEventListener('hashchange', revealHashTarget);
  const side = $('#side'), menu = $('#menu');
  const mobileNav = matchMedia('(max-width: 960px)');
  const contentsGroups = $$('.side .contents-group, .side .chapter-tree');
  contentsGroups.forEach((group, n) => {
    const key = 'solar8-contents:' + location.pathname + ':' + (group.dataset.navGroup || group.dataset.chapter || n);
    try { const saved = sessionStorage.getItem(key); if(saved !== null) group.open = saved === 'open'; } catch {}
    group.addEventListener('toggle', () => { try { sessionStorage.setItem(key, group.open ? 'open' : 'closed'); } catch {} });
  });
  function revealContents() {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const links = $$('.side nav a[href^="#"]');
    const link = links.find(a => a.hash.slice(1) === id) || links.find(a => {
      const dest = document.getElementById(a.hash.slice(1));
      const section = dest?.tagName === 'SECTION' ? dest : /^H[1-6]$/.test(dest?.tagName || '') ? dest.closest('section') : null;
      return section?.contains(target);
    });
    let node = link?.parentElement;
    while(node && node !== side) { if(node.tagName === 'DETAILS') node.open = true; node = node.parentElement; }
  }
  revealContents(); addEventListener('hashchange', revealContents);
  const outsideNav = $$('main, body > footer, body > .top');
  function setNavInert(value) { outsideNav.forEach(el => { el.inert = value; }); }
  function closeNav(returnFocus = false) {
    side?.classList.remove('open'); document.body.classList.remove('nav-open');
    side?.removeAttribute('role'); side?.removeAttribute('aria-modal');
    setNavInert(false);
    menu?.setAttribute('aria-expanded', 'false'); menu?.setAttribute('aria-label', 'Открыть меню');
    if (returnFocus) menu?.focus();
  }
  menu?.addEventListener('click', () => {
    const open = side?.classList.toggle('open'); document.body.classList.toggle('nav-open', !!open);
    menu.setAttribute('aria-expanded', String(!!open)); menu.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    setNavInert(!!open && mobileNav.matches);
    if (open) {
      side.setAttribute('role','dialog'); side.setAttribute('aria-modal','true');
      setTimeout(() => { if(side.classList.contains('open')) side.querySelector('.contents-close')?.focus(); }, 220);
    }
  });
  $('.contents-close')?.addEventListener('click', () => closeNav(true));
  $('.nav-backdrop')?.addEventListener('click', () => closeNav(true));
  $$('.side a').forEach(a => a.addEventListener('click', () => {
    const wasOpen = side?.classList.contains('open'); closeNav();
    if (wasOpen && a.getAttribute('href').startsWith('#')) {
      const target = document.getElementById(a.hash.slice(1));
      if(target) { target.setAttribute('tabindex','-1'); target.focus({preventScroll:true}); }
    }
  }));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && side?.classList.contains('open')) closeNav(true);
    if(e.key === 'Tab' && side?.classList.contains('open')) {
      const focusable = $$('a,button,summary,[tabindex="0"]', side).filter(el => el.getClientRects().length);
      const first=focusable[0], last=focusable[focusable.length-1];
      if(e.shiftKey && document.activeElement===first) {e.preventDefault();last?.focus();}
      else if(!e.shiftKey && document.activeElement===last) {e.preventDefault();first?.focus();}
    }
  });
  matchMedia('(min-width: 961px)').addEventListener('change', e => { if(e.matches) closeNav(); });
  // Observe the actual destinations on both the Bible and all dossier pages.
  const navLinks = $$('.side a[href^="#"]');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(a => { const active = a.hash === '#' + entry.target.id; a.classList.toggle('active', active); if(active) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current'); });
      contentsGroups.forEach(group => group.classList.toggle('has-current', !!group.querySelector('a[aria-current="location"]')));
    });
  }, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
  navLinks.forEach(a => { const target = document.getElementById(a.hash.slice(1)); if (target) observer.observe(target); });
  let ticking = false;
  const homeSections = $$('.bible main > section[id]');
  const siteLinks = $$('[data-site-section]');
  const updateProgress = () => {
    const height = document.documentElement.scrollHeight - innerHeight;
    $('.reading-progress').style.width = (height > 0 ? Math.min(100, scrollY / height * 100) : 0) + '%'; ticking = false;
    if(homeSections.length) {
      let section=homeSections[0];
      for(const item of homeSections) { if(item.getBoundingClientRect().top <= 140) section=item; else break; }
      const current=section.id==='characters'?'characters':section.id==='ships'?'fleet':['production','canon','rook-gameplay'].includes(section.id)?'materials':'worlds';
      siteLinks.forEach(a => { if(a.dataset.siteSection===current) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current'); });
    }
  };
  addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(updateProgress); ticking = true; } }, { passive: true });
  updateProgress();

  const searchDialog = $('#search-dialog'), input = $('#archive-search'), results = $('#search-results'), status = $('#search-status');
  let indexPromise;
  function loadIndex() {
    if (!indexPromise) indexPromise = fetch('assets/search-index.json').then(r => { if(!r.ok) throw new Error('Search unavailable'); return r.json(); }).catch(error => { indexPromise = undefined; throw error; });
    return indexPromise;
  }
  function openSearch() { closeNav(); searchDialog.showModal(); input.focus(); loadIndex().catch(() => { status.textContent = 'Не удалось загрузить поиск. Попробуйте ещё раз.'; }); }
  document.addEventListener('keydown', e => {
    if(e.key === 'Escape') {const dialog = document.querySelector('dialog[open]'); if(dialog) {e.preventDefault(); dialog.close();}}
  }, true);
  $$('.search-open').forEach(b => b.addEventListener('click', openSearch));
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); if(!searchDialog.open) openSearch(); }
  });
  let searchVersion = 0;
  input.addEventListener('input', async () => {
    const version = ++searchVersion, query = input.value.toLocaleLowerCase().trim(); results.replaceChildren();
    if (!query) { status.textContent = 'Начните вводить название или слово из сценария.'; return; }
    status.textContent = 'Поиск…';
    try {
      const index = await loadIndex(); if(version !== searchVersion) return;
      const words = query.split(/\s+/);
      const found = index.map(entry => ({...entry, score: words.every(w => (entry.title+' '+entry.page+' '+entry.text).toLocaleLowerCase().includes(w)) ? (entry.title.toLocaleLowerCase() === query ? 30 : entry.title.toLocaleLowerCase().includes(query) ? 10 : 1) + (entry.url.startsWith('character-') ? 2 : 0) : 0})).filter(x => x.score).sort((a,b) => b.score-a.score);
      status.textContent = found.length ? 'Найдено: '+found.length+(found.length>30?' · показаны первые 30':'') : 'Ничего не найдено. Попробуйте другое имя или слово.';
      found.slice(0,30).forEach(entry => {
        const a = document.createElement('a'); a.href = entry.url;
        const title = document.createElement('strong'); title.textContent = entry.title;
        const page = document.createElement('small'); page.textContent = entry.page;
        const snippet = document.createElement('p'); const pos = entry.text.toLocaleLowerCase().indexOf(words[0]); const start = Math.max(0,pos-45); snippet.textContent = (start?'…':'')+entry.text.slice(start,start+170)+'…';
        a.append(title,page,snippet); a.addEventListener('click', () => searchDialog.close()); results.append(a);
      });
    } catch { if(version === searchVersion) status.textContent = 'Поиск временно недоступен. Используйте оглавление.'; }
  });
  input.addEventListener('keydown', e => {
    if(e.key === 'Enter' && results.firstElementChild) { e.preventDefault(); results.firstElementChild.click(); }
    if(e.key === 'ArrowDown') { e.preventDefault(); results.querySelector('a')?.focus(); }
  });
  results.addEventListener('keydown', e => {
    if(e.key === 'ArrowDown') { e.preventDefault(); document.activeElement.nextElementSibling?.focus(); }
    if(e.key === 'ArrowUp') { e.preventDefault(); (document.activeElement.previousElementSibling || input).focus(); }
  });
  $$('dialog').forEach(dialog => {
    $('.dialog-close',dialog)?.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', e => { const r=dialog.getBoundingClientRect(); if(e.target===dialog && (e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)) dialog.close(); });
  });
  const imageDialog = $('#image-dialog');
  $$('.character-page .gallery img, .character-page .zoom img, .character-page .fullconcept img, .character-page .shot img, .character-page .canonical-hero img, .fleet-art img').forEach(img => {
    const anchor = img.closest('a');
    if(!anchor) { img.tabIndex = 0; img.setAttribute('role','button'); img.setAttribute('aria-label', 'Увеличить: '+img.alt); }
    function openImage(e) { e.preventDefault(); $('img',imageDialog).src=img.dataset.fullSrc || img.currentSrc || img.src; $('img',imageDialog).alt=img.alt; $('p',imageDialog).textContent=img.alt; imageDialog.showModal(); }
    (anchor || img).addEventListener('click',openImage);
    if(!anchor) img.addEventListener('keydown',e => { if(e.key==='Enter'||e.key===' ') openImage(e); });
  });
})();
