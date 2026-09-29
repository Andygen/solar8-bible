"""Prevent untranslated Russian prose and missing global language controls."""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup as Soup,Comment
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'assets/site-translations.json').read_text(encoding='utf8'))['strings']
cyrillic=re.compile('[\u0400-\u04ff]')
errors=[];count=0
def check(text,filename):
    text=text.strip()
    if not cyrillic.search(text) or text=='Русский':return
    entry=catalog.get(text)
    if not entry or not entry.get('en') or cyrillic.search(entry['en']):
        errors.append(f'{filename}: missing EN: {text[:100]}')
for path in ROOT.glob('*.html'):
    page=Soup(path.read_text(encoding='utf8'),'html.parser')
    if not page.select_one('.top'):continue # Legacy URL redirects have no reading interface.
    count+=1
    assert len(page.select('.top #site-language'))==1,path.name
    assert len(page.select('script[src*="assets/site-language.js"]'))==1,path.name
    assert len(page.select('link[href*="assets/site-language.css"]'))==1,path.name
    for node in page.find_all(string=True):
        if isinstance(node,Comment) or node.parent.name in ['script','style','code','pre']:continue
        if node.find_parent(attrs={'data-ru':True}):continue
        check(str(node),path.name)
    for node in page.select('[alt],[title],[aria-label],[placeholder]'):
        for attr in ['alt','title','aria-label','placeholder']:check(node.get(attr,''),path.name)
    for node in page.select('[data-en]'):check(node['data-en'],path.name)
assert not errors,'\n'.join(errors)
andygen=Soup((ROOT/'character-andygen.html').read_text(encoding='utf8'),'html.parser')
assert andygen.select_one('#pilot-ship img')['data-full-src']=='assets/ships/player-interceptor.png'
home=Soup((ROOT/'index.html').read_text(encoding='utf8'),'html.parser')
cast=home.select_one('.cast-banner img')
assert '1672w' in cast['srcset'] and 'cast-hq' in cast['src']
assert all(e.get('text_en') for e in json.loads((ROOT/'assets/search-index.json').read_text(encoding='utf8')))
print(f'Language PASS: {count} pages, global controls, complete Russian-prose EN coverage, bilingual search, pilot ship and full-size cast.')
