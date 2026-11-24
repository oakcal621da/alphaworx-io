"""Version labels for asset addresses in generated pages.

Every root-relative /assets/... reference in a generated page gets ?h=<hash of the file's bytes>, so a page
asks for a different address whenever the file it was built against has changed.

What the label is, and is not:
- It is a label on an ordinary address. The host ignores the query string, so /assets/x.css?h=<old label>
  returns whatever x.css is now. The label does NOT make the address immutable.
- With the headers the site sends today (every response is revalidated) it is safe and changes nothing a
  visitor can see. It records which version of each file a page was built against, and
  tests/test_asset_versions.py uses that to catch a page that was not rebuilt after an asset changed.
- It is not enough for a long or `immutable` browser cache lifetime. A browser that asks for an old address
  after a deploy (an older copy of a page, or a tab left open) would store the new bytes under the old label,
  and an old page can be served new files. That needs file names that contain the hash, with the old files
  kept across deploys: a separate piece of work. Do not add a cache header on the strength of this module.

Details:
- A stylesheet's label also covers the files it points to with url(), so changing one of those changes
  the stylesheet's address too.
- Scripts must not build asset addresses themselves; they read them from the page (data-* attributes),
  where this module has already labelled them.
- Absolute addresses (https://alphaworx.io/assets/share-card.png in social tags) are left alone, and so is
  anything this module does not find on disk.
- public/deck.html is hand-authored and not passed through here; its assets keep plain addresses.
- SALT is part of every label; changing it changes every address at once.
"""
import hashlib
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / 'public'
SALT = '1'  # changes every label at once; an ordinary change never needs it
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
