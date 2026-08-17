#!/usr/bin/env python3
"""Generate blog/index.html and blog/<slug>.html from content/blog/*.md.

No third-party dependencies — stdlib only, matching the rest of this
static site's zero-build-step approach.
"""
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
