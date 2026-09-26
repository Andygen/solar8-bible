"""Publication gate: local resources, IDs, JSON contracts and generated fallbacks."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,sys,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bs4 import BeautifulSoup as Soup
from dialogue_catalog import ROOT,load_catalog

data=load_catalog();entries={e['id']:e for e in data['entries']}
def git_catalog(ref):
    result=subprocess.run(['git','show',ref+':assets/dialogues.json'],cwd=ROOT,capture_output=True)
    return json.loads(result.stdout.decode('utf8')) if result.returncode==0 else None
previous=git_catalog('HEAD')
if previous==data: previous=git_catalog('HEAD^')
if previous and previous!=data:assert previous['revision']!=data['revision'],'Catalog changed without a new revision'
pages={p.relative_to(ROOT).as_posix():Soup(p.read_text(encoding='utf8'),'html.parser') for p in list(ROOT.glob('*.html'))+list((ROOT/'game').rglob('*.html'))}
files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts}
for name,page in pages.items():
    ids=[e['id'] for e in page.select('[id]')];assert len(ids)==len(set(ids)),('Duplicate ID',name)
    for el in page.select('a[href],link[href],script[src],img[src]'):
        ref=el.get('href',el.get('src',''));u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(ROOT/Path(name).parent/unquote(u.path)).resolve() if u.path else ROOT/name
        key=target.relative_to(ROOT).as_posix()
        assert key in files,('Missing or wrong-case path',name,ref)
        if u.fragment and key in pages:assert pages[key].find(id=unquote(u.fragment)) or (key=='dialogues.html' and unquote(u.fragment) in entries),(name,ref)
    for node in page.select('[data-dialogue-id]'):
        e=entries[node['data-dialogue-id']]
        assert node.get_text()==e['en'],('Stale bound HTML; edit JSON and rebuild',name,e['id'])
        assert node.get('data-dialogue-source')=='assets/dialogues.json'
    for img in page.select('img[srcset]'):
        for candidate in img['srcset'].split(','):assert candidate.strip().split()[0] in files
        assert urlsplit(img['data-full-src']).path in files
index=json.loads((ROOT/'assets/search-index.json').read_text(encoding='utf8'))
assert len(index)==len(set(e['url'] for e in index)), 'Duplicate search URL'
for e in index:
    u=urlsplit(e['url']);assert u.path in pages,e['url']
    assert not u.fragment or pages[u.path].find(id=u.fragment) or (u.path=='dialogues.html' and u.fragment in entries),e['url']
    if u.path=='dialogues.html':
        entry=entries[u.fragment];assert entry['en'] in e['text'] and entry['ru'] in e['text']
assert not pages['dialogues.html'].select('.dialogue-row'), 'Bilingual page must read JSON, not duplicated HTML'
print(f'Site PASS: {len(pages)} pages, {len(index)} search links, {len(entries)} persistent dialogue IDs.')
