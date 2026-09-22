/* Temporary message bridge. Remove this script tag from index.html to disable. */
(() => {
  const style = document.createElement('style');
  style.textContent = `
    #project-update{width:min(520px,calc(100vw - 32px));max-height:85dvh;overflow:auto;padding:28px;border:1px solid #eab47b70;border-radius:12px;background:#111419;color:#f0ede7;box-shadow:0 24px 100px #000b;font:15px/1.7 Manrope,system-ui,sans-serif}
    #project-update::backdrop{background:#000a;backdrop-filter:blur(5px)}
    #project-update h2{font-size:24px;line-height:1.3;margin:0 32px 18px 0}
    #project-update p{color:#bbc1ca;margin:14px 0}
    #project-update a{color:#eab47b}
    #project-update .update-close{position:absolute;right:12px;top:10px;background:transparent;border:0;color:#eee;font-size:26px;padding:5px 10px}
    #project-update .update-done{background:#eab47b;color:#16181b;border:0;border-radius:5px;padding:12px 20px;margin-top:12px;font-weight:700}
    #project-update-open{position:fixed;right:18px;bottom:18px;z-index:80;padding:12px 18px;background:#eab47b;color:#17191d;border:1px solid #f2c99c;border-radius:8px;box-shadow:0 6px 24px #0008;font:600 13px/1.4 Manrope,system-ui,sans-serif}
  `;
  document.head.append(style);
  const dialog = document.createElement('dialog');
  dialog.id = 'project-update';
  dialog.setAttribute('aria-labelledby', 'project-update-title');
  dialog.innerHTML = `
    <button class="update-close" aria-label="Закрыть сообщение" type="button">×</button>
    <h2 id="project-update-title">Ответ по обновлению сайта</h2>
    <p><strong>Освещение корабля на главной исправлено и опубликовано.</strong> Приглушены яркость корпуса и синий цвет, углублены тени, добавлен тёплый свет по краям. Форма Player Interceptor сохранена.</p>
    <p><a href="assets/helios-orbit-interceptor-lit.png" target="_blank" rel="noopener">Открыть обновлённую картинку ↗</a></p>
    <p>Этот временный попап добавлен, чтобы ответ был виден, пока сообщения чата не отображаются. Новый чат для этой правки не нужен — работа уже сохранена на сайте.</p>
    <p><small>Это вручную размещённое сообщение, не трансляция чата. Его можно снова открыть кнопкой «Ответ по сайту» внизу страницы.</small></p>
    <button class="update-done" type="button" autofocus>Понятно, посмотреть сайт</button>
  `;
  const opener = document.createElement('button');
  opener.id = 'project-update-open';
  opener.type = 'button';
  opener.textContent = 'Ответ по сайту';
  opener.setAttribute('aria-haspopup', 'dialog');
  opener.setAttribute('aria-controls', dialog.id);
  document.body.append(dialog, opener);
  const key = 'solar8-update-lighting-seen';
  const close = () => dialog.close();
  dialog.querySelector('.update-close').addEventListener('click', close);
  dialog.querySelector('.update-done').addEventListener('click', close);
  dialog.addEventListener('close', () => {
    try { sessionStorage.setItem(key, 'yes'); } catch {}
    opener.focus();
  });
  opener.addEventListener('click', () => dialog.showModal());
  let seen = false;
  try { seen = sessionStorage.getItem(key) === 'yes'; } catch {}
  if (!seen) dialog.showModal();
})();
