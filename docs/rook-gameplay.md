# ROOK gameplay clarification — 2026-09-21

Applied the user's supplied editorial brief to the Bible. Implementation status for Mercury/Venus comes from that brief; this repository contains the documentation website, not the game implementation.

- `character-rook.html#flight-role`: physical companion, player-selected interactions, scanner limitations, air-gapped operation and ordinary-mission survivability. Corrected the old claim that external operations begin on Earth.
- `index.html`: ROOK actions and status for missions 1-1 through 2-5. Existing routes, counts and summaries retained. Mission 1-3 stars now match the supplied requirements: no discharge damage; no hull damage throughout the mission.
- `index.html#rook-gameplay`: future chapter guidance, explicitly unimplemented defensive-laser proposal, tuning and HUD/art requirements.
- `scripts-mercury-venus.html`: gameplay cues and three supplied technical lines. Existing dialogue preserved in order.
- `scenario.html`: rebuilt from sources with `scripts/build-scenario.py`; 40 missions, 159 scenes, 457 dialogue lines, five interludes. Search entries updated.

Validation: existing dialogue preserved; source and reader dialogue match; original mission-summary paragraphs retained; no duplicate HTML IDs or missing local link/search destinations.

Rebuilding requires Python and BeautifulSoup 4. An isolated temporary Python runtime was used for this update; no system Python installation or repository runtime dependency was added.
