"""Publish the game soundtrack, preserving supplied audio bytes."""
from pathlib import Path
from html import escape as esc
import json
from bs4 import BeautifulSoup as Soup

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assets/music.json').read_text(encoding='utf8'))
page=Soup((ROOT/'resource-status.html').read_text(encoding='utf8'),'html.parser')
page.title.string='SOLAR 8 // Soundtrack'
for tag in page.select('script[src*="resource-status.js"],link[href*="resource-status.css"]'):tag.decompose()
page.head.append(Soup('<link rel="stylesheet" href="assets/music.css"/><script src="assets/music.js" defer></script>','html.parser'))
page.main.clear()
intro='<section id="overview"><div class="kicker">SOLAR 8 / SOUNDTRACK</div><h1>Музыка игры</h1><p>Шесть треков из текущей рабочей версии игры. Полные оригиналы и короткие игровые петли.</p><p>При запуске нового трека предыдущий останавливается.</p></section>'
cards=[]
for i,t in enumerate(data['tracks'],1):
    for key in ['original','loop']:assert (ROOT/t[key]).is_file(),t[key]
    body=f'<article class="card pad music-track" id="{t["id"]}"><div class="kicker">{i:02d} / SOUNDTRACK</div><h2>{esc(t["title"])}</h2><p>{esc(t["use"]["ru"])}</p>'
    for key,label,download in [('original','Полный оригинал','Скачать оригинал'),('loop','Игровая петля','Скачать петлю')]:
        seconds=f' · {t["loop_seconds"] // 60}:{t["loop_seconds"] % 60:02d}' if key=='loop' else ''
        body+=f'<div class="music-version"><h3><span>{label}</span>{seconds}</h3><audio controls preload="none" aria-label="{label}: {esc(t["title"])}"><source src="{t[key]}" type="audio/mpeg"/></audio><a href="{t[key]}" download>{download}</a></div>'
    cards.append(body+'</article>')
page.main.append(Soup(intro+'<section class="music-grid" aria-label="Саундтрек">'+''.join(cards)+'</section><section class="music-notes"><p>Треки предоставлены автором проекта. Названия отображены по именам файлов; назначение сверено с музыкальным контроллером игры 12.10.2026.</p><p>Игровые версии сокращены и зациклены для мобильной сборки. Полные оригиналы сохранены без изменений.</p></section>','html.parser'))
nav=page.select_one('.side nav');nav.clear()
nav.append(Soup('<a href="#overview">Саундтрек</a>'+''.join(f'<a href="#{t["id"]}">{esc(t["title"])}</a>' for t in data['tracks']),'html.parser'))
(ROOT/'music.html').write_text(str(page),encoding='utf8')
search=ROOT/'assets/search-index.json'
entries=[e for e in json.loads(search.read_text(encoding='utf8')) if not e['url'].startswith('music.html')]
for t in data['tracks']:entries.append(dict(title=t['title'],page='Soundtrack',url='music.html#'+t['id'],text=t['use']['ru'],text_en=t['use']['en']))
search.write_text(json.dumps(entries,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print('Music: six tracks, full originals and gameplay loops.')
