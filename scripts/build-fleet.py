"""Build the static fleet catalogue and chapter previews from assets/fleet.json.

Run with Python + BeautifulSoup 4. No browser-side data fetch is required.
"""
from pathlib import Path
from copy import deepcopy
from html import escape as esc
from urllib.parse import urlsplit
import json
from bs4 import BeautifulSoup as Soup

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'assets/fleet.json').read_text(encoding='utf-8'))
ships = data['ships']
active = [s for s in ships if not s['archived']]
archive = [s for s in ships if s['archived']]
roles = {'player': 'Корабль игрока', 'scout': 'Разведка', 'striker': 'Атака',
         'guard': 'Защита', 'support': 'Ремонт и поддержка', 'boss': 'Босс'}
assert len({s['id'] for s in ships}) == len(ships), 'Duplicate ship IDs'
for s in ships:
    assert (ROOT / urlsplit(s['image']).path).is_file(), s['image']

def parse(html):
    return Soup(html, 'html.parser')

def image(s, extra=''):
    return (f'<img src="{esc(s["image"])}" alt="{esc(s["name"])}" '
            f'width="{s["width"]}" height="{s["height"]}" loading="lazy" decoding="async" {extra}/>')

def card(s):
    feature = s['kind'] in ['boss', 'player'] and not s['archived']
    classes = 'fleet-card' + (' fleet-feature' if feature else '')
    label = 'Архивный концепт' if s['archived'] else roles[s['kind']]
    if s['name'] == 'Venus Guard':
        label = 'Защита и помехи'
    if s['mission']:
        label += ' · Миссия ' + s['mission']
    if s['phase']:
        label += ' · ' + s['phase']
    code = f'<small class="fleet-code">Техническое обозначение: {esc(s["technicalCode"])}</small>' if s['technicalCode'] else ''
    return f'''<article class="{classes}" id="ship-{s['id']}">
<a class="fleet-art" href="{esc(s['image'])}" aria-label="Увеличить: {esc(s['name'])}">{image(s)}<span class="fleet-zoom" aria-hidden="true">↗</span></a>
<div class="fleet-copy"><div class="kicker">{esc(label)}</div><h3>{esc(s['name'])}</h3>
<p>{esc(s['description'])}</p>{code}<div class="fleet-actions"><a href="{esc(s['image'])}" download="{Path(urlsplit(s['image']).path).name}">Скачать PNG ↓</a></div></div></article>'''

home = Soup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
legacy = {old: 'fleet.html#ship-' + s['id'] for s in ships for old in s['legacyIds']}
legacy.update({'ships-earth': 'fleet.html#earth', 'ships-mars': 'fleet.html#mars',
               'ship-concept-archive': 'fleet.html#archive', 'ship-naming': 'fleet.html#fleet-rules'})
old_section = home.find(id='ships')
teaser = f'''<section id="ships" class="fleet-teaser"><div class="head"><div class="n">12</div><div><h2 id="entry-93">Флот</h2><p>{len(active)} кораблей и аппаратов · {len(data['planets'])} планеты · отдельный каталог</p></div></div><p>Разведчики, ударные корабли, защитники и боссы — по планетам и ролям.</p><a class="btn primary" href="fleet.html">Открыть Флот <span aria-hidden="true">↗</span></a><div class="fleet-teaser-links">'''
teaser += ''.join(f'<a href="fleet.html#{p["id"]}">{p["name"]} →</a>' for p in data['planets'])
teaser += '</div>' + ''.join(f'<span hidden id="{old}" data-fleet-target="{url}"></span>' for old, url in legacy.items()) + '</section>'
old_section.replace_with(parse(teaser))

# Chapter previews are small links, not story cards: the scenario builder ignores them.
for block in home.select('[data-fleet-preview]'):
    block.decompose()
# The original Mercury SVG strip is replaced by the shared current-asset preview.
for block in home.select('#mercury > .gallery'):
    if block.select_one('img[src="assets/player_ship.svg"]'):
        block.decompose()
for p in data['planets']:
    group = [s for s in active if s['planet'] == p['name']]
    preview = f'<div class="fleet-preview" data-fleet-preview="{p["id"]}"><div class="fleet-preview-head"><span class="kicker">ФЛОТ / {p["name"].upper()}</span><a href="fleet.html#{p["id"]}">Флот {p["name"]} →</a></div><div class="fleet-thumbs">'
    preview += ''.join(f'<a class="fleet-thumb" href="fleet.html#ship-{s["id"]}">{image(s)}<span>{esc(s["name"])}</span></a>' for s in group)
    preview += '</div></div>'
    chapter = home.find(id=p['id'])
    (chapter.select_one('.chapter-art') or chapter.select_one('.head')).insert_after(parse(preview))
(ROOT / 'index.html').write_text(str(home), encoding='utf-8')

# Update shared navigation and links before copying the common shell.
for path in ROOT.glob('*.html'):
    if path.name == 'fleet.html':
        continue
    page = Soup(path.read_text(encoding='utf-8'), 'html.parser')
    top = page.select_one('.topnav')
    if top and not top.select_one('a[href="fleet.html"]'):
        top.insert(2, parse('<a href="fleet.html">Флот</a>'))
    side = page.select_one('.side')
    if side:
        old_link = side.select_one('a[href="#ships"],a[href="index.html#ships"]')
        if old_link:
            old_link['href'] = 'fleet.html'
            old_link.string = 'Флот'
        elif not side.select_one('a[href="fleet.html"]'):
            side.insert(1, parse('<a class="fleet-entry" href="fleet.html">Флот →</a>'))
    for a in page.select('a[href]'):
        u = urlsplit(a['href'])
        if u.path == 'index.html' or (not u.path and path.name == 'index.html'):
            if u.fragment in legacy:
                a['href'] = legacy[u.fragment]
    if path.name == 'index.html' and not page.select_one('link[href="assets/fleet.css"]'):
        page.head.append(parse('<link rel="stylesheet" href="assets/fleet.css"/>'))
    path.write_text(str(page), encoding='utf-8')

home = Soup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
header = deepcopy(home.select_one('header.top'))
for a in header.select('.topnav a'):
    a.attrs.pop('aria-current', None)
    if a['href'] == 'fleet.html':
        a['aria-current'] = 'page'
nav = '<a href="#overview">Обзор флота</a><a href="#player">Корабль Andygen</a><div class="nav-group">ПО ПЛАНЕТАМ</div>'
nav += ''.join(f'<a href="#{p["id"]}">{p["name"]} <span>{p["ru"]}</span></a>' for p in data['planets'])
nav += '<div class="nav-group">МАТЕРИАЛЫ</div><a href="#fleet-rules">Названия и способности</a><a href="#archive">Архив концептов</a>'
content = f'''<section class="fleet-intro" id="overview"><div class="kicker">SOLAR 8 / КАТАЛОГ КОРАБЛЕЙ</div><h1>Флот</h1><p>От солнечной обороны Mercury до промышленных машин Mars. Корабли, их роли и оригинальные изображения.</p><div class="fleet-stats"><span><b>{len(active):02d}</b> кораблей и аппаратов</span><span><b>{len(data['planets']):02d}</b> планеты</span></div><nav class="fleet-world-links" aria-label="Выбор планеты">'''
content += ''.join(f'<a href="#{p["id"]}">{p["name"]} <span>↘</span></a>' for p in data['planets']) + '</nav></section>'
player = next(s for s in active if s['kind'] == 'player')
content += '<section class="fleet-world" id="player"><div class="fleet-heading"><div><div class="kicker">ANDYGEN</div><h2>Корабль игрока</h2></div></div>' + card(player) + '</section>'
for n, p in enumerate(data['planets'], 1):
    group = [s for s in active if s['planet'] == p['name']]
    content += f'''<section class="fleet-world" id="{p['id']}"><div class="fleet-heading"><div><div class="kicker">{n:02d} / {p['ru']} · Аппаратов: {len(group)}</div><h2>{p['name']}</h2><p>{p['tagline']}</p></div><a href="index.html#{p['id']}">К главе →</a></div><div class="fleet-grid">'''
    content += ''.join(card(s) for s in group) + '</div></section>'
content += '<section class="fleet-rules" id="fleet-rules"><h2>Названия и способности</h2>' + ''.join(f'<p>{esc(p)}</p>' for p in data['notes']) + '</section>'
content += '<section class="fleet-archive" id="archive"><details><summary>Архив концептов <span>Вне действующего состава</span></summary><p>Ранние варианты сохранены для истории разработки.</p><div class="fleet-grid">' + ''.join(card(s) for s in archive) + '</div>' + ''.join(f'<p>{esc(p)}</p>' for p in data['archiveNotes']) + '</details></section>'
dialogs = ''.join(str(home.find(id=id)) for id in ['search-dialog', 'image-dialog'])
html = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="theme-color" content="#090b0e"/><title>SOLAR 8 // Флот</title><meta name="description" content="Флот SOLAR 8: корабли Mercury, Venus, Earth и Mars, боссы, роли и оригинальные PNG."/><link rel="icon" type="image/svg+xml" href="assets/solar-mark.svg"/><link rel="stylesheet" href="assets/solar.css"/><link rel="stylesheet" href="assets/fleet.css"/><script defer src="assets/solar.js"></script></head><body class="fleet-page"><a class="skip-link" href="#main-content">Перейти к содержанию</a>{header}<aside class="side document-side" id="side" aria-label="Оглавление флота"><a class="back-link" href="index.html">← К проекту</a><div class="eyebrow">КАТАЛОГ / SOLAR 8</div><nav>{nav}</nav></aside><main class="wrap" id="main-content">{content}<footer class="footer"><a href="index.html"><img src="assets/solar-logo.svg" width="130" height="24" alt="SOLAR 8"/></a><span>ФЛОТ / PROJECT BIBLE</span><a href="#overview">К началу ↑</a></footer></main>{dialogs}<div class="nav-backdrop" aria-hidden="true"></div><div class="reading-progress" aria-hidden="true"></div></body></html>'''
fleet = Soup(html, 'html.parser')
(ROOT / 'fleet.html').write_text(str(fleet), encoding='utf-8')

index_path = ROOT / 'assets/search-index.json'
index = json.loads(index_path.read_text(encoding='utf-8'))
old_urls = {'index.html#' + id for id in legacy} | {'index.html#entry-93'}
index = [e for e in index if e['url'] not in old_urls and not e['url'].startswith('fleet.html')]
for s in ships:
    block = fleet.find(id='ship-' + s['id'])
    index.append({'title': s['name'], 'page': 'Флот / ' + ('Архив концептов' if s['archived'] else s['planet']), 'url': 'fleet.html#ship-' + s['id'], 'text': block.get_text(' ', strip=True)})
for id in ['overview', 'fleet-rules', 'archive'] + [p['id'] for p in data['planets']]:
    block = fleet.find(id=id)
    index.append({'title': 'Флот' if id == 'overview' else 'Архив концептов' if id == 'archive' else block.find(['h1', 'h2']).get_text(), 'page': 'Флот SOLAR 8', 'url': 'fleet.html#' + id, 'text': block.get_text(' ', strip=True)})
index_path.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f'Built fleet: {len(active)} active ships, {len(archive)} archived concepts, {len(data["planets"])} chapter previews.')
