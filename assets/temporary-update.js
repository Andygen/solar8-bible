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
    <h2 id="project-update-title">Как продолжить работу</h2>
    <p>Сообщения доходят до меня, изменения сайта выполняются. По скриншоту похоже на сбой отображения панели Codex; точная причина пока неизвестна.</p>
    <ol>
      <li><strong>Сначала перезагрузи окно:</strong> сохрани открытые файлы, нажми Ctrl+Shift+P, введи <code>Developer: Reload Window</code> и нажми Enter. Затем снова открой этот разговор.</li>
      <li><strong>Если чат всё ещё пустой:</strong> полностью закрой VS Code и запусти снова.</li>
      <li><strong>Если не помогло — создай новый чат.</strong> Открой папку сайта через File → Open Folder: <code style="overflow-wrap:anywhere">C:\\Users\\mail\\OneDrive\\Work\\s8bible\\solar8-bible</code>. Это папка Bible, а не игры.</li>
    </ol>
    <p>В новом чате отправь:</p>
    <blockquote style="margin:12px 0;padding:14px;border-left:2px solid #eab47b">Продолжаем SOLAR 8 Bible. Прочитай docs/continue-work.md и проверь git status. Прошлый чат перестал отображать ответы. Кратко сообщи, что понял о текущем состоянии проекта, пока ничего не меняй.</blockquote>
    <p>Все изменения сайта сохранены в Git и опубликованы. Для нового чата подготовлена памятка; полная история разговора автоматически ему не передаётся. Старый чат удалять не нужно.</p>
    <p><small>Начать новый короткий чат при зависшем разговоре также рекомендует <a href="https://learn.chatgpt.com/docs/reference/troubleshooting" target="_blank" rel="noopener">официальная документация OpenAI</a>. Порядок с перезагрузкой окна выше — мой первый практический шаг для этого случая.</small></p>
    <button class="update-done" type="button" autofocus>Понятно, посмотреть сайт</button>
  `;
  const opener = document.createElement('button');
  opener.id = 'project-update-open';
  opener.type = 'button';
  opener.textContent = 'Ответ по сайту';
  opener.setAttribute('aria-haspopup', 'dialog');
  opener.setAttribute('aria-controls', dialog.id);
  document.body.append(dialog, opener);
  const key = 'solar8-update-chat-recovery-seen';
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
