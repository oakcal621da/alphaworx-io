"""Asset addresses in the built pages carry a hash of the file they point to.

If a file under public/assets/ changes and the pages are not rebuilt, the first test fails. The label is
not a cache guarantee: the host ignores the query string, so these addresses are still mutable and must
keep today's revalidate headers (see scripts/asset_versions.py).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import asset_versions as av  # noqa: E402
from site_chrome import FONT_DIR, site_head  # noqa: E402

PUBLIC = ROOT / 'public'
HAND_AUTHORED = {'deck.html'}  # not built by the scripts; its assets keep plain addresses
PAGES = sorted(p for p in PUBLIC.rglob('*.html') if str(p.relative_to(PUBLIC)) not in HAND_AUTHORED)
# Stylesheets that still point at files themselves. Those files are fetched at plain, unlabelled addresses;
# adding to this list is a decision, not a formality.
CSS_URL_EXCEPTIONS = {
    'assets/deck.css': 'hand-authored deck',
    'assets/principles-guide.css': 'twelve-principles guide, own chrome and own @font-face rules',
}


def test_there_are_built_pages_to_check():
    assert len(PAGES) >= 25


def test_every_asset_reference_in_built_pages_has_the_current_content_hash():
    stale = []
    for page in PAGES:
        for path, query in av.references(page.read_text()):
            file = PUBLIC / path.lstrip('/')
            if not file.is_file():
                stale.append(f'{page.relative_to(PUBLIC)}: {path} does not exist')
            elif query != f'{av.PARAM}={av.digest(path)}':
                stale.append(f'{page.relative_to(PUBLIC)}: {path}?{query} is not the current hash; rebuild the pages')
    assert not stale, '\n'.join(stale[:20])


def test_versioning_is_idempotent_and_leaves_other_addresses_alone():
    html = ('<link href="/assets/site/site.css?v=1"><img src="/assets/mark.png" srcset="/assets/mark.png 1x, /assets/mark.png 2x">'
            '<meta content="https://alphaworx.io/assets/share-card.png"><a href="/blog/">x</a><a href="/assets/nope.png">y</a>')
    once = av.version_assets(html)
    assert av.version_assets(once) == once
    assert once.count(av.versioned('/assets/mark.png')) == 3
    assert av.versioned('/assets/site/site.css') in once and '?v=1' not in once
    assert 'https://alphaworx.io/assets/share-card.png"' in once  # absolute address untouched
    assert 'href="/assets/nope.png"' in once  # unknown file untouched


def test_a_stylesheet_address_changes_when_a_file_it_points_to_changes(tmp_path):
    (tmp_path / 'assets').mkdir()
    (tmp_path / 'assets/a.css').write_text("@font-face{src:url('/assets/f.woff2') format('woff2')}")
    (tmp_path / 'assets/f.woff2').write_bytes(b'one')
    before = av.digest('/assets/a.css', tmp_path)
    av._cache.clear()
    (tmp_path / 'assets/f.woff2').write_bytes(b'two')
    assert av.digest('/assets/a.css', tmp_path) != before
    assert av.css_dependencies('/assets/a.css', tmp_path) == ['/assets/f.woff2']


def test_scripts_do_not_build_asset_addresses_themselves():
    offenders = [str(js.relative_to(PUBLIC)) for js in (PUBLIC / 'assets').rglob('*.js')
                 if re.search(r'''['"`]/assets/|\.(webp|png|jpg|mp4|woff2|css)['"`]''', js.read_text())]
    assert not offenders, f'these scripts name asset files; read the address from the page instead: {offenders}'


def test_only_the_known_stylesheets_point_at_files():
    pointing = {str(css.relative_to(PUBLIC)) for css in (PUBLIC / 'assets').rglob('*.css')
                if av.css_dependencies('/' + str(css.relative_to(PUBLIC)))}
    assert pointing == set(CSS_URL_EXCEPTIONS), pointing


def test_the_preloaded_fonts_are_the_ones_the_font_rules_use():
    head = av.version_assets(site_head('t', 'd', '/'))
    preloaded = re.findall(r'<link rel="preload" href="([^"]+)" as="font" type="font/woff2" crossorigin>', head)
    assert len(preloaded) == 2 and all(f'?{av.PARAM}=' in href for href in preloaded)
    style = re.search(r'<style>(.*?)</style>', head, flags=re.S).group(1)
    for href in preloaded:  # same address, character for character, or the browser downloads the font twice
        assert f"url('{href}') format('woff2')" in style
    for name in ('Regular', 'Medium', 'SemiBold'):
        assert (PUBLIC / FONT_DIR.lstrip('/') / f'Barlow-{name}.woff2').is_file()
    assert 'font-display:swap' in style and '"Barlow Fallback"' in style
    assert head.index('<style>') > head.rindex('<link rel="stylesheet"')  # after the stylesheets
