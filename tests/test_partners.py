"""The Partners page may only ship complete entries.

content/partners.json holds one entry per partner. An entry with a missing name, link, logo or summary is drawn as a dashed draft card so the layout can be reviewed before the material arrives. These
tests fail while such an entry exists, and while any entry is not marked approved (Don has confirmed
the partner agreed to be listed and the sentence is right), which keeps either from being published.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTNERS = json.loads((ROOT / 'content' / 'partners.json').read_text())['partners']
FIELDS = ('name', 'url', 'logo', 'summary')


def test_every_partner_entry_is_complete():
    missing = [(i + 1, [f for f in FIELDS if not p.get(f, '').strip()]) for i, p in enumerate(PARTNERS)]
    missing = [m for m in missing if m[1]]
    assert not missing, f'incomplete partner entries (entry number, missing fields): {missing}'


def test_every_partner_has_approved_its_logo_and_wording():
    waiting = [p.get('name') for p in PARTNERS if p.get('approved') is not True]
    assert not waiting, f'not marked approved yet: {waiting}'


def test_partner_links_and_logos_are_usable():
    for p in PARTNERS:
        if p.get('url'):
            assert p['url'].startswith('https://'), f"{p.get('name')}: link must start with https://"
        if p.get('logo'):
            assert (ROOT / 'public' / 'assets' / 'partners' / p['logo']).is_file(), \
                f"{p.get('name')}: logo file {p['logo']} is not in public/assets/partners/"


def test_built_page_has_no_draft_card():
    page = (ROOT / 'public' / 'partners.html').read_text()
    assert 'is-draft' not in page, 'public/partners.html still shows a draft partner card'
    assert '{{partners}}' not in page
