# Assembler Prime animated rig v1

Source: user-provided solar8-assembler-animation-v1 (1).zip, reviewed under
build/assembler-animation-v1-review/solar8-assembler-animation-v1. Ten transparent
PNGs are resized without cropping to below 500 KB each. Original masters,
manifest, SHA256SUMS, rig-data.json and assembler-rig.js remain in that directory.

scripts/visual/assembler_rig.gd ports the supplied Canvas formulas and layer order
to Sprite2D nodes. Pivot values are in original coordinates: 1254×1254 for all
parts except hatch (887×1774). The renderer compensates for resized dimensions.
Do not replace these images with trimmed sprites without migrating pivots.

The original still-image phases are not overwritten. Four arms use the supplied
shoulder/elbow poses, mirrored gripper fingers, rotating saw and moving drill arm
(not a fake axial drill spin). Hatches slide 0/35/98 original logical pixels;
the press retracts and the core appears in phase three. Destroyed arms stop and
darken. Collision targets and battle logic live separately in assembler_prime.gd
and assembler_target.gd.

Current Bible fleet page was checked 2026-09-29. It still describes the older
whole-phase images and component prototypes. This runtime rig is the separately
provided v1 handoff, not a claim that the website approved an engine build.
