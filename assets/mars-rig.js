/* The published rig uses original-image pivots with scaled game textures. */
(() => {
  'use strict';
  const canvas = document.getElementById('mars-rig-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const load = document.getElementById('mars-rig-load');
  const phase = document.getElementById('mars-rig-phase');
  const play = document.getElementById('mars-rig-play');
  const time = document.getElementById('mars-rig-time');
  const status = document.getElementById('mars-rig-status');
  const base = 'assets/mars-2026-09-29/';
  let rig, playing = false, visible = true, frame = 0, previous = 0, t = 0;
  const label = (node, text) => { node.textContent = window.SOLAR_I18N?.t(text) || text; };
  function draw() {
    if (!rig || !ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();ctx.translate(0, -150);
    rig.draw(ctx, { phase: phase.selectedIndex + 1, opening: Number(phase.value), t });
    ctx.restore();
  }
  function tick(now) {
    frame = 0;
    if (!playing || !visible || document.hidden) return;
    if (previous) t += Math.min((now - previous) / 1000, .1) / 8;
    previous = now; time.value = Math.round((t % 1) * 1000);
    draw();frame = requestAnimationFrame(tick);
  }
  function schedule() {
    cancelAnimationFrame(frame);frame = 0;previous = 0;
    if (playing && visible && !document.hidden) frame = requestAnimationFrame(tick);
  }
  function setPlaying(value) {
    playing = value;
    label(play, value ? 'Пауза' : 'Показать движение');
    play.setAttribute('aria-pressed', String(value));schedule();
  }
  load.addEventListener('click', async () => {
    load.disabled = true;label(status, 'Модель загружается…');
    try {
      const response = await fetch(base + 'assembler-animation-v1/manifest.json');
      if (!response.ok) throw new Error('Manifest unavailable');
      const manifest = await response.json();
      const images = Object.fromEntries(await Promise.all(manifest.assets.map(async part => {
        const image = new Image();
        image.src = base + 'art/runtime/mars/assembler/assembler-' + part.id + '.png';
        await image.decode();
        [image.sourceWidth, image.sourceHeight] = part.size;
        return [part.id, image];
      })));
      rig = makeAssemblerRig(images);draw();
      phase.disabled = play.disabled = time.disabled = false;
      load.hidden = true;label(status, 'Модель готова');
    } catch (error) {
      load.disabled = false;
      label(status, 'Не удалось загрузить модель. Повторите попытку.');
    }
  });
  play.addEventListener('click', () => setPlaying(!playing));
  phase.addEventListener('change', draw);
  time.addEventListener('input', () => { setPlaying(false);t = Number(time.value) / 1000;draw(); });
  document.addEventListener('visibilitychange', schedule);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting;schedule(); }).observe(canvas);
  // No autoplay: even reduced-motion users can explicitly inspect movement.
})();
