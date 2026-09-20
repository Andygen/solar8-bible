# Scenario reading edition

`scenario.html` gathers the existing story in campaign order. It does not invent new dialogue or translate the existing English VO.

Sources:
- `index.html`: overall plot, chapter introductions, 40 mission summaries, interludes tagged `AFTER n-n`, and Solar Crown gameplay.
- Four `scripts-*.html` pages: full dialogue scene sequences for each numbered mission; the final Solar Crown scene comes from `scripts-uranus-neptune.html`.

Rebuild with `python scripts/build-scenario.py` (Python and BeautifulSoup 4). It regenerates the reading edition and its search entries, and ensures the Scenario menu exists on every HTML page. Source pages retain their original IDs and remain available through each mission's source link.

The reader has native anchor navigation, eight expandable chapter trees with five missions each, previous/next links, keyboard-accessible disclosure controls, mobile contents, and optional local browser reading-position storage. Content remains readable when JavaScript or storage is disabled.

Verification on initial publication: all 40 mission dialogue sequences and the epilogue exactly match their source text after removing VO priority badges; 156 scenes / 454 dialogue lines; no missing source links; desktop and mobile navigation, search, resume and overflow checks pass.
