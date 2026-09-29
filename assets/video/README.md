# Hero phone video

Source: user-supplied `dreamina-2026-09-28-7678-Create a 5-second seamless cinematic loo....mp4` (Downloads).
The original is retained at its source location.

`solar8-phone-seamless.mp4`: H.264, 540×960, 24 fps, yuv420p, CRF 22,
faststart, audio removed for silent inline autoplay. A 0.5-second crossfade blends
the final half-second into the opening half-second. Playback starts at source 0.5s,
so the end of the blend flows directly into the next cycle (4.5s, 108 frames).
Original composition and marks are preserved; no cropping or black fades.
`solar8-phone-seamless-poster.jpg` matches the first frame. The previous loop/poster
files remain available for cached versions of the home page.

The bronze device is HTML/CSS in the home hero, styled by `hero-phone.css`.
`hero-phone.js` loops the video, pauses off-screen/in background tabs, and respects
reduced motion. The small overlay button toggles playback. The video fills the display
with a uniform thin bezel, without top/bottom letterboxing. On narrower screens the
device follows the hero copy rather than overlapping it.
