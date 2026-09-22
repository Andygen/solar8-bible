"""Check reader/source parity, interlude placement and local references."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup as Soup
import re

ROOT=Path(__file__).resolve().parents[1]
pages={p.name:Soup(p.read_text(encoding='utf8'),'html.parser') for p in ROOT.glob('*.html')}
reader=pages['scenario.html']
def normalized(scene):
    clone=Soup(str(scene),'html.parser')
    for el in clone.select('.priority'):el.decompose()
    return clone.get_text(' ',strip=True)
count=0
for name,source in pages.items():
    if not name.startswith('scripts-'):continue
    for mission in source.select('.mission'):
        mid=mission.select_one('.mid')
        if not mid or not re.fullmatch(r'[1-8]-[1-5]',mid.get_text(strip=True)):continue
        target=reader.select_one('#mission-'+mid.get_text(strip=True))
        assert target is not None
        assert [normalized(s) for s in mission.select(':scope > .scene')]==[normalized(s) for s in target.select(':scope > .scene')],mid
        count+=1
assert count==40
for card in pages['index.html'].select('#production article'):
    kicker=card.select_one('.kicker')
    if not kicker:continue
    match=re.fullmatch(r'(BEFORE|AFTER) ([1-8]-[1-5])',kicker.get_text(strip=True))
    if not match:continue
    target=reader.select_one('#mission-'+match[2])
    interlude=next((a for a in target.select('.interlude') if card.h3.get_text(strip=True) in a.get_text()),None)
    assert interlude is not None,card.h3
    children=list(target.children)
    first_scene=target.select_one(':scope > .scene')
    assert (children.index(interlude)<children.index(first_scene))==(match[1]=='BEFORE')
for name,page in pages.items():
    ids=[e['id'] for e in page.select('[id]')];assert len(ids)==len(set(ids)),('duplicate IDs',name)
    for link in page.select('a[href]'):
        u=urlsplit(link['href'])
        if u.scheme or u.netloc:continue
        path=unquote(u.path) or name
        assert (ROOT/path).exists(),(name,path)
        if u.fragment and path in pages:assert pages[path].find(id=unquote(u.fragment)),(name,path,u.fragment)
assert 'Last confirmed memory: Saturn departure.' in reader.get_text()
assert 'Two transports clear. We lost the third.' in reader.get_text()
assert reader.select_one('#mission-8-1').get_text().find('It\'s ROOK.')>=0
assert 'ROOK reboot' not in reader.select_one('#mission-8-1').get_text()
assert 'System integrity nominal.' in reader.select_one('#mission-8-2').get_text()
print(f'PASS: {count} missions match VO sources; all BEFORE/AFTER scenes present and ordered; {len(pages)} pages have valid local links and unique IDs; ROOK chronology and convoy branch intact.')
