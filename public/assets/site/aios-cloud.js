/* AIOS Cloud page: workspace tabs. External file because the site's CSP blocks inline scripts. */
(function () {
  var tabs = [].slice.call(document.querySelectorAll('.anat-tab'));
  var screen = document.querySelector('.anat-shot .screen');
  if (!tabs.length || !screen) return;
  var img = screen.querySelector('img');
  var label = screen.querySelector('.ws-label');
  var list = tabs[0].parentNode;
  var loaders = {};  // tab id -> Image, so each screenshot is requested once
  var wanted = null; // the tab chosen last; a slower earlier choice must not replace it

  function srcset(tab) { return tab.dataset.img + ' 1600w, ' + tab.dataset.full + ' 2560w'; }

  // Request a tab's screenshot the way the visible image would, so the browser picks the same file.
  function load(tab) {
    if (!loaders[tab.id]) {
      var im = loaders[tab.id] = new Image();
      im.sizes = img.sizes;
      im.srcset = srcset(tab);
      im.src = tab.dataset.img;
    }
    return loaders[tab.id];
  }

  function show(tab) {
    img.srcset = srcset(tab);
    img.src = tab.dataset.img;
    img.alt = tab.dataset.alt;
    screen.setAttribute('data-full', tab.dataset.full);
    screen.removeAttribute('aria-busy');
  }

  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (panel) panel.hidden = !on;
    });
    if (label) label.textContent = tab.dataset.label;
    wanted = tab;
    var im = load(tab);
    if (im.complete) { show(tab); return; }
    // Keep the current screenshot until the new one has arrived. If it fails, show() leaves its alt text.
    screen.setAttribute('aria-busy', 'true');
    function done() { if (wanted === tab) show(tab); }
    im.addEventListener('load', done);
    im.addEventListener('error', done);
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
  });

  // Fetch the other tabs' screenshots when the visitor first reaches for the tabs, not on page load.
  function warm() {
    tabs.forEach(function (t) { if (t.getAttribute('aria-selected') !== 'true') load(t); });
  }
  ['pointerenter', 'touchstart', 'focusin'].forEach(function (type) {
    list.addEventListener(type, warm, { once: true, passive: true });
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
