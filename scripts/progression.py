"""Shared documentation data and draft hangar scene rendering."""
from pathlib import Path
from html import escape as esc
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'assets/player-progression.json').read_text(encoding='utf-8'))
STAGES = DATA['stages']

def paragraphs(items):
    return ''.join('<p>'+esc(t)+'</p>' for t in items)

def scene(stage, location='scenario'):
    slug = stage['id']
    chapter = ['mercury','venus','earth','mars','jupiter','saturn','uranus','neptune'][int(stage['after'][0])-1]
    links = f'<a href="player-upgrades.html#stage-{slug}">Оборудование и ангарный вид ↗</a>'
    if location == 'upgrades':
        links = f'<a href="scenario.html#upgrade-{slug}">Место сцены в сценарии ↗</a>'
    if location != 'source':
        links += f' · <a href="{stage["script"]}#upgrade-{slug}">Исходный VO ↗</a>'
    vo = ''.join(f'<div class="line"><div class="speaker">{esc(l["speaker"])}</div><div class="text" lang="en">{esc(l["text"])}</div></div>' for l in stage['dialogue'])
    ru = ''.join(f'<p><b>{esc(l["speaker"])}</b>: {esc(l["text"])}</p>' for l in stage['translation'])
    return f'''<aside class="upgrade-interlude" id="upgrade-{slug}" data-chapter="{chapter}"><div class="kicker">АНГАР / ПРЕДЛАГАЕМАЯ СЦЕНА</div><h3>{esc(stage['title'])}</h3><p class="upgrade-label">VO-черновик · игровые эффекты предложены к реализации · числовые бонусы не определены.</p><p>{esc(stage['when'])}. Акцент на новом оборудовании; предполагаемая длительность 12–18 секунд, сцену можно пропустить.</p><div class="upgrade-dialogue">{vo}</div><details class="upgrade-translation"><summary>Русский смысл реплик</summary>{ru}</details>{paragraphs(stage['notes'])}<p>{links}</p></aside>'''
