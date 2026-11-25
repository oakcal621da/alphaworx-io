"""Build the site's pages from content/pages/*.html fragments and the shared chrome.

Each fragment holds only the page's <main> content. The head, header, navigation and
footer come from site_chrome.py, so they cannot drift between pages. Asset addresses are written
plain in the sources; asset_versions.py adds ?h=<content hash> to each one as the page is written.
Run: python3 scripts/build_pages.py
"""
from pathlib import Path
from asset_versions import version_assets
from site_chrome import site_head, site_header, site_footer, ORG_JSONLD

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / 'public'  # the only folder the static host publishes
PAGES_DIR = ROOT / 'content' / 'pages'

# out: file written (relative to public/) · src: fragment in content/pages/
# path: canonical path (None = no canonical/og) · nav: key in site_chrome.NAV to mark current
PAGES = [
    dict(out='index.html', src='home.html', path='/', nav=None, jsonld=ORG_JSONLD,
         title='Alphaworx — AI Strategy, Leadership and Governance',
         desc='Alphaworx gives organizations the platform to govern AI, and their leaders and teams '
              'the knowledge to put it to work: AIOS Cloud, the CAIO Knowledge Base, the AI Knowledge Base, '
              'and independent advisory.'),
    dict(out='aios-cloud.html', src='aios-cloud.html', path='/aios-cloud.html', nav='aios',
         css=['/assets/site/aios-cloud.css'], js=['/assets/site/aios-cloud.js'],
         title='AIOS Cloud — The AI Strategy and Governance Platform by Alphaworx',
         desc='AIOS Cloud brings AI strategy, initiatives, risk, and governance into one connected platform '
              'for enterprises, small businesses, and government entities.'),
    dict(out='knowledge-bases.html', src='knowledge-bases.html', path='/knowledge-bases.html', nav='kb',
         title='Knowledge Bases for Leaders and Teams — Alphaworx',
         desc='Two knowledge bases for the organization adopting AI: the CAIO Knowledge Base for the people '
              'accountable for it, and the AI Knowledge Base for every team.'),
    dict(out='advisory.html', src='advisory.html', path='/advisory.html', nav='advisory',
         css=['/assets/site/advisory.css'],
         title='AI Strategy & Advisory — Alphaworx',
         desc='Independent strategy and hands-on counsel that connects AI ambition with the work of operating it.'),
    dict(out='schedule/index.html', src='schedule.html', path='/schedule/', nav=None,
         css=['/assets/site/schedule.css'],
         js=['/assets/schedule.js'],
         title='Request a demo or schedule a conversation — Alphaworx',
         desc='Choose a 30-minute time for a demo of AIOS Cloud or a conversation about your AI priorities.'),
    dict(out='about.html', src='about.html', path='/about.html', nav='about',
         title='About Alphaworx',
         desc='Alphaworx builds AIOS Cloud, the CAIO Knowledge Base and the AI Knowledge Base, and advises '
              'leaders on AI strategy and governance.'),
    dict(out='partners.html', src='partners.html', path='/partners.html', nav='partners',
         css=['/assets/site/partners.css'],
         title='Partners — Alphaworx',
         desc='The companies Alphaworx works with to sell and deliver its products and advisory services.'),
    dict(out='careers.html', src='careers.html', path='/careers.html', nav=None,
         css=['/assets/site/careers.css'],
         title='Careers — Alphaworx',
         desc='Open roles at Alphaworx: remote roles in the United States and Europe, plus contract advisory '
              'and reviewer work.'),
    dict(out='privacy/index.html', src='privacy.html', path='/privacy/', nav=None, legal=True,
         label='Privacy', heading='Privacy notice', updated='Last updated November 25, 2026',
         title='Privacy notice — Alphaworx',
         desc='How Alphaworx handles information when you visit this website, send an inquiry, schedule a conversation, '
              'or apply for a role.'),
    # No terms page (Don, 2026-11-23). An unreviewed draft is kept at content/pages/terms.html; it is not built.
    dict(out='404.html', src='404.html', path=None, nav=None, noindex=True,
         title='Page not found — Alphaworx', desc=''),
]


CHROME_PREFIXES = ('header', '.brand', 'nav', '.hdr-right', '.nav-cta', '.signin', '.m-only',
                   'footer', 'body::before', '.skip')


def _is_chrome(selector):
    parts = [s.strip() for s in selector.split(',')]
    return all(s == '.wrap' or s.startswith(CHROME_PREFIXES) for s in parts)


def _scope(selector):
    """Bare `nav` rules must only reach the site header; articles have their own <nav>."""
    return ','.join('header ' + s.strip() if s.strip().startswith('nav') else s.strip()
                    for s in selector.split(','))


def _blocks(css):
    """Yield (prelude, body) for each top-level block of a stylesheet."""
    i, n = 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            return
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {'{': 1, '}': -1}.get(css[k], 0)
            k += 1
        yield css[i:j].strip(), css[j + 1:k - 1]
        i = k


def build_chrome_css():
    """Write assets/site/chrome.css: fonts, tokens and the header/footer rules taken from
    site.css + alphaworx.css, for pages (the Insights guides) that keep their own layout CSS."""
    import re
    out = ['/* GENERATED by scripts/build_pages.py from site.css and alphaworx.css. Do not edit. */']
    for name in ('site.css', 'alphaworx.css'):
        css = re.sub(r'/\*.*?\*/', '', (PUBLIC / 'assets/site' / name).read_text(), flags=re.S)
        for prelude, body in _blocks(css):
            if prelude.startswith('@font-face') or prelude == ':root':
                out.append(f'{prelude}{{{body.strip()}}}')
            elif prelude.startswith('@media'):
                inner = [f'{_scope(s)}{{{b.strip()}}}' for s, b in _blocks(body) if _is_chrome(s)]
                if inner:
                    out.append(f'{prelude}{{{"".join(inner)}}}')
            elif _is_chrome(prelude):
                out.append(f'{_scope(prelude)}{{{body.strip()}}}')
    (PUBLIC / 'assets/site/chrome.css').write_text('\n'.join(out) + '\n')


def partner_cards():
    """Cards for the Partners page, from content/partners.json. An entry with a field missing is drawn
    as a dashed draft card; tests/test_partners.py fails while one exists."""
    import json
    from html import escape
    cards = []
    for p in json.loads((ROOT / 'content' / 'partners.json').read_text())['partners']:
        name, url, logo, summary = (p.get(k, '').strip() for k in ('name', 'url', 'logo', 'summary'))
        logo_html = (f'<img src="/assets/partners/{escape(logo)}" alt="{escape(name)}" loading="lazy">' if logo
                     else 'Logo to come')
        text = (f'<h3>{escape(name or "Partner name")}</h3>'
                f'<p>{escape(summary or "One sentence on what this firm does, from the partner.")}</p>')
        if all((name, url, logo, summary)):
            cards.append(f'      <a class="partner" href="{escape(url)}" rel="noopener">'
                         f'<span class="partner-logo">{logo_html}</span>{text}'
                         '<span class="text-cta">Visit website</span></a>')
        else:  # shows what has arrived so far
            cards.append(f'      <div class="partner is-draft"><span class="partner-logo">{logo_html}</span>{text}</div>')
    return '\n'.join(cards)


def _careers():
    import json
    return json.loads((ROOT / 'content' / 'careers.json').read_text())


def _apply_href(role):
    from urllib.parse import quote
    return f'mailto:jobs@alphaworx.io?subject={quote(role["title"])}'


def _role_meta(role):
    from html import escape
    return (f'<div class="role-meta"><b>{escape(role["status"])}</b><span>{escape(role["type"])}</span>'
            f'<span>{escape(role["location"])}</span></div>')


def role_cards():
    """The list of roles on the Careers page, from content/careers.json. Each card links to the role's own page."""
    from html import escape
    out = []
    for r in _careers()['roles']:
        out.append(
            f'      <a class="role-card" href="/careers/{escape(r["slug"])}.html" id="{escape(r["slug"])}">'
            f'<div class="role-top"><h3>{escape(r["title"])}</h3>{_role_meta(r)}</div>'
            f'<p>{escape(r["summary"])}</p><span class="text-cta">Read the role</span></a>')
    return '\n'.join(out)


def role_pages():
    """One page per role at /careers/<slug>.html, from content/careers.json. Pay is printed only when a figure is set."""
    from html import escape
    data = _careers()
    paras = lambda items: ''.join(f'<p>{escape(x)}</p>' for x in items)
    bullets = lambda items: '<ul>' + ''.join(f'<li>{escape(x)}</li>' for x in items) + '</ul>'

    def do_list(items):
        if all(isinstance(x, str) for x in items):
            return bullets(items)
        return ''.join(f'<h3>{escape(g["group"])}</h3>' + bullets(g['items']) for g in items)

    pages = []
    for r in data['roles']:
        apply = _apply_href(r)
        pay = r.get('pay', '').strip()
        sections = [('About Alphaworx', paras(data['company'])), ('About the role', paras(r['about'])),
                    ("What you'll do", do_list(r['do'])), ('What you bring', bullets(r['bring']))]
        if r.get('nice'):
            sections.append(('Nice to have', bullets(r['nice'])))
        if r.get('first_months'):
            sections.append(('Your first months', bullets(r['first_months'])))
        sections.append(('How we work', bullets(data['how_we_work'])))
        apply_text = escape(data['apply']).replace('jobs@alphaworx.io', '<a href="mailto:jobs@alphaworx.io">jobs@alphaworx.io</a>', 1)
        sections.append(('How to apply', f'<p>{apply_text}</p><p>How we handle applications is in our '
                                          f'<a href="/privacy/#applications">privacy notice</a>.</p>'))
        article = ''.join(f'<section><h2>{t}</h2>{h}</section>' for t, h in sections)
        facts = ''.join(f'<div><small>{k}</small><b>{escape(v)}</b></div>' for k, v in
                        (('Type', r['type']), ('Location', r['location']), ('Status', r['status'])) + ((('Pay', pay),) if pay else ()))
        body = (
            f'<section class="phero role-hero"><div class="wrap"><div>'
            f'<span class="eyebrow"><i></i><a href="/careers.html">Careers</a></span>'
            f'<h1>{escape(r["title"])}</h1>{_role_meta(r)}<p class="lead">{escape(r["summary"])}</p>'
            f'<div class="closing-btns"><a class="primary" href="{apply}">Apply by email <span>→</span></a>'
            f'<a class="text-cta" href="/careers.html">All open roles</a></div></div></div></section>\n'
            f'<section class="section role-body"><div class="wrap role-layout">'
            f'<article class="role-text">{article}</article>'
            f'<aside class="role-aside"><div class="role-facts">{facts}</div>'
            f'<a class="primary" href="{apply}">Apply by email <span>→</span></a>'
            f'<a class="text-cta" href="/careers.html">All open roles</a></aside>'
            f'</div></section>')
        pages.append(dict(out=f'careers/{r["slug"]}.html', path=f'/careers/{r["slug"]}.html', nav=None, body=body,
                          css=['/assets/site/careers.css'],
                          title=f'{r["title"]} — Careers at Alphaworx',
                          desc=f'{r["summary"]} {r["type"]}, {r["location"]}.'))
    return pages


def render(page):
    body = page['body'] if 'body' in page else (PAGES_DIR / page['src']).read_text()
    if '{{roles}}' in body:
        body = body.replace('{{roles}}', role_cards())
    if '{{how_we_work}}' in body:
        from html import escape
        body = body.replace('{{how_we_work}}', '<ul class="work-list">' + ''.join(
            f'<li>{escape(x)}</li>' for x in _careers()['how_we_work']) + '</ul>')
    if '{{partners}}' in body:
        body = body.replace('{{partners}}', partner_cards())
    if page.get('legal'):
        body = (f'<section class="phero"><div class="wrap"><div><span class="eyebrow"><i></i>{page["label"]}</span>'
                f'<h1>{page["heading"]}</h1></div></div></section>\n'
                f'<section class="section"><div class="wrap legal"><p class="updated">{page["updated"]}</p>\n'
                f'{body}\n</div></section>')
    return (site_head(page['title'], page['desc'], page['path'], css=page.get('css', ()),
                      noindex=page.get('noindex', False), jsonld=page.get('jsonld'))
            + '\n' + site_header(page.get('nav'))
            + '\n<main id="main">\n' + body.strip() + '\n</main>\n'
            + site_footer(page.get('js', ())))


def main():
    build_chrome_css()
    built, skipped = [], []
    for page in PAGES + role_pages():
        if 'body' not in page and not (PAGES_DIR / page['src']).exists():
            skipped.append(page['out'])
            continue
        out = PUBLIC / page['out']
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(version_assets(render(page)))  # asset addresses get their content hash here
        built.append(page['out'])
    print('Built:', ', '.join(built))
    if skipped:
        print('Not yet rebuilt (no fragment, old page left as is):', ', '.join(skipped))


if __name__ == '__main__':
    main()
