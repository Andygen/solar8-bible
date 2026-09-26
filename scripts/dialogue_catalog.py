"""Validate the public game/Bible contract without changing persistent IDs."""
from pathlib import Path
import json, re, hashlib

ROOT = Path(__file__).resolve().parents[1]
LOCKED = ('speaker', 'mission', 'context', 'trigger', 'order', 'legacy_text')

def placeholders(value):
    return re.findall(r'%(?:[-+0 #]*\d*(?:\.\d+)?)[sdif]', value.replace('%%', ''))

def load_catalog(root=ROOT):
    data = json.loads((root/'assets/dialogues.json').read_text(encoding='utf8'))
    contract = json.loads((root/'assets/dialogue-contract.json').read_text(encoding='utf8'))
    assert data['schema_version'] == contract['schema_version'] == 1
    assert isinstance(data['revision'], str) and data['revision'].strip()
    entries = data['entries']; ids = [e['id'] for e in entries]
    assert len(ids) == len(set(ids)), 'Duplicate dialogue ID'
    by_id = {e['id']: e for e in entries}
    if data['revision'] == contract.get('baseline_revision'):
        digest = hashlib.sha256(json.dumps([[e['id'],e['en'],e['ru']] for e in entries],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        assert digest == contract['baseline_translation_hash'], 'Change revision when editing dialogue text'
    for e in entries:
        assert re.fullmatch(r'dlg\.[a-z0-9_.-]+', e['id']), e['id']
        assert e['speaker'] in contract['speakers'], e['id']
        assert e['speaker'] in data['speakers'], e['id']
        for lang in ['en', 'ru']:
            assert isinstance(e[lang], str) and e[lang].strip(), (e['id'], lang)
        assert placeholders(e['en']) == placeholders(e['ru']), (e['id'], 'format parameters')
        assert placeholders(e['en']) == placeholders(e['legacy_text']), (e['id'], 'game format parameters')
        assert e['relationship'] in ['verbatim_en', 'gameplay_adaptation'], e['id']
        assert e['bible'].startswith('https://andygen.github.io/solar8-bible/'), e['id']
    for old in contract['entries']:
        assert old['id'] in by_id, ('Removed game ID', old['id'])
        for key in LOCKED:
            assert old[key] == by_id[old['id']][key], ('Migration required', old['id'], key)
    return data

if __name__ == '__main__':
    data = load_catalog()
    print(f'Dialogue contract PASS: {len(data["entries"])} entries, revision {data["revision"]}')
