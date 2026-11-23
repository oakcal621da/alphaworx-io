/* Shared page behavior. External file because the site's CSP blocks inline scripts. */
(function () {
  // Full-size screenshot viewer for .zoom[data-full]
  var lb, opener;
  function trap(e) {
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'Tab' && lb) { e.preventDefault(); lb.querySelector('button').focus(); }
  }
  function open(src, alt) {
    if (lb) return;
    opener = document.activeElement;
    lb = document.createElement('div');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', alt);
    lb.innerHTML = '<button class="lb-x" type="button" aria-label="Close">×</button><img alt="">';
    var img = lb.querySelector('img');
    img.src = src;
    img.alt = alt;
    lb.addEventListener('click', close);
    document.addEventListener('keydown', trap);
    document.body.appendChild(lb);
    document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-x').focus();
  }
  function close() {
    if (!lb) return;
    lb.remove();
    lb = null;
    document.body.style.overflow = '';
    document.removeEventListener('keydown', trap);
    if (opener && opener.focus) opener.focus();
    opener = null;
  }
  document.querySelectorAll('.zoom[data-full]').forEach(function (el) {
    function go(e) {
      if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') return;
      e.preventDefault();
      var im = el.querySelector('img');
      open(el.getAttribute('data-full'), (im && im.alt) || 'Full-size screenshot');
    }
    el.addEventListener('click', go);
    el.addEventListener('keydown', go);
  });

  // Serve the smaller film file on phones
  if (matchMedia('(max-width: 760px)').matches) {
    document.querySelectorAll('video[data-compact]').forEach(function (video) {
      video.querySelector('source').src = video.getAttribute('data-compact');
      video.load();
    });
  }
})();
