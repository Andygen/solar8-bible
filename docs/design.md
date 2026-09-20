# SOLAR 8 visual refresh

The shared design lives in `assets/solar.css` and `assets/solar.js`. All twelve original pages remain static and work on GitHub Pages. Original story, mission and art-brief copy is preserved; only the homepage introduction and navigation/footer presentation changed.

## Art direction

Graphite archive surfaces, restrained solar amber, off-white typography, locally hosted Manrope, technical labels, and large editorial environment studies. Generated environment paintings are mood studies, not approved changes to ship or character canon.

- `assets/helios-orbit.webp`: new cinematic cover, generated with built-in imagegen.
- `assets/worlds/*.webp`: eight tiles from one generated world moodboard, optimized for the website.
- `assets/portraits/*`: existing approved images extracted losslessly from original HTML data URIs; identical images deduplicated.
- `assets/solar-logo.svg` and `assets/solar-mark.svg`: new website wordmark adaptation using the solar orbit, spacecraft and eight motifs. These are newly drawn site assets, not recovered original logo files.

## Generation prompts

### Cover

Use case: stylized-concept. Create a premium cinematic hard-science-fiction website hero background for SOLAR 8, a story about an infected solar-system infrastructure. Ultra-wide landscape 2560x1440. Astonishing physically grounded orbital vista above Mercury: a massive cratered planet curving through the bottom right, bright white-gold sun crest at the upper right edge, a monumental dark industrial solar harvesting station ring curving diagonally in the distance, tiny cold cyan technical lights. One small graphite and pale titanium delta-wing interceptor with blue engines in the right-center foreground, travelling toward the station. Huge scale, quiet tension, sophisticated film production matte painting, fine atmospheric depth, precise plausible industrial detailing, restrained bloom, warm amber sunlight against desaturated ink blue shadows. The LEFT 48 percent must be very dark almost black open space with only sparse stars, clean negative space for website typography. Main focal art concentrated in right 55 percent. No text, letters, logo, UI, watermark, humans, fireballs, colorful nebula, or busy particle noise. This is environment mood artwork, not a new canonical ship design.

### World moodboard

Create one cohesive concept-art atlas / visual moodboard for the 8 worlds of SOLAR 8. Exactly FOUR equal columns and TWO equal rows, eight edge-to-edge panels, NO gaps, NO borders, NO typography or labels. Overall image 3072x2048 landscape; every tile 768x1024 portrait. Carefully ordered top row left-to-right: 1 Mercury: cratered brown planet horizon, giant blazing sun and industrial solar arrays, burnished gold light. 2 Venus: towering orbital cloud station half submerged in dense acid-gold atmospheric clouds, mysterious amber fog. 3 Earth: blue living Earth with white clouds curving behind human orbital-defense station, brilliant restrained cyan. 4 Mars: rusty red desert canyon with giant functional industrial foundry towers and dust haze. Bottom row left-to-right: 5 Jupiter: tremendous ochre banded gas giant beyond a tiny industrial platform amid pale electric storm light, enormous scale. 6 Saturn: pale gold Saturn and immense elegant rings cutting diagonally through midnight space with distant archival station. 7 Uranus: pale teal ice giant behind geometrically severe silent dark alien craft, ice crystals and lonely cold atmosphere. 8 Neptune: deep ultramarine planet behind a mysterious enormous black angular integration structure with subtle violet light, alien first contact, clean geometry. Film production matte painting, premium realistic hard-surface sci-fi, awe and quiet tension, believable physical lighting, refined cinematic color grading, detailed materials, NO colorful nebulae or fantasy landscapes. Each tile has ONE composition and reads beautifully as a tall cinematic world card with its primary subject in the upper two thirds and calm darker lower third. No characters, logos, text, watermark, interface, extra panels. All images share graphite shadows, carefully controlled practical lights, and a mature AAA art direction. This is a single world moodboard asset, not a diagram.

The generated moodboard was delivered at 1536×1024. Its eight tiles are 384×512. The cover was delivered at 1672×941. The website retains these native dimensions without artificial upscaling; framing is used for wide screens.

## Validation

- The original eleven pages checked in Chromium at 390, 768 and 1440 pixel widths.
- No JavaScript errors, missing assets or horizontal page overflow. Wide tables scroll within their own region.
- Mobile menu, search results, Escape dismissal and image lightbox exercised.
- Local links and fragment destinations checked against all HTML pages.
- Original paragraphs, headings, dialogue text and art prompts compared with the previous revision; narrative copy preserved.

- The concurrently added Admiral Vale page and roster update were preserved and styled, then checked at desktop and mobile sizes.

## Maintenance

When adding or editing content, update `assets/search-index.json` with the corresponding title, page, relative URL and text excerpt. The browser uses this local index and does not send search queries to a third party.
