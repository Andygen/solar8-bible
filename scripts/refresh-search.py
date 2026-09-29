"""Refresh existing search records from current page content after editorial edits."""
from pathlib import Path
from urllib.parse import urlsplit
import json
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'assets/search-index.json';entries=json.loads(path.read_text(encoding='utf8'))
pages={p.name:Soup(p.read_text(encoding='utf8'),'html.parser') for p in ROOT.glob('*.html')}
catalog=json.loads((ROOT/'assets/site-translations.json').read_text(encoding='utf8'))['strings']
game={e['id']:e for e in json.loads((ROOT/'assets/dialogues.json').read_text(encoding='utf8'))['entries']}
def english(node):
    clone=Soup(str(node),'html.parser')
    for tag in clone.select('[data-en]'):
        tag.clear();tag.append(tag['data-en'])
    for text in clone.find_all(string=True):
        source=str(text).strip()
        if source in catalog:text.replace_with(catalog[source]['en'])
    return clone.get_text(' ',strip=True)
for entry in entries:
    url=urlsplit(entry['url']);page=pages.get(url.path)
    if page is None:continue
    if url.path=='dialogues.html' and url.fragment in game:
        entry['text_en']=game[url.fragment]['en'];continue
    node=page.find(id=url.fragment) if url.fragment else page.main
    if node is None:continue
    if node.name in ['h1','h2','h3','h4']:
        if node.find_parent('article'):node=node.find_parent('article')
        elif 'head' in node.parent.get('class',[]):
            block=node.parent;pieces=[block.get_text(' ',strip=True)];en_pieces=[english(block)]
            for sibling in block.find_next_siblings():
                if 'head' in sibling.get('class',[]):break
                pieces.append(sibling.get_text(' ',strip=True))
                en_pieces.append(english(sibling))
            entry['text']=' '.join(pieces);entry['text_en']=' '.join(en_pieces);continue
        else:node=node.find_parent('section') or node.parent
    entry['text']=node.get_text(' ',strip=True)+' '+' '.join(n['data-ru'] for n in node.select('[data-ru]'))
    entry['text_en']=english(node)
path.write_text(json.dumps(entries,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print('Refreshed',len(entries),'search records from current HTML.')
