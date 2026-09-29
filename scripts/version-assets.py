"""Version shared CSS/JS URLs, or normalize them before running content builders."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib,sys
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[1]
normalize='--normalize' in sys.argv
for path in ROOT.glob('*.html'):
    page=Soup(path.read_text(encoding='utf8'),'html.parser')
    for node in page.select('script[src],link[rel="stylesheet"][href],link[rel="icon"][href]'):
        attr='src' if node.name=='script' else 'href'
        source=node.get('data-asset-source',node[attr]);u=urlsplit(source)
        if u.scheme or u.netloc or not (ROOT/u.path).is_file():continue
        if normalize:
            if node.get('data-asset-source'):node[attr]=source;del node['data-asset-source']
        else:
            node['data-asset-source']=source
            digest=hashlib.sha256((ROOT/u.path).read_text(encoding='utf8').encode('utf8')).hexdigest()[:12]
            node[attr]=u.path+'?v='+digest
    path.write_text(str(page),encoding='utf8')
