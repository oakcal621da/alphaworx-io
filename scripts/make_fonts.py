"""Build the web fonts and print the fallback-font metrics used in site_chrome.py.

Run: python3 scripts/make_fonts.py        (needs fontTools and brotli: pip install fonttools brotli)

1. Writes public/assets/aios-cloud/Barlow-<weight>.woff2 next to each .ttf. Same glyphs, same tables,
   smaller file: nothing is subset, so every character the .ttf covers is still covered. Barlow is under
   the SIL Open Font License 1.1 with no Reserved Font Name (OFL.txt sits in the same folder), which
   allows conversion and redistribution with the license.
2. Prints `size-adjust` and the ascent/descent overrides that make local Arial take up the same room as
   Barlow, measured on the site's own text. Copy them into FALLBACK_FACES in site_chrome.py if they change.
   Without them the page re-wraps when Barlow arrives after the first paint.
"""
import html, io, re
from collections import Counter
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / 'public/assets/aios-cloud'
WEIGHTS = {'Regular': (400, 'Arial.ttf'), 'Medium': (500, 'Arial.ttf'), 'SemiBold': (600, 'Arial Bold.ttf')}
ARIAL_DIRS = [Path('/System/Library/Fonts/Supplemental'), Path('/Library/Fonts'), Path('C:/Windows/Fonts')]


def site_text():
    text = ''
    for page in sorted((ROOT / 'content/pages').glob('*.html')):
        body = re.sub(r'<(script|style)\b.*?</\1>', ' ', page.read_text(), flags=re.S)
        text += html.unescape(re.sub(r'<[^>]+>', ' ', body))
    return Counter(re.sub(r'\s+', ' ', text))


def average_advance(font, counts):
    cmap, hmtx, upm = font.getBestCmap(), font['hmtx'], font['head'].unitsPerEm
    used = {c: n for c, n in counts.items() if ord(c) in cmap}
    return sum(hmtx[cmap[ord(c)]][0] * n for c, n in used.items()) / sum(used.values()) / upm


def find_arial(name):
    for folder in ARIAL_DIRS:
        if (folder / name).exists():
            return TTFont(folder / name)
    raise SystemExit(f'{name} not found; run this on a Mac or Windows machine with Arial installed')


def main():
    counts = site_text()
    for name, (weight, arial_name) in WEIGHTS.items():
        ttf = FONTS / f'Barlow-{name}.ttf'
        font = TTFont(ttf)
        font.flavor = 'woff2'
        out = io.BytesIO()
        font.save(out)
        (FONTS / f'Barlow-{name}.woff2').write_bytes(out.getvalue())
        back, orig = TTFont(io.BytesIO(out.getvalue())), TTFont(ttf)
        assert back.getBestCmap() == orig.getBestCmap() and back.getGlyphOrder() == orig.getGlyphOrder(), name
        missing = sorted(c for c in counts if ord(c) not in orig.getBestCmap() and not c.isspace())
        barlow, arial = average_advance(orig, counts), average_advance(find_arial(arial_name), counts)
        adjust = barlow / arial
        hhea, upm = orig['hhea'], orig['head'].unitsPerEm
        print(f'Barlow-{name}.woff2  {len(out.getvalue())} bytes (ttf {ttf.stat().st_size}), '
              f'{len(orig.getGlyphOrder())} glyphs, {len(orig.getBestCmap())} characters, same as the ttf; '
              f'site characters not covered: {missing or "none"}')
        print(f'  weight {weight} vs {arial_name}: size-adjust:{adjust * 100:.2f}%; '
              f'ascent-override:{hhea.ascent / upm / adjust * 100:.2f}%; '
              f'descent-override:{-hhea.descent / upm / adjust * 100:.2f}%; '
              f'line-gap-override:{hhea.lineGap / upm / adjust * 100:.2f}%')


if __name__ == '__main__':
    main()
