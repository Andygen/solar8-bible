"""Refresh existing search records from current page content after editorial edits."""
from pathlib import Path
from urllib.parse import urlsplit
import json
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'assets/search-index.json';entries=json.loads(path.read_text(encoding='utf8'))
pages={p.name:Soup(p.read_text(encoding='utf8'),'html.parser') for p in ROOT.glob('*.html')}
for entry in entries:
    url=urlsplit(entry['url']);page=pages.get(url.path)
    if page is None:continue
    node=page.find(id=url.fragment) if url.fragment else page.main
    if node is None:continue
    if node.name in ['h1','h2','h3','h4']:
        if node.find_parent('article'):node=node.find_parent('article')
        elif 'head' in node.parent.get('class',[]):
            block=node.parent;pieces=[block.get_text(' ',strip=True)]
            for sibling in block.find_next_siblings():
                if 'head' in sibling.get('class',[]):break
                pieces.append(sibling.get_text(' ',strip=True))
            entry['text']=' '.join(pieces);continue
        else:node=node.find_parent('section') or node.parent
    entry['text']=node.get_text(' ',strip=True)
path.write_text(json.dumps(entries,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print('Refreshed',len(entries),'search records from current HTML.')
