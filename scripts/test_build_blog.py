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
