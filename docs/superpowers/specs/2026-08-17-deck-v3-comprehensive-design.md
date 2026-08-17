# Deck v3: Comprehensive Value + Risk Presentation — Design

**Date:** 2026-08-17
**Status:** Approved by user, ready for implementation planning

## Context

Two rounds of feedback moved this deck through three distinct states:
1. v1 (12 slides): text-only, risk-focused.
2. v2 (21 slides, `deck-expansion` branch, not yet merged): added monochrome charts and pulled in the security/reliability/governance blog series — still judged "way too minimal" per slide, and entirely risk/control-framed with no value narrative.
3. v3 (this design): a comprehensive ~41-slide deck built from the user's newly-created **AI Strategy Playbook v2** (`/Users/DSA/Seneca Projects/AI Strategy Playbook/AI Strategy Playbook v2.html`), which adds a full value-creation layer (Value Thesis, Value Pools, Portfolio System, Data Foundation, Operating Model detail, Workforce Adoption, Metrics/ROI, Industry Overlays) on top of the existing risk/control material. The user's explicit goal: this must function as a genuine sales asset for Alphaworx, not a warning list — "each page too minimal," "missing the value/selling narrative," and "not enough depth per topic" were the three confirmed gaps.

**Critical constraint from the user:** don't give away the working methodology in a form a prospect could self-execute — the deck should demonstrate rigor and create the desire to hire Alphaworx to run the system, not function as a free deliverable. This shapes content depth on a slide-by-slide basis (see "Content depth policy" below).

The `deck-expansion` branch (v2, 21 slides) is superseded by this design and will not be merged — v3 replaces it entirely, built fresh on top of `main`'s current 12-slide `deck.html`.

## Content depth policy

**Full detail** (evidence and stories — these build urgency and credibility without reducing the need for Alphaworx):
- All 8 existing risk/evidence findings (Economics, Data Exposure, Vendor Strategy, Adoption vs. Governance, Excessive Agency, Supply Chain, Reliability, EU AI Act) — sourced from public research, safe to show in full.
- Narrative walkthroughs (the logistics-company thesis evolution, the 28-idea portfolio triage, the claims-team adoption story, the legal-team ROI story) — these are specific illustrative cases, not reusable templates, and are the most persuasive "we know how to do this" content in the deck.
- The maturity matrix, proof section, and closing CTA.

**Shape, not the tool** (name the framework and its components, illustrate with one example, withhold the full operational worksheet):
- Portfolio Scoring: name the 10 dimensions as a list; do not show the full "what high means / what low means" grading rubric.
- Data Foundation: name the 7 readiness layers; do not show the full questions-to-answer / failure-mode checklist.
- Ownership & RACI: state the core finding (ownership ambiguity stalls programs) with 1-2 example decisions; do not show the complete 6-decision operational RACI table.
- Metrics & ROI: state the "usage ≠ value" insight with 2-3 good-vs-bad-proxy examples; do not show all 6 metric families in full.
- Workforce Adoption: name the 5 segments with the core insight; do not show the complete need/common-mistake breakdown for all 5.
- Industry Overlays: show 3-4 industries as illustrative examples; do not show the complete 8-industry reference table.

## Visual system changes

Approved via mockup comparison: move from the current sparse single-column slide layout to a richer, table-driven "consulting-grade" template for content slides, while keeping the existing full-bleed dramatic treatment for title, section dividers, and the closing slide (pacing contrast between dense information slides and big-idea pause slides is intentional, not an oversight).

**New slide frame components:**
1. **Rich header** — kicker (unchanged) + a larger, bolder `h2` (up to ~60% width) + an optional right-aligned pull-quote "takeaway" callout (border-left accent, ~32% width) sitting alongside the headline instead of below it.
2. **Data table** — a full-width table component: uppercase small-caps header row with a bottom border, data rows with light row separators, first column bold where it's a category label. Reuses the deck's existing monochrome palette (`#111`/`#888`/`#ececec`, matching values already used elsewhere on the site).
3. **Footline** — replaces the floating corner `.num` label on rich-template slides with a bottom bar: "alphaworx.io — Enterprise AI Strategy" (left) + slide number (right). Simple/dramatic slides (title, dividers, closing) keep the existing floating `.num` corner label unchanged.

Existing chart components (`.bar-chart`, `.timeline`, `.split-compare`, `.stat-pair`, `.big`/`.lab`, `.matrix`) are retained and reused inside the new rich frame for the evidence/risk slides — same visual grammar, now presented with a headline+takeaway header and footline instead of the sparser original frame.

All monochrome — no new colors introduced, consistent with the rest of the site and confirmed again during this round's mockup comparison.

## Full slide structure (41 slides)

**Open (3)** — dramatic/simple style
1. Title — "The AI Strategy Gap"
2. The Stakes — "3" years old
3. The Executive Promise — 5-item list (Strategy, Portfolio, Control, Change, Evidence — from the Playbook v2's own framing)

**Part 1 — Where AI Creates Value (7)** — rich style
4. Section divider
5. The AI Value Thesis — weak vs. strong statement comparison (2-row example table)
6. Three categories — Table-stakes / Differentiating / Strategic options
7. Thesis walkthrough — the logistics-company example, full narrative
8. Six Value Pools — full table (pool name + 1-2 example opportunities + what to measure, condensed from the source's 3-column table)
9. Value discovery method — "map the workflow before collecting ideas" + one red flag
10. Portfolio Scoring — the 10 dimensions named (shape-not-tool)

**Part 2 — Building the Portfolio (3)** — rich style
11. Six Portfolio Classes — named with one-line descriptions (Quick Wins, Strategic Bets, Platform Investments, Risk Necessities, Experiments, Park/Kill)
12. Portfolio walkthrough — the 28-idea triage example, full narrative
13. Data Foundation — the 7 readiness layers named (shape-not-tool)

**Part 3 — What Puts That Value at Risk (10)** — rich style, full detail
14. Section divider
15. Economics (bar chart)
16. Data Exposure (big-stat)
17. Vendor Strategy (split-compare)
18. Adoption vs. Governance (bar chart, dark)
19. Excessive Agency (stat-pair)
20. Supply Chain (big-stat)
21. Reliability / Model Deprecation (split-compare)
22. EU AI Act Timeline (timeline)
23. Five things the vendor pitch leaves out — consolidated into one dense table slide (5 rows: claim + one-line counter-evidence), replacing the two-slide treatment from v2

**Part 4 — The Operating System (9)** — rich style
24. Section divider
25. The Fix — governed operating system, not a subscription
26. Initial Assessment
27. Ownership & RACI — the ambiguous-ownership finding + 1-2 example decisions (shape-not-tool)
28. Thin Platform Hub Design
29. 90-Day Stand-Up — 3 phases named with one-line focus each (trimmed from the source's full exit-criteria detail)
30. 180-Day / 12-Month Horizon — 3-row table (horizon, management question, proof point)
31. Operating Cadence
32. Agent Readiness — the lethal-trifecta framing, shared-API-key finding, OWASP ASI taxonomy named, the 74%/21% adoption-vs-governance-maturity stat (real, already used elsewhere — reused here in its Agent Readiness context)

**Part 5 — Making Value Real (5)** — rich style
33. Section divider
34. Workforce Adoption — 5 segments named + the core insight (shape-not-tool)
35. Adoption walkthrough — the claims-team example, full narrative
36. Metrics & ROI — the "usage ≠ value" insight + 2-3 good-vs-bad-proxy examples (shape-not-tool)
37. ROI walkthrough — the legal-team contract-review example, full narrative

**Close (4)**
38. Industry Overlays — 3-4 industries as illustrative examples (shape-not-tool)
39. Maturity matrix capstone — expanded from the v2 8-row matrix to include Value Strategy and Operating Model categories alongside the existing risk categories
40. Proof — AIR/ATRE
41. Closing / CTA

## Testing / verification

- Given the size (41 slides, largest single file on the site by a wide margin), implementation will proceed in multiple sequential append-based tasks rather than one full-file replacement, each independently structurally verified before the next builds on it.
- Live click-through of all 41 slides in the Browser pane, confirming the progress bar and footline slide-count math (`N / 41`) update correctly throughout.
- Print-mode check carried over from the v2 build: the `@media print` vw-based chart-spacing override already fixed on the `deck-expansion` branch will be ported into this build rather than re-discovered.
- Spot-check that no "shape-not-tool" slide accidentally regresses into the full operational detail during drafting — this is a content-review concern as much as a code-review one, and should be an explicit check in the final holistic review pass.

## Out of scope

- No chart library, external images, or icon set — everything stays hand-coded CSS/HTML, zero dependencies, consistent with the rest of the site.
- No changes to `index.html`, the blog, or any other part of the site.
- The `deck-expansion` branch (v2) will be discarded, not merged, once this design is implemented — its worktree and branch should be cleaned up as part of finishing this work.
