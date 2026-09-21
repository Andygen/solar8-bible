"""Build the v9 Player Interceptor proposal page from the supplied Markdown.
Requires BeautifulSoup 4 and Python-Markdown. Does not modify campaign VO.
"""
from pathlib import Path
from html import escape as esc
import json,re
import markdown
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[1]
source='docs/art-imports/solar8-player-upgrades-v9/UPGRADES-RU.md'
text=(ROOT/source).read_text(encoding='utf-8')
media=json.loads((ROOT/'assets/media-imports.json').read_text(encoding='utf-8'))
assets=[m for m in media if m['archive']=='solar8-player-upgrades-v9']
stages=[('mercury','Mercury','base'),('venus','Venus','venus-upgrade-concept'),('earth','Earth','earth-upgrade-concept'),('mars','Mars','mars-upgrade-concept'),('jupiter','Jupiter','jupiter-upgrade-concept'),('saturn','Saturn','saturn-upgrade-concept'),('uranus','Uranus','uranus-upgrade-concept'),('neptune','Neptune','neptune-upgrade-concept'),('solar-crown','Solar Crown','solar-crown-upgrade-concept')]
table=re.search(r'## Этапы\n(.*?)(?=\n## )',text,re.S)[1]
rows=[[cell.strip() for cell in line.strip().strip('|').split('|')] for line in table.splitlines() if line.startswith('|')][2:]
assert len(rows)==len(stages)==9
page=Soup((ROOT/'fleet.html').read_text(encoding='utf-8'),'html.parser')
page.title.string='SOLAR 8 // Развитие Player Interceptor — концепт v9'
page.find('meta',attrs={'name':'description'})['content']='Девять концептов развития корабля Andygen: модули, износ и предлагаемые сцены Max. Проект механик и реплик, не готовая реализация.'
page.body['class']=['fleet-page','upgrades-page']
page.head.append(Soup('<link rel="stylesheet" href="assets/upgrades.css"/>','html.parser'))
for a in page.select('.topnav a'):a.attrs.pop('aria-current',None)
side=page.select_one('.side');side.select_one('.back-link')['href']='fleet.html#player';side.select_one('.back-link').string='← К флоту'
side.select_one('.eyebrow').string='PLAYER INTERCEPTOR / V9'
nav=side.nav;nav.clear();nav.append(Soup('<a href="#overview">Развитие корабля</a>','html.parser'))
content='<section class="fleet-intro" id="overview"><div class="kicker">PLAYER INTERCEPTOR / VERSION 9</div><h1>Один корабль.<br/>Вся кампания.</h1><p>Девять последовательных концептов: новые модули, ремонт и накопленный износ от Mercury до Solar Crown.</p><div class="upgrade-status"><strong>Предложение к сценарию и реализации</strong><p>Механики, численные бонусы и новые реплики ниже — проект. Изображения не означают, что эти возможности уже работают в игре. Текущая карточка Player Interceptor сохранена отдельно.</p></div><p><a href="fleet.html#ship-player-interceptor">Корабль в действующем каталоге ↗</a> · <a href="'+source+'" download>Скачать исходный план v9 ↓</a></p><nav class="fleet-world-links" aria-label="Этапы развития">'+''.join(f'<a href="#stage-{id}">{name} ↘</a>' for id,name,_ in stages)+'</nav></section>'
for number,((id,name,suffix),row) in enumerate(zip(stages,rows),1):
    when,chapter,change,benefit,light=row
    m=next(m for m in assets if m['file']=='player-interceptor-'+suffix+'.png')
    content+=f'''<section class="upgrade-stage" id="stage-{id}"><div class="fleet-heading"><div><div class="kicker">{number:02d} / КОНЦЕПТ ЭТАПА</div><h2>{name}</h2><p>{esc(when)}</p></div></div><article class="fleet-card fleet-feature"><a class="fleet-art" href="{m['original']}" aria-label="Увеличить: Player Interceptor / {name}"><img src="{m['preview']}" data-full-src="{m['original']}" width="{m['width']}" height="{m['height']}" alt="Player Interceptor — концепт {name}, версия 9" loading="lazy" decoding="async"/><span class="fleet-zoom" aria-hidden="true">↗</span></a><div class="fleet-copy"><h3>{esc(change)}</h3><p><b>Предлагаемая польза:</b> {esc(benefit)}</p><p><b>Освещение:</b> {esc(light)}</p><div class="fleet-actions"><a href="{m['original']}" download>Скачать оригинальный PNG ↓</a></div></div></article></section>'''
    nav.append(Soup(f'<a href="#stage-{id}">{number:02d} / {name}</a>','html.parser'))

titles={'Основной принцип':'principle','Как Max представляет обновление':'hangar-scenes','Цвет и читаемость':'readability','Презентация Neptune — после 7-5, перед 8-1':'neptune-presentation','Презентация Solar Crown — после титров, при открытии эпилога':'crown-presentation','Ревизия 9 — выхлоп и накопленный износ':'revision-nine'}
for section in re.split(r'(?=^## )',text,flags=re.M):
    lines=section.splitlines();title=lines[0].removeprefix('## ') if lines else ''
    if title not in titles:continue
    body='\n'.join(lines[1:]).strip()
    body=body.replace('Код игры и сайт не менялись.','').replace('Старые архивы и исходные изображения не перезаписаны. Для передачи использовать 9 PNG из этого архива.','')
    rendered=Soup(markdown.markdown(body,extensions=['tables','sane_lists','nl2br']),'html.parser')
    for table_node in rendered.select('table'):
        wrapper=rendered.new_tag('div',attrs={'class':'table-scroll','role':'region','aria-label':'Таблица износа корабля','tabindex':'0'});table_node.wrap(wrapper)
    id=titles[title]
    content+=f'<section class="upgrade-notes" id="{id}"><h2>{esc(title)}</h2>'
    if id in ['hangar-scenes','neptune-presentation','crown-presentation']:content+='<p class="upgrade-label">Предлагаемые сцены и VO-черновик. В основной сценарий не включены.</p>'
    content+=str(rendered)+'</section>'
    nav.append(Soup(f'<a href="#{id}">{esc(title)}</a>','html.parser'))
footer=page.select_one('main .footer').extract();page.main.clear();page.main.append(Soup(content,'html.parser'));page.main.append(footer)
footer.select_one('span').string='PLAYER INTERCEPTOR / CONCEPT V9'
(ROOT/'player-upgrades.html').write_text(str(page),encoding='utf-8')
idx_path=ROOT/'assets/search-index.json';idx=json.loads(idx_path.read_text(encoding='utf-8'));idx=[e for e in idx if not e['url'].startswith('player-upgrades.html')]
for section in page.select('main > section[id]'):
    h=section.find(['h1','h2']);idx.append(dict(title=h.get_text(' ',strip=True),page='Player Interceptor / развитие v9 · предложение',url='player-upgrades.html#'+section['id'],text=section.get_text(' ',strip=True)))
idx_path.write_text(json.dumps(idx,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Built nine upgrade concepts and proposed hangar scenes; campaign VO unchanged.')
