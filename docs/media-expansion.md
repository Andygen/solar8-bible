# Character and upgrade media

The nine September 2026 archives contributed 56 original PNGs. `assets/media-imports.json` maps each source file to its unchanged original and display preview. Character and upgrade previews are WebP; download links and the shared image dialog open the original PNG. Source notes are retained in `docs/art-imports/` as reference material.

Build with Python, BeautifulSoup 4 and Python-Markdown installed:

```sh
python scripts/build-dossiers.py
python scripts/build-upgrades.py
python scripts/build-fleet.py
```

`assets/dossiers.json` supplies the six character dossiers, roster links and existing campaign quotes. Appearance text comes from the corresponding art briefs. ROOK Mk II extends his existing dossier; his restored personality and missing recent memories remain unchanged.

`player-upgrades.html` is generated from the v9 source Markdown. Mechanics, numerical bonuses and proposed hangar dialogue remain proposals on this separate page. The campaign scripts and current player-ship image are not replaced.

Solar Crown is an extra fleet category in `assets/fleet.json`. Three artwork stages do not establish a three-phase encounter. The clean alien seed is auxiliary artwork, not another phase or a confirmed identity link to the Emissary's escaped seed.

Rebuild the fleet last to refresh shared navigation and chapter previews. Generated pages are committed for static GitHub Pages hosting.
