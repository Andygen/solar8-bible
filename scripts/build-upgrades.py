"""Build progression and draft transitions. Run before build-scenario.py and build-fleet.py."""
from bs4 import BeautifulSoup as Soup
from html import escape as esc
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from progression import ROOT, DATA, STAGES, paragraphs, scene

def parse(text): return Soup(text, 'html.parser')
def save(path, page): (ROOT/path).write_text(str(page), encoding='utf-8')

page = parse((ROOT/'fleet.html').read_text(encoding='utf-8'))
page.title.string = 'SOLAR 8 // Player Interceptor — развитие корабля'
page.select_one('meta[name="description"]')['content'] = 'Один корабль на всю кампанию: девять ангарных стадий, накопленный износ, отражения окружения и предлагаемые сцены Max.'
page.body['class'] = ['fleet-page','upgrades-page']
page.head.append(parse('<link rel="stylesheet" href="assets/upgrades.css"/>'))
for a in page.select('.topnav a'): a.attrs.pop('aria-current',None)
side=page.select_one('.side');side.select_one('.back-link')['href']='fleet.html#player';side.select_one('.back-link').string='← К флоту'
side.select_one('.eyebrow').string='PLAYER INTERCEPTOR / РАЗВИТИЕ'
nav=side.nav;nav.clear()
content='''<section class="fleet-intro" id="overview"><div class="kicker">PLAYER INTERCEPTOR / РАЗВИТИЕ КОРАБЛЯ</div><h1>Один корабль.<br/>Вся кампания.</h1><div class="upgrade-status"><strong>Задано владельцем проекта</strong><p>Один узнаваемый корабль, накопленные улучшения и износ, презентация нового оборудования Максом.</p><strong>Предложено к реализации</strong><p>Игровые эффекты, параметры сцен и английские реплики — проект. Числовые бонусы пока не определены. Наличие изображений не подтверждает реализацию механик.</p></div><p><a href="fleet.html#ship-player-interceptor">Карточка Player Interceptor ↗</a> · <a href="#hangar-scenes">Межглавные сцены Max ↓</a></p></section>'''
content+='<section class="upgrade-notes" id="principle"><h2>Один корабль на всю кампанию</h2>'+paragraphs(DATA['principle'])+'</section>'
content+='''<section class="upgrade-notes" id="stages"><h2>Девять стадий развития</h2><p>Название стадии обозначает планету, к которой корабль подготовлен. Например, версия Jupiter появляется после прохождения Mars.</p><p>Улучшения помогают справляться с условиями следующей главы. Ветер, холод, плазменные стены и солнечные вспышки сохраняют свою роль. Баланс урона, прочности, ёмкости и перезарядки определяется при реализации.</p><p>Ангарные виды — существующие изображения из проекта игры, с локальным свечением сопел без длинного полётного выхлопа. Полётные концепты v9 доступны отдельно в каждой карточке.</p><nav class="fleet-world-links" aria-label="Стадии развития">'''+''.join(f'<a href="#stage-{s["id"]}">{s["name"]} ↘</a>' for s in STAGES)+'</nav></section>'
for n,s in enumerate(STAGES,1):
    slug=s['id'];assert (ROOT/s['image']).is_file()
    suffix='base' if slug=='mercury' else slug+'-upgrade-concept'
    flight='assets/ships/upgrades/originals/player-interceptor-'+suffix+'.png'
    transition='' if n==1 else f'<p><a href="scenario.html#upgrade-{slug}">Презентация Max в сценарии ↗</a></p>'
    content+=f'''<section class="upgrade-stage" id="stage-{slug}"><div class="fleet-heading"><div><div class="kicker">{n:02d} / АНГАРНЫЙ ВИД</div><h2>{s['name']}</h2><p>{esc(s['when'])}</p></div></div><article class="fleet-card fleet-feature"><a class="fleet-art" href="{s['image']}" aria-label="Увеличить ангарный вид: {s['name']}"><img src="{s['image']}" width="{s['width']}" height="{s['height']}" alt="Player Interceptor — {s['name']}, ангарное состояние" loading="lazy" decoding="async"/><span class="fleet-zoom" aria-hidden="true">↗</span></a><div class="fleet-copy"><h3>{esc(s['change'])}</h3><p><b>Предлагаемая роль в игре:</b> {esc(s['benefit'])}</p><p><b>Накопленный износ:</b> {esc(s['wear'])}</p>{transition}<div class="fleet-actions"><a href="{s['image']}" download>Ангарный PNG ↓</a><a href="{flight}" download>Полётный концепт v9 ↓</a></div></div></article></section>'''

def table(headers, rows):
    return '<div class="table-scroll" role="region" aria-label="'+esc(headers[-1])+'" tabindex="0"><table><thead><tr>'+''.join('<th scope="col">'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

content+='<section class="upgrade-notes" id="revision-nine"><h2>Накопленный износ</h2>'+paragraphs(DATA['wearIntro'])+table(['Стадия','Состояние старого корпуса'],[(s['name'],s['wear']) for s in STAGES])+paragraphs(DATA['wearNotes'])+'</section>'
content+='<section class="upgrade-notes" id="readability"><h2>Отражения окружения</h2>'+paragraphs(DATA['lightIntro'])+table(['Локация','Отражённый свет'],[(s['name'],s['light']) for s in STAGES])+paragraphs(DATA['lightNotes'])+'</section>'
content+='<section class="upgrade-notes" id="engines"><h2>Двигатели и ангарное состояние</h2>'+paragraphs(DATA['engines'])+'</section>'
content+='<section class="upgrade-notes" id="hangar-scenes"><h2>Как Max представляет улучшение</h2>'+paragraphs(DATA['presentation'])+'<p>Английские реплики — VO-черновик; русский смысл доступен под каждой сценой. Получение улучшения не зависит от просмотра сцены; повторный просмотр не выдаёт награду заново.</p>'+''.join(scene(s,'upgrades') for s in STAGES[1:])+'</section>'
content+='<section class="upgrade-notes" id="story-links"><h2>Сюжетные связи</h2>'+paragraphs(DATA['story'])+'</section>'
content+='<span id="neptune-presentation"><a href="#upgrade-neptune">Презентация Neptune ↑</a></span><span id="crown-presentation"><a href="#upgrade-solar-crown">Презентация Solar Crown ↑</a></span>'
footer=page.select_one('main .footer').extract();page.main.clear();page.main.append(parse(content));page.main.append(footer)
footer.select_one('span').string='PLAYER INTERCEPTOR / РАЗВИТИЕ КОРАБЛЯ'
for section in page.select('main > section[id]'):
    h=section.find(['h1','h2']);nav.append(parse(f'<a href="#{section["id"]}">{esc(h.get_text(" ",strip=True))}</a>'))
save('player-upgrades.html',page)

# Separately labelled proposals preserve every original scene and line.
for filename in sorted({s['script'] for s in STAGES[1:]}):
    doc=parse((ROOT/filename).read_text(encoding='utf-8'))
    for old in doc.select('.upgrade-interlude'):old.decompose()
    if not doc.select_one('link[href="assets/upgrades.css"]'):doc.head.append(parse('<link rel="stylesheet" href="assets/upgrades.css"/>'))
    for s in STAGES[1:]:
        if s['script']!=filename:continue
        if s['id']=='solar-crown':doc.select('.mission')[-1].insert(0,parse(scene(s,'source')))
        else:
            m=next(m for m in doc.select('.mission') if m.select_one('.mid') and m.select_one('.mid').get_text(strip=True)==s['after'])
            m.append(parse(scene(s,'source')))
    save(filename,doc)

p=ROOT/'assets/search-index.json';idx=json.loads(p.read_text(encoding='utf-8'))
idx=[e for e in idx if not e['url'].startswith('player-upgrades.html') and not (e['url'].startswith('scripts-') and '#upgrade-' in e['url'])]
for section in page.select('main > section[id],.upgrade-interlude'):
    h=section.find(['h1','h2','h3']);idx.append(dict(title=h.get_text(' ',strip=True),page='Player Interceptor / развитие',url='player-upgrades.html#'+section['id'],text=section.get_text(' ',strip=True)))
for s in STAGES[1:]:idx.append(dict(title=s['title']+' / VO-черновик',page='Межглавная сцена Max',url=s['script']+'#upgrade-'+s['id'],text=parse(scene(s)).get_text(' ',strip=True)))
p.write_text(json.dumps(idx,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Built nine hangar stages and eight proposed transitions; original dialogue preserved.')
