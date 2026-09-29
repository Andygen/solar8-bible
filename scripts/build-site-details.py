"""Shared branding and the pilot's ship; generated from the fleet master."""
from pathlib import Path
from html import escape as esc
import json
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[1]
fleet=json.loads((ROOT/'assets/fleet.json').read_text(encoding='utf8'))
ship=next(s for s in fleet['ships'] if s['id']=='player-interceptor')
for path in ROOT.glob('*.html'):
    page=Soup(path.read_text(encoding='utf8'),'html.parser')
    for icon in page.select('link[rel="icon"]'):icon.decompose()
    page.head.append(page.new_tag('link',rel='icon',href='assets/solar-mark.svg',type='image/svg+xml'))
    if path.name=='character-andygen.html':
        old=page.find(id='pilot-ship')
        if old:old.decompose()
        section=Soup(f'''<section class="section" id="pilot-ship"><h2>Корабль Andygen</h2><h3>{esc(ship['name'])}</h3><a href="{ship['image']}" aria-label="Увеличить Player Interceptor"><img src="{ship['image']}" width="{ship['width']}" height="{ship['height']}" alt="Player Interceptor — корабль Andygen" loading="lazy" decoding="async" style="display:block;width:100%;max-width:600px;height:auto;object-fit:contain"/></a><p>{esc(ship['description'])}</p><p><a href="fleet.html#ship-player-interceptor">Карточка во Флоте →</a> · <a href="player-upgrades.html">Девять стадий развития →</a> · <a href="{ship['image']}" download>Оригинальный PNG ↓</a></p></section>''','html.parser')
        footer=page.main.find('footer')
        if footer:footer.insert_before(section)
        else:page.main.append(section)
    path.write_text(str(page),encoding='utf8')
