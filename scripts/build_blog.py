#!/usr/bin/env python3
"""Generate blog/index.html and blog/<slug>.html from content/blog/*.md.

No third-party dependencies — stdlib only, matching the rest of this
static site's zero-build-step approach.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "blog"
OUTPUT_DIR = REPO_ROOT / "blog"


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
