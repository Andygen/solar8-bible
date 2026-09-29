/* One language preference for the site and the story reader. */
(() => {
  const select=document.querySelector('#site-language');
  if(!select)return;
  let language='ru',catalog,applying=false;
  const originalTitle=document.title;
  const originals=new WeakMap();
  try{language=localStorage.getItem('solar8-dialogue-language')==='en'?'en':'ru';}catch(_){}
  select.value=language;
  const skip='script,style,code,pre,[data-en],[data-ru],[data-dialogue-id],.dialogue-pair';
  function t(source){
    if(catalog?.[source])return catalog[source][language] || source;
    if(language==='ru')return source;
    const patterns=[
      [/^Показано (\d+) из (\d+)$/, 'Showing $1 of $2'],
      [/^(\d+) из (\d+) реплик · версия (.+)$/, '$1 of $2 lines · revision $3'],
      [/^Найдено: (\d+)( · показаны первые 30)?$/, (_,n,more)=>'Found: '+n+(more?' · first 30 shown':'')],
      [/^Продолжить: (.+)$/, 'Continue: $1'],
      [/^Общий источник · (.+) · связанных реплик: (\d+)$/, 'Shared source · $1 · linked lines: $2'],
      [/^Без перевода: (\d+)\. Показан EN\.$/, '$1 untranslated. Showing EN.'],
      [/^(EN совпадает со сценарием|Игровая адаптация)( · .+) · запись (\d+)$/, (_,label,context,n)=>(label.startsWith('EN')?'EN matches scenario':'Game adaptation')+context+' · record '+n],
      [/^Увеличить: (.+)$/, (_,label)=>'Enlarge: '+t(label)]
    ];
    for(const [pattern,replacement] of patterns)if(pattern.test(source))return source.replace(pattern,replacement);
    return source;
  }
  window.SOLAR_I18N={t,get language(){return language;}};
  function translate(root=document.body){
    if(!catalog)return;
    applying=true;
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
    let n;
    while((n=walker.nextNode())){
      if(n.parentElement?.closest(skip))continue;
      const text=n.nodeValue,trim=text.trim();
      const previous=originals.get(n);
      const source=previous && (text===previous.rendered || text===previous.source) ? previous.source : text;
      const output=t(source.trim());
      if(!output)continue;
      const rendered=source.replace(source.trim(),output);
      originals.set(n,{source,rendered});
      if(n.nodeValue!==rendered)n.nodeValue=rendered;
    }
    for(const el of root.querySelectorAll('[aria-label],[title],[placeholder],[alt]')){
      for(const attr of ['aria-label','title','placeholder','alt']){
        if(!el.hasAttribute(attr))continue;
        const key='i18nOriginal'+attr.replace('-','');
        const current=el.getAttribute(attr),old=el.dataset[key];
        const source=old && (current===old || current===el.dataset[key+'Rendered']) ? old : current;
        const output=t(source);
        if(output!==current){el.dataset[key]=source;el.dataset[key+'Rendered']=output;el.setAttribute(attr,output);}
      }
    }
    document.documentElement.lang=language;
    const title=catalog[originalTitle];
    if(title)document.title=title[language];
    applying=false;
  }
  function apply(){
    language=select.value;
    try{localStorage.setItem('solar8-dialogue-language',language);}catch(_){}
    for(const local of document.querySelectorAll('#story-language-select,#bound-language')){
      local.value=language;local.dispatchEvent(new Event('change'));
    }
    translate();
    document.dispatchEvent(new CustomEvent('site-language-change',{detail:language}));
  }
  select.addEventListener('change',apply);
  const read=url=>fetch(url,{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json();});
  Promise.all([read('assets/site-translations.json'),read('assets/dialogues.json').catch(()=>null)]).then(([data,game])=>{
    catalog=data.strings;
    // Unbound quotation excerpts resolve from the same master, never a second copy.
    for(const e of game?.entries || []){
      catalog[e.en]={en:e.en,ru:e.ru};
      catalog['“'+e.en+'”']={en:'“'+e.en+'”',ru:'«'+e.ru+'»'};
    }
    apply();
    let scheduled=false;
    new MutationObserver(records=>{
      if(applying||scheduled)return;
      if(!records.length)return;
      scheduled=true;requestAnimationFrame(()=>{scheduled=false;translate();});
    }).observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder','alt']});
  }).catch(()=>{
    select.title='Не удалось загрузить переводы. Обновите страницу.';
  });
})();
