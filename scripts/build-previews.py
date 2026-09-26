"""Generate derived WebP previews; never modify production PNG originals."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib,json
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from bs4 import BeautifulSoup as Soup

ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'assets/previews';dest.mkdir(exist_ok=True)
cache={};manifest={}
paths=sorted(ROOT.glob('*.html'))
pages={path:Soup(path.read_text(encoding='utf8'),'html.parser') for path in paths}
sources=set()
for page in pages.values():
    for img in page.select('img[src]'):
        source=urlsplit(img.get('data-full-src',img['src']))
        if not source.scheme and not source.netloc and source.path.lower().endswith('.png') and (ROOT/source.path).is_file():sources.add(source.path)
def generate(source):
    file=ROOT/source;digest=hashlib.sha256(file.read_bytes()).hexdigest()[:12];variants=[]
    with Image.open(file) as im:
        for width in [320,640,960]:
            if width>im.width and variants:continue
            thumb=im.copy();thumb.thumbnail((width,width),Image.Resampling.LANCZOS)
            target=dest/f'{file.stem}-{digest}-m4-{width}.webp'
            if not target.exists():thumb.save(target,'WEBP',quality=85,method=4)
            variants.append((target.relative_to(ROOT).as_posix(),thumb.width))
    return source,variants,{'sha256':digest,'original_bytes':file.stat().st_size,'variants':[{'file':p,'width':w,'bytes':(ROOT/p).stat().st_size} for p,w in variants]}
with ThreadPoolExecutor(max_workers=4) as pool:
    for source,variants,record in pool.map(generate,sorted(sources)):
        cache[source]=variants;manifest[source]=record
for path,page in pages.items():
    for img in page.select('img[src]'):
        original=img.get('data-full-src',img['src']);source=urlsplit(original)
        if source.path not in cache:continue
        variants=cache[source.path];img['data-full-src']=original
        img['src']=variants[min(1,len(variants)-1)][0]
        img['srcset']=', '.join(f'{p} {w}w' for p,w in variants)
        if img.find_parent(class_='fleet-thumb'):sizes='(max-width: 620px) 40vw, 180px'
        elif img.find_parent(class_='brand') or img.find_parent('footer'):sizes='180px'
        else:sizes='(max-width: 620px) 90vw, (max-width: 1100px) 45vw, 640px'
        img['sizes']=sizes
    path.write_text(str(page),encoding='utf8')
(ROOT/'assets/preview-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Previews: {len(cache)} originals preserved; {sum(len(v) for v in cache.values())} derived WebP files.')
