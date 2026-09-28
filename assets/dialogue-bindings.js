/* Text is owned by dialogues.json; HTML is a generated offline fallback. */
(() => {
  const nodes=[...document.querySelectorAll('[data-dialogue-id]')];
  if(!nodes.length)return;
  const select=document.querySelector('#bound-language'),status=document.querySelector('#bound-status');
  let entries;
  try {select.value=localStorage.getItem('solar8-dialogue-language') || 'ru';} catch (_) {select.value='ru';}
  function render(){for(const node of nodes){const e=entries.get(node.dataset.dialogueId);if(!e)throw new Error('Missing ID: '+node.dataset.dialogueId);node.textContent=e[select.value];node.lang=select.value;node.title=e.id+' · dialogues.json';}}
  select.disabled=true;
  fetch('assets/dialogues.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json();}).then(data=>{
    entries=new Map(data.entries.map(e=>[e.id,e]));select.disabled=false;render();
    status.textContent=`Общий источник · ${data.revision} · связанных реплик: ${nodes.length}`;
    select.addEventListener('change',()=>{render();try{localStorage.setItem('solar8-dialogue-language',select.value);}catch(_){}});
  }).catch(()=>{status.textContent='Общий JSON недоступен. Показана сохранённая английская версия; перевод временно недоступен.';});
})();
