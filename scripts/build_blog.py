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
    '<a href="../index.html#why">Why it matters</a>'
    '<a href="../index.html#value">The value gap</a>'
    '<a href="../index.html#help">How we help</a>'
    '<a href="index.html" class="on">Insights</a>'
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

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800'
    '&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)

STYLE = """
:root { --paper:#F7F8FA; --surface:#fff; --ink:#0B0C0E; --ink2:#454952; --ink3:#8A8F99; --rule:#E1E4E9; --rule2:#EEF0F3;
  --cyan:#06B6D4; --cobalt:#2563EB; --amber:#F59E0B; --coral:#F43F5E; --violet:#7C3AED; --teal:#0D9488; --hue:var(--cobalt);
  --display:'Bricolage Grotesque','Helvetica Neue',Arial,sans-serif; --body:'Instrument Sans',-apple-system,'Helvetica Neue',Arial,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace; --ease:cubic-bezier(.2,.7,.2,1); }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:var(--body); background:var(--paper); color:var(--ink); -webkit-font-smoothing:antialiased; line-height:1.5; }
.wrap { max-width:860px; margin:0 auto; padding:0 32px; }
header { position:sticky; top:0; background:rgba(247,248,250,.72); backdrop-filter:blur(14px) saturate(1.4); border-bottom:1px solid rgba(11,12,14,.08); z-index:10; }
header .row { display:flex; align-items:center; justify-content:space-between; height:64px; }
header .brand { display:flex; align-items:center; gap:12px; text-decoration:none; color:inherit; }
header img.mark { width:28px; height:28px; border-radius:7px; }
header .word { font-family:var(--display); font-size:14px; letter-spacing:.12em; font-weight:600; }
header .word .dim { color:var(--ink3); font-weight:400; }
header nav { display:flex; gap:26px; }
header nav a { font-size:13.5px; color:var(--ink2); text-decoration:none; background:linear-gradient(90deg,var(--cyan),var(--cobalt)) no-repeat 0 100%/0 2px; transition:background-size .3s var(--ease), color .2s; padding-bottom:2px; }
header nav a:hover, header nav a.on { color:var(--ink); background-size:100% 2px; }
.label { font-family:var(--mono); font-size:12px; letter-spacing:.08em; color:var(--ink3); text-transform:uppercase; margin-bottom:18px; display:flex; align-items:center; gap:10px; }
.label::before { content:""; width:18px; height:2px; border-radius:2px; background:linear-gradient(90deg,var(--cyan),var(--cobalt)); }
.grad-text { background:linear-gradient(90deg,var(--cyan),var(--cobalt) 45%,var(--coral) 80%,var(--amber)); background-size:200% 100%; -webkit-background-clip:text; background-clip:text; color:transparent; animation:sheen 6s linear infinite; }
@keyframes sheen { to { background-position:200% 0; } }
.list-hero { position:relative; padding:72px 0 44px; overflow:hidden; isolation:isolate; }
.list-hero::before { content:""; position:absolute; inset:-20% -10%; z-index:-1; filter:blur(70px); opacity:.55; pointer-events:none;
  background:radial-gradient(40% 50% at 80% 30%, rgba(6,182,212,.7), transparent 70%), radial-gradient(35% 45% at 95% 80%, rgba(244,63,94,.45), transparent 70%), radial-gradient(35% 45% at 60% 90%, rgba(245,158,11,.45), transparent 70%); }
.list-hero h2 { font-family:var(--display); font-weight:500; font-size:clamp(32px,4vw,48px); letter-spacing:-.025em; line-height:1.05; max-width:620px; margin-bottom:14px; text-wrap:balance; }
.list-hero p { font-size:16px; color:var(--ink2); max-width:520px; line-height:1.65; }
.post-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; padding:0 0 72px; }
.post-card { position:relative; border:1px solid var(--rule); border-radius:14px; padding:26px 24px; text-decoration:none; color:inherit; display:block; background:var(--surface); overflow:hidden; transition:transform .3s var(--ease), box-shadow .3s var(--ease); }
.post-card::before { content:""; position:absolute; inset:-1px; border-radius:15px; padding:1px; background:conic-gradient(from var(--ang,0deg),var(--cyan),var(--cobalt),var(--coral),var(--amber),var(--cyan)); -webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask-composite:exclude; opacity:0; transition:opacity .35s; pointer-events:none; }
.post-card:hover { transform:translateY(-4px); box-shadow:0 28px 60px -34px rgba(11,12,14,.4); }
.post-card:hover::before { opacity:1; animation:spin 3s linear infinite; }
@property --ang { syntax:'<angle>'; inherits:false; initial-value:0deg; }
@keyframes spin { to { --ang:360deg; } }
.post-card .cat { font-family:var(--mono); font-size:11px; letter-spacing:.08em; color:var(--hue); text-transform:uppercase; margin-bottom:12px; }
.post-card h3 { font-family:var(--display); font-size:17px; font-weight:600; letter-spacing:-.01em; line-height:1.35; margin-bottom:10px; }
.post-card p { font-size:13.5px; color:var(--ink3); line-height:1.6; margin-bottom:14px; }
.post-card .date { font-family:var(--mono); font-size:11px; letter-spacing:.04em; color:var(--ink3); }
.post-hero { padding:72px 0 36px; }
.post-hero .cat { font-family:var(--mono); font-size:12px; letter-spacing:.08em; color:var(--hue); text-transform:uppercase; margin-bottom:16px; display:flex; align-items:center; gap:10px; }
.post-hero .cat::before { content:""; width:18px; height:2px; border-radius:2px; background:var(--hue); }
.post-hero h2 { font-family:var(--display); font-weight:500; font-size:clamp(32px,4vw,46px); letter-spacing:-.025em; line-height:1.08; margin-bottom:14px; max-width:680px; text-wrap:balance; }
.post-hero .meta { font-family:var(--mono); font-size:12px; letter-spacing:.04em; color:var(--ink3); }
.post-body { padding-bottom:50px; font-size:16.5px; line-height:1.8; color:var(--ink2); max-width:660px; }
.post-body p { margin-bottom:20px; }
.post-body b { color:var(--ink); }
.post-body blockquote { border-left:3px solid var(--hue); padding-left:18px; font-family:var(--display); font-weight:500; font-size:20px; letter-spacing:-.01em; color:var(--ink); margin:28px 0; line-height:1.4; }
.post-cta { position:relative; border:1px solid var(--rule); border-radius:14px; background:var(--surface); padding:24px 26px; margin-top:10px; display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; max-width:660px; overflow:hidden; }
.post-cta::before { content:""; position:absolute; inset:0; background:radial-gradient(420px 200px at 100% 0%, color-mix(in srgb, var(--hue) 18%, transparent), transparent 65%); pointer-events:none; }
.post-cta p { font-size:14px; color:var(--ink2); max-width:400px; position:relative; }
.post-cta a.work { position:relative; font-size:13.5px; font-weight:600; color:#fff; background:var(--ink); padding:12px 18px; border-radius:10px; text-decoration:none; white-space:nowrap; }
.back { display:inline-block; margin-top:28px; font-size:14px; font-weight:500; color:var(--ink); text-decoration:none; background:linear-gradient(90deg,var(--cyan),var(--cobalt)) no-repeat 0 100%/100% 2px; padding-bottom:3px; }
footer { padding:36px 0 44px; border-top:1px solid var(--rule); margin-top:24px; }
footer .row { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
footer .meta { font-size:13px; color:var(--ink3); }
footer a { color:var(--ink); text-decoration:none; font-size:13px; }
.h-econ{--hue:var(--amber)} .h-data{--hue:var(--coral)} .h-vendor{--hue:var(--violet)} .h-adopt{--hue:var(--cobalt)} .h-sec{--hue:var(--teal)} .h-rel{--hue:var(--cyan)} .h-ops{--hue:var(--cobalt)} .h-gov{--hue:var(--violet)}
@media (max-width:700px){ .post-grid{grid-template-columns:1fr;} }
@media (max-width:640px){ header nav{display:none;} }
@media (prefers-reduced-motion:reduce){ *,*::before,*::after{animation:none!important; transition:none!important;} }
"""

HUE_CLASS = {
    "economics": "h-econ", "data exposure": "h-data", "vendor strategy": "h-vendor",
    "adoption": "h-adopt", "security": "h-sec", "reliability": "h-rel",
    "operating model": "h-ops", "governance": "h-gov",
}


def hue_for(category):
    """Map a post category to the site's per-topic accent class (defaults to cobalt)."""
    key = category.strip().lower()
    for name, cls in HUE_CLASS.items():
        if name in key:
            return cls
    return "h-adopt"


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
        "<link rel=\"icon\" type=\"image/png\" href=\"../assets/mark.png\">"
        + FONTS +
        f"<style>{STYLE}</style></head><body class=\"{hue_for(fields['category'])}\">"
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
        f'<a class="post-card {hue_for(p["category"])}" href="{p["slug"]}.html">'
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
        "<link rel=\"icon\" type=\"image/png\" href=\"../assets/mark.png\">"
        + FONTS +
        f"<style>{STYLE}</style></head><body>"
        + HEADER +
        "<div class=\"wrap\"><div class=\"list-hero\">"
        "<div class=\"label\">Insights</div>"
        "<h2>Straight talk on <span class=\"grad-text\">enterprise AI strategy.</span></h2>"
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
