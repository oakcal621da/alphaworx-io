from build_blog import parse_frontmatter


def test_parse_frontmatter_extracts_fields_and_body():
    source = (
        "---\n"
        "title: Example Post\n"
        "category: Economics\n"
        "date: 2026-08-17\n"
        "excerpt: One line summary.\n"
        "slug: example-post\n"
        "---\n"
        "First paragraph.\n"
        "\n"
        "Second paragraph.\n"
    )

    fields, body = parse_frontmatter(source)

    assert fields == {
        "title": "Example Post",
        "category": "Economics",
        "date": "2026-08-17",
        "excerpt": "One line summary.",
        "slug": "example-post",
    }
    assert body == "First paragraph.\n\nSecond paragraph."


def test_parse_frontmatter_rejects_missing_opening_delimiter():
    try:
        parse_frontmatter("title: no delimiter\n")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "frontmatter" in str(e)


from build_blog import markdown_to_html


def test_markdown_to_html_wraps_paragraphs():
    html = markdown_to_html("First paragraph.\n\nSecond paragraph.")
    assert html == "<p>First paragraph.</p>\n<p>Second paragraph.</p>"


def test_markdown_to_html_converts_blockquote():
    html = markdown_to_html("> A quoted line.")
    assert html == "<blockquote>A quoted line.</blockquote>"


def test_markdown_to_html_converts_bold():
    html = markdown_to_html("This has **bold text** in it.")
    assert html == "<p>This has <b>bold text</b> in it.</p>"


from build_blog import format_byline, render_post, render_index, render_sitemap


def test_format_byline_renders_month_and_year():
    assert format_byline("2026-08-17") == "August 2026"


def test_render_post_includes_title_category_and_body():
    fields = {
        "title": "Example Post",
        "category": "Economics",
        "date": "2026-08-17",
        "excerpt": "One line summary.",
        "slug": "example-post",
    }
    html = render_post(fields, "<p>Body text.</p>")

    assert "<title>Example Post — Alphaworx Insights</title>" in html
    assert "<div class=\"cat\">Economics</div>" in html
    assert "<h2>Example Post</h2>" in html
    assert "Alphaworx Insights · August 2026" in html
    assert "<p>Body text.</p>" in html
    assert 'href="../index.html"' in html


def test_render_index_lists_every_post_with_link():
    posts = [
        {
            "title": "Example Post",
            "category": "Economics",
            "date": "2026-08-17",
            "excerpt": "One line summary.",
            "slug": "example-post",
        },
        {
            "title": "Second Post",
            "category": "Vendor Strategy",
            "date": "2026-08-10",
            "excerpt": "Another summary.",
            "slug": "second-post",
        },
    ]
    html = render_index(posts)

    assert "Example Post" in html
    assert "Second Post" in html
    assert 'href="example-post.html"' in html
    assert 'href="second-post.html"' in html
    # Newest post first
    assert html.index("Example Post") < html.index("Second Post")


def test_render_sitemap_lists_static_pages_and_every_post():
    posts = [
        {"slug": "example-post", "date": "2026-08-17"},
        {"slug": "second-post", "date": "2026-08-10"},
    ]
    xml = render_sitemap(posts)

    assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "<urlset" in xml
    assert "<loc>https://alphaworx-io.onrender.com/</loc>" in xml
    assert "<loc>https://alphaworx-io.onrender.com/deck.html</loc>" in xml
    assert "<loc>https://alphaworx-io.onrender.com/blog/</loc>" in xml
    assert "<loc>https://alphaworx-io.onrender.com/blog/example-post.html</loc>" in xml
    assert "<loc>https://alphaworx-io.onrender.com/blog/second-post.html</loc>" in xml
    assert "<lastmod>2026-08-17</lastmod>" in xml
