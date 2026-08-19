#!/usr/bin/env python3
"""Generate blog/index.html and blog/<slug>.html from content/blog/*.md.

No third-party dependencies — stdlib only, matching the rest of this
static site's zero-build-step approach.
"""
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "blog"
OUTPUT_DIR = REPO_ROOT / "blog"
SITE_URL = "https://alphaworx-io.onrender.com"

NAV = (
    '<nav>'
    '<a href="../index.html#help">How we help</a>'
    '<a href="index.html" style="color:#111;font-weight:600;">Insights</a>'
    '<a href="../index.html#why">Why it matters</a>'
    '<a href="../index.html#about">About</a>'
    '</nav>'
)

HEADER = (
    '<header><div class="wrap row">'
    '<a class="brand" href="../index.html">'
    '<img class="mark" src="../assets/mark.png" alt="Alphaworx">'
    '<div class="word">ALPHAWORX<span class="dim">.IO</span></div>'
    '</a>' + NAV + '</div></header>'
)

FOOTER = (
    '<footer><div class="wrap"><div class="row">'
    '<div class="meta">&copy; 2026 Alphaworx Ltd</div>'
    '<a href="mailto:info@alphaworx.io">info@alphaworx.io</a>'
    '</div></div></footer>'
)

STYLE = """
* { box-sizing: border-box; margin:0; padding:0; }
body { font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; background:#fff; color:#111; -webkit-font-smoothing:antialiased; }
.wrap { max-width:820px; margin:0 auto; padding:0 32px; }
header { position:sticky; top:0; background:rgba(255,255,255,0.9); backdrop-filter:blur(6px); border-bottom:1px solid #f0f0f0; z-index:10; }
header .row { display:flex; align-items:center; justify-content:space-between; padding:18px 0; }
header .brand { display:flex; align-items:center; gap:12px; text-decoration:none; color:inherit; }
header img.mark { width:30px; height:30px; border-radius:8px; }
header .word { font-size:13px; letter-spacing:0.16em; font-weight:600; }
header .word .dim { color:#a3a3a3; font-weight:400; }
header nav { display:flex; gap:26px; }
header nav a { font-size:12.5px; color:#6b6b6e; text-decoration:none; }
header nav a:hover { color:#111; }
.label { font-size:11px; letter-spacing:0.14em; color:#a3a3a3; text-transform:uppercase; margin-bottom:20px; }
.list-hero { padding:60px 0 40px; }
.list-hero h2 { font-size:30px; font-weight:300; letter-spacing:-0.02em; max-width:520px; margin-bottom:12px; }
.list-hero p { font-size:14.5px; color:#5b5b5e; max-width:480px; line-height:1.65; }
.post-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; padding:0 0 60px; }
.post-card { border:1px solid #ececec; border-radius:14px; padding:26px 24px; text-decoration:none; color:inherit; display:block; }
.post-card .cat { font-size:10.5px; letter-spacing:0.08em; color:#a3a3a3; text-transform:uppercase; margin-bottom:12px; }
.post-card h3 { font-size:16px; font-weight:600; line-height:1.4; margin-bottom:10px; }
.post-card p { font-size:13px; color:#888; line-height:1.6; margin-bottom:14px; }
.post-card .date { font-size:11px; color:#bbb; }
.post-hero { padding:60px 0 36px; }
.post-hero .cat { font-size:11px; letter-spacing:0.1em; color:#a3a3a3; text-transform:uppercase; margin-bottom:16px; }
.post-hero h2 { font-size:30px; font-weight:300; letter-spacing:-0.02em; line-height:1.3; margin-bottom:14px; max-width:640px; }
.post-hero .meta { font-size:12.5px; color:#aaa; }
.post-body { padding-bottom:50px; font-size:15px; line-height:1.8; color:#333; max-width:640px; }
.post-body p { margin-bottom:18px; }
.post-body blockquote { border-left:2px solid #111; padding-left:18px; font-size:16px; color:#111; margin:26px 0; }
.post-cta { border-top:1px solid #ececec; border-bottom:1px solid #ececec; padding:26px 0; margin-top:10px; display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; max-width:640px; }
.post-cta p { font-size:13.5px; color:#5b5b5e; max-width:400px; }
.post-cta a.work { font-size:13px; color:#fff; background:#111; padding:10px 18px; border-radius:6px; text-decoration:none; white-space:nowrap; }
.back { display:inline-block; margin-top:26px; font-size:13px; color:#111; text-decoration:none; border-bottom:1px solid #111; }
footer { padding:60px 0 50px; }
footer .row { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
footer .meta { font-size:12.5px; color:#9a9a9a; }
footer a { color:#111; text-decoration:none; font-size:12.5px; border-bottom:1px solid #d6d6d6; }
@media (max-width:700px){ .post-grid{grid-template-columns:1fr;} }
@media (max-width:640px){ header nav{display:none;} }
"""


def parse_frontmatter(text):
    """Split a post source into (fields dict, body markdown string).

    Frontmatter is delimited by '---' lines and holds flat 'key: value'
    pairs — no nested structures needed for this site's posts.
    """
    if not text.startswith("---\n"):
        raise ValueError("post is missing frontmatter opening '---'")
    end = text.index("\n---\n", 4)
    frontmatter_block = text[4:end]
    body = text[end + 5:].strip("\n")

    fields = {}
    for line in frontmatter_block.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, body


def markdown_to_html(body):
    """Convert a small Markdown subset to HTML.

    Supports: blank-line-separated paragraphs, a '> ' prefix for a
    single-paragraph blockquote, and **bold** inline text. That's the
    full set this site's posts use — anything more isn't needed yet.
    """
    blocks = re.split(r"\n\s*\n", body.strip())
    html_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        block = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", block)
        if block.startswith("> "):
            html_blocks.append(f"<blockquote>{block[2:].strip()}</blockquote>")
        else:
            html_blocks.append(f"<p>{block}</p>")
    return "\n".join(html_blocks)


def format_byline(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %Y")


def render_post(fields, body_html):
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{fields['title']} — Alphaworx Insights</title>"
        f"<meta name=\"description\" content=\"{fields['excerpt']}\">"
        f"<style>{STYLE}</style></head><body>"
        + HEADER +
        "<div class=\"wrap\"><div class=\"post-hero\">"
        f"<div class=\"cat\">{fields['category']}</div>"
        f"<h2>{fields['title']}</h2>"
        f"<div class=\"meta\">Alphaworx Insights · {format_byline(fields['date'])}</div>"
        "</div>"
        f"<div class=\"post-body\">{body_html}</div>"
        "<div class=\"post-cta\">"
        "<p>This is exactly the kind of gap we help close before it becomes a production incident.</p>"
        "<a class=\"work\" href=\"mailto:info@alphaworx.io\">Work with us</a>"
        "</div>"
        "<a class=\"back\" href=\"index.html\">&larr; All insights</a>"
        "</div>"
        + FOOTER +
        "</body></html>"
    )


def render_index(posts):
    ordered = sorted(posts, key=lambda p: p["date"], reverse=True)
    cards = "".join(
        f'<a class="post-card" href="{p["slug"]}.html">'
        f'<div class="cat">{p["category"]}</div>'
        f'<h3>{p["title"]}</h3>'
        f'<p>{p["excerpt"]}</p>'
        f'<div class="date">{format_byline(p["date"])}</div>'
        f'</a>'
        for p in ordered
    )
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>Insights — Alphaworx</title>"
        "<meta name=\"description\" content=\"Straight talk on enterprise AI strategy.\">"
        f"<style>{STYLE}</style></head><body>"
        + HEADER +
        "<div class=\"wrap\"><div class=\"list-hero\">"
        "<div class=\"label\">Insights</div>"
        "<h2>Straight talk on enterprise AI strategy.</h2>"
        "<p>No hype, no vendor pitch decks — the same diagnostic thinking behind our advisory work, written out.</p>"
        "</div>"
        f"<div class=\"post-grid\">{cards}</div>"
        "</div>"
        + FOOTER +
        "</body></html>"
    )


def render_sitemap(posts):
    """Build sitemap.xml covering the homepage, deck, blog index, and every post.

    Regenerated on every build so it can't drift out of sync with the
    actual set of published posts.
    """
    ordered = sorted(posts, key=lambda p: p["date"], reverse=True)
    static_urls = [
        (f"{SITE_URL}/", ordered[0]["date"] if ordered else None),
        (f"{SITE_URL}/deck.html", None),
        (f"{SITE_URL}/blog/", ordered[0]["date"] if ordered else None),
    ]
    entries = []
    for loc, lastmod in static_urls:
        lastmod_tag = f"<lastmod>{lastmod}</lastmod>" if lastmod else ""
        entries.append(f"<url><loc>{loc}</loc>{lastmod_tag}</url>")
    for p in ordered:
        entries.append(
            f"<url><loc>{SITE_URL}/blog/{p['slug']}.html</loc>"
            f"<lastmod>{p['date']}</lastmod></url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries) +
        "\n</urlset>\n"
    )


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    posts = []
    for md_path in sorted(CONTENT_DIR.glob("*.md")):
        fields, body = parse_frontmatter(md_path.read_text())
        body_html = markdown_to_html(body)
        (OUTPUT_DIR / f"{fields['slug']}.html").write_text(render_post(fields, body_html))
        posts.append(fields)
    (OUTPUT_DIR / "index.html").write_text(render_index(posts))
    (REPO_ROOT / "sitemap.xml").write_text(render_sitemap(posts))
    print(f"Generated {len(posts)} post(s) + index into {OUTPUT_DIR}")
    print(f"Generated sitemap.xml with {len(posts) + 3} URLs")


if __name__ == "__main__":
    main()
