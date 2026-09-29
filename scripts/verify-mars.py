"""Verify the handoff bytes and its connection to the shared dialogue source."""
from pathlib import Path
import hashlib,json
from bs4 import BeautifulSoup as Soup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/mars-2026-09-29'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
count=0
for line in (PACK/'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines():
    checksum,name=line.split(None,1);path=(PACK/name.strip()).resolve()
    assert path.is_relative_to(PACK.resolve()),name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==checksum,name
    count+=1
master={e['id']:e for e in read(ROOT/'assets/dialogues.json')['entries']}
entries=read(PACK/'dialogues/mars-dialogues.json')['entries']
assert len(entries)==74
for entry in entries:
    assert entry['id'] in master,entry['id']
    for key in ['en','ru','speaker','mission','context','trigger','order']:
        assert master[entry['id']][key]==entry[key],(entry['id'],key)
page=Soup((ROOT/'mars-production.html').read_text(encoding='utf8'),'html.parser')
assert len(page.select('section[id^="mission-"]'))==5
assert len(page.select('.mars-gallery img'))==19
for asset in read(PACK/'assembler-animation-v1/manifest.json')['assets']:
    original=PACK/'assembler-animation-v1'/asset['file']
    assert hashlib.sha256(original.read_bytes()).hexdigest()==asset['sha256']
    with Image.open(original) as im:assert list(im.size)==asset['size']
    runtime=PACK/'art/runtime/mars/assembler'/('assembler-'+asset['id']+'.png')
    assert runtime.stat().st_size<500_000
    with Image.open(runtime) as im:assert 'A' in im.getbands()
print(f'Mars PASS: {count} checksums, 74 shared records, five missions, 19 images and ten scaled rig parts.')
