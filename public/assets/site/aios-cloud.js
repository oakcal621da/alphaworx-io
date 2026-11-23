/* AIOS Cloud page: workspace tabs. External file because the site's CSP blocks inline scripts. */
(function () {
  var tabs = [].slice.call(document.querySelectorAll('.anat-tab'));
  var screen = document.querySelector('.anat-shot .screen');
  if (!tabs.length || !screen) return;
  var img = screen.querySelector('img');
  var label = screen.querySelector('.ws-label');

  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (panel) panel.hidden = !on;
    });
    var full = tab.dataset.img.replace(/\.webp$/, '-full.webp');
    img.srcset = tab.dataset.img + ' 1600w, ' + full + ' 2560w';
    img.src = tab.dataset.img;
    img.alt = tab.dataset.alt;
    screen.setAttribute('data-full', full);
    if (label) label.textContent = tab.dataset.label;
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { select(tab); });
    tab.addEventListener('keydown', function (e) {
      var step = (e.key === 'ArrowDown' || e.key === 'ArrowRight') ? 1
        : (e.key === 'ArrowUp' || e.key === 'ArrowLeft') ? -1 : 0;
      if (!step) return;
      e.preventDefault();
      var next = tabs[(i + step + tabs.length) % tabs.length];
      select(next);
      next.focus();
    });
    new Image().src = tab.dataset.img;
  });

  // Links such as /aios-cloud.html#heading-policy-workflow open the matching tab.
  function fromHash() {
    var id = location.hash.slice(1);
    var tab = id && tabs.filter(function (t) { return t.id === id; })[0];
    if (tab) select(tab);
  }
  fromHash();
  window.addEventListener('hashchange', fromHash);
})();
