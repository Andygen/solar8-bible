(() => {
  const route = JSON.parse(document.querySelector('#legacy-route').textContent);
  let key = location.hash.slice(1);
  try { key = decodeURIComponent(key); } catch (_) {}
  location.replace('scenario.html#' + (route.anchors[key] || route.default));
})();
