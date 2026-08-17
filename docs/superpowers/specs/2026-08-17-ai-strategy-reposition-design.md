# Alphaworx: AI Strategy Repositioning — Design

**Date:** 2026-08-17
**Status:** Approved by user, ready for implementation planning

## Context

The current live site (alphaworx-io.onrender.com) positions Alphaworx as an applied-AI *builder* (AIR, ATRE, developer-flavored proof points). The user is now positioning himself for exec-level AI Strategy roles and wants the site to lead with **enterprise AI strategy advisory**, not engineering. This also opens a lead-gen angle: convince visiting executives that Alphaworx can help their company develop the right AI strategy.

Source material for the new positioning and content comes from `/Users/DSA/Seneca Projects/AI Strategy Playbook/AI Strategy Playbook.html` (a rigorous, sourced operating-system document for enterprise AI strategy) and its companion piece `Understanding Enterprise AI Risk`.

This design covers four connected pieces, to be built in this order:
1. Homepage repositioning
2. Blog infrastructure
3. Initial blog content (4 posts)
4. "Why AI strategy matters" slide deck

All four keep the site's existing **Minimal Monochrome** visual style (white background, black type, thin geometric sans, generous whitespace) — no new color introduced, confirmed by the user after comparing a red-accent alternative.

## Decisions carried over from the original build

- Single-page-per-concern static HTML, no build tooling required for Render (any generation happens locally, output is committed).
- Contact CTA stays a simple `mailto:info@alphaworx.io` — no form backend, no scheduling tool, for now.
- Personal presence is minimized: no founder name, no photo, no first-person narrative anywhere on the site. At most one low-key, unnamed reference to being founder-led.
- Hosted on Render as a static site (already live), repo at `github.com/oakcal621da/alphaworx-io` (public).

## 1. Homepage repositioning

Restructure `index.html` in place (same file, same monochrome CSS system already in use).

**Nav:** How we help · Insights · Why it matters · About

**Hero**
- Eyebrow: "Enterprise AI Strategy"
- Headline: **"The AI strategy gap is still small. It won't stay that way."**
- Subhead: "Three years in, most companies are still improvising. The ones building a real strategy now are the ones that won't be left behind."
- Primary CTA: "Work with us" → `mailto:info@alphaworx.io`
- Secondary link: "See the full case ↗" → `deck.html`

**"Why it matters"** — four findings pulled from the Playbook's Initial Assessment section, each a bolded claim + one-line elaboration:
1. Token prices fall while the actual bill rises (5–9× cost swing from configuration alone).
2. Shadow AI is usually the biggest exposure channel.
3. You don't control the control plane (vendors hold the important switches).
4. Adoption is near-universal; governed operation is not — that gap is where risk and wasted money concentrate.

Links to `deck.html` for the fuller argument.

**"How we help"** — 4 offerings drafted from the Playbook's own operating system, framed as a sequence:
1. **Initial Assessment** — diagnostic across cost, data exposure, security, ownership.
2. **Platform Hub Design** — standing up a thin platform hub with real mandate.
3. **Operating Cadence** — portfolio discipline, vendor strategy, agent readiness as an ongoing rhythm.
4. **Advisory** (ongoing) — continued counsel as strategy evolves.

**"Insights"** — 3-card teaser grid pulling the most recent blog posts (category tag, title, one-line excerpt), linking to `/blog/`.

**Proof strip + compact "What we've built"** — AIR/ATRE compressed to a single summary line ("We don't just advise. AIR and ATRE are AI systems we've architected and validated ourselves — the same governance discipline we bring to your strategy."), linking to a `#products` anchor. That anchor is a compact two-line section (not the old full two-card layout): AIR and ATRE each get a name + one-sentence description, no expanded copy, no separate "See it live" sub-link — the fuller AIR description and Primer Desk link now live in the Insights/blog content instead, keeping the homepage's engineering detail minimal.

**About** — minimal, company-voiced: "Alphaworx is a Dallas-based advisory and applied-AI company, founder-led by an operator with 20+ years diagnosing what's actually broken across trading, aviation, and energy — before turning that instinct toward enterprise AI strategy." No name. Facts row retained (Headquarters, Focus, Type).

**Footer** — unchanged (`© 2026 Alphaworx Ltd`, `info@alphaworx.io`).

## 2. Blog infrastructure

**Authoring approach:** Markdown source files → a small local generator script → committed static HTML output. Render continues deploying pure static files with no build step of its own.

**Proposed structure:**
```
content/blog/*.md          — post source (frontmatter: title, category, date, excerpt, slug)
scripts/build-blog.py      — reads content/blog/*.md + templates, writes blog/*.html and blog/index.html
blog/index.html            — generated listing page
blog/<slug>.html           — generated post pages
```

**Listing page (`/blog/`)** — same header/nav as homepage, active state on "Insights". Hero label + heading ("Straight talk on enterprise AI strategy.") + one-line description. Below: a card grid (no images), each card showing category tag, title, one-line excerpt, date.

**Post template (`/blog/<slug>.html`)** — same header/nav. Post hero: category tag, title, byline ("Alphaworx Insights · <Month Year>" — no personal name). Body: standard paragraph flow plus a pull-quote style matching the homepage's "Recent work" card (left border rule, larger serif-free quote text). Closing CTA block (consistent copy pattern, e.g. "This is exactly the kind of gap we help close" → "Work with us" button) before a "← All insights" back-link.

Exact template markup/CSS to be finalized during implementation, reusing the existing site's typographic scale and spacing units.

## 3. Initial blog content

Four posts at launch, each adapted (not copied verbatim) from a Playbook section:

| Category | Title | Source section |
|---|---|---|
| Economics | Why AI pilots stall before production | 1.1 What is actually broken |
| Data Exposure | Shadow AI is your biggest exposure | 2.2 Data Exposure & Shadow AI |
| Vendor Strategy | You don't control the control plane | 2.7 Vendor Strategy |
| Operating System | The 90-day platform stand-up | 3.3 90-Day Stand-Up |

Each post is original web copy informed by the Playbook's findings and evidence, not a republished excerpt — written to stand alone for a visitor who hasn't read the Playbook.

## 4. "Why AI strategy matters" slide deck

**File:** `deck.html` — single self-contained HTML file, no external libraries.

**Behavior:**
- Fullscreen, keyboard (arrow keys) and click navigable between slides — usable as an actual presentation surface.
- A print stylesheet (`@media print`) renders one slide per page for clean "Print to PDF" export from the browser — no separate export tooling.
- Visual style matches the site: monochrome, occasional full-black slide for rhythm/emphasis (as shown in the approved mockup).

**Planned slide flow (~12 slides):**
1. Title — "The AI Strategy Gap"
2. The Stakes — "3 years old" framing stat
3. The gap thesis (adoption vs. governed operation)
4–7. One slide per "Why it matters" finding, expanded with supporting detail from the Playbook
8. The operating-system solution overview
9. Initial Assessment (detail)
10. Platform Hub + Operating Cadence (detail)
11. Proof — AIR/ATRE as evidence Alphaworx builds validated systems, not just advises
12. Closing / CTA — "The gap is closeable. It won't stay small." → contact

Exact slide-by-slide copy to be drafted during implementation, pulling further supporting detail from the Playbook and its companion risk document.

## Testing / verification

- Visual check in the Browser pane (as done for the current live homepage) after each piece deploys, confirming layout, links, and content render correctly at desktop and mobile widths.
- Confirm all internal links (`#help`, `#insights`, `#why`, `#about`, `deck.html`, `/blog/`, individual post pages) resolve correctly after deployment.
- Confirm the blog generator script is idempotent — re-running it with unchanged Markdown produces no diff.
- Confirm `deck.html` print-to-PDF output is legible (one slide per page, no clipped content) via a manual browser print-preview check.

## Out of scope for this design

- Contact form / scheduling integration (mailto stays for now).
- CMS or non-local authoring workflow for blog posts.
- Analytics/tracking.
- Custom domain (alphaworx.io) wiring — user is deferring this, currently using the `*.onrender.com` URL.
