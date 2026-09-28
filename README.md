# SOLAR 8 Project Bible

Public project bible website for SOLAR 8.

Full build and publication checks: `python -m pip install -r requirements.txt`, then
`python scripts/build.py` and `python scripts/test-dialogue-contract.py`.
The Pages workflow runs these checks before deployment. Generated HTML and JSON
must be committed after rebuilding; production PNGs remain unchanged.

Game dialogue master: `assets/dialogues.json` → `dialogues.html` and existing
`data-dialogue-id` nodes. Edit `en`/`ru` in JSON and update `revision`; do not edit
bound HTML fallbacks or immutable game fields. See `docs/dialogues-sync.md` and
`docs/dialogue-integration-report.md`. The bilingual page uses `textContent` from
JSON; untranslated future literary chapters remain separate. `dialogue-contract.json`
protects IDs, speakers, mission/context/trigger/order and legacy aliases.

Dated gameplay facts: `assets/production-status.json`. `build-status.py` publishes
`resource-status.html` / `assets/resource-status.json` and updates the corresponding
story-rule rows and ROOK tuning. This does not declare PNGs integrated into a game.

`build-previews.py` creates derived WebP sizes for page display; `data-full-src`,
zoom links and downloads retain original PNGs. Do not edit files under previews
manually. The image manifest records their source fingerprints.

Narrative rules and missing asset priorities: `docs/story-rules.md` → `python scripts/build-story-rules.py` → `story-rules.html`. After editorial changes, run `python scripts/refresh-search.py` and `python scripts/verify-narrative.py`. The rules builder requires Python Markdown in addition to BeautifulSoup.

Ship catalogue data: `assets/fleet.json`. Rebuild the fleet page and planet previews with `python scripts/build-fleet.py` (Python + BeautifulSoup 4). See [fleet maintenance](docs/fleet.md) and [scenario maintenance](docs/scenario-reader.md).

Unified story reader: `assets/story-scenes.json` → `scenario.html`, with game strings resolved by ID from `assets/dialogues.json`. Old `scripts-*.html` URLs redirect to the exact chapter/mission. See `docs/scenario-reader.md` for editorial translations and source ownership.
