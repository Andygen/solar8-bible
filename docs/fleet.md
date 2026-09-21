# Fleet catalogue

`assets/fleet.json` is the single source for ship names, images, descriptions, roles, technical codes, mission/phase labels and archive status. Planet order and introductory text also live here.

Run `python scripts/build-fleet.py` with BeautifulSoup 4 installed after editing this data. The builder regenerates:

- `fleet.html`, with the player ship, planet categories, larger boss cards and collapsed concept archive;
- compact linked previews in the corresponding `index.html` planet chapters;
- the homepage fleet entry and legacy ship-anchor redirects;
- fleet entries in `assets/search-index.json`;
- shared desktop/mobile navigation and links from existing art briefs.

All catalogue content is static HTML and remains readable without JavaScript. Shared `solar.js` supplies image enlargement, search, archive opening for direct card links, and redirects from old homepage ship anchors. Full PNG downloads remain ordinary links.

Presentation lives in `assets/fleet.css`. The chapter previews use divs rather than narrative article cards, so `scripts/build-scenario.py` does not copy fleet previews into the reading edition. When changing both story sources and the fleet, run the scenario builder followed by the fleet builder.

To add a ship, copy its original PNG to `assets/ships`, add an entry to `fleet.json`, and rebuild. Set `kind` to `boss` for the wide boss layout; set `phase` when the supplied artwork depicts only one phase. Add a planet to `planets` when its first assets are ready. Retain `legacyIds` to preserve published links.

Boss `variants` hold additional phase images (name, description, image, width, height). These appear inside the same boss card with independent enlargement and download links, and are included in its search text. The primary image remains the chapter thumbnail. `object`, `formation`, `control` and `alien` kinds distinguish scanning targets and alien units from conventional ships.

Jupiter, Uranus and Neptune were imported from the three user-supplied ZIP archives. All 16 PNGs are retained unchanged. Shard, Lattice and Assimilator repeat the same source artwork in Uranus and Neptune; catalogue placement does not assign them to specific mission waves. Tempest Crown and Null Vessel show phase 1 only. Integration Ark has phase 1 plus phase 2 and Command Seed (phase 3) variants; these static images are not an animation-ready sequence. No Saturn assets were supplied in this batch.
