# Deck Expansion: "The AI Strategy Gap" — Design

**Date:** 2026-08-17
**Status:** Approved by user, ready for implementation planning

## Context

The current `deck.html` (built in the earlier AI-strategy-repositioning project) has 12 text-only slides making the case for enterprise AI strategy. The user's feedback: "way too basic" — needs much more content and real visuals. This design expands it to roughly 21 slides, pulls in material from the full blog series (not just the original 4 "why it matters" findings), and adds hand-coded, zero-dependency data visualizations (bar charts, a timeline, stat callouts, a summary matrix) instead of text-only slides throughout.

Visual style stays **pure monochrome** — confirmed by the user after comparing a monochrome-vs-red-accent chart treatment (both a ranking-movement bar chart and an EU AI Act timeline were mocked up; monochrome won both times, consistent with every other visual decision on this site).

## Technical approach

- `deck.html` stays a single, self-contained HTML/CSS/JS file — no chart library, no build step. All charts are hand-built with flexbox/CSS (bars, timeline dots/line, big-number stat callouts, a grid) using the same visual language already established (`.kicker`, `.num`, dark/light slide alternation, viewport-unit type scale).
- The existing navigation JS (`show()`, keyboard/click handling, progress bar), the `@media print` stylesheet, and the overall slide shell are unchanged — this expansion only adds slide content and a small set of new reusable chart CSS classes.
- Slide count moves from 12 to `data-slide="1"` through `data-slide="21"`; every slide's `.num` label and the `slides.length`-driven progress bar continue to work automatically since the progress bar math already reads slide count dynamically.

## New chart components (all monochrome, all CSS/flexbox — no SVG library, no canvas)

1. **Bar comparison** — two (or more) vertical bars with value labels above and category labels below, darker/black bar marking the "current" or "worse" value, light gray for the baseline (used for the OWASP ranking-movement mockup, token-cost range, and the adoption-vs-governance contrast).
2. **Timeline** — a horizontal line with dots marking dated milestones, labels above/below alternating or stacked (used for the EU AI Act calendar).
3. **Big-stat callout** — a large numeral/percentage with a short label underneath (already exists from slide 2's "3" — reused for shadow-AI stats, MCP vulnerability count, etc.).
4. **Maturity matrix** — a simple grid/table-like layout of risk category → one-word maturity status (e.g., "Mature", "Emerging", "Unsolved"), used once as a capstone slide pulling every category covered in the deck into a single summary view, echoing the source report's own response matrix.

## Slide-by-slide content plan

### Section 1 — Open (slides 1-3, largely unchanged from current deck)
1. Title: "The AI Strategy Gap" (dark slide, unchanged)
2. The Stakes: "3" years old big-stat callout (unchanged)
3. The Gap thesis: "Adoption is nearly universal. Governed operation is not." (unchanged)

### Section 2 — Evidence (slides 4-7, each gets a real chart; replaces the old single evidence-summary slide)
4. **Economics** — bar comparison chart: cost of an identical job across configurations, $0.06 to $0.55 (9.2× swing), sourced from the Understanding Enterprise AI Risk report. Kicker: "Finding 01 — Economics."
5. **Data Exposure** — big-stat callout + small supporting line: 43% of breached organizations had a shadow-AI incident (up from 20%), $5.39M average cost. Secondary line noting the 78%→47% personal-account-usage trend as the one improving number. Kicker: "Finding 02 — Data Exposure."
6. **Vendor Strategy** — bar/visual on control-plane ownership (conceptual, not a numeric chart — reuses the "you don't control the control plane" framing with a simple visual split between "customer-configurable" and "vendor-controlled" properties). Kicker: "Finding 03 — Vendor Strategy."
7. **Adoption vs. Governance** — bar comparison: 74% of organizations expect substantial agentic AI use by 2027 vs. only 21% report mature agent governance today. Dark slide (matches current slide 7's dark treatment). Kicker: "Finding 04 — Adoption vs. Governance."

### Section 3 — Security (slides 8-10, new)
8. Section divider: "The Security Layer" — short intro line framing security as design constraint, not a bolt-on feature (dark slide, matches deck's section-divider rhythm).
9. **Excessive agency** — bar comparison chart: OWASP GenAI/LLM Top 10 rank, 6th (2025) → 3rd (2026). From the "Excessive agency" blog post.
10. **Supply chain** — big-stat callout: 200,000+ vulnerable MCP instances found in the wild. From the "AI supply chain" blog post.

### Section 4 — Reliability & Governance (slides 11-12, new)
11. **Model deprecation** — visual on the ~60-day observed retirement window vs. typical regulated-industry revalidation cycles (simple two-bar or two-block comparison). From the "Model deprecation" blog post.
12. **EU AI Act timeline** — the 3-point timeline chart already mocked up and approved: Feb 2025 (AI-literacy live) → Dec 2026 (Article 5 safeguards due) → Dec 2027 (high-risk regime). From the "AI Act obligations" blog post.

### Section 5 — Vendor Reality Check (slides 13-14, new)
13. Intro: "Five things the vendor pitch leaves out" framing slide — sets up the falsifiable-claims format.
14. **Token price paradox** — bar comparison chart: the same evidence base showing both falling per-token prices AND rising frontier-model run costs on two bars, making the "industry quotes whichever suits" point visually. From the "Five things" blog post (claim one, the sharpest/most chart-friendly of the five).

### Section 6 — The Fix → Close (slides 15-21, expands current slides 8-12)
15. The Fix intro (unchanged from current slide 8, renumbered)
16. Initial Assessment (unchanged from current slide 9, renumbered)
17. **Platform Hub Design** (split out of current slide 10, which combined this with Operating Cadence) — the thin-hub, 4-8-person, real-mandate framing on its own slide.
18. **Operating Cadence** (the other half of current slide 10) — portfolio discipline, vendor strategy, agent readiness, on its own slide.
19. **Maturity matrix capstone** (new) — grid summarizing every category covered in the deck (Economics, Data Exposure, Vendor Strategy, Security × 2, Reliability, Governance) against a one-word maturity status, closing the evidence sections with a single pulled-together view before pivoting to proof/close.
20. Proof: AIR/ATRE (unchanged from current slide 11, renumbered)
21. Closing/CTA (unchanged from current slide 12, renumbered)

This totals 21 slides (3+4+3+2+2+7), matching the ~20-24 target agreed in brainstorming.

## Testing / verification

- Visual check in the Browser pane: navigate all 21 (or 20) slides via click and keyboard, confirm progress bar reaches 100% at the last slide.
- Confirm every new chart renders correctly at the deck's fixed `min(92vw, 960px)` slide width — no overflow, no clipped bars/labels.
- Confirm the `@media print` stylesheet still produces one slide per page with no chart clipping (manual print-preview check, same as the original deck build).
- Confirm dark/light slide alternation still reads cleanly with the new slide count (deciding which new slides are dark is an implementation-time call, following the existing rhythm of roughly one dark slide per section).

## Out of scope

- No chart library, no SVG icon set, no external images — everything stays hand-coded CSS/HTML, consistent with the rest of the site.
- No changes to the navigation JS, print stylesheet mechanics, or overall slide shell — only content and new chart CSS classes.
- No changes to `index.html`, the blog, or any other part of the site.
