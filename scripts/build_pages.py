"""Build small site pages with the same editorial shell as Insights."""
from pathlib import Path
from site_chrome import HEADER, FOOTER, FONTS
ROOT=Path(__file__).resolve().parent.parent

def page(title, label, body, canonical=None, noindex=False):
    meta=f'<link rel="canonical" href="https://alphaworx.io{canonical}">' if canonical else ''
    if noindex:meta+='<meta name="robots" content="noindex">'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Alphaworx</title>{meta}<link rel="icon" href="/assets/mark.png">{FONTS}<link rel="stylesheet" href="/assets/editorial.css?v=review-1"></head><body>{HEADER}<main id="main" class="wrap utility"><div class="post-hero"><div class="label">{label}</div><h1>{title}</h1></div><div class="post-body">{body}</div></main>{FOOTER}</body></html>'''

def main():
    (ROOT/'privacy').mkdir(exist_ok=True)
    (ROOT/'privacy/index.html').write_text(page('Privacy notice','Last updated · September 5, 2026',(ROOT/'content/pages/privacy.html').read_text(),'/privacy/'))
    (ROOT/'404.html').write_text(page('This page has moved or is missing.','404 · Page not found','<p>Find our current work, insights, and ways to get in touch from the Alphaworx homepage.</p><a class="work" href="/">Back to Alphaworx →</a>',noindex=True))
if __name__=='__main__':main()
