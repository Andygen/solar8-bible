"""Build the reading edition from the existing Bible and four VO sources.
Run: python scripts/build-scenario.py (no generated dialogue or plot changes).
"""
from pathlib import Path
from bs4 import BeautifulSoup
from copy import deepcopy
from html import escape
import json,re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from progression import STAGES, scene as upgrade_scene
r=Path(__file__).resolve().parents[1]
home=BeautifulSoup((r/'index.html').read_text(encoding='utf-8'),'html.parser')
s=BeautifulSoup((r/'scripts-mercury-venus.html').read_text(encoding='utf-8'),'html.parser')
s.title.string='SOLAR 8 // Сценарий — полная история'
s.body['class']=['script-page','scenario-page']
s.html['class']=['scenario-document']
meta=s.select_one('meta[name="description"]')
if not meta:meta=s.new_tag('meta',attrs={'name':'description'});s.head.append(meta)
meta['content']='Полный сценарий SOLAR 8: общий сюжет, восемь планет, 40 миссий, диалоги и эпилог Solar Crown. Читайте по порядку или выбирайте главу в дереве.'
s.head.append(s.new_tag('link',rel='stylesheet',href='assets/scenario.css'));s.head.append(s.new_tag('script',src='assets/scenario.js',defer=True))
if not s.select_one('link[href="assets/upgrades.css"]'):s.head.append(s.new_tag('link',rel='stylesheet',href='assets/upgrades.css'))
main=s.main;main.clear();main['class']=['wrap','reader']
planets=['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune']
files=['scripts-mercury-venus.html','scripts-earth-mars.html','scripts-jupiter-saturn.html','scripts-uranus-neptune.html']
vo={};epilogue=None
for filename in files:
 doc=BeautifulSoup((r/filename).read_text(encoding='utf-8'),'html.parser')
 for m in doc.select('.mission'):
  mid=m.select_one('.mid')
  if mid and re.fullmatch(r'[1-8]-[1-5]',mid.get_text(strip=True)):vo[mid.get_text(strip=True)]=(filename,m)
 if filename==files[-1]:epilogue=doc.select('.mission')[-1]
assert len(vo)==40

def clean(node):
 n=deepcopy(node)
 for t in [n]+n.find_all(True):
  t.attrs.pop('id',None);t.attrs.pop('style',None)
 return n

def scenes(m):
 out=''
 for scene in m.select(':scope > .scene'):
  n=clean(scene)
  for priority in n.select('.priority'):priority.decompose()
  out+=str(n)
 return out

def prose(cards):
 out=''
 for c in cards:
  if c.h3:out+='<h3>'+escape(c.h3.get_text(' ',strip=True))+'</h3>'
  for p in c.find_all(['p','blockquote'],recursive=False):out+=str(clean(p))
  timeline=c.select_one('.timeline')
  if timeline:out+='<p class="story-path">'+escape(timeline.get_text(' ',strip=True))+'</p>'
  quote=c.select_one('.quote')
  if quote:out+='<blockquote>'+quote.decode_contents()+'</blockquote>'
 return out

intro='''<section id="overview" class="reader-section"><div class="kicker">SOLAR 8 / СЦЕНАРИЙ</div><h1>От первого сигнала<br>до первого контакта.</h1><p class="reader-lead">История целиком: восемь планет, сорок миссий и эпилог у самого Солнца.</p><div class="reader-actions"><a class="reader-button" href="#mercury">Начать читать →</a><button type="button" class="reader-button resume-reading" hidden>Продолжить чтение →</button><button type="button" class="reader-button open-contents">Оглавление</button></div><p class="edition-note">Описание событий — на русском. Диалоги сохранены на английском из текущего сценария. Все сюжетные раскрытия включены.</p><h2>Общий сюжет</h2>'''
intro+=prose(home.select('#story .card'))+'</section>'
html=intro;tree='<a href="#overview">Общий сюжет</a>'
search=[{'title':'Сценарий','page':'История SOLAR 8','url':'scenario.html#overview','text':BeautifulSoup(intro,'html.parser').get_text(' ',strip=True)}]
mission_titles={}
interludes={}
for c in home.select('#production article'):
 k=c.select_one('.kicker')
 if k:
  match=re.fullmatch(r'AFTER ([1-8]-[1-5])',k.get_text(strip=True))
  if match:interludes.setdefault(match.group(1),[]).append(c)
for no,planet in enumerate(planets,1):
 slug=planet.lower();chapter=home.find(id=slug);missions=chapter.select('.missions > .mission');assert len(missions)==5,(slug,len(missions))
 tree+=f'<details class="chapter-tree" data-chapter="{slug}"><summary><span>{planet}</span><small>05</small></summary><div class="tree-children"><a href="#{slug}">О главе</a>'
 chunk=f'<section class="reader-section chapter-reader" id="{slug}"><div class="chapter-heading"><div class="kicker">ГЛАВА {no:02d} / 08</div><h2>{planet}</h2>'
 path=chapter.select_one('.path')
 if path:chunk+='<p class="story-path">'+escape(path.get_text(' ',strip=True))+'</p>'
 chunk+='</div>'
 # Intro/story-beat cards outside the mission list, when available.
 cards=[c for c in chapter.select('article.card') if not c.find_parent(class_='missions') and 'mission' not in c.get('class',[]) and c.h3]
 chunk+=prose(cards)
 chapter_intro=BeautifulSoup(chunk,'html.parser').get_text(' ',strip=True)
 for m in missions:
  mid=m.select_one('.mid').get_text(strip=True);title=m.h3.get_text(' ',strip=True);mission_titles[mid]=title
  tree+=f'<a href="#mission-{mid}"><span>{mid}</span> {escape(title)}</a>'
  filename,v=vo[mid];chunk+=f'<article class="reader-mission" id="mission-{mid}" data-chapter="{slug}"><header><div class="kicker">МИССИЯ {mid}</div><h3>{escape(title)}</h3></header>'
  for item in m.select('.meta > div'):chunk+='<p class="mission-context">'+item.decode_contents()+'</p>'
  body=m.find_all('p');kind=m.select_one('.kind')
  chunk+='<details class="mission-gameplay"><summary>Действие и механика миссии</summary>'
  if kind:chunk+='<p class="kind">'+escape(kind.get_text(' ',strip=True))+'</p>'
  chunk+=''.join(str(clean(p)) for p in body)+'</details>'
  chunk+=f'<div class="dialogue-heading" id="dialogue-{mid}"><h4>Диалоги и сцены</h4><a href="{filename}#{v.h3.get("id")}">Исходный VO ↗</a></div>'+scenes(v)
  for c in interludes.get(mid,[]):chunk+='<aside class="interlude"><div class="kicker">ПОСЛЕ МИССИИ / АНГАР</div>'+prose([c])+'</aside>'
  for stage in STAGES[1:-1]:
   if stage['after']==mid:
    chunk+=upgrade_scene(stage)
    tree+=f'<a href="#upgrade-{stage["id"]}">Ангар Max → {stage["name"]} · черновик</a>'
  chunk+=f'<nav class="mission-pagination" aria-label="Переходы после миссии {mid}" data-mission="{mid}"></nav></article>'
  search.append({'title':mid+' · '+title,'page':'Сценарий / '+planet,'url':'scenario.html#mission-'+mid,'text':m.get_text(' ',strip=True)+' '+v.get_text(' ',strip=True)})
 chunk+='</section>';html+=chunk;tree+='</div></details>'
 search.append({'title':planet,'page':'Сценарий / глава '+str(no),'url':'scenario.html#'+slug,'text':chapter_intro+' '+', '.join(mission_titles[f'{no}-{i}'] for i in range(1,6))})
crown_cards=[]
for title in ['Почти внутри короны']:
 h=home.find('h3',string=title)
 if h:crown_cards.append(h.find_parent('article'))
crown='<section class="reader-section" id="solar-crown"><div class="kicker">ЭПИЛОГ / ПОСЛЕ ТИТРОВ</div><h2>Solar Crown</h2><p class="reader-lead">Бонусная миссия у самого Солнца. Основная история завершена на Neptune; здесь появляется следующая загадка.</p>'+prose(crown_cards)+upgrade_scene(STAGES[-1])+'<h3>Координаты происхождения</h3>'+scenes(epilogue)+'<p>Крючок для продолжения. Основной финал остаётся завершённым и без прохождения бонуса.</p><nav class="mission-pagination"><a href="#mission-8-5">← Финал Neptune</a><a href="#overview">К началу ↑</a></nav></section>'
for stage in STAGES[1:]:
 search.append({'title':stage['title']+' / VO-черновик','page':'Сценарий / ангар Max','url':'scenario.html#upgrade-'+stage['id'],'text':BeautifulSoup(upgrade_scene(stage),'html.parser').get_text(' ',strip=True)})
html+=crown;tree+='<a href="#solar-crown">Solar Crown <small>Эпилог</small></a>'
search.append({'title':'Solar Crown','page':'Сценарий / эпилог','url':'scenario.html#solar-crown','text':BeautifulSoup(crown,'html.parser').get_text(' ',strip=True)})
html+='<footer class="footer"><a href="index.html"><img src="assets/solar-logo-polished.png" alt="SOLAR 8" width="2048" height="768"></a><span>СЦЕНАРИЙ / ЧИТАТЕЛЬСКАЯ ВЕРСИЯ</span><a href="#overview">К началу ↑</a></footer>'
main.append(BeautifulSoup(html,'html.parser'))
ids=list(mission_titles)
for n,mid in enumerate(ids):
 nav=main.select_one(f'nav[data-mission="{mid}"]');prev='#overview' if n==0 else '#mission-'+ids[n-1];nxt='#solar-crown' if n==39 else '#mission-'+ids[n+1]
 nav.append(BeautifulSoup(f'<a href="{prev}">← '+('Общий сюжет' if n==0 else ids[n-1]+' · '+escape(mission_titles[ids[n-1]]))+f'</a><a href="{nxt}">'+('Solar Crown' if n==39 else ids[n+1]+' · '+escape(mission_titles[ids[n+1]]))+' →</a>','html.parser'))
aside=s.select_one('.side');aside.clear();aside['class']=['side','document-side','reader-side']
aside.append(BeautifulSoup('<a class="back-link" href="index.html">← К проекту</a><div class="eyebrow">СЦЕНАРИЙ / ОГЛАВЛЕНИЕ</div><div class="tree-controls"><button type="button" data-tree="open">Раскрыть всё</button><button type="button" data-tree="close">Свернуть</button></div><nav aria-label="Дерево сценария" class="scenario-tree">'+tree+'</nav>','html.parser'))
(r/'scenario.html').write_text(str(s),encoding='utf-8')
p=r/'assets/search-index.json';idx=json.loads(p.read_text(encoding='utf-8'));idx=[e for e in idx if not e['url'].startswith('scenario.html')];idx+=search;p.write_text(json.dumps(idx,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
# One shared entry on every page, including mobile side menus.
for p in r.glob('*.html'):
 d=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser');top=d.select_one('.topnav')
 if top and not top.select_one('a[href="scenario.html"]'):
  a=d.new_tag('a',href='scenario.html');a.string='Сценарий';top.insert(1,a)
 if p.name=='scenario.html':
  top.select_one('a[href="scenario.html"]')['aria-current']='page'
 else:
  side=d.select_one('.side')
  if side and not side.select_one('a[href="scenario.html"]'):
   a=d.new_tag('a',href='scenario.html',attrs={'class':'scenario-entry'});a.string='Сценарий →';side.insert(0,a)
 if p.name=='index.html':
  for a in d.select('.hero-copy a[href="#story"]'):a['href']='scenario.html'
  prod=d.find(id='production')
  if not prod.select_one('.read-scenario'):
   a=d.new_tag('a',href='scenario.html',attrs={'class':'read-scenario'});a.string='Читать сценарий целиком: сюжет, 40 миссий и Solar Crown →';prod.select_one('.head').insert_after(a)
 p.write_text(str(d),encoding='utf-8')
print('Built scenario: 40 missions,',len(main.select('.scene')),'scenes,',len(main.select('.line')),'dialogue lines;',len(interludes),'interludes')

# Normalize the shared navigation after generating page content.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from navigation import update_navigation
update_navigation()
