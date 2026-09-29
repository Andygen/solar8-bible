"""Install the single language control across public Bible pages."""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'assets/site-translations.json').read_text(encoding='utf8'))['strings']
for path in ROOT.glob('*.html'):
    page=Soup(path.read_text(encoding='utf8'),'html.parser');top=page.select_one('.top')
    if not top:continue
    for node in page.find_all(string=True):
        source=str(node).strip()
        if re.search('[\u0400-\u04ff]',source) and source in catalog and catalog[source]['ru']!=source:
            node.replace_with(str(node).replace(source,catalog[source]['ru']))
    for old in page.select('.site-language'):old.decompose()
    control=Soup('<label class="site-language"><select id="site-language" aria-label="Язык сайта"><option value="ru">RU</option><option value="en">EN</option></select></label>','html.parser')
    search=top.select_one('.search-open')
    if search:search.insert_before(control)
    else:top.append(control)
    for selector in ['script[src="assets/site-language.js"]','link[href="assets/site-language.css"]']:
        for old in page.select(selector):old.decompose()
    page.head.append(page.new_tag('link',rel='stylesheet',href='assets/site-language.css'))
    page.head.append(page.new_tag('script',src='assets/site-language.js',defer=True))
    path.write_text(str(page),encoding='utf8')
