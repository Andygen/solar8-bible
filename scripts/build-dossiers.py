"""Build imported character dossiers, ROOK Mk II gallery and roster links.
Sources: assets/dossiers.json, assets/media-imports.json and existing art/VO pages.
Requires BeautifulSoup 4. Run before build-fleet.py.
"""
from pathlib import Path
from copy import deepcopy
from html import escape as esc
import json
from bs4 import BeautifulSoup as Soup

ROOT=Path(__file__).resolve().parents[1]
def read(name): return Soup((ROOT/name).read_text(encoding='utf-8'),'html.parser')
def fragment(html): return Soup(html,'html.parser')
def save(name,page): (ROOT/name).write_text(str(page),encoding='utf-8')
records=json.loads((ROOT/'assets/dossiers.json').read_text(encoding='utf-8'))
media=json.loads((ROOT/'assets/media-imports.json').read_text(encoding='utf-8'))
template=read('character-maya.html')
home=read('index.html')
search_path=ROOT/'assets/search-index.json'
search=json.loads(search_path.read_text(encoding='utf-8'))
labels={'front':'Анфас','profile-left':'Профиль влево','profile-right':'Профиль вправо','full-body':'Полный рост','back':'Вид со спины','waist-calm':'Спокойное состояние','waist-focused':'Сосредоточенность','three-quarter':'Три четверти','corrupted':'Заражённое состояние','liberated':'Освобождённое состояние','three-quarter-left':'Три четверти слева','three-quarter-right':'Три четверти справа','optic-detail':'Крупный план оптики','robe-full-front':'Полный рост спереди','robe-full-back':'Полный рост сзади','robe-waist-front':'Поясной портрет','robe-waist-three-quarter':'Поясной портрет / три четверти','robe-waist-hood':'Поднятый капюшон','mk2-hero':'Основной концепт Mk II','mk2-front':'Анфас Mk II','mk2-back':'Вид сзади / стыковочный узел','mk2-side':'Боковой ракурс / сторона ремонта','mk2-repair-detail':'Сменная панель и сервисный захват'}
def label(m): return labels.get(Path(m['file']).stem.split('-',1)[1],Path(m['file']).stem)
def img(m,alt,eager=False):
    return f'<img src="{m["preview"]}" data-full-src="{m["original"]}" width="{m["width"]}" height="{m["height"]}" alt="{esc(alt)}" decoding="async" '+('fetchpriority="high"' if eager else 'loading="lazy"')+'/>'
def gallery(items,name):
    return '<div class="gallery">'+''.join(f'<figure class="card"><a href="{m["original"]}" aria-label="Увеличить: {esc(name)} — {esc(label(m))}">{img(m,name+" — "+label(m))}</a><figcaption class="caption"><b>{esc(label(m))}</b><br/><a class="dossier-download" href="{m["original"]}" download>Скачать оригинальный PNG ↓</a></figcaption></figure>' for m in items)+'</div>'

vo=[]
for path in sorted(ROOT.glob('scripts-*.html')):
    page=read(path.name)
    for line in page.select('.line'):
        speaker=line.select_one('.speaker'); text=line.select_one('.text')
        if not speaker or not text: continue
        mission=line.find_parent('article')
        anchor=mission.h3.get('id') if mission and mission.h3 else None
        vo.append((speaker.get_text(' ',strip=True).split(' P')[0],text.get_text(' ',strip=True),path.name+('#'+anchor if anchor else '')))

for d in records:
    page=deepcopy(template); page.title.string='SOLAR 8 // '+d['title']+' — Character Bible'
    page.find('meta',attrs={'name':'description'})['content']=d['lead']
    for css in page.select('link[href="assets/maya.css"]'): css.decompose()
    page.head.append(fragment('<link rel="stylesheet" href="assets/dossiers.css"/>'))
    page.body['class']=['character-page','dossier-page']
    assets=[m for m in media if m['archive']==d['archive']]
    hero=next(m for m in assets if m['file']==d['hero'])
    states=[m for m in assets if any(x in m['file'] for x in ['waist-calm','waist-focused','corrupted','liberated','waist-hood'])]
    views=[m for m in assets if m not in states]
    if hero not in views and hero not in states: views.insert(0,hero)
    # Calm portraits remain visible as reference as well as dialogue states.
    if hero not in views and 'waist-calm' in hero['file']: views.append(hero)
    content=f'<section class="hero" id="overview"><div><div class="kicker">CHARACTER BIBLE / {esc(d["short"])}</div><h1>{esc(d["title"])}</h1><p class="lead">{esc(d["lead"])}</p><div class="dossier-status">{esc(d["status"])}</div><p>{esc(d["role"])}</p></div><div class="heroimg canonical-hero"><a href="{hero["original"]}">{img(hero,d["title"],True)}</a></div></section>'
    content+='<section class="section" id="reference-views"><h2>Ракурсы и детали</h2><p>Нажми на изображение, чтобы открыть оригинал целиком.</p>'+gallery(views,d['short'])+'</section>'
    if states: content+='<section class="section" id="states"><h2>Состояния образа</h2>'+gallery(states,d['short'])+'</section>'
    art=read(d['artSource'])
    source=next(a for a in art.select('article') if a.h3 and d['artMatch'].lower() in a.h3.text.lower())
    description=''.join(str(e) for e in source.select('.body > h4,.body > p') if not e.find('a'))
    if d['id']=='emissary':
        description+='<h4>Балахон / версия 2</h4><p>Матовая ткань, объёмный ворот, асимметричный подол и тонкие световые нити в швах. Капюшон показан опущенным и поднятым. Этот костюм относится к аватару, не описывает биологию чужой цивилизации.</p>'
    content+='<section class="section" id="appearance"><h2>Образ и характер</h2><div class="card pad">'+description+'</div><p><a class="source-link" href="'+d['artSource']+'#'+source.h3['id']+'">Исходный арт-бриф ↗</a></p></section>'
    content+='<section class="section" id="story-arc"><h2>Роль в истории</h2><div class="card pad">'+''.join('<div class="story"><strong>'+esc(chapter)+'</strong><span>'+esc(text)+'</span></div>' for chapter,text in d['story'])+'</div></section>'
    content+='<section class="section" id="voice"><h2>Реплики из сценария</h2><p>Существующие английские реплики; новые диалоги здесь не добавлены.</p><div class="grid2">'
    for quote in d['quotes']:
        match=next((v for v in vo if v[0]==d['speaker'] and v[1]==quote),None)
        assert match, (d['id'],quote)
        content+='<article class="card pad"><blockquote>'+esc(quote)+'</blockquote><p><a class="source-link" href="'+match[2]+'">Сцена в сценарии ↗</a></p></article>'
    content+='</div></section><section class="section" id="production-notes"><h2>Материалы для производства</h2>'+''.join('<p>'+esc(n)+'</p>' for n in d['notes'])+'</section>'
    main=page.main; footer=deepcopy(main.select_one('.footer')); main.clear();main.append(fragment(content));main.append(footer)
    footer.select_one('span').string=d['short'].upper()+' / CHARACTER BIBLE'
    nav=page.select_one('.side nav');nav.clear()
    for anchor,title in [('overview',d['short']),('reference-views','Ракурсы и детали'),('states','Состояния образа'),('appearance','Образ и характер'),('story-arc','Роль в истории'),('voice','Реплики'),('production-notes','Материалы для производства')]:
        if page.find(id=anchor):nav.append(fragment(f'<a href="#{anchor}">{esc(title)}</a>'))
    filename='character-'+d['id']+'.html';save(filename,page)
    portrait=home.find(id=d['rosterId']).find_parent('article').select_one('.portrait')
    portrait.clear();portrait['class']=['portrait'];portrait.append(fragment('<a href="'+filename+'">'+img(hero,d['title'])+'</a>'))
    roster=home.find(id=d['rosterId']).find_parent('article')
    if not roster.select_one('a.dossier-link'):roster.select_one('.copy').append(fragment(f'<a class="dossier-link" href="{filename}">Открыть досье ↗</a>'))
    if d['id']=='emissary':roster.select_one('.role').string=d['role']
    search=[e for e in search if not e['url'].startswith(filename+'#')]
    for section in page.select('main > section[id]'):
        heading=section.find(['h1','h2']);search.append(dict(title=heading.get_text(' ',strip=True),page=d['title'],url=filename+'#'+section['id'],text=section.get_text(' ',strip=True)))
    for e in search:
        if e['url']=='index.html#'+d['rosterId']:e['text']=roster.get_text(' ',strip=True)
    if not source.select_one('a[href="'+filename+'"]'):
        source.append(fragment(f'<p><a href="{filename}">Досье и галерея {esc(d["short"])} ↗</a></p>'))
    save(d['artSource'],art)

rook=read('character-rook.html');section=rook.find(id='entry-11').find_parent('section')
for old in section.select('.rook-media-content'):old.decompose()
for old in section.select('.canonbox'):old.decompose()
section['class']=['section','rook-media']
rook_assets=[m for m in media if m['archive']=='solar8-rook-mk2-bible']
rook_assets.sort(key=lambda m:(m['file']!='rook-mk2-hero.png',m['file']))
section.append(fragment('<div class="rook-media-content"><p>Текущий концепт Mk II: две антенны разной длины, две диагональные янтарные полосы на серой сменной панели и маркировка II на верхнем стабилизаторе. Сохраняются круглый cyan-сенсор, четыре стабилизатора и узнаваемый силуэт Mk I.</p>'+gallery(rook_assets,'ROOK Mk II')+'<p>Основной hero-концепт задаёт конструкцию. Перед 3D-производством крепления и панели нужно согласовать между ракурсами. Восстановление из backup возвращает личность и знакомые функции, но не последние дни памяти и не воспоминание о жертве.</p></div>'))
if not rook.select_one('link[href="assets/dossiers.css"]'):rook.head.append(fragment('<link rel="stylesheet" href="assets/dossiers.css"/>'))
save('character-rook.html',rook)
for e in search:
    if e['url']=='character-rook.html#entry-11':e['text']=section.get_text(' ',strip=True)
save('index.html',home)
search_path.write_text(json.dumps(search,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Built six dossiers, updated roster portraits and ROOK Mk II gallery.')
