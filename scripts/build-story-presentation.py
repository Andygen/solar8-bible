"""Publish one story reader; retain old URLs as anchor-aware transition pages."""
from pathlib import Path
from urllib.parse import urlsplit
from html import escape as esc
import json,sys
from bs4 import BeautifulSoup as Soup
sys.path.insert(0,str(Path(__file__).resolve().parent))
from story_data import ROOT,STORY,GAME

path=ROOT/'scenario.html';page=Soup(path.read_text(encoding='utf8'),'html.parser')
for node in page.select('#dialogue-language, #story-language, script[src="assets/dialogue-bindings.js"]'):node.decompose()
for node in page.select('[data-dialogue-id]'):
    e=GAME[node['data-dialogue-id']];node['data-en']=e['en'];node['data-ru']=e['ru']
labels=json.loads((ROOT/'assets/story-labels.json').read_text(encoding='utf8'))
for node in page.select('.scene-title'):
    en=node.get_text(' ',strip=True)
    if en in labels:node['data-en']=en;node['data-ru']=labels[en]
for scene in page.select('.scene,.upgrade-interlude'):
    for old in scene.select(':scope > .translation-state'):old.decompose()
    lines=scene.select('.text[data-en]')
    if not lines:continue
    bound=sum(bool(n.get('data-dialogue-id')) for n in lines)
    label='Перевод из игрового каталога' if bound==len(lines) else 'Игровой перевод + редакционный черновик RU' if bound else 'Редакционный черновик RU · литературная сцена'
    scene.insert(0,Soup('<p class="translation-state">'+label+'</p>','html.parser'))
for node in page.select('.upgrade-translation'):node.decompose()
page.main.insert(0,Soup('''<aside id="story-language" class="dialogue-language"><label>Язык реплик <select id="story-language-select"><option value="ru">Русский</option><option value="en">English</option></select></label><p>Игровые переводы сохранены. Остальные переводы — редакционный черновик; это не отметка готовности сцены в игре. Описания событий и режиссёрские заметки — на русском.</p><a href="dialogues.html">Каталог игровых реплик: ID, варианты и переводы →</a><span id="story-language-status" role="status"></span><noscript>Без JavaScript показан английский оригинал реплик.</noscript></aside>''','html.parser'))
if not page.select_one('script[src="assets/story-language.js"]'):page.head.append(page.new_tag('script',src='assets/story-language.js',defer=True))
path.write_text(str(page),encoding='utf8')

for name,route in STORY['legacy_routes'].items():
    mapping=route['anchors'];default=route['default']
    items=''.join(f'<li id="{esc(old)}"><a href="scenario.html#{esc(new)}">{esc(old)} → {esc(new)}</a></li>' for old,new in mapping.items())
    html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SOLAR 8 — сценарий переехал</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="https://andygen.github.io/solar8-bible/scenario.html#{default}"><link rel="stylesheet" href="assets/solar.css"></head><body><main class="wrap"><h1>Сцены перенесены в общий сценарий</h1><p>Все главы, реплики RU / EN и режиссёрские заметки теперь собраны вместе.</p><p><a href="scenario.html#{default}">Открыть сценарий →</a></p><details><summary>Переходы по прежним ссылкам</summary><ul>{items}</ul></details></main><script type="application/json" id="legacy-route">{json.dumps(route,ensure_ascii=False)}</script><script src="assets/story-redirect.js" defer></script></body></html>'''
    (ROOT/name).write_text(html,encoding='utf8')

# Existing links keep their exact mission destination; the old addresses remain
# available to external bookmarks and immutable links inside the game catalog.
for path in ROOT.glob('*.html'):
    if path.name in STORY['legacy_routes']:continue
    page=Soup(path.read_text(encoding='utf8'),'html.parser')
    if path.name=='index.html':
        import re
        speakers={e['speaker'] for e in GAME.values()}|{'SYSTEM','SHIP AI','EMISSARY','NAVARRO','YARA','NOVA','VALE'}
        destinations={}
        for mission in STORY['missions']:
            for scene in mission['scenes']:
                for block in scene['blocks']:
                    if block['type']!='line':continue
                    e=block['line'];text=GAME.get(e.get('dialogue_id')) or e
                    destinations.setdefault(' '.join(text['en'].split()),mission['id'])
        parents=set()
        for row in list(page.select('.dialogue')):
            speaker=row.select_one('.speaker');line=row.select_one('.line')
            if not speaker or not line or speaker.get_text(strip=True).upper() not in speakers:continue
            article=row.find_parent('article') or row.parent
            mission=destinations.get(' '.join(line.get_text(' ',strip=True).split()))
            kicker=article.select_one('.kicker');number=re.search(r'\b([1-8]-[1-5])\b',kicker.get_text() if kicker else '')
            if number:mission=number[1]
            if not mission:
                text=line.get_text()
                mission='1-2' if 'Structural failure' in text else '2-5' if 'Core overload' in text or 'Earth Orbital' in text else '5-1' if 'wind' in text else 'overview'
            target='mission-'+mission if re.fullmatch(r'[1-8]-[1-5]',mission) else mission
            key=id(article)
            if key not in parents:
                row.insert_before(Soup(f'<p class="scene-reference"><a href="scenario.html#{target}">Читать сцену RU / EN →</a></p>','html.parser'));parents.add(key)
            row.decompose()
        if not page.select('[data-dialogue-id]'):
            for node in page.select('#dialogue-language,script[src="assets/dialogue-bindings.js"]'):node.decompose()
        for card in page.select('a.card[href^="scenario.html"]'):
            if card.h3:
                card.h3.string=card.h3.get_text().replace(' — full VO pass',' — сцены RU / EN')
                kicker=card.select_one('.kicker')
                if kicker:kicker.string='СЦЕНАРИЙ / ГЛАВЫ'
    for a in page.select('a[href]'):
        u=urlsplit(a['href']);route=STORY['legacy_routes'].get(u.path)
        if route and not u.scheme:
            a['href']='scenario.html#'+route['anchors'].get(u.fragment,route['default'])
            if not a.select('[id]'):a.string='Сцены в общем сценарии →'
    path.write_text(str(page),encoding='utf8')
index=ROOT/'assets/search-index.json';entries=json.loads(index.read_text(encoding='utf8'))
entries=[e for e in entries if not urlsplit(e['url']).path.startswith('scripts-')]
index.write_text(json.dumps(entries,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print('Published one story reader and four legacy transition pages.')
