# AI Strategy Repositioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the Alphaworx homepage around enterprise AI strategy, stand up a blog with 4 launch posts adapted from the AI Strategy Playbook, and build a presentable/printable "why AI strategy matters" slide deck — all as plain static HTML deployed to the existing Render static site.

**Architecture:** Everything stays static, no server, no build step on Render. The homepage is a single hand-edited `index.html`. Blog posts are authored as Markdown with flat frontmatter under `content/blog/`, converted to static HTML by a small dependency-free Python generator (`scripts/build_blog.py`) whose output (`blog/index.html`, `blog/<slug>.html`) is committed like any other file. The deck is a single hand-authored `deck.html` with inline JS for slide navigation and a print stylesheet for PDF export.

**Tech Stack:** Plain HTML/CSS/JS, Python 3 (stdlib only, no pip installs) for the blog generator, pytest for the generator's unit tests.

---

## Reference: design spec

Full design is in [`docs/superpowers/specs/2026-08-17-ai-strategy-reposition-design.md`](../specs/2026-08-17-ai-strategy-reposition-design.md). Read it before starting if you weren't in the brainstorming session — it has the rationale for the copy and structure decisions below.

## File Structure

- Modify: `index.html` — full content replacement (Task 1)
- Create: `scripts/build_blog.py` — the blog generator (Tasks 3–5)
- Create: `scripts/test_build_blog.py` — pytest unit tests for the generator (Tasks 3–5)
- Create: `content/blog/why-ai-pilots-stall.md` (Task 2)
- Create: `content/blog/shadow-ai-biggest-exposure.md` (Task 6)
- Create: `content/blog/you-dont-control-the-control-plane.md` (Task 6)
- Create: `content/blog/the-90-day-platform-stand-up.md` (Task 6)
- Generate (via script, then commit): `blog/index.html`, `blog/why-ai-pilots-stall.html`, `blog/shadow-ai-biggest-exposure.html`, `blog/you-dont-control-the-control-plane.html`, `blog/the-90-day-platform-stand-up.html`
- Create: `deck.html` (Tasks 7–8)

All paths are relative to the repo root: `/Users/DSA/Seneca Projects/Alphaworx Website`.

---

## Task 1: Repositioned homepage

**Files:**
- Modify: `index.html` (full replacement)

- [ ] **Step 1: Replace `index.html` with the repositioned content**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alphaworx — Enterprise AI Strategy</title>
<meta name="description" content="The AI strategy gap is still small. It won't stay that way. Alphaworx helps enterprise leaders build a governed AI strategy — before the wrong one costs them.">
<link rel="icon" type="image/png" href="/assets/mark.png">
<meta property="og:title" content="Alphaworx — Enterprise AI Strategy">
<meta property="og:description" content="The AI strategy gap is still small. It won't stay that way. Alphaworx helps enterprise leaders build a governed AI strategy — before the wrong one costs them.">
<meta property="og:image" content="https://alphaworx-io.onrender.com/assets/mark.png">
<meta property="og:url" content="https://alphaworx-io.onrender.com">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<style>
  * { box-sizing: border-box; margin:0; padding:0; }
  body {
    font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
    background:#ffffff; color:#111111;
    -webkit-font-smoothing: antialiased;
  }
  .wrap { max-width: 880px; margin: 0 auto; padding: 0 32px; }

  header { position:sticky; top:0; background:rgba(255,255,255,0.9); backdrop-filter:blur(6px); border-bottom:1px solid #f0f0f0; z-index:10; }
  header .row { display:flex; align-items:center; justify-content:space-between; padding:18px 0; }
  header .brand { display:flex; align-items:center; gap:12px; }
  header img.mark { width:30px; height:30px; border-radius:8px; }
  header .word { font-size:13px; letter-spacing:0.16em; font-weight:600; }
  header .word .dim { color:#a3a3a3; font-weight:400; }
  header nav { display:flex; gap:26px; }
  header nav a { font-size:12.5px; color:#6b6b6e; text-decoration:none; letter-spacing:0.01em; }
  header nav a:hover { color:#111; }
  @media (max-width:640px){ header nav{display:none;} }

  .hero { padding: 100px 0 90px; }
  .eyebrow { font-size:11px; letter-spacing:0.14em; color:#a3a3a3; text-transform:uppercase; margin-bottom:16px; }
  .hero h1 {
    font-size: 44px; font-weight:300; letter-spacing:-0.02em; line-height:1.2;
    max-width: 620px;
  }
  .hero p.sub {
    margin-top:22px; max-width: 520px; font-size:17px; line-height:1.6; color:#5b5b5e; font-weight:400;
  }
  .hero .cta { margin-top:34px; display:flex; gap:16px; flex-wrap:wrap; }
  .hero a.btn {
    display:inline-block; background:#111; color:#fff; text-decoration:none;
    font-size:13px; letter-spacing:0.04em; padding:13px 22px; border-radius:6px;
  }
  .hero a.link {
    display:inline-flex; align-items:center; color:#111; text-decoration:none;
    font-size:13px; letter-spacing:0.02em; padding:13px 4px; border-bottom:1px solid transparent;
  }
  .hero a.link:hover { border-bottom-color:#111; }

  .divider { border-top:1px solid #ececec; }
  section { padding: 90px 0; }
  .label { font-size:11px; letter-spacing:0.14em; color:#a3a3a3; text-transform:uppercase; margin-bottom:20px; }
  h2.h { font-size:28px; font-weight:400; letter-spacing:-0.01em; max-width:560px; line-height:1.3; margin-bottom:20px; }
  p.lead { font-size:15.5px; line-height:1.75; color:#3d3d40; max-width:640px; }

  .findings { margin-top:36px; display:flex; flex-direction:column; }
  .finding { display:flex; gap:20px; padding:20px 0; border-top:1px solid #ececec; }
  .finding:last-child { border-bottom:1px solid #ececec; }
  .finding .n { font-size:13px; color:#c4c4c4; font-weight:600; flex:none; width:20px; padding-top:2px; }
  .finding .t { font-size:14.5px; line-height:1.6; color:#2c2c2e; }
  .finding .t b { font-weight:600; color:#111; }
  .findings-cta { margin-top:24px; }
  .findings-cta a { font-size:13px; color:#111; text-decoration:none; border-bottom:1px solid #111; }

  .offer-grid { display:grid; grid-template-columns:1fr 1fr; gap:22px; margin-top:36px; }
  .offer { border:1px solid #ececec; border-radius:14px; padding:28px 26px; }
  .offer .step { font-size:11px; letter-spacing:0.08em; color:#a3a3a3; text-transform:uppercase; margin-bottom:8px; }
  .offer h4 { font-size:15px; font-weight:600; margin-bottom:10px; }
  .offer p { font-size:13.5px; color:#5b5b5e; line-height:1.6; }

  .insight-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-top:36px; }
  .insight { border:1px solid #ececec; border-radius:14px; padding:22px 20px; text-decoration:none; display:block; color:inherit; }
  .insight .cat { font-size:10.5px; letter-spacing:0.08em; color:#a3a3a3; text-transform:uppercase; margin-bottom:10px; }
  .insight h4 { font-size:14px; font-weight:600; line-height:1.4; margin-bottom:8px; }
  .insight p { font-size:12.5px; color:#888; line-height:1.5; }
  .insight-cta { margin-top:24px; }
  .insight-cta a { font-size:13px; color:#111; text-decoration:none; border-bottom:1px solid #111; }

  .proof-strip { margin-top:0; border-top:1px solid #ececec; padding:26px 0; display:flex; justify-content:space-between; align-items:center; gap:20px; flex-wrap:wrap; }
  .proof-strip p { font-size:14px; color:#3d3d40; line-height:1.6; max-width:560px; }
  .proof-strip a { font-size:13px; color:#111; text-decoration:none; border-bottom:1px solid #111; white-space:nowrap; }

  .products-compact { padding:26px 0 0; display:grid; grid-template-columns:1fr 1fr; gap:22px; }
  .products-compact .p { }
  .products-compact .tag { font-size:11px; letter-spacing:0.08em; color:#111; font-weight:600; margin-bottom:4px; }
  .products-compact p { font-size:13px; color:#5b5b5e; line-height:1.55; }

  .about-row { display:flex; gap:48px; margin-top:36px; flex-wrap:wrap; }
  .about-row .facts { min-width:200px; display:flex; flex-direction:column; gap:14px; }
  .about-row .facts .fact .k { font-size:11px; letter-spacing:0.08em; color:#a3a3a3; text-transform:uppercase; margin-bottom:3px; }
  .about-row .facts .fact .v { font-size:14px; color:#111; }
  .about-row p { font-size:15px; line-height:1.75; color:#3d3d40; max-width:520px; flex:1; min-width:260px; }

  footer { padding: 60px 0 50px; }
  footer .row { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
  footer .meta { font-size:12.5px; color:#9a9a9a; }
  footer a { color:#111; text-decoration:none; font-size:12.5px; border-bottom:1px solid #d6d6d6; }

  @media (max-width:700px){ .offer-grid,.insight-grid,.products-compact{grid-template-columns:1fr;} .hero h1{font-size:32px;} h2.h{font-size:23px;} }
</style>
</head>
<body>

  <header>
    <div class="wrap row">
      <div class="brand">
        <img class="mark" src="/assets/mark.png" alt="Alphaworx">
        <div class="word">ALPHAWORX<span class="dim">.IO</span></div>
      </div>
      <nav>
        <a href="#help">How we help</a>
        <a href="blog/index.html">Insights</a>
        <a href="#why">Why it matters</a>
        <a href="#about">About</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Enterprise AI Strategy</div>
      <h1>The AI strategy gap is still small.<br>It won't stay that way.</h1>
      <p class="sub">Three years in, most companies are still improvising. The ones building a real strategy now are the ones that won't be left behind.</p>
      <div class="cta">
        <a class="btn" href="mailto:info@alphaworx.io">Work with us</a>
        <a class="link" href="deck.html">See the full case ↗</a>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <section id="why">
    <div class="wrap">
      <div class="label">Why it matters</div>
      <h2 class="h">The evidence is already in.</h2>
      <div class="findings">
        <div class="finding"><div class="n">01</div><div class="t"><b>Token prices fall while the actual bill rises.</b> Configuration choices alone can move the cost of the same job 5–9×.</div></div>
        <div class="finding"><div class="n">02</div><div class="t"><b>Shadow AI is usually the biggest exposure channel.</b> Same tools, different contract, different data terms.</div></div>
        <div class="finding"><div class="n">03</div><div class="t"><b>You don't control the control plane.</b> The important switches still sit largely with the vendors.</div></div>
        <div class="finding"><div class="n">04</div><div class="t"><b>Adoption is near-universal. Governed operation is not.</b> That gap is where risk and wasted money concentrate.</div></div>
      </div>
      <div class="findings-cta"><a href="deck.html">See the full case ↗</a></div>
    </div>
  </section>

  <div class="divider"></div>

  <section id="help">
    <div class="wrap">
      <div class="label">How we help</div>
      <h2 class="h">A governed operating system, not a subscription.</h2>
      <p class="lead">Access to a model isn't a strategy. We help enterprise leaders install the structure that turns scattered pilots into a system that can be run, measured, and defended.</p>
      <div class="offer-grid">
        <div class="offer">
          <div class="step">Step 1</div>
          <h4>Initial Assessment</h4>
          <p>We run the same diagnostic we'd run ourselves — cost, data exposure, security, and ownership — to find what's actually broken before recommending anything.</p>
        </div>
        <div class="offer">
          <div class="step">Step 2</div>
          <h4>Platform Hub Design</h4>
          <p>We help you stand up a thin platform hub with real mandate — the structure that turns scattered pilots into a governed system.</p>
        </div>
        <div class="offer">
          <div class="step">Step 3</div>
          <h4>Operating Cadence</h4>
          <p>We install the ongoing cadence — portfolio discipline, vendor strategy, agent readiness — that keeps the system defensible as it scales.</p>
        </div>
        <div class="offer">
          <div class="step">Ongoing</div>
          <h4>Advisory</h4>
          <p>Continued counsel as your AI strategy evolves — a second set of eyes trained to find what's actually broken before it costs you.</p>
        </div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <section id="insights">
    <div class="wrap">
      <div class="label">Insights</div>
      <h2 class="h">Straight talk on enterprise AI strategy.</h2>
      <div class="insight-grid">
        <a class="insight" href="blog/why-ai-pilots-stall.html">
          <div class="cat">Economics</div>
          <h4>Why AI pilots stall before production</h4>
          <p>The hand-off between a pilot and a defensible system is where most efforts break.</p>
        </a>
        <a class="insight" href="blog/shadow-ai-biggest-exposure.html">
          <div class="cat">Data Exposure</div>
          <h4>Shadow AI is your biggest exposure</h4>
          <p>Same tools your team already uses — different contract, different data terms.</p>
        </a>
        <a class="insight" href="blog/the-90-day-platform-stand-up.html">
          <div class="cat">Operating System</div>
          <h4>The 90-day platform stand-up</h4>
          <p>What a thin platform hub actually needs to have real mandate from day one.</p>
        </a>
      </div>
      <div class="insight-cta"><a href="blog/index.html">All insights →</a></div>
    </div>
  </section>

  <div class="divider"></div>

  <div class="wrap">
    <div class="proof-strip">
      <p>We don't just advise. AIR and ATRE are AI systems we've architected and validated ourselves — the same governance discipline we bring to your strategy.</p>
      <a href="#products">See what we've built ↓</a>
    </div>
    <div class="products-compact" id="products">
      <div class="p"><div class="tag">AIR — Atlas Intelligence Research</div><p>An autonomous research agent that runs its own drafts through a five-layer adversarial self-review before publishing.</p></div>
      <div class="p"><div class="tag">ATRE — Atlas Trading &amp; Risk Engine</div><p>A quantitative portfolio and risk management system, validated out-of-sample before it informs a decision.</p></div>
    </div>
  </div>

  <section id="about">
    <div class="wrap">
      <div class="label">About</div>
      <h2 class="h">Built around one discipline.</h2>
      <div class="about-row">
        <p>Alphaworx is a Dallas-based advisory and applied-AI company, founder-led by an operator with 20+ years diagnosing what's actually broken across trading, aviation, and energy — before turning that instinct toward enterprise AI strategy.</p>
        <div class="facts">
          <div class="fact"><div class="k">Headquarters</div><div class="v">Dallas, TX</div></div>
          <div class="fact"><div class="k">Focus</div><div class="v">Enterprise AI Strategy</div></div>
          <div class="fact"><div class="k">Type</div><div class="v">Privately held</div></div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <footer>
    <div class="wrap">
      <div class="row">
        <div class="meta">© 2026 Alphaworx Ltd</div>
        <a href="mailto:info@alphaworx.io">info@alphaworx.io</a>
      </div>
    </div>
  </footer>

</body>
</html>
```

- [ ] **Step 2: Verify locally in the Browser pane**

Open `index.html` directly (or via the Render preview once deployed) and confirm:
- Hero headline reads "The AI strategy gap is still small. It won't stay that way."
- Nav links `#help`, `#why`, `#about` scroll to the matching sections on the same page
- Nav "Insights" link and the "All insights →" link point to `blog/index.html` (will 404 until Task 6 — expected at this point)
- The three Insights cards link to `blog/why-ai-pilots-stall.html`, `blog/shadow-ai-biggest-exposure.html`, `blog/the-90-day-platform-stand-up.html` (will 404 until Task 6 — expected)
- "See the full case ↗" links (hero and Why-it-matters) point to `deck.html` (will 404 until Task 8 — expected)
- The `#products` compact section shows AIR and ATRE one-liners

- [ ] **Step 3: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add index.html
git commit -m "Reposition homepage around enterprise AI strategy"
```

---

## Task 2: First blog post source + frontmatter format

**Files:**
- Create: `content/blog/why-ai-pilots-stall.md`

This defines the frontmatter format the generator (Task 3) will parse: flat `key: value` lines between two `---` delimiters, followed by a blank line, followed by the post body in a small Markdown subset — paragraphs separated by blank lines, `> ` prefix for a blockquote paragraph, `**text**` for bold.

- [ ] **Step 1: Create the directory and first post**

```bash
mkdir -p "/Users/DSA/Seneca Projects/Alphaworx Website/content/blog"
```

Write `content/blog/why-ai-pilots-stall.md`:

```markdown
---
title: Why AI pilots stall before production
category: Economics
date: 2026-08-17
excerpt: The hand-off between a pilot and a defensible system is where most efforts break.
slug: why-ai-pilots-stall
---
Most companies are not failing because the models are not good enough. They are failing at the hand-off between a successful pilot and a system that can be run, measured, and defended in production.

That hand-off is where three things collide: cost becomes an unforecastable utility bill, data leaves through official and unofficial channels, and ownership is fragmented across multiple senior roles with no single-threaded accountability.

A pilot only has to work once, in front of a friendly audience, on a curated example. A production system has to work every time, against real inputs, with someone accountable when it doesn't. Most organizations don't have a plan for that jump — they have a plan for the pilot.

> Token prices fall while the actual bill rises. Configuration choices alone can move the cost of the same job 5–9×.

The fix isn't a better model. It's a governed operating system that catches the three collisions before they become a production incident — an initial assessment that finds what's actually broken, a platform hub with real mandate, and an operating cadence that keeps the system defensible as it scales.

That's the gap between a company that has adopted AI and one that has an AI strategy. Right now, almost every company has done the first. Very few have done the second.
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add content/blog/why-ai-pilots-stall.md
git commit -m "Add first blog post source: why AI pilots stall"
```

---

## Task 3: Blog generator — frontmatter parsing (TDD)

**Files:**
- Create: `scripts/build_blog.py`
- Test: `scripts/test_build_blog.py`

- [ ] **Step 1: Write the failing test**

Create `scripts/test_build_blog.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/scripts"
python3 -m pytest test_build_blog.py -v
```

Expected: `ModuleNotFoundError: No module named 'build_blog'` (file doesn't exist yet).

- [ ] **Step 3: Write minimal implementation**

Create `scripts/build_blog.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/scripts"
python3 -m pytest test_build_blog.py -v
```

Expected: both tests PASS.

- [ ] **Step 5: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add scripts/build_blog.py scripts/test_build_blog.py
git commit -m "Add frontmatter parser for blog generator"
```

---

## Task 4: Blog generator — Markdown-to-HTML conversion (TDD)

**Files:**
- Modify: `scripts/build_blog.py`
- Test: `scripts/test_build_blog.py`

- [ ] **Step 1: Write the failing tests**

Add to `scripts/test_build_blog.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/scripts"
python3 -m pytest test_build_blog.py -v
```

Expected: the three new tests FAIL with `ImportError: cannot import name 'markdown_to_html'`.

- [ ] **Step 3: Write minimal implementation**

Add `import re` as a new line at the top of `scripts/build_blog.py`, next to the existing `from pathlib import Path` line (don't duplicate the `Path` import — just add the one new `import re` line near it).

Then add the following function below `parse_frontmatter`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/scripts"
python3 -m pytest test_build_blog.py -v
```

Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add scripts/build_blog.py scripts/test_build_blog.py
git commit -m "Add markdown-to-HTML conversion to blog generator"
```

---

## Task 5: Blog generator — page rendering + CLI (TDD)

**Files:**
- Modify: `scripts/build_blog.py`
- Test: `scripts/test_build_blog.py`

- [ ] **Step 1: Write the failing tests**

Add to `scripts/test_build_blog.py`:

```python
from build_blog import format_byline, render_post, render_index


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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/scripts"
python3 -m pytest test_build_blog.py -v
```

Expected: the 3 new tests FAIL with `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/build_blog.py`:

```python
from datetime import datetime

NAV = (
    '<nav>'
    '<a href="../index.html#help">How we help</a>'
    '<a href="index.html">Insights</a>'
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
"""


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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/scripts"
python3 -m pytest test_build_blog.py -v
```

Expected: all 8 tests PASS.

- [ ] **Step 5: Add the CLI entry point**

Add to the bottom of `scripts/build_blog.py`:

```python
def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    posts = []
    for md_path in sorted(CONTENT_DIR.glob("*.md")):
        fields, body = parse_frontmatter(md_path.read_text())
        body_html = markdown_to_html(body)
        (OUTPUT_DIR / f"{fields['slug']}.html").write_text(render_post(fields, body_html))
        posts.append(fields)
    (OUTPUT_DIR / "index.html").write_text(render_index(posts))
    print(f"Generated {len(posts)} post(s) + index into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run the generator against the one real post and verify in the browser**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
python3 scripts/build_blog.py
```

Expected output: `Generated 1 post(s) + index into .../blog`

Open `blog/index.html` and `blog/why-ai-pilots-stall.html` in the Browser pane and confirm:
- The index page shows one card: "Why AI pilots stall before production" under "Economics"
- Clicking through leads to the post page with the blockquote rendering correctly
- The header nav's "How we help", "Why it matters", "About" links point back to `../index.html#help` etc.
- "All insights" back-link and header "Insights" link work between the two pages

- [ ] **Step 7: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add scripts/build_blog.py scripts/test_build_blog.py blog/
git commit -m "Add blog page rendering and generate first post"
```

---

## Task 6: Remaining 3 launch posts

**Files:**
- Create: `content/blog/shadow-ai-biggest-exposure.md`
- Create: `content/blog/you-dont-control-the-control-plane.md`
- Create: `content/blog/the-90-day-platform-stand-up.md`

- [ ] **Step 1: Write `content/blog/shadow-ai-biggest-exposure.md`**

```markdown
---
title: Shadow AI is your biggest exposure
category: Data Exposure
date: 2026-08-17
excerpt: Same tools your team already uses — different contract, different data terms.
slug: shadow-ai-biggest-exposure
---
Every enterprise leader we talk to has a rollout plan for the AI tools they've approved. Almost none of them have a plan for the AI tools their employees are already using without approval.

That's shadow AI, and it's usually the single biggest exposure channel in the whole stack — not because the tools themselves are dangerous, but because the terms are different. The consumer version of a tool your company already trusts under an enterprise agreement can have a completely different data-retention and training policy the moment an employee signs in with a personal account.

The pattern repeats everywhere: a team under deadline pressure finds the fastest path to an answer, pastes in something they shouldn't have, and nobody finds out until it shows up somewhere it shouldn't.

> Shadow AI is usually the biggest exposure channel. Same tools, different contract, different data terms.

The fix isn't a ban — bans just push the behavior further out of sight. It's governed provisioning: give people a sanctioned path that's as fast as the unsanctioned one, so there's no reason to go around it. That's a platform hub decision, not a policy memo.
```

- [ ] **Step 2: Write `content/blog/you-dont-control-the-control-plane.md`**

```markdown
---
title: You don't control the control plane
category: Vendor Strategy
date: 2026-08-16
excerpt: The important switches in your AI stack still sit with the vendor, not you.
slug: you-dont-control-the-control-plane
---
Ask most enterprise AI leads who controls their stack, and they'll point to their own architecture diagram — the orchestration layer, the retrieval pipeline, the agents they've wired together. All real, all theirs.

None of it is the control plane. The control plane is pricing, model deprecation schedules, rate limits, and the terms under which your data can or can't be used — and those switches sit with the vendor, not with you. A provider can deprecate the exact model version your evaluation suite was tuned against, change token pricing structure overnight, or update a usage policy that quietly changes what you're allowed to do with your own outputs.

> You don't control the control plane. The important switches still sit largely with the vendors.

That's not an argument against using vendor models — almost nobody is training frontier models in-house, and almost nobody should. It's an argument for treating vendor strategy as a first-class part of AI strategy: a real portfolio view across providers, an actual read on switching costs before you need to switch, and a standing watch on the deprecation and policy calendar instead of finding out from a support email.
```

- [ ] **Step 3: Write `content/blog/the-90-day-platform-stand-up.md`**

```markdown
---
title: The 90-day platform stand-up
category: Operating System
date: 2026-08-15
excerpt: What a thin platform hub actually needs to have real mandate from day one.
slug: the-90-day-platform-stand-up
---
Most companies don't lack an AI strategy because nobody's thought about it. They lack one because the thinking never got installed as an actual operating structure — a hub with a mandate, a cadence, and the authority to say no.

A thin platform hub isn't a committee and it isn't a full center of excellence with its own P&L. It's a small, senior team — often four to eight people — sitting at the intersection of engineering, security, legal, and the business, with the explicit mandate to own provisioning, vendor relationships, and the shared infrastructure that every team building on AI actually needs.

The first 90 days matter disproportionately, because that's the window where the hub either earns real authority or gets treated as a formality everyone routes around. That means shipping something people actually feel in the first month — usually governed, fast provisioning that's a genuine upgrade over whatever ad hoc access existed before — not spending the whole quarter writing a charter nobody reads.

> Adoption is near-universal. Governed operation is not. That gap is where risk and wasted money concentrate.

By day 90, a real platform hub should be able to name every production AI system in the company, who owns it, what it costs, and what happens if the underlying model gets deprecated next week. Most companies can't answer that today. That's the gap a hub with real mandate closes.
```

- [ ] **Step 4: Regenerate and verify all 4 posts**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
python3 scripts/build_blog.py
```

Expected output: `Generated 4 post(s) + index into .../blog`

Open `blog/index.html` in the Browser pane and confirm:
- All 4 cards appear, newest first: "Why AI pilots stall before production" (2026-08-17), "Shadow AI is your biggest exposure" (2026-08-17), "You don't control the control plane" (2026-08-16), "The 90-day platform stand-up" (2026-08-15)
- Each card's link opens the correct post with correct category/title/body/blockquote

Then reopen `index.html` (homepage) and confirm the 3 Insights teaser links now resolve correctly (no more 404s for those three).

- [ ] **Step 5: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add content/blog/ blog/
git commit -m "Add remaining 3 launch blog posts"
```

---

## Task 7: Slide deck shell + navigation

**Files:**
- Create: `deck.html`

- [ ] **Step 1: Create `deck.html` with the slide shell, first 2 slides, and JS navigation**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The AI Strategy Gap — Alphaworx</title>
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  html, body { height:100%; overflow:hidden; background:#e5e5e5; }
  body { font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; }
  .deck { height:100%; display:flex; align-items:center; justify-content:center; }
  .slide {
    display:none; width:min(92vw, 960px); aspect-ratio:16/9; background:#fff; color:#111;
    padding:6vh 6vw; flex-direction:column; justify-content:center; position:relative;
    box-shadow:0 10px 40px rgba(0,0,0,0.15);
  }
  .slide.active { display:flex; }
  .slide.dark { background:#111; color:#fff; }
  .slide.dark p { color:#aaa; }
  .kicker { font-size:0.8vw; min-font-size:11px; letter-spacing:0.14em; color:#a3a3a3; text-transform:uppercase; margin-bottom:2.2vh; }
  .slide h1 { font-size:3.4vw; font-weight:300; letter-spacing:-0.01em; line-height:1.2; margin-bottom:1.6vh; }
  .slide h2 { font-size:2.2vw; font-weight:300; letter-spacing:-0.01em; line-height:1.3; margin-bottom:1.6vh; }
  .slide p { font-size:1.15vw; color:#5b5b5e; line-height:1.6; max-width:640px; }
  .slide .big { font-size:6vw; font-weight:200; letter-spacing:-0.02em; line-height:1; }
  .slide .lab { font-size:1.3vw; margin-top:2vh; max-width:560px; line-height:1.55; color:#3d3d40; }
  .findings-list div { font-size:1.05vw; line-height:2; color:#333; }
  .findings-list b { color:#111; }
  .num { position:absolute; bottom:3vh; right:4vw; font-size:0.75vw; color:#ccc; }
  .slide.dark .num { color:#555; }
  .progress { position:fixed; bottom:0; left:0; height:3px; background:#111; transition:width 0.2s; }
  .hint { position:fixed; bottom:16px; left:50%; transform:translateX(-50%); font-size:11px; color:#999; letter-spacing:0.04em; }

  @media print {
    html, body { height:auto; overflow:visible; background:#fff; }
    .deck { display:block; height:auto; }
    .slide { display:flex !important; width:100%; aspect-ratio:16/9; page-break-after:always; box-shadow:none; }
    .progress, .hint { display:none; }
  }
</style>
</head>
<body>
  <div class="deck">

    <div class="slide dark active" data-slide="1">
      <div class="kicker">Alphaworx</div>
      <h1>The AI Strategy Gap</h1>
      <p>Why the businesses winning right now aren't the ones with the best model.</p>
      <div class="num">1 / 12</div>
    </div>

    <div class="slide" data-slide="2">
      <div class="kicker">The Stakes</div>
      <div class="big">3</div>
      <div class="lab">years old. AI as a serious enterprise capability is barely three years into its cycle — the gap between the companies getting it right and the ones improvising is just starting to open.</div>
      <div class="num">2 / 12</div>
    </div>

  </div>

  <div class="progress" id="progress" style="width:8.3%"></div>
  <div class="hint">Use ← → arrow keys, or click, to navigate</div>

<script>
  const slides = Array.from(document.querySelectorAll('.slide'));
  let current = 0;

  function show(index) {
    if (index < 0 || index >= slides.length) return;
    slides[current].classList.remove('active');
    current = index;
    slides[current].classList.add('active');
    document.getElementById('progress').style.width = ((current + 1) / slides.length * 100) + '%';
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') show(current + 1);
    if (e.key === 'ArrowLeft') show(current - 1);
  });

  document.querySelector('.deck').addEventListener('click', () => show(current + 1));
</script>
</body>
</html>
```

- [ ] **Step 2: Verify navigation works**

Open `deck.html` in the Browser pane. Confirm:
- Slide 1 (dark, "The AI Strategy Gap") shows first
- Pressing the right arrow key (or clicking) advances to slide 2 (the "3 years old" stat)
- The progress bar at the bottom fills proportionally
- The left arrow key goes back to slide 1

- [ ] **Step 3: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add deck.html
git commit -m "Add slide deck shell with keyboard/click navigation"
```

---

## Task 8: Remaining 10 slides + print verification

**Files:**
- Modify: `deck.html`

- [ ] **Step 1: Insert slides 3–12 between the existing slide 2 and the closing `</div>` of `.deck`**

```html
    <div class="slide" data-slide="3">
      <div class="kicker">The Gap</div>
      <h2>Adoption is nearly universal.<br>Governed operation is not.</h2>
      <p class="lab">That gap — not model quality — is where risk and wasted money concentrate. It's also the gap that determines who's actually ahead three years from now.</p>
      <div class="num">3 / 12</div>
    </div>

    <div class="slide" data-slide="4">
      <div class="kicker">Finding 01 — Economics</div>
      <h2>Token prices fall.<br>The bill still rises.</h2>
      <p class="lab">Configuration choices alone — not usage growth — can move the cost of the exact same job by 5–9×. Nobody is forecasting that swing, so nobody budgets for it, and it shows up as a surprise months in.</p>
      <div class="num">4 / 12</div>
    </div>

    <div class="slide" data-slide="5">
      <div class="kicker">Finding 02 — Data Exposure</div>
      <h2>Shadow AI is usually the<br>biggest exposure channel.</h2>
      <p class="lab">Same tools your team already trusts under an enterprise agreement — but a different contract, different data-retention terms, the moment someone signs in with a personal account.</p>
      <div class="num">5 / 12</div>
    </div>

    <div class="slide" data-slide="6">
      <div class="kicker">Finding 03 — Vendor Strategy</div>
      <h2>You don't control<br>the control plane.</h2>
      <p class="lab">Pricing, deprecation schedules, and usage terms sit with the vendor, not you. Vendor strategy has to be a first-class part of AI strategy, not an afterthought once a contract's already signed.</p>
      <div class="num">6 / 12</div>
    </div>

    <div class="slide dark" data-slide="7">
      <div class="kicker">Finding 04 — Adoption vs. Governance</div>
      <h2>Everyone has adopted AI.<br>Almost no one has governed it.</h2>
      <p>That's not a compliance footnote. It's the single biggest predictor of which companies are exposed and which aren't.</p>
      <div class="num">7 / 12</div>
    </div>

    <div class="slide" data-slide="8">
      <div class="kicker">The Fix</div>
      <h2>A governed operating system,<br>not a subscription.</h2>
      <p class="lab">Buying access to a model isn't a strategy. The organizations closing the gap are the ones installing an actual operating system around their AI use — not the ones with the newest model.</p>
      <div class="num">8 / 12</div>
    </div>

    <div class="slide" data-slide="9">
      <div class="kicker">Step 1</div>
      <h2>Initial Assessment</h2>
      <p class="lab">The same diagnostic we'd run on ourselves — cost, data exposure, security, and ownership — to find what's actually broken before recommending anything. Most engagements start here because most companies genuinely don't know their own exposure yet.</p>
      <div class="num">9 / 12</div>
    </div>

    <div class="slide" data-slide="10">
      <div class="kicker">Steps 2 &amp; 3</div>
      <h2>Platform Hub, then Cadence.</h2>
      <p class="lab">A thin platform hub with real mandate — 4 to 8 people, senior enough to say no — followed by the ongoing cadence that keeps it defensible: portfolio discipline, vendor strategy, agent readiness.</p>
      <div class="num">10 / 12</div>
    </div>

    <div class="slide" data-slide="11">
      <div class="kicker">Proof</div>
      <h2>We don't just advise.<br>We build and validate.</h2>
      <p class="lab">AIR and ATRE are AI systems we've architected ourselves, each gated by the same adversarial-review and out-of-sample validation discipline we bring to every engagement.</p>
      <div class="num">11 / 12</div>
    </div>

    <div class="slide dark" data-slide="12">
      <div class="kicker">Work With Us</div>
      <h2>The gap is closeable.<br>It won't stay small.</h2>
      <p>Alphaworx installs the operating system that turns AI access into a governed, defensible advantage. info@alphaworx.io</p>
      <div class="num">12 / 12</div>
    </div>
```

- [ ] **Step 2: Update the progress bar's initial width for the new slide count**

The progress bar width is computed dynamically by the existing script (`(current + 1) / slides.length * 100`), so no code change is needed — `slides.length` will now correctly read 12 once the new slides are in the DOM. Just double check the initial inline `style="width:8.3%"` on the `#progress` div still matches `1/12 = 8.3%` (it does, no edit needed).

- [ ] **Step 3: Verify full navigation and print output**

Open `deck.html` in the Browser pane and:
- Press the right arrow key 11 times, confirming each slide advances in order through slide 12, with the progress bar reaching 100% and content matching the code above at each step
- Press the left arrow key back to slide 1, confirming it steps back correctly
- Open the browser's print preview (Cmd+P) and confirm all 12 slides render one-per-page, none clipped, with the `.hint` and `.progress` elements hidden (per the `@media print` rule)

- [ ] **Step 4: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add deck.html
git commit -m "Add remaining slide deck content and verify print output"
```

---

## Task 9: Push and confirm live deployment

**Files:** none (deployment verification only)

- [ ] **Step 1: Push all commits**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git push
```

- [ ] **Step 2: Wait for Render to redeploy, then verify the live site**

Render auto-deploys on push to `main`. Once the deploy finishes (check the Render dashboard, or just retry after ~1 minute), open `https://alphaworx-io.onrender.com/` in the Browser pane and confirm:
- New hero headline and full repositioned homepage content
- `Insights` nav link and homepage teaser cards lead to working blog pages
- `blog/index.html` lists all 4 posts
- `deck.html` loads and is keyboard-navigable
- No console errors (`read_console_messages` with `onlyErrors: true`)

- [ ] **Step 3: Report back to the user**

Summarize what's live and flag anything that needs a follow-up decision (e.g. whether to wire up the alphaworx.io custom domain now).
