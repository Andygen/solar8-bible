"""One deterministic production pipeline. Run: python scripts/build.py"""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/version-assets.py'),'--normalize'],cwd=ROOT,check=True)
for script in ['build-dossiers.py','build-upgrades.py','build-status.py','build-story-rules.py',
               'build-fleet.py','build-dialogues.py','build-scenario.py','build-dialogues.py',
               'build-story-presentation.py','build-dialogues.py','navigation.py','build-previews.py','refresh-search.py','version-assets.py','verify-narrative.py','verify-site.py','verify-story.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
