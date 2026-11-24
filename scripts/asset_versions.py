"""Content-derived versions for asset addresses in generated pages.

Every root-relative /assets/... reference in a generated page gets ?h=<hash of the file's bytes>, so the
address changes exactly when the file changes. That is what makes a long browser cache lifetime safe for
these addresses: a page (always revalidated) points at the new address as soon as the file is different.

- A stylesheet's hash also covers the files it points to with url(), so changing one of those changes
  the stylesheet's address too.
- Scripts must not build asset addresses themselves; they read them from the page (data-* attributes),
  where this module has already versioned them. tests/test_asset_versions.py checks both.
- Absolute addresses (https://alphaworx.io/assets/share-card.png in social tags) are left alone, and so is
  anything this module does not find on disk.
- public/deck.html is hand-authored and not passed through here; its assets keep plain addresses.

Rolling back: a visitor's browser may hold a newer file under an older address (a tab opened before a
deploy that fetched an asset after it). Reverting the content would bring that older address back. So a
rollback also bumps SALT below, which gives every asset a fresh address.
"""
import hashlib
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / 'public'
SALT = '1'  # bump on a rollback (see above); never needed for an ordinary change
PARAM = 'h'

# A root-relative asset path with an extension, plus any query already on it. The lookbehind skips
# absolute URLs (…alphaworx.io/assets/…) and longer paths that merely contain "/assets/".
ASSET_REF = re.compile(r'(?<![\w.:/-])(/assets/[A-Za-z0-9_./-]*\.[A-Za-z0-9]+)(\?[A-Za-z0-9_=.&%-]*)?')
CSS_URL = re.compile(r'''url\(\s*['"]?([^'")\s]+)['"]?\s*\)''')

_cache = {}


def css_dependencies(path, public=PUBLIC):
    """Root-relative files a stylesheet points to with url(), as written (query strings removed)."""
    text = (public / path.lstrip('/')).read_text()
    refs = {ref.split('?')[0].split('#')[0] for ref in CSS_URL.findall(text) if not ref.startswith('data:')}
    return sorted(ref for ref in refs if ref.startswith('/assets/'))


def digest(path, public=PUBLIC):
    """Ten hex characters identifying the file at `path` (root-relative) and, for CSS, what it points to."""
    key = (str(public), path)
    if key not in _cache:
        file = public / path.lstrip('/')
        h = hashlib.sha256(SALT.encode() + b'\0' + file.read_bytes())
        if file.suffix == '.css':
            for dep in css_dependencies(path, public):
                if (public / dep.lstrip('/')).is_file():
                    h.update(dep.encode() + b'\0' + digest(dep, public).encode())
        _cache[key] = h.hexdigest()[:10]
    return _cache[key]


def versioned(path, public=PUBLIC):
    return f'{path}?{PARAM}={digest(path, public)}'


def version_assets(html, public=PUBLIC):
    """Return `html` with every root-relative /assets/ reference that exists on disk given its content hash."""
    def replace(match):
        path = match.group(1)
        if not (public / path.lstrip('/')).is_file():
            return match.group(0)
        return versioned(path, public)
    return ASSET_REF.sub(replace, html)


def references(html):
    """(path, query) for each root-relative asset reference in `html`; used by the tests."""
    return [(m.group(1), (m.group(2) or '')[1:]) for m in ASSET_REF.finditer(html)]
