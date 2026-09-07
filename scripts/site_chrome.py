"""Shared navigation, typography and metadata for editorial and utility pages."""
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
HEADER = '''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="site-row">
<a class="brand" href="/"><img src="/assets/mark.png" alt="Alphaworx" width="28" height="28"><span class="word">ALPHAWORX<span>.IO</span></span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu ＋</button>
<nav id="site-nav" aria-label="Main navigation"><a href="/#opportunity">Opportunity</a><a href="/#workflow">Our approach</a><a href="/#assessment">Assessment</a><a href="/blog/">Insights</a><a href="/#about">About</a><a href="/schedule/">Schedule</a><a href="/#contact">Let’s talk ↗</a></nav>
</div></header>'''
FOOTER = '''<footer class="site-footer"><div class="site-row"><span>© 2026 Alphaworx Ltd</span><a href="/deck.html">Assessment walkthrough ↗</a><a href="/privacy/">Privacy</a><a href="mailto:info@alphaworx.io">info@alphaworx.io</a></div></footer><script src="/assets/site-nav.js" defer></script>'''

SOCIAL = '<meta property="og:image" content="https://alphaworx.io/assets/share-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Alphaworx — From strategy to execution."><meta name="twitter:card" content="summary_large_image">'
