"""The Careers page may only ship complete role entries.

content/careers.json holds one entry per role. Pay is optional (Don, Nov 25, 2026: left off for now).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROLES = json.loads((ROOT / 'content' / 'careers.json').read_text())['roles']
TEXT = ('slug', 'title', 'type', 'location', 'status', 'summary')


def test_every_role_is_complete():
    for r in ROLES:
        missing = [f for f in TEXT if not r.get(f, '').strip()] + [f for f in ('do', 'bring') if not r.get(f)]
        assert not missing, f"{r.get('title') or r.get('slug')}: missing {missing}"
        assert r['type'] in ('Full-time', 'Contract'), f"{r['title']}: type must be Full-time or Contract"
    slugs = [r['slug'] for r in ROLES]
    assert len(slugs) == len(set(slugs)), 'two roles share a slug'


def test_built_page_lists_every_role():
    page = (ROOT / 'public' / 'careers.html').read_text()
    assert '{{roles}}' not in page
    for r in ROLES:
        assert f'id="{r["slug"]}"' in page, f"{r['title']} is not on the built page; run scripts/build_pages.py"
