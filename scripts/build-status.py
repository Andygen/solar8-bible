"""Publish a conservative, searchable readiness register and sync checked facts."""
from pathlib import Path
from html import escape as esc
import json
from urllib.parse import urlsplit
from PIL import Image
from bs4 import BeautifulSoup as Soup

ROOT=Path(__file__).resolve().parents[1]
status=json.loads((ROOT/'assets/production-status.json').read_text(encoding='utf8'))
checks={e['id']:e for e in status['checks']}
fleet=json.loads((ROOT/'assets/fleet.json').read_text(encoding='utf8'))
for ship in fleet['ships']:
    key={'venus-striker':'venus-striker-acid','venus-guard':'venus-guard-jamming'}.get(ship['id'])
    if key:ship['description']=checks[key]['description']+' Сверка рабочей игры: '+checks[key]['checked_at']+'.'
for i,note in enumerate(fleet['notes']):
    if note.startswith('Сверка рабочей версии игры'):
        fleet['notes'][i]='Сверка рабочей версии игры: '+checks['venus-striker-acid']['description']+' '+checks['venus-guard-jamming']['description']+' Дата: '+checks['venus-guard-jamming']['checked_at']+'. Это статус локальной рабочей версии, а не опубликованного билда.'
(ROOT/'assets/fleet.json').write_text(json.dumps(fleet,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
manifest=json.loads((ROOT/'docs/asset-handoff-2026-09-26.json').read_text(encoding='utf8'))
pack={e['file']:e for e in manifest['assets']}
rows=[]
for ship in fleet['ships']:
    if ship['archived']:continue
    groups=[(ship, 'Основной PNG')]+[(v,'Цельная фаза / вариант') for v in ship.get('variants',[])]
    for group in ship.get('resourceGroups',[]):groups += [(v,group['title']) for v in group['items']]
    for item,kind in groups:
        source=pack.get(item['image'],{})
        if '/concepts/' in item['image']: readiness='Концепт; не анимационный слой'
        elif '/rig/' in item['image']:readiness='Прототип движения; не установлен на босса'
        elif '/parts/' in item['image']:readiness='Отдельная деталь; требуется совмещение'
        else:readiness='Изображение опубликовано; анимация отдельно'
        rows.append(dict(id=ship['id']+'--'+Path(item['image']).stem,entity=ship['name'],name=item['name'],planet=ship['planet'],kind=kind,file=item['image'],width=item['width'],height=item['height'],readiness=readiness,visual='Текущий опубликованный набор; отдельная приёмка не зафиксирована',game='Наличие PNG не подтверждает интеграцию в игру',checked_at=status['revision'],url='fleet.html#ship-'+ship['id']))
unique={row['file']:row for row in rows}
# Include published character references, player upgrades and world references,
# without treating a rendered view as a validated animation/model or game asset.
for page_path in sorted(ROOT.glob('character-*.html'))+[ROOT/'player-upgrades.html',ROOT/'index.html']:
    page=Soup(page_path.read_text(encoding='utf8'),'html.parser')
    images=page.select('main img') if page_path.name!='index.html' else page.select('.world-card img,.chapter-art img')
    for img in images:
        if img.find_parent('footer'):continue
        source=img.get('data-full-src',img.get('src',''))
        parent=img.find_parent('a')
        if parent and urlsplit(parent.get('href','')).path.lower().endswith(('.png','.webp','.jpg')):source=parent['href']
        parsed=urlsplit(source);file=parsed.path
        if parsed.scheme or not file or file in unique or not (ROOT/file).is_file():continue
        with Image.open(ROOT/file) as im:width,height=im.size
        section=img.find_parent('section',id=True)
        anchor='#'+section['id'] if section else ''
        name=img.get('alt') or Path(file).stem
        category='Персонажи' if page_path.name.startswith('character-') else 'Развитие игрока' if page_path.name=='player-upgrades.html' else 'Миры'
        unique[file]=dict(id=page_path.stem+'--'+Path(file).stem,entity=page.h1.get_text(' ',strip=True) if page.h1 else category,name=name,planet=category,kind='Визуальный референс',file=file,width=width,height=height,readiness='Статический референс опубликован',visual='Текущий опубликованный набор; отдельная приёмка не зафиксирована',game='Изображение не подтверждает готовую анимацию, техлист или игровую интеграцию',checked_at=status['revision'],url=page_path.name+anchor)
rows=list(unique.values())
(ROOT/'assets/resource-status.json').write_text(json.dumps({'revision':status['revision'],'resources':rows,'game_checks':status['checks']},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
doc=ROOT/'docs/story-rules.md';text=doc.read_text(encoding='utf8')
lines=text.splitlines()
for i,line in enumerate(lines):
    for key,label in [('venus-striker-acid','Venus Striker'),('venus-guard-jamming','Venus Guard')]:
        if line.startswith('| '+label+' |'):
            pieces=line.split('|');pieces[3]=' '+checks[key]['description']+' Сверка '+checks[key]['checked_at']+'. ';lines[i]='|'.join(pieces)
doc.write_text('\n'.join(lines)+'\n',encoding='utf8')
home=Soup((ROOT/'index.html').read_text(encoding='utf8'),'html.parser')
for li in home.select('#rook-gameplay li'):
    if li.get_text().startswith('ретранслятор 1-1:'):li.string='ретранслятор 1-1: '+checks['rook-relay']['description']
(ROOT/'index.html').write_text(str(home),encoding='utf8')
shell=Soup((ROOT/'story-rules.html').read_text(encoding='utf8'),'html.parser')
shell.title.string='SOLAR 8 // Готовность материалов';shell.body['class']=['document-page','resource-page']
shell.main.clear();shell.main.append(Soup('<section id="overview"><div class="kicker">ПРОИЗВОДСТВО</div><h1>Готовность материалов</h1><p>Отдельно учитываем изображение, визуальную приёмку, подготовку к анимации и механику игры. Опубликованный PNG не означает готовую игровую сущность.</p><p><a href="assets/resource-status.json" download>Скачать реестр JSON</a> · <a href="story-rules.html#assets">Что ещё подготовить →</a></p></section><section id="game-checks"><h2>Проверенные игровые функции</h2><p>'+esc(status['scope'])+'</p>'+''.join('<article class="card pad"><h3>'+esc(e['entity'])+'</h3><p>'+esc(e['status'])+' · '+esc(e['checked_at'])+'</p><p>'+esc(e['description'])+'</p><small>'+esc(e['source'])+'</small></article>' for e in status['checks'])+'</section><section id="resources"><h2>Изображения и детали</h2><label>Найти материал <input type="search" id="resource-query" placeholder="Планета, корабль, файл, статус"/></label><p id="resource-count" role="status"></p><div class="resource-grid">'+''.join(f'<article class="card pad resource-row" id="resource-{r["id"]}"><h3>{esc(r["name"])}</h3><p>{esc(r["entity"])} · {esc(r["planet"])}</p><p><b>{esc(r["readiness"])}</b></p><p>{esc(r["visual"])}</p><p>{esc(r["game"])}</p><small>{r["width"]} × {r["height"]} · учёт {r["checked_at"]}</small><p><a href="{r["url"]}">Карточка →</a> · <a href="{r["file"]}" download>PNG ↓</a></p></article>' for r in rows)+'</div></section>','html.parser'))
nav=shell.select_one('.side nav');nav.clear();nav.append(Soup('<a href="#overview">О реестре</a><a href="#game-checks">Игровые функции</a><a href="#resources">Ресурсы</a>','html.parser'))
for s in shell.select('script[src]'):
    if s['src']!='assets/solar.js':s.decompose()
shell.head.append(shell.new_tag('script',src='assets/resource-status.js',defer=True))
shell.head.append(shell.new_tag('link',rel='stylesheet',href='assets/resource-status.css'))
(ROOT/'resource-status.html').write_text(str(shell),encoding='utf8')
path=ROOT/'assets/search-index.json';index=json.loads(path.read_text(encoding='utf8'));index=[e for e in index if not e['url'].startswith('resource-status.html')]
index.append(dict(title='Готовность материалов',page='Производство',url='resource-status.html#overview',text='PNG, анимация, совмещение слоёв, игровые проверки, статусы готовности'))
path.write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print(f'Readiness register: {len(rows)} unique resources, {len(checks)} dated game checks.')
