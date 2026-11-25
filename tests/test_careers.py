"""The Careers page may only ship complete role entries.

content/careers.json holds one entry per role. Pay is optional (Don, Nov 25, 2026: left off for now).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROLES = json.loads((ROOT / 'content' / 'careers.json').read_text())['roles']
TEXT = ('slug', 'title', 'type', 'location', 'status', 'summary')
DATA = json.loads((ROOT / 'content' / 'careers.json').read_text())


def test_every_role_is_complete():
    for r in ROLES:
        missing = [f for f in TEXT if not r.get(f, '').strip()] + [f for f in ('about', 'do', 'bring') if not r.get(f)]
        assert not missing, f"{r.get('title') or r.get('slug')}: missing {missing}"
        assert r['type'] in ('Full-time', 'Contract'), f"{r['title']}: type must be Full-time or Contract"
    slugs = [r['slug'] for r in ROLES]
    assert len(slugs) == len(set(slugs)), 'two roles share a slug'


def test_shared_sections_are_present():
    assert DATA['company'] and DATA['how_we_work'] and 'jobs@alphaworx.io' in DATA['apply']


def test_built_pages_list_and_link_every_role():
    index = (ROOT / 'public' / 'careers.html').read_text()
    assert '{{roles}}' not in index and '{{how_we_work}}' not in index
    sitemap = (ROOT / 'public' / 'sitemap.xml').read_text()
    for r in ROLES:
        assert f'href="/careers/{r["slug"]}.html"' in index, f"{r['title']} is not linked from careers.html"
        page = (ROOT / 'public' / 'careers' / f'{r["slug"]}.html').read_text()
        assert r['title'] in page.replace('&amp;', '&')
        assert 'mailto:jobs@alphaworx.io?subject=' in page
        assert f'/careers/{r["slug"]}.html</loc>' in sitemap, f"{r['slug']} is missing from the sitemap"
