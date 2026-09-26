"""Bind exact literary matches to persistent game IDs, then build the RU/EN reader.

Only the initial match uses legacy English. Existing data-dialogue-id survives edits.
Bound HTML is a generated fallback; runtime textContent reads the same public JSON.
Future literary dialogue and gameplay adaptations are never silently merged.
"""
from pathlib import Path
from collections import defaultdict
from copy import deepcopy
import json, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bs4 import BeautifulSoup as Soup
from dialogue_catalog import ROOT, load_catalog

data = load_catalog(); by_id = {e['id']: e for e in data['entries']}
matches = defaultdict(list)
def norm(text): return ' '.join(text.split())
for e in data['entries']:
    if e['relationship'] == 'verbatim_en':
        for text in set([e['en'], e['legacy_text']]):
            matches[(e['speaker'], norm(text))].append(e)

bindings = []; ambiguous = []
for path in sorted(ROOT.glob('*.html')):
    if path.name in ['dialogues.html', 'resource-status.html']: continue
    page = Soup(path.read_text(encoding='utf8'), 'html.parser')
    nodes = page.select('.scene .line > .text, .dialogue > .line, [data-dialogue-id]')
    for node in nodes:
        key = node.get('data-dialogue-id')
        if not key:
            row = node.parent; speaker = row.select_one('.speaker')
            if not speaker: continue
            candidates = {e['id']: e for e in matches[(speaker.get_text(' ',strip=True).upper(), norm(node.get_text(' ',strip=True)))]}
            mission = node.find_parent(class_='mission') or node.find_parent(class_='reader-mission')
            mid = mission.select_one('.mid') if mission else None
            num = mid.get_text(strip=True) if mid else (mission.get('id','').replace('mission-','') if mission else '')
            if not num:
                article = node.find_parent('article')
                kicker = article.select_one('.kicker') if article else None
                number = re.search(r'\b([1-8]-[1-5])\b', kicker.get_text() if kicker else '')
                if number: num = number[1]
            if num:
                candidates = {k:e for k,e in candidates.items() if not e['mission'] or e['mission'].endswith('_'+num.replace('-','_'))}
                exact = {k:e for k,e in candidates.items() if e['mission']}
                if exact: candidates = exact
            if len(candidates)>1 and all(e['context']=='evacuation_corridor' for e in candidates.values()):
                scene = node.find_parent(class_='scene')
                heading = scene.select_one('.scene-title') if scene else None
                if heading:
                    trigger = 'DAMAGED_ENDING' if 'two transports' in heading.get_text().lower() else 'ENDING'
                    candidates = {k:e for k,e in candidates.items() if e['trigger']==trigger}
            if len(candidates) == 1: key = next(iter(candidates))
            elif candidates: ambiguous.append({'page':path.name,'speaker':speaker.get_text(),'candidates':list(candidates)})
        if key:
            assert key in by_id, key
            node['data-dialogue-id'] = key
            node['data-dialogue-source'] = 'assets/dialogues.json'
            node['lang'] = 'en'; node.string = by_id[key]['en']
            bindings.append({'page':path.name,'id':key})
    bound = page.select('[data-dialogue-id]')
    if bound:
        if not page.select_one('script[src="assets/dialogue-bindings.js"]'):
            page.head.append(page.new_tag('script',src='assets/dialogue-bindings.js',defer=True))
        if not page.select_one('link[href="assets/dialogues.css"]'):
            page.head.append(page.new_tag('link',rel='stylesheet',href='assets/dialogues.css'))
        old = page.find(id='dialogue-language');
        if old: old.decompose()
        bar = Soup('<aside class="dialogue-language" id="dialogue-language"><a href="dialogues.html">Реплики игры · RU / EN →</a><label>Связанные реплики <select id="bound-language"><option value="en">English</option><option value="ru">Русский</option></select></label><p>Перевод переключается только у реплик с постоянным ID. Остальной текст — литературный сценарий и будущие главы; игровые адаптации доступны отдельно в каталоге.</p><span role="status" id="bound-status">Загрузка общего источника…</span></aside>', 'html.parser')
        page.main.insert(0, bar)
    path.write_text(str(page),encoding='utf8')

shell = Soup((ROOT/'story-rules.html').read_text(encoding='utf8'),'html.parser')
shell.title.string = 'SOLAR 8 // Реплики игры — RU / EN'
shell.body['class'] = ['document-page', 'dialogues-page']
main = shell.main; main.clear()
main.append(Soup('''<section id="overview"><div class="kicker">BIBLE ↔ ИГРА</div><h1>Реплики · RU / EN</h1><p>Общий источник реализованных игровых реплик и ангара. Будущие главы литературного сценария не считаются переведёнными автоматически.</p><p><a href="assets/dialogues.json" download>Скачать JSON</a> · <a href="docs/dialogues-sync.md">Правила редактирования и синхронизации</a> · <a href="scenario.html">Литературный сценарий →</a></p><p>«EN совпадает со сценарием» — связь с литературным текстом, не отметка приёмки перевода. Игровые адаптации сохраняют отдельный статус. Порядковый номер записи не является временем запуска.</p></section><section id="catalog"><h2>Каталог реплик</h2><div class="dialogue-filters"><label>Поиск<input id="dialogue-query" type="search" placeholder="ID, реплика, персонаж"/></label><label>Миссия<select id="dialogue-mission"><option value="">Все миссии и контексты</option></select></label><label>Персонаж<select id="dialogue-speaker"><option value="">Все персонажи</option></select></label><label>Связь со сценарием<select id="dialogue-relationship"><option value="">Все записи</option><option value="verbatim_en">EN совпадает со сценарием</option><option value="gameplay_adaptation">Игровая адаптация</option></select></label></div><p id="dialogue-status" role="status">Загрузка общего JSON…</p><button type="button" id="dialogue-retry" hidden>Повторить загрузку</button><noscript>Для отображения каталога включите JavaScript или скачайте JSON по ссылке выше.</noscript><div id="dialogue-rows"></div></section>''','html.parser'))
shell.select_one('.side nav').clear()
shell.select_one('.side nav').append(Soup('<a href="#overview">Об источнике</a><a href="#catalog">Каталог RU / EN</a>','html.parser'))
for script in shell.select('script[src]'):
    if script['src'] != 'assets/solar.js': script.decompose()
shell.head.append(shell.new_tag('script',src='assets/dialogues.js',defer=True))
if not shell.select_one('link[href="assets/dialogues.css"]'):shell.head.append(shell.new_tag('link',rel='stylesheet',href='assets/dialogues.css'))
(ROOT/'dialogues.html').write_text(str(shell),encoding='utf8')
(ROOT/'assets/dialogue-bindings.json').write_text(json.dumps({'revision':data['revision'],'bindings':bindings,'ambiguous':ambiguous},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
bound_ids={b['id'] for b in bindings}
unmatched=[e for e in data['entries'] if e['relationship']=='verbatim_en' and e['id'] not in bound_ids]
report=f'# Подключение общего источника реплик\n\nВерсия: `{data["revision"]}`. В каталоге {len(data["entries"])} записей. Связано {len(bindings)} мест на страницах с {len(bound_ids)} постоянными ID. Все поля игры и исходные переводы сохранены.\n\nСвязанные HTML-тексты — генерируемый английский fallback; редактируются только `en`/`ru` в `assets/dialogues.json` с обновлением `revision`. ID и игровая привязка проверяются относительно `assets/dialogue-contract.json`.\n\nИгровые адаптации не заменяют литературные реплики. Будущие главы остаются отдельным сценарием. При одинаковом тексте связь выбирается по миссии и ветке завершения; ID не создаются из изменяемого текста.\n\n## Требуют сверки экспорта\n\n'
for e in unmatched:report+=f'- `{e["id"]}` — {e["speaker"]}: «{e["en"]}». Экспорт помечен verbatim_en, но точной пары в текущем сценарии не найдено. Запись сохранена; насильно привязывать к другой фразе нельзя.\n'
report+='\n`dlg.chapter_transmission.rook.001` содержит имя ANDYGEN вместо обычной реплики. Это вероятный служебный фрагмент экспорта; удаление или изменение полей связи требует миграции игры.\n'
(ROOT/'docs/dialogue-integration-report.md').write_text(report,encoding='utf8')
page=Soup((ROOT/'dialogues.html').read_text(encoding='utf8'),'html.parser')
page.find(id='overview').append(Soup('<p><a href="docs/dialogue-integration-report.md">Покрытие привязок и записи, требующие сверки →</a></p>','html.parser'))
(ROOT/'dialogues.html').write_text(str(page),encoding='utf8')
index_path=ROOT/'assets/search-index.json';index=json.loads(index_path.read_text(encoding='utf8'))
index=[e for e in index if not e['url'].startswith('dialogues.html')]
for e in data['entries']:
    index.append({'title':e['speaker']+' · '+(e['mission'] or e['context']),'page':'Реплики игры RU / EN','url':'dialogues.html#'+e['id'],'text':e['id']+' '+e['en']+' '+e['ru']})
index_path.write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print(f'Dialogues: {len(data["entries"])} entries; {len(bindings)} linked occurrences, {len(set(b["id"] for b in bindings))} IDs; {len(ambiguous)} ambiguous occurrences left unchanged.')
