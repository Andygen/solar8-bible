"""Canonical literary scenes; game-bound text is resolved only by persistent ID."""
from pathlib import Path
from html import escape as esc
import json
ROOT=Path(__file__).resolve().parents[1]
STORY=json.loads((ROOT/'assets/story-scenes.json').read_text(encoding='utf8'))
GAME={e['id']:e for e in json.loads((ROOT/'assets/dialogues.json').read_text(encoding='utf8'))['entries']}

def render_scenes(mission):
    html=''
    for scene in mission['scenes']:
        html+='<div class="scene" data-scene-id="'+scene['id']+'">'
        for block in scene['blocks']:
            if block['type']=='markup':html+=block['html'];continue
            line=block['line'];game=GAME.get(line.get('dialogue_id'));text=game or line
            attrs=f' data-story-id="{line["id"]}" data-ru="{esc(text["ru"],quote=True)}" data-en="{esc(text["en"],quote=True)}"'
            if game:attrs+=f' data-dialogue-id="{game["id"]}" data-dialogue-source="assets/dialogues.json"'
            html+=f'<div class="line"><div class="speaker">{esc(line["speaker"])}</div><div class="text" lang="en"{attrs}>{esc(text["en"])}</div></div>'
        html+='</div>'
    return html
