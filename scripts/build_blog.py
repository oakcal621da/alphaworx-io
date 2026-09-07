#!/usr/bin/env python3
"""Generate blog/index.html and blog/<slug>.html from content/blog/*.md.

No third-party dependencies — stdlib only, matching the rest of this
static site's zero-build-step approach.
"""
import re
import html
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "blog"
OUTPUT_DIR = REPO_ROOT / "blog"
SITE_URL = "https://alphaworx.io"

from site_chrome import HEADER, FOOTER, FONTS, SOCIAL

STYLE = ""  # Layout is shared in assets/editorial.css.

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
    """Render paragraphs, headings, quotes, bold, and HTTPS source links."""
    def inline(text):
        text = html.escape(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        return re.sub(r"\[([^\]]+)\]\((https://[^\s)]+)\)", r'<a href="\2">\1</a>', text)
    output=[]
    for block in re.split(r"\n\s*\n", body.strip()):
        block=block.strip()
        if not block:
            continue
        if block.startswith('## '):
            output.append('<h2>'+inline(block[3:])+'</h2>')
        elif block.startswith('> '):
            output.append('<blockquote>'+inline(block[2:])+'</blockquote>')
        else:
            output.append('<p>'+inline(block)+'</p>')
    return "\n".join(output)


def format_byline(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %Y")


def render_post(fields, body_html):
    if fields["slug"] == "twelve-first-principles-enterprise-ai":
        from render_principles import render_principles
        return render_principles(fields, body_html)
    from render_insight import guide_for, render_insight
    guide = guide_for(fields["slug"])
    if guide:
        return render_insight(fields, body_html, guide)
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{fields['title']} — Alphaworx Insights</title>"
        f"<meta name=\"description\" content=\"{fields['excerpt']}\">"
        f'<link rel="canonical" href="{SITE_URL}/blog/{fields["slug"]}.html">'
        "<link rel=\"icon\" type=\"image/png\" href=\"../assets/mark.png\">"
        + FONTS + SOCIAL +
        '<link rel="stylesheet" href="/assets/editorial.css?v=review-1"><link rel="stylesheet" href="/assets/essay.css"></head><body>'
        + HEADER +
        "<main id=\"main\" class=\"wrap\"><div class=\"post-hero\">"
        f"<div class=\"cat\">{fields['category']}</div>"
        f"<h1>{fields['title']}</h1>"
        f"<div class=\"meta\">{fields.get('author', 'Alphaworx Insights')} · {format_byline(fields['date'])}</div>"
        "</div>"
        f"<div class=\"post-body\">{body_html}</div>"
        "<div class=\"post-cta\">"
        f"<p>{fields.get('cta', 'Connect these ideas to your organization’s next AI decision.')}</p>"
        "<a class=\"work\" href=\"/#contact\">Work with us</a>"
        "</div>"
        "<a class=\"back\" href=\"index.html\">&larr; All insights</a>"
        "</main>"
        + FOOTER +
        "</body></html>"
    )


def render_index(posts):
    ordered = sorted(posts, key=lambda p: p["date"], reverse=True)
    featured = next((p for p in ordered if p.get('featured') == 'true'), None)
    feature = ''
    if featured:
        feature = (
            f'<a class="research-feature" href="{html.escape(featured["slug"])}.html">'
            '<div><span class="cat">Featured research · Executive briefing</span>'
            f'<h2>{html.escape(featured["title"])}</h2><p>{html.escape(featured["excerpt"])}</p>'
            '<span class="research-feature-cta">Explore the briefing ↗</span></div>'
            '<div class="research-feature-map" aria-hidden="true"><span>THE OPERATING QUESTIONS</span>'
            '<b>01 / Value</b><b>02 / Data</b><b>03 / Actions</b><b>04 / Reliability</b>'
            '<b>05 / Providers</b><b>06 / Ownership</b><small>Adapted from AIR research</small></div></a>'
        )
    cards = "".join(
        f'<a class="post-card {hue_for(p["category"])}" href="{p["slug"]}.html">'
        f'<div class="cat">{p["category"]}</div>'
        f'<h3>{p["title"]}</h3>'
        f'<p>{p["excerpt"]}</p>'
        f'<div class="date">{format_byline(p["date"])}</div>'
        f'</a>'
        for p in ordered if p is not featured
    )
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        '<title>Insights — Alphaworx</title><link rel="canonical" href="https://alphaworx.io/blog/">'
        "<meta name=\"description\" content=\"Straight talk on enterprise AI strategy.\">"
        "<link rel=\"icon\" type=\"image/png\" href=\"../assets/mark.png\">"
        + FONTS + SOCIAL +
        '<link rel="stylesheet" href="/assets/editorial.css?v=review-1"><link rel="stylesheet" href="/assets/essay.css"><link rel="stylesheet" href="/assets/research-feature.css?v=1"></head><body>'
        + HEADER +
        "<main id=\"main\" class=\"wrap\"><div class=\"list-hero\">"
        "<div class=\"label\">Insights</div>"
        "<h1>Straight talk on <span class=\"grad-text\">enterprise AI strategy.</span></h1>"
        "<p>No hype, no vendor pitch decks — the same diagnostic thinking behind our advisory work, written out.</p>"
        "</div>"
        + feature + f"<div class=\"post-grid\">{cards}</div>"
        "</main>"
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
        (f"{SITE_URL}/privacy/", None),
        (f"{SITE_URL}/schedule/", "2026-09-07"),
        (f"{SITE_URL}/blog/", ordered[0]["date"] if ordered else None),
    ]
    entries = []
    for loc, lastmod in static_urls:
        lastmod_tag = f"<lastmod>{lastmod}</lastmod>" if lastmod else ""
        entries.append(f"<url><loc>{loc}</loc>{lastmod_tag}</url>")
    for p in ordered:
        entries.append(
            f"<url><loc>{SITE_URL}/blog/{p['slug']}.html</loc>"
            f"<lastmod>{p.get('updated', p['date'])}</lastmod></url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries) +
        "\n</urlset>\n"
    )


def load_posts():
    posts = []
    for md_path in sorted(CONTENT_DIR.iterdir()):
        if md_path.suffix not in {".md", ".html"}:
            continue
        fields, body = parse_frontmatter(md_path.read_text())
        fields["body_html"] = body if md_path.suffix == ".html" else markdown_to_html(body)
        posts.append(fields)
    return posts


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    posts = load_posts()
    for fields in posts:
        (OUTPUT_DIR / f"{fields['slug']}.html").write_text(render_post(fields, fields["body_html"]))
    (OUTPUT_DIR / "index.html").write_text(render_index(posts))
    (REPO_ROOT / "sitemap.xml").write_text(render_sitemap(posts))
    print(f"Generated {len(posts)} post(s) + index into {OUTPUT_DIR}")
    print(f"Generated sitemap.xml with {len(posts) + 5} URLs")


if __name__ == "__main__":
    main()
