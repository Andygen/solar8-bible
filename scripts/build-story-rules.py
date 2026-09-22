"""Build the editorial rules reference from docs/story-rules.md."""
from pathlib import Path
import json
import markdown
from bs4 import BeautifulSoup as Soup
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from navigation import update_navigation

ROOT=Path(__file__).resolve().parents[1]
page=Soup((ROOT/'art-briefs-earth-mars.html').read_text(encoding='utf-8'),'html.parser')
page.title.string='SOLAR 8 // Правила истории и производства'
page.select_one('meta[name="description"]')['content']='Хронология, правила заражения, логистика, исходы миссий и реестр недостающих материалов SOLAR 8.'
body=Soup(markdown.markdown((ROOT/'docs/story-rules.md').read_text(encoding='utf-8'),extensions=['tables']),'html.parser')
main=page.main;main.clear()
intro=page.new_tag('section',id='overview',attrs={'class':'section'});main.append(intro)
current=intro
for node in list(body.contents):
    if getattr(node,'name',None)=='h2':
        current=page.new_tag('section',attrs={'class':'section'});main.append(current)
    current.append(node.extract())
main.append(Soup('<footer class="footer"><a href="index.html#production">← Материалы</a> · SOLAR 8 / РЕДАКЦИЯ 22.09.2026</footer>','html.parser'))
nav=page.select_one('.side nav');nav.clear()
for h in main.select('h2[id]'):
    a=page.new_tag('a',href='#'+h['id']);a.string=h.get_text(' ',strip=True);nav.append(a)
page.body['class']=['script-page','story-rules-page']
style=page.new_tag('style');style.string='.story-rules-page .section{margin:32px 0}.story-rules-page table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse;font-size:13px}.story-rules-page th,.story-rules-page td{padding:12px;border:1px solid #ffffff20;min-width:150px;vertical-align:top}.story-rules-page p,.story-rules-page li{line-height:1.75}.story-rules-page li{margin-bottom:10px}'
page.head.append(style)
(ROOT/'story-rules.html').write_text(str(page),encoding='utf-8')
index=ROOT/'assets/search-index.json';entries=json.loads(index.read_text(encoding='utf-8'))
entries=[e for e in entries if not e['url'].startswith('story-rules.html')]
for sec in main.select('section'):
    h=sec.find(['h1','h2']);anchor=h.get('id','overview')
    entries.append({'title':h.get_text(' ',strip=True),'page':'Правила истории','url':'story-rules.html#'+anchor,'text':sec.get_text(' ',strip=True)})
index.write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
update_navigation()
print('Built story rules and search entries.')
