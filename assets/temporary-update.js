(() => {
  const dialog = document.createElement('dialog');
  dialog.setAttribute('aria-labelledby', 'reload-reminder-title');
  dialog.style.cssText = 'width:min(520px,calc(100vw - 40px));box-sizing:border-box;padding:28px;border:1px solid #eab47b88;border-radius:12px;background:#12161d;color:#f1f3f6;font:16px/1.6 system-ui;box-shadow:0 24px 100px #000b';
  dialog.innerHTML = '<h2 id="reload-reminder-title" style="margin:0 0 16px;font-size:23px">Как вернуть чат в VS Code</h2><p>В окне VS Code нажми <b>Ctrl + Shift + P</b>.</p><p>Введи команду:</p><p style="padding:12px;background:#070b11;border-radius:6px;font-size:19px"><code>Developer: Reload Window</code></p><p>Нажми <b>Enter</b>. Окно перезагрузится. В прошлый раз это восстановило историю чата.</p><p>Новый чат создавать не нужно.</p><form method="dialog"><button style="padding:10px 20px;border:0;border-radius:6px;background:#eab47b;color:#12161d;font:inherit;cursor:pointer">Понятно</button></form>';
  document.body.append(dialog);
  dialog.showModal();
})();
