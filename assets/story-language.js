/* Generated fallbacks and editorial drafts come from story-scenes.json.
   Game-linked strings remain owned by dialogues.json. */
(() => {
  const select = document.querySelector('#story-language-select');
  const status = document.querySelector('#story-language-status');
  const nodes = [...document.querySelectorAll('[data-en][data-ru]')];
  let language = 'ru';
  try { language = localStorage.getItem('solar8-dialogue-language') || 'ru'; } catch (_) {}
  select.value = language === 'en' ? 'en' : 'ru';
  function render() {
    let missing = 0;
    for (const node of nodes) {
      const text = node.dataset[select.value];
      node.textContent = select.value==='en' && !node.dataset.dialogueId ? (window.SOLAR_I18N?.t(text || node.dataset.en) || text || node.dataset.en) : text || node.dataset.en;
      node.lang = text ? select.value : 'en';
      if (!text) { missing++; node.title = 'Перевод отсутствует; показан EN'; }
    }
    status.textContent = missing ? `Без перевода: ${missing}. Показан EN.` : 'Перевод доступен для всех реплик.';
    try { localStorage.setItem('solar8-dialogue-language', select.value); } catch (_) {}
  }
  select.addEventListener('change', render);
  render();
  fetch('assets/dialogues.json', {cache:'no-cache'}).then(r => {
    if (!r.ok) throw Error(r.status); return r.json();
  }).then(data => {
    const entries = new Map(data.entries.map(e => [e.id,e]));
    for (const node of nodes.filter(n => n.dataset.dialogueId)) {
      const e = entries.get(node.dataset.dialogueId);
      if (!e) throw Error('Missing dialogue ID');
      node.dataset.ru=e.ru; node.dataset.en=e.en;
    }
    render();
  }).catch(() => {status.textContent += ' Каталог недоступен: показана версия из сборки сайта.';});
})();
