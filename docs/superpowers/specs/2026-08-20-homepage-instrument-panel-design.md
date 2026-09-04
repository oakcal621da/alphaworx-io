# Homepage redesign — "The Instrument Panel"

**Status:** approved direction (prototype first, then replace `index.html` if approved)

## Goal

Rebuild the Alphaworx homepage so it feels alive and distinctly ours — not a
generic template — while staying light, crisp, and content-forward. Motion is
allowed only where it restates the thesis (the AI strategy gap).

## Visual system

- **Ground:** cool off-white paper `#F5F6F8`, white `#FFFFFF` surfaces, hairline
  rules `#DFE2E7`. A faint blueprint grid behind the hero.
- **Ink:** `#0B0C0E` headings, `#454952` body, `#8A8F99` muted/mono labels.
- **Signal:** one amber accent `#F0A500` (fills, lines, marks) and `#9A6700`
  for amber text on white. Used only for actionable/signal moments: primary
  CTA, chart gap, timeline nodes, live status dot, link underlines.
- **Type:** Bricolage Grotesque (display), Instrument Sans (body),
  JetBrains Mono (data labels, counters, eyebrows). Google Fonts.
- **Shape:** 8px radius cards, 1px borders, no drop shadows.

## Motion (all disabled under `prefers-reduced-motion`)

1. Hero chart draws itself on load: adoption path rises steeply, governed
   path stays flat, the gap between them shades in amber (hatched).
2. Headline words reveal with a short stagger.
3. Stat band counts up on scroll (43%, 9.2×, 21%, 60 days).
4. Findings run as a slow marquee (pauses on hover) above the numbered list.
5. 90-day timeline draws its line and pops its three nodes on scroll.
6. Sections fade/slide in on entry; cards lift on hover; link underlines draw.
7. Header shows a live "Day N of the enterprise AI era" counter (from
   30 Nov 2022) with a pulsing amber status dot; an amber scroll-progress
   hairline sits at the top of the page.

## Content

Reuses the current homepage copy: hero, six findings, how-we-help steps +
90-day timeline, industries, three insights, AIR/ATRE proof, about +
principles. CTAs unchanged (`mailto:info@alphaworx.io`, `deck.html`).

## Out of scope

Blog templates and the deck keep their current styling until the homepage
direction is approved.
