# Scenario reading edition

`scenario.html` gathers the existing story in campaign order. It does not invent new dialogue or translate the existing English VO.

Sources:
- `index.html`: overall plot, chapter introductions, 40 mission summaries, interludes tagged `BEFORE n-n` or `AFTER n-n`, and Solar Crown gameplay. BEFORE scenes are placed before gameplay dialogue and included in search.
- Four `scripts-*.html` pages: full dialogue scene sequences for each numbered mission; the final Solar Crown scene comes from `scripts-uranus-neptune.html`.

Rebuild with `python scripts/build-scenario.py` (Python and BeautifulSoup 4). It regenerates the reading edition and its search entries, and ensures the Scenario menu exists on every HTML page. Source pages retain their original IDs and remain available through each mission's source link.

The reader has native anchor navigation, eight expandable chapter trees with five missions each, previous/next links, keyboard-accessible disclosure controls, mobile contents, and optional local browser reading-position storage. Content remains readable when JavaScript or storage is disabled.

Verification on initial publication: all 40 mission dialogue sequences and the epilogue exactly match their source text after removing VO priority badges; 156 scenes / 454 dialogue lines; no missing source links; desktop and mobile navigation, search, resume and overflow checks pass.

Revision 2026-09-22: source VO was intentionally edited to resolve the narrative audit. The reader now contains 170 source scenes / 514 dialogue lines, plus the separate proposed upgrade exchanges. Conditional scene notes are part of the source and must remain in the reader. `scripts/verify-narrative.py` checks source parity, BEFORE/AFTER placement, links and core continuity.

Editorial reference: `docs/story-rules.md` → `scripts/build-story-rules.py` → `story-rules.html`. Build after the content generators. Run `scripts/refresh-search.py` last to refresh existing records after direct source edits. These tools require BeautifulSoup; the rules builder also uses Python Markdown. New scenes are VO drafts, not claims of game implementation.
