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


# --- Fonts: Barlow, self-hosted. scripts/make_fonts.py writes the .woff2 files and prints the numbers below.
FONT_DIR = '/assets/aios-cloud'
FONT_WEIGHTS = (('Regular', 400), ('Medium', 500), ('SemiBold', 600))
# The two weights every page paints first; fetched alongside the stylesheets instead of after them.
FONT_PRELOAD = ''.join(f'<link rel="preload" href="{FONT_DIR}/Barlow-{name}.woff2" as="font" type="font/woff2" crossorigin>'
                       for name in ('Regular', 'Medium'))
# Local Arial resized to take up the same room as Barlow, so text does not re-wrap when Barlow arrives.
# (weight, local font names, size-adjust, ascent-override, descent-override), measured on the site's own text.
FALLBACK_FACES = ((400, ('Arial', 'ArialMT'), '96.48%', '103.65%', '20.73%'),
                  (500, ('Arial', 'ArialMT'), '97.52%', '102.54%', '20.51%'),
                  (600, ('Arial Bold', 'Arial-BoldMT'), '91.32%', '109.51%', '21.90%'))
# Placed after the stylesheets so these rules replace the .ttf-only ones in site.css, which stays a plain
# copy of the knowledge base sites' file. The unicode-range keeps arrows and check marks on plain Arial, as before.
FONT_CSS = ('<style>'
            + ''.join(f"@font-face{{font-family:Barlow;src:url('{FONT_DIR}/Barlow-{name}.woff2') format('woff2'),"
                      f"url('{FONT_DIR}/Barlow-{name}.ttf') format('truetype');font-weight:{weight};font-style:normal;font-display:swap}}"
                      for name, weight in FONT_WEIGHTS)
            + ''.join('@font-face{font-family:"Barlow Fallback";src:' + ','.join(f'local("{n}")' for n in names)
                      + f';font-weight:{weight};size-adjust:{size};ascent-override:{ascent};descent-override:{descent};'
                        'line-gap-override:0%;unicode-range:U+20-7E,U+A0-FF,U+2010-2027}'
                      for weight, names, size, ascent, descent in FALLBACK_FACES)
            + ':root{--font:"Barlow","Barlow Fallback",Arial,sans-serif}</style>')


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
    out.append(FONT_PRELOAD)
    if base:  # pages with their own layout CSS pass base=False and list chrome.css instead
        out += ['<link rel="stylesheet" href="/assets/site/site.css">',
                '<link rel="stylesheet" href="/assets/site/alphaworx.css">']
    out.append('<link rel="stylesheet" href="/assets/site/contact.css">')
    out += [f'<link rel="stylesheet" href="{href}">' for href in css]
    out.append(FONT_CSS)
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


# The inquiry form, on every page. assets/contact.js opens it from any link to mailto:info@alphaworx.io
# (without JavaScript those links still open an email). Styles: assets/site/contact.css.
CONTACT_DIALOG = '''<dialog class="contact-dialog" id="contact-dialog" aria-labelledby="contact-title" aria-describedby="contact-description">
<div class="contact-dialog-head" id="contact-dialog-head">
<span class="contact-eyebrow"><i></i>Start a conversation</span>
<button class="contact-dismiss" type="button" data-close-contact aria-label="Close contact form">×</button>
<h2 id="contact-title">What would you like to discuss?</h2>
<p id="contact-description">Tell us a little about your organization and where you're looking to take AI.</p>
</div>
<form class="contact-form" id="contact-form">
<div class="contact-fields">
<div class="contact-field"><label for="contact-name">Name</label><input id="contact-name" name="name" autocomplete="name" maxlength="120" required autofocus></div>
<div class="contact-field"><label for="contact-email">Work email</label><input id="contact-email" name="email" type="email" autocomplete="email" maxlength="254" required></div>
<div class="contact-field"><label for="contact-company">Company <span>(optional)</span></label><input id="contact-company" name="company" autocomplete="organization" maxlength="160"></div>
<div class="contact-field"><label for="contact-role">Role <span>(optional)</span></label><input id="contact-role" name="role" autocomplete="organization-title" maxlength="120"></div>
<div class="contact-field full"><label for="contact-topic">I'd like to discuss</label><select id="contact-topic" name="topic"><option>General conversation</option><option>AI strategy assessment</option><option>Executive AI advisory</option><option>AI for growth</option><option>AI for efficiency</option><option>Customer experience</option><option>Operational resilience</option><option>AI governance and operations</option></select></div>
<div class="contact-field full"><label for="contact-message">What are you working toward?</label><textarea id="contact-message" name="message" maxlength="3000" placeholder="Your priorities, challenges, or the question you'd like to explore…" required></textarea></div>
</div>
<div class="contact-honeypot" aria-hidden="true"><label for="contact-website">Leave this blank</label><input id="contact-website" name="_gotcha" tabindex="-1" autocomplete="off"></div>
<p class="contact-form-note" id="contact-delivery-note"></p>
<p class="contact-form-note">By sending an inquiry, you ask Alphaworx to contact you about it. See our <a href="/privacy/" target="_blank" rel="noopener">privacy notice</a>.</p>
<div class="contact-actions"><button class="contact-btn" id="contact-submit" type="submit">Continue in email ↗</button><button class="contact-cancel" type="button" data-close-contact>Cancel</button></div>
<p class="contact-status" id="contact-status" role="status" aria-live="polite" aria-atomic="true"></p>
</form>
<section class="contact-success" id="contact-success" role="status" aria-live="polite" aria-labelledby="contact-success-title" hidden>
<div class="contact-success-mark" aria-hidden="true">✓</div>
<span class="contact-eyebrow"><i></i>Inquiry received</span>
<h2 id="contact-success-title" tabindex="-1">Thank you for reaching out.</h2>
<p>Your inquiry has been sent to Alphaworx. Our team will review your message and reach out shortly. If you are ready, you can choose a time for the conversation now.</p>
<div class="contact-success-actions"><a class="contact-btn" href="/schedule/">Choose a time <span>→</span></a><button class="contact-return" type="button" data-close-contact>Return to the site</button></div>
</section>
</dialog>'''

SITE_JS = ('/assets/site/site.js', '/assets/contact-config.js', '/assets/contact.js')


def site_footer(js=()):
    scripts = ''.join(f'<script defer src="{src}"></script>' for src in (*SITE_JS, *js))
    return ('<footer><div class="wrap">'
            f'<span>Alphaworx · © 2026 {LEGAL_NAME}</span>'
            '<div class="links"><a href="/aios-cloud.html">AIOS Cloud</a>'
            '<a href="https://caiokb.com/">CAIO Knowledge Base</a>'
            '<a href="https://theaikb.com/teams">AI Knowledge Base</a>'
            '<a href="/advisory.html">Advisory</a><a href="/blog/">Insights</a><a href="/about.html">About</a>'
            '<a href="/privacy/">Privacy</a>'
            '<a href="mailto:info@alphaworx.io">Contact</a></div>'
            '</div></footer>\n' + CONTACT_DIALOG + '\n' + scripts + '\n' + ANALYTICS + '\n</body></html>\n')
