"""Guard the canonical story, language coverage and legacy link migration."""
from pathlib import Path
import json,re,sys
from bs4 import BeautifulSoup as Soup
sys.path.insert(0,str(Path(__file__).resolve().parent))
from story_data import STORY,GAME,ROOT
reader=Soup((ROOT/'scenario.html').read_text(encoding='utf8'),'html.parser')
ids=set();lines=0
for mission in STORY['missions']:
    for scene in mission['scenes']:
        assert scene['id'] not in ids;ids.add(scene['id'])
        for block in scene['blocks']:
            if block['type']!='line':continue
            e=block['line'];assert e['id'] not in ids;ids.add(e['id']);lines+=1
            if e.get('dialogue_id'):
                assert e['dialogue_id'] in GAME
                assert 'en' not in e and 'ru' not in e,'Game strings must not have an independent literary copy'
            else:
                assert e['en'].strip() and e['ru'].strip(),e['id']
                assert e['translation_status'] in ['editorial_draft','reviewed'],e['id']
            assert reader.select_one('[data-story-id="'+e['id']+'"]'),e['id']
for node in reader.select('.line > .text,.dialogue > .line'):
    assert node.get('data-en') and node.get('data-ru'),str(node)[:200]
for name,route in STORY['legacy_routes'].items():
    page=Soup((ROOT/name).read_text(encoding='utf8'),'html.parser')
    assert not page.select('.scene,.dialogue'),name
    assert json.loads(page.select_one('#legacy-route').string)==route
    for old,target in route['anchors'].items():
        assert page.find(id=old), (name,old)
        assert reader.find(id=target),(name,target)
index=json.loads((ROOT/'assets/search-index.json').read_text(encoding='utf8'))
assert not any(e['url'].startswith('scripts-') for e in index)
assert any('Пересекай поток' in e['text'] and 'scenario.html#mission-5-1'==e['url'] for e in index)
assert not Soup((ROOT/'player-upgrades.html').read_text(encoding='utf8'),'html.parser').select('.upgrade-dialogue')
print(f'Story PASS: {lines} source lines, bilingual reader, all legacy destinations and Russian search.')
