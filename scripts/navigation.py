"""One shared navigation shell, applied after any content generator."""
from pathlib import Path
from copy import deepcopy
from html import escape
from bs4 import BeautifulSoup as Soup

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [('worlds','Миры','index.html#campaign'),('story','Сценарий','scenario.html'),('fleet','Флот','fleet.html'),('characters','Персонажи','index.html#characters'),('materials','Материалы','index.html#production')]

def fragment(text): return Soup(text,'html.parser')
def anchor(href, label): return f'<a href="{escape(href)}">{escape(label)}</a>'
def group(key, label, links, opened=False):
    return f'<details class="contents-group" data-nav-group="{key}"'+(' open' if opened else '')+f'><summary>{escape(label)}<span class="contents-count">{len(links):02d}</span></summary><div class="contents-children">'+''.join(links)+'</div></details>'

def update_navigation():
    for path in sorted(ROOT.glob('*.html')):
        page=Soup(path.read_text(encoding='utf-8'),'html.parser');side=page.select_one('.side');top=page.select_one('.topnav')
        if not side or not top:continue
        name=path.name
        section=('characters' if name.startswith('character-') else 'story' if name=='scenario.html' else 'fleet' if name in ['fleet.html','player-upgrades.html'] else 'materials' if name.startswith(('scripts-','art-briefs')) or name=='story-rules.html' else 'worlds')
        top.clear()
        for key,title,url in SECTIONS:
            a=page.new_tag('a',href=url,attrs={'data-site-section':key});a.string=title
            if key==section and name!='index.html':a['aria-current']='page'
            top.append(a)
        top['aria-label']='Разделы сайта'
        mobile='<div class="mobile-site-links" role="navigation" aria-label="Разделы сайта"><div class="contents-label">Разделы сайта</div>'+top.decode_contents()+'</div>'
        local=side.select_one('nav');links=[]
        if local:
            for a in local.select('a[href^="#"]'):
                if not any(url==a['href'] for url,_ in links):links.append((a['href'],a.get_text(' ',strip=True)))
        parent='';title='На этой странице';content='';controls=''
        if name=='index.html':
            title='Путеводитель'
            content=group('project','О проекте',[anchor('#home','Обзор'),anchor('#story','Основной сюжет')],True)
            content+=group('worlds','Планеты',[anchor('#campaign','Карта кампании')]+[anchor('#'+p.lower(),p) for p in ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune']])
            content+=group('production','Разработка',[anchor('#production','Правила и исходники'),anchor('#canon','Канон'),anchor('#rook-gameplay','ROOK в игровом процессе')])
        elif name=='scenario.html':
            title='Оглавление сценария';content=local.decode_contents() if local else ''
            controls='<div class="tree-controls"><button type="button" data-tree="open">Раскрыть главы</button><button type="button" data-tree="close">Свернуть</button></div>'
            parent=anchor('index.html#story','← К обзору истории')
        elif name=='fleet.html':
            title='Каталог флота';parent=anchor('index.html#campaign','← К мирам')
            content=anchor('#overview','Обзор каталога')+anchor('#player','Корабль Andygen')
            planets=[anchor(url,text) for url,text in links if url not in ['#overview','#player','#fleet-rules','#archive']]
            content+=group('planets','По планетам',planets)+group('reference','Справочник',[anchor('#fleet-rules','Названия и способности'),anchor('#archive','Архив концептов')])
        elif name=='player-upgrades.html':
            title='Развитие корабля';parent=anchor('fleet.html#player','← Корабль Andygen')
            content=anchor('#overview','Обзор развития')
            content+=group('stages','Девять стадий',[anchor(url,text) for url,text in links if url.startswith('#stage-')])
            content+=group('principles','Внешний вид и правила',[anchor(url,text) for url,text in links if url in ['#principle','#revision-nine','#readability','#engines']])
            content+=group('story','Презентация и сюжет',[anchor('#hangar-scenes','Сцены Max'),anchor('#story-links','Сюжетные связи')])
        elif name=='story-rules.html':
            title='Правила истории';parent=anchor('index.html#production','← К материалам')
            content=anchor('#overview','Обзор')+''.join(anchor(url,label) for url,label in links if url!='#overview')
        elif name.startswith('scripts-'):
            title='Исходные диалоги';parent=anchor('scenario.html','← Читать сценарий')
            for i,chapter in enumerate(page.select('main > .chapter')):
                heading=chapter.find('h2');items=[]
                if not heading or not heading.get('id'):continue
                items.append(anchor('#'+heading['id'],'О главе'))
                for h in chapter.select('h3[id]'):items.append(anchor('#'+h['id'],h.get_text(' ',strip=True)))
                for h in chapter.select('.upgrade-interlude[id]'):items.append(anchor('#'+h['id'],h.h3.get_text(' ',strip=True)+' · черновик'))
                content+=group('chapter-'+str(i),heading.get_text(' ',strip=True).replace('Chapter ','Глава '),items)
            if not content:content=''.join(anchor(url,label) for url,label in links)
        elif name.startswith('art-briefs'):
            title='Визуальные брифы';parent=anchor('index.html#production','← К материалам')
            for i,(url,label) in enumerate(links):
                h=page.find(id=url[1:]);container=h.find_parent('section') if h else None
                if not h or h.name!='h2':continue
                items=[anchor(url,'Обзор раздела')]
                if container:
                    items += [anchor('#'+n['id'],n.get_text(' ',strip=True)) for n in container.select('h3[id]')]
                content+=group('brief-'+str(i),h.get_text(' ',strip=True),items)
        else:
            title='Досье персонажа';parent=anchor('index.html#characters','← Все персонажи')
            translations={'Reference views':'Ракурсы','Canonical appearance':'Внешность','Personality':'Характер','Pilot suit':'Костюм пилота','Story arc':'Сюжетная арка','Character brief':'Описание персонажа','Voice direction':'Голос','Production concept':'Основной концепт','Zoom / конструктивные детали':'Детали конструкции','Personality & voice':'Характер и голос'}
            links=[(url,translations.get(label,label)) for url,label in links]
            split=min(3,len(links))
            content=group('visual','Образ и ракурсы',[anchor(url,label) for url,label in links[:split]],True)
            content+=group('character','Персонаж и история',[anchor(url,label) for url,label in links[split:]])
        side.clear();side['aria-label']=title;side['data-navigation']='local'
        if parent:
            back=fragment(parent).a;back['class']=['back-link'];side.append(back)
        # Keep a local nav as the first nav element for existing content builders.
        side.append(fragment('<div class="contents-heading"><div class="eyebrow">'+title+'</div><button type="button" class="contents-close" aria-label="Закрыть меню">×</button></div>'+mobile+controls))
        nav=page.new_tag('nav',attrs={'aria-label':title,'class':'scenario-tree' if name=='scenario.html' else 'page-contents'})
        nav.append(fragment(content));side.append(nav)
        if not page.select_one('link[href="assets/navigation.css"]'):page.head.append(fragment('<link rel="stylesheet" href="assets/navigation.css"/>'))
        else:
            css=page.select_one('link[href="assets/navigation.css"]').extract();page.head.append(css)
        menu=page.find(id='menu')
        if menu:menu['aria-label']='Открыть меню';menu['title']='Разделы и оглавление'
        path.write_text(str(page),encoding='utf-8')

if __name__=='__main__':
    update_navigation()
    print('Updated global navigation and contextual contents on all pages.')
