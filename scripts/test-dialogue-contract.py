"""Meaningful negative cases for the published game interface."""
from pathlib import Path
import copy,json,sys,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from dialogue_catalog import ROOT,load_catalog

original=load_catalog()
cases={
 'deleted ID':lambda d:d['entries'].pop(0),
 'duplicate ID':lambda d:d['entries'].append(copy.deepcopy(d['entries'][0])),
 'unknown speaker':lambda d:d['entries'][0].update(speaker='UNKNOWN'),
 'empty translation':lambda d:d['entries'][0].update(ru=' '),
 'changed mission':lambda d:d['entries'][0].update(mission='neptune_8_5'),
 'changed legacy alias':lambda d:d['entries'][0].update(legacy_text='replacement'),
 'incompatible placeholder':lambda d:d['entries'][0].update(ru='Wrong %s'),
 'text edit without revision':lambda d:d['entries'][0].update(ru='Другой текст'),
}
with tempfile.TemporaryDirectory() as folder:
    root=Path(folder);(root/'assets').mkdir()
    (root/'assets/dialogue-contract.json').write_bytes((ROOT/'assets/dialogue-contract.json').read_bytes())
    for label,mutate in cases.items():
        data=copy.deepcopy(original)
        if label != 'text edit without revision': data['revision']='negative-test'
        mutate(data)
        (root/'assets/dialogues.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
        try:load_catalog(root)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('Accepted invalid catalog: '+label)
    data=copy.deepcopy(original);data['revision']='test-translation-update';data['entries'][0]['ru']='Проверенный новый перевод.'
    (root/'assets/dialogues.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
    load_catalog(root)
print('Dialogue contract: rejected 8 invalid catalogs; accepted a translation edit.')
