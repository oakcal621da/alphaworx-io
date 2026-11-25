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
PUBLIC_DIR = REPO_ROOT / "public"  # the only folder the static host publishes
OUTPUT_DIR = PUBLIC_DIR / "blog"
SITE_URL = "https://alphaworx.io"

from site_chrome import site_head, site_header, site_footer
from asset_versions import version_assets

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
        site_head(f"{fields['title']} — Alphaworx Insights", fields['excerpt'],
                  f"/blog/{fields['slug']}.html", og_type='article')
        + site_header('insights') +
        '<main id="main"><section class="phero post-hero"><div class="wrap"><div>'
        f"<div class=\"cat\">{fields['category']}</div>"
        f"<h1>{fields['title']}</h1>"
        f"<div class=\"meta\">{fields.get('author', 'Alphaworx Insights')} · {format_byline(fields['date'])}</div>"
        '</div></div></section>'
        '<section class="section"><div class="wrap">'
        f"<div class=\"post-body\">{body_html}</div>"
        "<div class=\"post-cta\">"
        f"<p>{fields.get('cta', 'Connect these ideas to your organization’s next AI decision.')}</p>"
        "<a class=\"primary\" href=\"/advisory.html#contact\">Work with us <span>→</span></a>"
        "</div>"
        "<a class=\"back\" href=\"index.html\">&larr; All insights</a>"
        '</div></section></main>'
        + site_footer()
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
            '<b>05 / Providers</b><b>06 / Ownership</b></div></a>'
        )
    if featured and featured['slug'] == 'introducing-aios-cloud-why-we-built-it':
        feature = (
            f'<a class="research-feature" href="{html.escape(featured["slug"])}.html">'
            '<div><span class="cat">Introducing AIOS Cloud · Platform perspective</span>'
            f'<h2>{html.escape(featured["title"])}</h2><p>{html.escape(featured["excerpt"])}</p>'
            '<span class="research-feature-cta">Explore why we built it ↗</span></div>'
            '<div class="research-feature-map" aria-hidden="true"><span>FROM AMBITION TO ACCOUNTABLE ACTION</span>'
            '<b>01 / Direction</b><b>02 / Evidence</b><b>03 / Decisions</b><b>04 / Follow-through</b>'
            '<small>AIOS Cloud by Alphaworx</small></div></a>'
        )
    cards = "".join(
        f'<a class="post-card" href="{p["slug"]}.html">'
        f'<div class="cat">{p["category"]}</div>'
        f'<h3>{p["title"]}</h3>'
        f'<p>{p["excerpt"]}</p>'
        f'<div class="date">{format_byline(p["date"])}</div>'
        f'</a>'
        for p in ordered if p is not featured
    )
    return (
        site_head('Insights — Alphaworx',
                  'Straight talk on AI strategy, governance and operations from Alphaworx.',
                  '/blog/', css=['/assets/research-feature.css'])
        + site_header('insights') +
        '<main id="main"><section class="phero"><div class="wrap"><div>'
        '<span class="eyebrow"><i></i>Insights</span>'
        '<h1>Straight talk on AI strategy and governance.</h1>'
        '<p class="lead">The thinking behind our platform, '
        'knowledge bases and advisory work, written out.</p>'
        '</div></div></section>'
        '<section class="section"><div class="wrap">'
        + feature + f"<div class=\"post-grid\">{cards}</div>"
        '</div></section></main>'
        + site_footer()
    )


def render_sitemap(posts):
    """Build sitemap.xml covering the homepage, deck, blog index, and every post.

    Regenerated on every build so it can't drift out of sync with the
    actual set of published posts.
    """
    ordered = sorted(posts, key=lambda p: p["date"], reverse=True)
    static_urls = [
        (f"{SITE_URL}/", ordered[0]["date"] if ordered else None),
        (f"{SITE_URL}/aios-cloud.html", "2026-10-23"),
        (f"{SITE_URL}/knowledge-bases.html", None),
        (f"{SITE_URL}/advisory.html", "2026-10-23"),
        (f"{SITE_URL}/about.html", "2026-10-23"),
        (f"{SITE_URL}/partners.html", None),
        (f"{SITE_URL}/careers.html", None),
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    posts = load_posts()
    for fields in posts:
        (OUTPUT_DIR / f"{fields['slug']}.html").write_text(version_assets(render_post(fields, fields["body_html"])))
    (OUTPUT_DIR / "index.html").write_text(version_assets(render_index(posts)))
    (PUBLIC_DIR / "sitemap.xml").write_text(render_sitemap(posts))
    print(f"Generated {len(posts)} post(s) + index into {OUTPUT_DIR}")
    print(f"Generated sitemap.xml with {len(posts) + 9} URLs")


if __name__ == "__main__":
    main()
