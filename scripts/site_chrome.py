"""Shared head, header, navigation and footer for every page of the site."""
SOCIAL = '<meta property="og:image" content="https://alphaworx.io/assets/share-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Alphaworx: AI strategy, leadership and governance."><meta name="twitter:card" content="summary_large_image">'

ANALYTICS = '<!-- Cloudflare Web Analytics --><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "cfed6b70e1ae4f62b44f449d4b40b2ae"}\'></script><!-- End Cloudflare Web Analytics -->'


# --- New site UI (shared with caiokb.com / theaikb.com): assets/site/site.css -----------
SITE_URL = 'https://alphaworx.io'
LEGAL_NAME = 'Alphaworx Intelligence LLC'
NAV = [
    ('aios', '/aios-cloud.html', 'AIOS Cloud'),
    ('kb', '/knowledge-bases.html', 'Knowledge Bases'),
    ('advisory', '/advisory.html', 'Advisory'),
    ('insights', '/blog/', 'Insights'),
    ('about', '/about.html', 'About'),
]
ORG_JSONLD = ('{"@context":"https://schema.org","@type":"Organization","name":"Alphaworx",'
              '"legalName":"Alphaworx Intelligence LLC","url":"https://alphaworx.io/",'
              '"logo":"https://alphaworx.io/assets/mark.png","email":"info@alphaworx.io",'
              '"description":"AI strategy, leadership and governance: AIOS Cloud, the CAIO Knowledge Base, '
              'the AI Knowledge Base, and independent advisory."}')


def site_head(title, desc, path, css=(), noindex=False, jsonld=None, base=True, body_class='', og_type='website'):
    """<head> for a page on the new UI. `path` is the canonical path, or None for no canonical."""
    import html as _h
    t, d = _h.escape(title), _h.escape(desc or '')
    out = ['<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           f'<title>{t}</title>']
    if d:
        out.append(f'<meta name="description" content="{d}">')
    if noindex:
        out.append('<meta name="robots" content="noindex">')
    if path:
        out += [f'<meta property="og:title" content="{t}">',
                f'<meta property="og:description" content="{d}">',
                f'<meta property="og:type" content="{og_type}">',
                f'<meta property="og:url" content="{SITE_URL}{path}">',
                f'<meta property="og:image" content="{SITE_URL}/assets/share-card.png">',
                '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
                '<meta property="og:image:alt" content="Alphaworx: AI strategy, leadership and governance.">',
                '<meta name="twitter:card" content="summary_large_image">',
                f'<link rel="canonical" href="{SITE_URL}{path}">']
    out.append('<link rel="icon" type="image/png" href="/assets/mark.png">')
    if base:  # pages with their own layout CSS pass base=False and list chrome.css instead
        out += ['<link rel="stylesheet" href="/assets/site/site.css?v=1">',
                '<link rel="stylesheet" href="/assets/site/alphaworx.css?v=1">']
    out += [f'<link rel="stylesheet" href="{href}">' for href in css]
    if jsonld:
        out.append(f'<script type="application/ld+json">{jsonld}</script>')
    out.append('</head><body' + (f' class="{body_class}"' if body_class else '') + '>')
    return '\n'.join(out)


def site_header(current=None):
    links = ''.join(
        f'<a href="{href}"' + (' aria-current="page"' if key == current else '') + f'>{label}</a>'
        for key, href, label in NAV)
    return ('<a class="skip" href="#main">Skip to content</a>\n<header><div class="wrap">'
            '<a class="brand" href="/" aria-label="Alphaworx home"><img class="brand-logo" src="/assets/site/alphaworx-logo.webp" alt="Alphaworx" width="238" height="32"></a>'
            f'<nav aria-label="Main">{links}</nav>'
            '<div class="hdr-right"><a class="nav-cta" href="/schedule/">Request a demo ↗</a></div>'
            '</div></header>')


def site_footer(js=()):
    scripts = ''.join(f'<script defer src="{src}"></script>' for src in ('/assets/site/site.js?v=1', *js))
    return ('<footer><div class="wrap">'
            f'<span>Alphaworx · © 2026 {LEGAL_NAME}</span>'
            '<div class="links"><a href="/aios-cloud.html">AIOS Cloud</a>'
            '<a href="https://caiokb.com/">CAIO Knowledge Base</a>'
            '<a href="https://theaikb.com/teams">AI Knowledge Base</a>'
            '<a href="/advisory.html">Advisory</a><a href="/blog/">Insights</a><a href="/about.html">About</a>'
            '<a href="/privacy/">Privacy</a>'
            '<a href="mailto:info@alphaworx.io">Contact</a></div>'
            '</div></footer>\n' + scripts + '\n' + ANALYTICS + '\n</body></html>\n')
