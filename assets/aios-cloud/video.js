(() => {
  const compact = matchMedia('(max-width: 760px)').matches;
  document.querySelectorAll('video.aios-film').forEach(video => {
    if (compact) {
      video.querySelector('source').src = '/assets/video/aios-cloud-film-v3-720p.mp4';
      video.load();
    }
  });
})();
