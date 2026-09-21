# Character and upgrade media

The nine September 2026 archives contributed 56 original PNGs. `assets/media-imports.json` maps each source file to its unchanged original and display preview. Character and upgrade previews are WebP; download links and the shared image dialog open the original PNG. Source notes are retained in `docs/art-imports/` as reference material.

Build with Python and BeautifulSoup 4 installed:

```sh
python scripts/build-dossiers.py
python scripts/build-upgrades.py
python scripts/build-scenario.py
python scripts/build-fleet.py
```

`assets/dossiers.json` supplies the six character dossiers, roster links and existing campaign quotes. Appearance text comes from the corresponding art briefs. ROOK Mk II extends his existing dossier; his restored personality and missing recent memories remain unchanged.

`player-upgrades.html` is generated from `assets/player-progression.json`, transcribed from the owner's later request in `docs/player-progression-request.txt`. The visual progression, wear and Max's presentations are owner-defined; gameplay effects and VO remain proposals with no numerical bonuses assigned. The eight transitions are also inserted into the four VO source pages and the reading edition as labelled draft asides, preserving original scenes. Solar Crown's presentation is in the post-credits epilogue; the Neptune shield presentation is before 8-1, with the backup revelation still after 8-1.

The nine hangar PNGs in `assets/ships/upgrades/hangar/` were copied unchanged from the game project's `assets/art/hangar/ship.png` (Mercury) and `assets/art/hangar/ships/` (eight later stages). Source paths, sizes and SHA-256 hashes are recorded in the progression JSON. All nine were visually checked against equipment progression. No artwork was generated or altered. Flight v9 PNGs remain separate labelled downloads. The original player fleet image remains in place.

Solar Crown is an extra fleet category in `assets/fleet.json`. Three artwork stages do not establish a three-phase encounter. The clean alien seed is auxiliary artwork, not another phase or a confirmed identity link to the Emissary's escaped seed.

Rebuild the fleet last to refresh shared navigation and chapter previews. Generated pages are committed for static GitHub Pages hosting.
