# Game soundtrack

`assets/music.json` records the six tracks used by the local game on 2026-10-12.
Usage comes from `scripts/audio/menu_music.gd` and `assets/audio/music/README.md`
in the game checkout. Display titles follow the source filenames.

`assets/music/originals/` preserves the user-supplied full tracks from the game's
`build/media-originals-20260929/assets/audio/music/` backup. `assets/music/loops/`
preserves the current shortened mobile files from `assets/audio/music/`.
Neither collection is re-encoded for this site.

Run `python scripts/build.py` to regenerate `music.html`, shared navigation,
translations and search. Edit metadata in `assets/music.json`; add new Russian
copy and its English translation to `assets/site-translations.json` together.
Native audio controls load media on demand. Starting another player pauses the
previous player; links download the corresponding original or loop.
