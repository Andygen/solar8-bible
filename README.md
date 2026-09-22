# SOLAR 8 Project Bible

Public project bible website for SOLAR 8.

Narrative rules and missing asset priorities: `docs/story-rules.md` → `python scripts/build-story-rules.py` → `story-rules.html`. After editorial changes, run `python scripts/refresh-search.py` and `python scripts/verify-narrative.py`. The rules builder requires Python Markdown in addition to BeautifulSoup.

Ship catalogue data: `assets/fleet.json`. Rebuild the fleet page and planet previews with `python scripts/build-fleet.py` (Python + BeautifulSoup 4). See [fleet maintenance](docs/fleet.md) and [scenario maintenance](docs/scenario-reader.md).
