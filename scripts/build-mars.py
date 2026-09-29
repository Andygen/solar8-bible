"""Publish the dated Mars handoff, retaining art approval and balance distinctions."""
from pathlib import Path
from html import escape as esc
import json
from bs4 import BeautifulSoup as Soup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK='assets/mars-2026-09-29/'
catalog_path=ROOT/'assets/site-translations.json'
catalog=json.loads(catalog_path.read_text(encoding='utf8'))
def tr(ru,en):
    catalog['strings'][ru]={'ru':ru,'en':en}
    return esc(ru)
def link(url,ru,en):return f'<a href="{esc(url)}">{tr(ru,en)}</a>'
def para(ru,en):return '<p>'+tr(ru,en)+'</p>'
def heading(ru,en):return '<h2>'+tr(ru,en)+'</h2>'
missions=[
 ('4-1','Red Line','Красная линия',
  ('Пройти транспортный пояс: четыре платформы, четыре механические руки и девять волн Mars Scout / Striker / Guard. Предупреждение длится 3 секунды, движение — 6; безопасный маршрут остаётся доступен.',
   'Cross the transport belt: four platforms, four mechanical arms and nine waves of Mars Scout / Striker / Guard. Warnings last 3 seconds and movement 6; a safe route remains available.'),
  ('Победа после прохода всех восьми механизмов, завершения очереди волн и зачистки. Один механизм учитывает столкновение только один раз. Щит или неуязвимость сохраняют корпус, но не отменяют контакт; урон от врагов учитывается отдельно.',
   'Win after all eight machines pass, the wave queue ends and enemies are cleared. Each machine counts contact only once. Shields or invulnerability preserve hull HP but do not erase contact; enemy damage is tracked separately.'),
  [('Пройти пояс','Cross the belt'),('Ни одного контакта с механизмами','No machinery contact'),('Без урона корпусу от механизмов','No hull damage from machinery')],
  ('Производство работает на 310%; неизвестные приказы ведут к фабрике 4-2. Живая сборка и восстановление врагов здесь ещё не вводятся.',
   'Production runs at 310%; unknown orders lead to factory 4-2. Live enemy assembly and revival are not introduced here.'),
  [('industrial-arm','Industrial arm'),('mag-rail-loader','Mag-rail loader')],['red-line-loader','red-line-arm']),
 ('4-2','Factory Without Shift','Фабрика без смены',
  ('Уничтожить три стапеля и зачистить сектор. Стапели собирают врагов на экране; Mars Repair Unit может вернуть тяжёлую машину в бой. Уничтожение ремонтного аппарата прерывает восстановление.',
   'Destroy three assembly cradles and clear the sector. Cradles build enemies on screen; Mars Repair Unit can revive a heavy craft. Destroying the repair unit interrupts restoration.'),
  ('Текущая настройка: стапель — 24 HP, цикл сборки — 10 секунд, до семи защитников. Обломок существует 12 секунд, ремонт занимает 6 секунд после прибытия. Каждая тяжёлая машина возрождается один раз и не даёт повторных очков.',
   'Current tuning: 24 HP per cradle, a 10-second assembly cycle, up to seven defenders. Wrecks last 12 seconds; repair takes 6 seconds after arrival. Each heavy craft revives once without duplicate score.'),
  [('Остановить стапели и зачистить сектор','Stop production and clear the sector'),('Ни одного восстановления врага','Prevent every enemy revival'),('Без урона корпусу','No hull damage')],
  ('Макс и Лена находят незнакомые компоненты. После финала открывается реализованная миссия 4-3; раскрытие NOVA остаётся там.',
   'Max and Lena discover unfamiliar components. The ending leads to implemented mission 4-3, where NOVA is revealed.'),
  [('assembly-cradle','Assembly cradle'),('factory-floor','Factory floor')],['factory-repair-warning']),
 ('4-3','NOVA','NOVA',
  ('Защитить три узла памяти, пока ROOK читает NOVA через изолированный сервисный интерфейс. У интерфейса нет доступа к управлению кораблём. Огонь игрока не повреждает узлы; потеря любого узла означает поражение.',
   'Protect three memory nodes while ROOK reads NOVA through an isolated service interface with no access to flight controls. Player fire cannot damage nodes; losing any node fails the mission.'),
  ('Текущая настройка: 10 HP на узел, вступление 24 секунды, 60 секунд активного чтения, пауза 4 секунды каждые 22 секунды. Девять пар атакующих с интервалом 8 секунд. Для завершения ROOK должен вернуться, а оставшиеся враги — быть уничтожены.',
   'Current tuning: 10 HP per node, a 24-second introduction, 60 seconds of active reading, 4-second interruptions every 22 seconds. Nine attacker pairs arrive 8 seconds apart. Completion requires ROOK to return and surviving attackers to be cleared.'),
  [('Сохранить изолированный фрагмент','Preserve the isolated fragment'),('Ни одного повреждения узлов','No node damage'),('Без урона корпусу','No hull damage')],
  ('Макс сохраняет небольшой чистый фрагмент личности. NOVA не исцелена целиком; фрагмент остаётся в отдельном хранилище. Следующая миссия — 4-4.',
   'Max preserves a small clean personality fragment. NOVA is not fully cured; the fragment remains in separate storage. Next mission: 4-4.'),
  [('nova-dialogue','NOVA dialogue avatar'),('nova-memory-node','NOVA memory node'),('nova-server','NOVA server corridor')],['nova-defense']),
 ('4-4','Foreign Template','Чужой шаблон',
  ('Последовательно просканировать три образца A → B → C и сохранить все до конца. ROOK физически перемещается между ними и читает только в рабочей зоне. Огонь игрока безопасен для образцов; враг может уничтожить даже уже просканированный образец и вызвать поражение.',
   'Scan three samples sequentially, A → B → C, and preserve all until completion. ROOK physically travels between them and reads only in range. Player fire is harmless to samples; enemies can destroy even a scanned sample and cause failure.'),
  ('Текущая настройка: 10 HP на образец, вступление 12 секунд, по 22 секунды активного сканирования. Волна каждые 10 секунд: один, затем два и три противника. После третьего скана новые волны прекращаются; победа ждёт стыковки ROOK и зачистки.',
   'Current tuning: 10 HP per sample, a 12-second introduction and 22 seconds of active scanning each. Waves every 10 seconds grow from one to two to three enemies. After scan three, new waves stop; victory waits for ROOK to dock and enemies to be cleared.'),
  [('Просканировать и сохранить все образцы','Scan and preserve all samples'),('Ни одного повреждения образцов','No sample damage'),('Без урона корпусу','No hull damage')],
  ('Получен первый полный блок чужого кода. Вейл ограничивает доступ; глава продолжается боем с Assembler Prime в 4-5.',
   'The first complete block of alien code is obtained. Vale restricts access; the chapter continues with Assembler Prime in 4-5.'),
  [('foreign-module','Foreign module'),('foreign-sample','Foreign sample')],['template-scan']),
 ('4-5','Assembler Prime','Мегасборщик',
  ('Три фазы: уничтожение четырёх инструментов и дронов; отключение двух ремонтных модулей; сканирование и уничтожение чужого ядра. Разрушенный инструмент останавливается и отменяет подготовленный удар. Третья фаза недоступна, пока жив хотя бы один ремонтный модуль.',
   'Three phases: destroy four tools and drones; disable two repair modules; scan and destroy the alien core. Destroyed tools stop and cancel pending strikes. Phase three cannot begin while any repair module survives.'),
  ('Текущая настройка: инструменты — по 16 HP, ремонтные модули — по 12 HP, броня — 60 HP, ядро — 42 HP. Модуль возвращает 3 HP брони каждые 2 секунды. В третьей фазе Макс сканирует ядро через сенсорный канал ROOK 5 секунд; до завершения скана ядро защищено от огня.',
   'Current tuning: 16 HP per tool, 12 HP per repair module, 60 armor HP and 42 core HP. Each module restores 3 armor HP every 2 seconds. In phase three Max scans through ROOK’s sensor link for 5 seconds; the core is protected until scanning completes.'),
  [('Просканировать и уничтожить ядро','Scan and destroy the core'),('Не допустить восстановления брони','Prevent all armor regeneration'),('Без урона корпусу','No hull damage')],
  ('Чистый фрагмент SOLAR, обрыв связи и трасса к Юпитеру. Текущая игра возвращает в меню: миссии Jupiter и эффект новых турбин ещё не реализованы. Предлагаемая ангарная сцена не включена автоматически.',
   'A clean SOLAR fragment, interrupted contact and a vector to Jupiter. The current game returns to the menu: Jupiter missions and new turbine effects remain unimplemented. The proposed hangar scene is not automatically enabled.'),
  [('assembly-ring','Assembly ring')],['assembler-phase1','assembler-repair-modules','assembler-phase3','assembler-solar'])
]
runtime={'nova-dialogue':'art/runtime/nova/dialogue.png','industrial-arm':'art/runtime/mars/props/industrial-arm-concept.png','mag-rail-loader':'art/runtime/mars/props/mag-rail-loader-concept.png'}
props={'assembly-cradle','nova-memory-node','foreign-sample'}
resources=[]
visual=tr('Новая графика; визуальная приёмка ожидается','New artwork; visual approval pending')
game=tr('Используется в локальной реализации из пакета 29.09.2026; ручная проверка отдельно','Used in the local implementation supplied on 29 September 2026; manual review separate')
def art(mid,stem,name):
    master=PACK+f'art/masters/{mid}/{stem}.png'
    rt=PACK+runtime.get(stem,'art/runtime/mars/'+('props/' if stem in props else '')+stem+'.png')
    with Image.open(ROOT/master) as im:w,h=im.size
    resources.append(dict(id='mars-2026-09-29--'+stem,entity=name,name=name,planet='Mars',kind='Mission artwork',file=master,width=w,height=h,readiness='Статический референс опубликован',visual=visual,game=game,checked_at='2026-09-29',url='mars-production.html#mission-'+mid))
    return f'<figure><a href="{master}"><img src="{master}" width="{w}" height="{h}" alt="{name}" loading="lazy" decoding="async"/></a><figcaption><b>{name}</b><br/>'+link(master,'Оригинал PNG','Original PNG')+' · '+link(rt,'Версия в игре','Game version')+'</figcaption></figure>'
shell=Soup((ROOT/'story-rules.html').read_text(encoding='utf8'),'html.parser')
title=tr('SOLAR 8 // Mars — реализованная глава','SOLAR 8 // Mars — implemented chapter')
shell.title.string=title;shell.body['class']=['document-page','mars-page'];shell.main.clear()
for node in shell.select('script[src]'):
    if node['src']!='assets/solar.js':node.decompose()
html='<section id="overview"><div class="kicker">MARS / 2026-09-29</div><h1>'+tr('Марс: пять миссий','Mars: five missions')+'</h1>'
html+=para('Глава реализована в локальной игре: 4-1 → 4-2 → 4-3 → 4-4 → 4-5 → меню. Здесь собраны текущие правила, графика и подвижная сборка босса из полного пакета 29.09.2026.','The local game implements the chapter: 4-1 → 4-2 → 4-3 → 4-4 → 4-5 → menu. This page collects current mechanics, artwork and the animated boss rig from the complete 29 September 2026 handoff.')
html+=para('Автоматические проверки заявлены в пакете; мы не запускали игру из этих выдержек. Тестовый пилот 4-2–4-5 был неуязвим: это проверка достижимости победы, а не окончательной сложности. Ручное прохождение и визуальная приёмка ещё нужны. APK всей главы в комплекте нет.','The package reports automated checks; these excerpts were not used to run the game here. The 4-2–4-5 test pilot was invulnerable: this verifies completion, not final difficulty. Human playtesting and visual approval remain required. No full-chapter APK is included.')
html+='<p>'+link('scenario.html#mars','Читать сюжет Mars','Read the Mars story')+' · '+link('fleet.html#mars','Флот Mars','Mars fleet')+' · '+link('#assembler','Посмотреть движение босса','View boss animation')+'</p></section>'
checks=[]
for mid,name,ru_name,summary,rules,stars,outcome,arts,shots in missions:
    html+=f'<section id="mission-{mid}"><div class="kicker">MARS / {mid}</div><h2>{mid} · '+tr(ru_name,name)+'</h2>'+para(*summary)+para(*rules)
    html+='<h3>'+tr('Три звезды в текущей игре','Three stars in the current game')+'</h3><ol>'+''.join('<li>'+tr(*star)+'</li>' for star in stars)+'</ol>'
    html+=para('Звёзды выдаются только при победе. Числа HP, таймеры и дополнительные условия — текущая настройка для согласования, а не утверждённый числовой канон.','Stars require mission success. HP, timers and extra conditions are current tuning proposals, not approved numerical canon.')+para(*outcome)
    html+='<p>'+link('scenario.html#mission-'+mid,'Сцены и реплики →','Scenes and dialogue →')+' · '+link(PACK+'missions/'+mid+'.md','Подробная записка реализации','Full implementation notes')+'</p>'
    html+='<div class="mars-gallery">'+''.join(art(mid,stem,label) for stem,label in arts)+'</div>'
    html+='<details class="mars-captures"><summary>'+tr('Кадры автоматических проверок','Automated-test captures')+'</summary>'+para('Это кадры тестов, не запись обычного прохождения. Таймеры и реплики могли переключаться тестом.','These are test captures, not normal playthrough footage. Timers and dialogue may have been advanced by the test.')+'<div class="mars-gallery">'
    for shot in shots:
        file=PACK+'screenshots/'+shot+'.png'
        with Image.open(ROOT/file) as im:w,h=im.size
        html+=f'<figure><a href="{file}"><img src="{file}" width="{w}" height="{h}" loading="lazy" alt="{name} — {shot}"/></a><figcaption>{name} · {shot}</figcaption></figure>'
    html+='</div></details></section>'
    checks.append(dict(id='mars-'+mid,entity='Mars '+mid+' / '+name,checked_at='2026-09-29',status=tr('Реализовано в локальной игре; по данным переданного пакета','Implemented locally; reported by the supplied package'),description=summary[0]+' '+outcome[0],source=PACK+'missions/'+mid+'.md'))
    tr(summary[0]+' '+outcome[0],summary[1]+' '+outcome[1])
html+='<section id="assembler">'+heading('Assembler Prime: подвижная сборка v1','Assembler Prime: animated rig v1')
html+=para('Десять отдельных деталей, четыре манипулятора, раскрывающиеся захваты и центральный отсек. В пакете от 29.09 подтверждён перенос в Sprite2D для 4-5; более ранний manifest исходной сборки ещё помечен как прототип. Старые цельные фазы сохраняются отдельно.','Ten separate parts, four manipulators, opening grippers and a central bay. The 29 September package reports a Sprite2D port used in 4-5; the earlier source-rig manifest still labels it a prototype. Previous whole-phase images remain separate.')
html+=para('Просмотр показывает геометрию и движение, а не игровые столкновения или баланс. Пивоты считаются в координатах оригинальных PNG; уменьшенные игровые копии рисуются с компенсацией масштаба.','This preview shows geometry and movement, not combat collisions or balance. Pivots use original PNG coordinates; smaller game images are rendered with scale compensation.')
html+='<div class="mars-rig"><canvas id="mars-rig-canvas" width="1100" height="850" aria-label="Assembler Prime"></canvas><p id="mars-rig-status" role="status">'+tr('Модель загружается по кнопке','Load the model using the button')+'</p><div class="mars-rig-controls"><button id="mars-rig-load" type="button">'+tr('Загрузить модель','Load model')+'</button><label>'+tr('Состояние','State')+' <select id="mars-rig-phase" disabled><option value="0">'+tr('Производство','Production')+'</option><option value="35">'+tr('Охлаждение','Cooling')+'</option><option value="98">'+tr('Чужой модуль','Alien module')+'</option></select></label><button id="mars-rig-play" type="button" disabled>'+tr('Показать движение','Play animation')+'</button><label>'+tr('Положение','Position')+' <input id="mars-rig-time" type="range" min="0" max="1000" value="0" disabled/></label></div></div>'
html+='<p>'+link('fleet.html#ship-assembler-prime','Цельные фазы и прежние детали','Whole phases and earlier parts')+' · '+link(PACK+'assembler-animation-v1/demo.html','Исходная демонстрация','Original demo')+' · '+link(PACK+'assembler-animation-v1/rig-data.json','Пивоты JSON','Pivot JSON')+' · '+link(PACK+'assembler-animation-v1/README-RU.md','Документация сборки','Rig documentation')+'</p><div class="mars-parts">'
manifest=json.loads((ROOT/PACK/'assembler-animation-v1/manifest.json').read_text(encoding='utf8'))
html+='<ul class="mars-parts">'
for asset in manifest['assets']:html+='<li>'+link(PACK+'assembler-animation-v1/'+asset['file'],asset['id']+' · PNG',asset['id']+' · PNG')+'</li>'
html+='</ul>'
html+='</div></section><section id="sources">'+heading('Общий источник реплик и исходники','Shared dialogue master and sources')
html+=para('74 реплики Mars: 12 существующих сохранены, 62 добавлены по постоянным ID. 48 новых сюжетных строк связаны со сценарием; 14 новых строк инструктажа остаются игровыми адаптациями. NOVA добавлена в список говорящих.','74 Mars lines: 12 existing records preserved and 62 added by persistent ID. 48 new story lines are linked to the scenario; 14 new briefing lines remain game adaptations. NOVA is now an allowed speaker.')
html+='<p>'+link('dialogues.html','Открыть общий каталог RU / EN','Open the shared RU / EN catalog')+' · '+link('assets/dialogues.json','Актуальный мастер JSON','Current master JSON')+'</p>'
html+=para('Файлы внутри пакета — снимок передачи, а не второй редактируемый каталог. Игра должна получать дальнейшие редакторские изменения из общего assets/dialogues.json.','Files inside the handoff are an archival snapshot, not a second editable catalog. The game should pull future editorial changes from the shared assets/dialogues.json.')
html+='<p>'+link(PACK+'README.md','README пакета','Package README')+' · '+link(PACK+'manifest.json','Манифест ресурсов','Asset manifest')+' · '+link(PACK+'SHA256SUMS.txt','Контрольные суммы','Checksums')+' · '+link(PACK+'dialogues/game-bindings.json','Связи с игровыми файлами','Game-file bindings')+'</p></section>'
shell.main.append(Soup(html,'html.parser'))
nav=shell.select_one('.side nav');nav.clear()
nav.append(Soup(link('#overview','О главе','About the chapter')+''.join(f'<a href="#mission-{m[0]}">{m[0]} · {m[1]}</a>' for m in missions)+link('#assembler','Подвижный Assembler Prime','Animated Assembler Prime')+link('#sources','Источники','Sources'),'html.parser'))
for src in [PACK+'assembler-animation-v1/assembler-rig.js','assets/mars-rig.js']:shell.head.append(shell.new_tag('script',src=src,defer=True))
if not shell.select_one('link[href="assets/mars-production.css"]'):shell.head.append(shell.new_tag('link',rel='stylesheet',href='assets/mars-production.css'))
(ROOT/'mars-production.html').write_text(str(shell),encoding='utf8')
# Add contextual links after the shared page generators have run.
for filename,selector,anchor in [('index.html','#mars','overview'),('fleet.html','#ship-assembler-prime','assembler'),('character-nova.html','main','mission-4-3'),('scenario.html','#mars','overview')]:
    path=ROOT/filename;page=Soup(path.read_text(encoding='utf8'),'html.parser');target=page.select_one(selector)
    assert target is not None,(filename,selector)
    for old in target.select('.mars-handoff-link'):old.decompose()
    note=Soup('<p class="mars-handoff-link">'+link('mars-production.html#'+anchor,'Mars в игре: миссии, графика и сборка босса →','Mars in the game: missions, artwork and boss rig →')+'</p>','html.parser')
    if filename=='character-nova.html':target.append(note)
    elif filename=='index.html':
        badge=target.select_one('.badge')
        if badge:badge.string=tr('В ЛОКАЛЬНОЙ ИГРЕ · 29.09.2026','IN THE LOCAL GAME · 29 SEP 2026')
        target.select_one('.head').insert_after(note)
    else:target.insert(1,note)
    path.write_text(str(page),encoding='utf8')
status_path=ROOT/'assets/production-status.json';status=json.loads(status_path.read_text(encoding='utf8'))
status['revision']='2026-09-29';status['checks']=[c for c in status['checks'] if not c['id'].startswith('mars-')]+checks
status_path.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(ROOT/'assets/mars-resources.json').write_text(json.dumps(resources,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for row in resources:tr(f'{row["width"]} × {row["height"]} · учёт 2026-09-29',f'{row["width"]} × {row["height"]} · recorded 2026-09-29')
for ru,en in [('Модель загружается…','Loading model…'),('Модель готова','Model ready'),('Не удалось загрузить модель. Повторите попытку.','Could not load model. Try again.'),('Пауза','Pause'),('Реализованная глава Mars','Implemented Mars chapter')]:tr(ru,en)
# The inventory date changes independently of each entry's review status.
for key,value in list(catalog['strings'].items()):
    if ' · учёт ' in key:
        new_key=key.split(' · учёт ')[0]+' · учёт 2026-09-29'
        tr(new_key,value['en'].rsplit(' ',1)[0]+' 2026-09-29')
for mid,name,ru_name,*_ in missions:tr(mid+' · '+ru_name,mid+' · '+name)
tr('← Mars','← Mars')
tr('Реализовано в локальной игре; по данным переданного пакета · 2026-09-29','Implemented locally; reported by the supplied package · 2026-09-29')
catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
index_path=ROOT/'assets/search-index.json';index=json.loads(index_path.read_text(encoding='utf8'));index=[e for e in index if not e['url'].startswith('mars-production.html')]
for mid,name,*_ in missions:index.append(dict(title='Mars '+mid+' / '+name,page='Mars',url='mars-production.html#mission-'+mid,text=name))
index.append(dict(title='Assembler Prime / animation v1',page='Mars',url='mars-production.html#assembler',text=''))
index_path.write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print('Mars: five implementation cards, ten masters, nine captures, rig viewer and dated readiness.')
