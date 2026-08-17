# Deck Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `deck.html` from 12 text-only slides to 21 slides with hand-coded monochrome data visualizations (bar charts, a timeline, split comparisons, stat pairs, a maturity matrix), pulling in material from the full 9-post blog series instead of just the original 4 findings.

**Architecture:** `deck.html` stays a single, self-contained, dependency-free HTML/CSS/JS file. The existing navigation script, print stylesheet, and slide shell are untouched — this is a content and CSS expansion only. Five new reusable chart CSS component classes (`.bar-chart`, `.timeline`, `.split-compare`, `.stat-pair`, `.matrix`) are added alongside the existing slide typography classes, then used across the new and reworked slides.

**Tech Stack:** Plain HTML/CSS/JS — no chart library, no build step, no new dependencies.

---

## Reference: design spec

Full design is in [`docs/superpowers/specs/2026-08-17-deck-expansion-design.md`](../specs/2026-08-17-deck-expansion-design.md). It has the rationale for the section structure and chart choices below.

## File Structure

- Modify: `deck.html` (full content replacement — CSS additions + all 21 slides)

All paths are relative to the repo root: `/Users/DSA/Seneca Projects/Alphaworx Website`.

---

## Task 1: Replace `deck.html` with the expanded 21-slide version

**Files:**
- Modify: `deck.html` (full replacement)

- [ ] **Step 1: Replace `deck.html` with the exact content below**

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
  .kicker { font-size:max(0.8vw, 11px); letter-spacing:0.14em; color:#a3a3a3; text-transform:uppercase; margin-bottom:2.2vh; }
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

  .bar-chart { display:flex; align-items:flex-end; gap:3vw; height:22vh; margin-top:3vh; max-width:520px; }
  .bar-chart .bar-col { display:flex; flex-direction:column; align-items:center; justify-content:flex-end; gap:1vh; flex:1; height:100%; }
  .bar-chart .bar-val { font-size:1.3vw; font-weight:600; }
  .bar-chart .bar { width:100%; border-radius:3px 3px 0 0; background:#d4d4d4; }
  .bar-chart .bar.hi { background:#111; }
  .bar-chart .bar-label { font-size:0.85vw; color:#888; text-align:center; }
  .slide.dark .bar-chart .bar-label { color:#999; }
  .slide.dark .bar-chart .bar { background:#444; }
  .slide.dark .bar-chart .bar.hi { background:#fff; }
  .chart-caption { font-size:0.85vw; color:#888; margin-top:1.5vh; max-width:520px; }

  .timeline { display:flex; align-items:center; margin:3vh 0 2vh; max-width:600px; position:relative; height:2px; background:#ddd; }
  .timeline .pt { position:absolute; top:-4px; width:10px; height:10px; border-radius:50%; background:#111; }
  .timeline-labels { display:flex; justify-content:space-between; max-width:600px; font-size:0.8vw; color:#666; }
  .timeline-labels div { max-width:33%; }

  .split-compare { display:flex; gap:3vw; margin-top:3vh; max-width:640px; }
  .split-compare .col { flex:1; }
  .split-compare .col-label { font-size:0.85vw; text-transform:uppercase; letter-spacing:0.08em; color:#111; font-weight:600; margin-bottom:1vh; }
  .split-compare .col-body { font-size:1.05vw; color:#5b5b5e; line-height:1.6; }

  .stat-pair { display:flex; gap:4vw; margin-top:3vh; }
  .stat-pair .item { flex:1; }
  .stat-pair .item .val { font-size:3.2vw; font-weight:200; letter-spacing:-0.02em; }
  .stat-pair .item .lbl { font-size:0.9vw; color:#666; margin-top:0.8vh; max-width:260px; }

  .matrix { display:flex; flex-direction:column; max-width:640px; margin-top:2.5vh; }
  .matrix-row { display:flex; justify-content:space-between; align-items:center; padding:1vh 0; border-top:1px solid #ececec; }
  .matrix-row:last-child { border-bottom:1px solid #ececec; }
  .matrix-row .cat { font-size:0.95vw; color:#333; }
  .matrix-row .status { font-size:0.75vw; letter-spacing:0.04em; text-transform:uppercase; color:#888; font-weight:600; }

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
      <div class="num">1 / 21</div>
    </div>

    <div class="slide" data-slide="2">
      <div class="kicker">The Stakes</div>
      <div class="big">3</div>
      <div class="lab">years old. AI as a serious enterprise capability is barely three years into its cycle — the gap between the companies getting it right and the ones improvising is just starting to open.</div>
      <div class="num">2 / 21</div>
    </div>

    <div class="slide" data-slide="3">
      <div class="kicker">The Gap</div>
      <h2>Adoption is nearly universal.<br>Governed operation is not.</h2>
      <p class="lab">That gap — not model quality — is where risk and wasted money concentrate. It's also the gap that determines who's actually ahead three years from now.</p>
      <div class="num">3 / 21</div>
    </div>

    <div class="slide" data-slide="4">
      <div class="kicker">Finding 01 — Economics</div>
      <h2>Token prices fall.<br>The bill still rises.</h2>
      <div class="bar-chart">
        <div class="bar-col"><div class="bar-val">$0.06</div><div class="bar" style="height:12%;"></div><div class="bar-label">Cheapest config</div></div>
        <div class="bar-col"><div class="bar-val">$0.55</div><div class="bar hi" style="height:100%;"></div><div class="bar-label">Priciest config</div></div>
      </div>
      <div class="chart-caption">Same 50k-input, 2k-output job. A 9.2× swing driven by caching, batching, reasoning tokens, and tokenizer settings — before a single line of business logic changes.</div>
      <div class="num">4 / 21</div>
    </div>

    <div class="slide" data-slide="5">
      <div class="kicker">Finding 02 — Data Exposure</div>
      <div class="big">43%</div>
      <div class="lab">of breached organizations had a shadow-AI incident in 2026 — up from 20% the year before. Average cost: $5.39M per incident.</div>
      <div class="chart-caption">The one number moving the right way: personal-account use among workplace gen-AI users fell from 78% to 47% in a year, as governed alternatives rolled out.</div>
      <div class="num">5 / 21</div>
    </div>

    <div class="slide" data-slide="6">
      <div class="kicker">Finding 03 — Vendor Strategy</div>
      <h2>You don't control<br>the control plane.</h2>
      <div class="split-compare">
        <div class="col"><div class="col-label">You control</div><div class="col-body">Orchestration, retrieval pipeline, agent wiring, prompts.</div></div>
        <div class="col"><div class="col-label">The vendor controls</div><div class="col-body">Pricing, deprecation schedule, rate limits, data-use terms.</div></div>
      </div>
      <div class="num">6 / 21</div>
    </div>

    <div class="slide dark" data-slide="7">
      <div class="kicker">Finding 04 — Adoption vs. Governance</div>
      <h2>Everyone has adopted AI.<br>Almost no one has governed it.</h2>
      <div class="bar-chart">
        <div class="bar-col"><div class="bar-val">74%</div><div class="bar hi" style="height:100%;"></div><div class="bar-label">Expect substantial agent use by 2027</div></div>
        <div class="bar-col"><div class="bar-val">21%</div><div class="bar" style="height:28%;"></div><div class="bar-label">Report mature agent governance today</div></div>
      </div>
      <div class="num">7 / 21</div>
    </div>

    <div class="slide dark" data-slide="8">
      <div class="kicker">Part 3</div>
      <h2>The Security Layer.</h2>
      <p>Every control that measurably works does so by removing capability. Guardrails are a design constraint, not something you bolt on later.</p>
      <div class="num">8 / 21</div>
    </div>

    <div class="slide" data-slide="9">
      <div class="kicker">Finding 05 — Security</div>
      <h2>Excessive agency jumped<br>from 6th to 3rd.</h2>
      <div class="bar-chart">
        <div class="bar-col"><div class="bar-val">6th</div><div class="bar" style="height:40%;"></div><div class="bar-label">2025 rank</div></div>
        <div class="bar-col"><div class="bar-val">3rd</div><div class="bar hi" style="height:75%;"></div><div class="bar-label">2026 rank</div></div>
      </div>
      <div class="chart-caption">OWASP GenAI/LLM Top 10 (lower rank = higher risk). No attacker required — just an agent with permissions nobody scoped down.</div>
      <div class="num">9 / 21</div>
    </div>

    <div class="slide" data-slide="10">
      <div class="kicker">Finding 06 — Security</div>
      <div class="big">200,000+</div>
      <div class="lab">vulnerable instances of the protocol connecting AI assistants to outside tools — model files that can execute code the moment they're loaded.</div>
      <div class="num">10 / 21</div>
    </div>

    <div class="slide" data-slide="11">
      <div class="kicker">Finding 07 — Reliability</div>
      <h2>Model deprecation is a<br>reliability risk, not an IT ticket.</h2>
      <div class="split-compare">
        <div class="col"><div class="col-label">What vendors give you</div><div class="col-body">An observed ~60-day retirement window once a successor ships.</div></div>
        <div class="col"><div class="col-label">What regulated workflows need</div><div class="col-body">Explicit version pinning and golden-set regression suites — before the clock runs out.</div></div>
      </div>
      <div class="num">11 / 21</div>
    </div>

    <div class="slide" data-slide="12">
      <div class="kicker">Finding 08 — Governance &amp; Law</div>
      <h2>The AI Act timeline.</h2>
      <div class="timeline">
        <div class="pt" style="left:5%;"></div>
        <div class="pt" style="left:45%;"></div>
        <div class="pt" style="left:85%;"></div>
      </div>
      <div class="timeline-labels">
        <div>Feb 2025<br>AI-literacy already binding</div>
        <div>Dec 2026<br>Article 5 safeguards due</div>
        <div>Dec 2027<br>High-risk regime begins</div>
      </div>
      <div class="num">12 / 21</div>
    </div>

    <div class="slide" data-slide="13">
      <div class="kicker">Part 5</div>
      <h2>Five things the vendor<br>pitch leaves out.</h2>
      <p class="lab">Each one contradicts a piece of consensus, rests on disclosed evidence, and can be proven wrong by a specific, named piece of counter-evidence.</p>
      <div class="num">13 / 21</div>
    </div>

    <div class="slide" data-slide="14">
      <div class="kicker">Claim One</div>
      <h2>Falling token prices.<br>Rising task costs. Both true.</h2>
      <div class="stat-pair">
        <div class="item"><div class="val">5–10×</div><div class="lbl">cheaper per year, for a fixed capability level</div></div>
        <div class="item"><div class="val">3–18×</div><div class="lbl">pricier per year, to run the frontier model</div></div>
      </div>
      <div class="chart-caption">The industry quotes whichever one suits the conversation.</div>
      <div class="num">14 / 21</div>
    </div>

    <div class="slide" data-slide="15">
      <div class="kicker">The Fix</div>
      <h2>A governed operating system,<br>not a subscription.</h2>
      <p class="lab">Buying access to a model isn't a strategy. The organizations closing the gap are the ones installing an actual operating system around their AI use — not the ones with the newest model.</p>
      <div class="num">15 / 21</div>
    </div>

    <div class="slide" data-slide="16">
      <div class="kicker">Step 1</div>
      <h2>Initial Assessment</h2>
      <p class="lab">The same diagnostic we'd run on ourselves — cost, data exposure, security, and ownership — to find what's actually broken before recommending anything. Most engagements start here because most companies genuinely don't know their own exposure yet.</p>
      <div class="num">16 / 21</div>
    </div>

    <div class="slide" data-slide="17">
      <div class="kicker">Step 2</div>
      <h2>Platform Hub Design</h2>
      <p class="lab">A thin platform hub with real mandate — 4 to 8 people, senior enough to say no. The structure that turns scattered pilots into a governed system.</p>
      <div class="num">17 / 21</div>
    </div>

    <div class="slide" data-slide="18">
      <div class="kicker">Step 3</div>
      <h2>Operating Cadence</h2>
      <p class="lab">Portfolio discipline, vendor strategy, agent readiness — the ongoing rhythm that keeps the system defensible as it scales.</p>
      <div class="num">18 / 21</div>
    </div>

    <div class="slide" data-slide="19">
      <div class="kicker">Where Things Stand</div>
      <h2>Eight categories.<br>Uneven maturity.</h2>
      <div class="matrix">
        <div class="matrix-row"><div class="cat">Economics</div><div class="status">Emerging</div></div>
        <div class="matrix-row"><div class="cat">Data Exposure</div><div class="status">Known controls, thin adoption</div></div>
        <div class="matrix-row"><div class="cat">Vendor Strategy</div><div class="status">Unsolved</div></div>
        <div class="matrix-row"><div class="cat">Adoption vs. Governance</div><div class="status">Emerging consensus</div></div>
        <div class="matrix-row"><div class="cat">Security — Excessive Agency</div><div class="status">Partial by design</div></div>
        <div class="matrix-row"><div class="cat">Security — Supply Chain</div><div class="status">Known controls, thin adoption</div></div>
        <div class="matrix-row"><div class="cat">Reliability</div><div class="status">Mature, under-adopted</div></div>
        <div class="matrix-row"><div class="cat">Governance &amp; Law</div><div class="status">Mature instruments</div></div>
      </div>
      <div class="num">19 / 21</div>
    </div>

    <div class="slide" data-slide="20">
      <div class="kicker">Proof</div>
      <h2>We don't just advise.<br>We build and validate.</h2>
      <p class="lab">AIR and ATRE are AI systems we've architected ourselves, each gated by the same adversarial-review and out-of-sample validation discipline we bring to every engagement.</p>
      <div class="num">20 / 21</div>
    </div>

    <div class="slide dark" data-slide="21">
      <div class="kicker">Work With Us</div>
      <h2>The gap is closeable.<br>It won't stay small.</h2>
      <p>Alphaworx installs the operating system that turns AI access into a governed, defensible advantage. info@alphaworx.io</p>
      <div class="num">21 / 21</div>
    </div>

  </div>

  <div class="progress" id="progress" style="width:4.8%"></div>
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

- [ ] **Step 2: Verify structurally (no browser available to you)**

Read the file back and confirm:
- Exactly 21 elements matching `<div class="slide` (search/count them), with `data-slide="1"` through `data-slide="21"` in order, all inside the single `<div class="deck">...</div>` container.
- Exactly 4 slides carry the `dark` class: `data-slide="1"`, `data-slide="7"`, `data-slide="8"`, `data-slide="21"`. No others.
- Every slide's `.num` div reads `N / 21` where `N` matches that slide's own `data-slide` number — spot check at least slides 1, 9, 14, 19, and 21.
- The `#progress` div's inline `style="width:4.8%"` is present (this is `1/21` as a percentage, replacing the old `8.3%` which was `1/12`).
- The `<script>` block, `.hint` div, and the five new CSS component blocks (`.bar-chart`, `.timeline`, `.split-compare`, `.stat-pair`, `.matrix` and their nested rules) are all present exactly as given above — this was a full-file replacement, so confirm nothing from the original file's structure (the `<script>` logic in particular) was accidentally altered.

- [ ] **Step 3: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git add deck.html
git commit -m "Expand deck to 21 slides with monochrome data visualizations"
```

---

## Task 2: Live verification

**Files:** none (verification only)

- [ ] **Step 1: Click through all 21 slides in the Browser pane**

Open `deck.html` (via the deployed Render URL or a local preview) and click through from slide 1 to slide 21, confirming:
- The progress bar fills smoothly from ~4.8% to 100%.
- Each of the 5 new chart types renders without overflow or clipped text at the deck's `min(92vw, 960px)` width: the Economics bar chart (slide 4), the Data Exposure big-stat (slide 5), the Vendor Strategy split-compare (slide 6), the Adoption-vs-Governance bar chart (slide 7, dark), the Security section divider (slide 8, dark), the Excessive Agency bar chart (slide 9), the Supply Chain big-stat (slide 10), the Reliability split-compare (slide 11), the EU AI Act timeline (slide 12), the Vendor Reality Check intro (slide 13), the token-price stat-pair (slide 14), and the maturity matrix (slide 19, 8 rows).
- Left-arrow navigation steps backward correctly from slide 21.

- [ ] **Step 2: Check print output**

Open the browser's print preview (Cmd+P) and confirm all 21 slides render one per page, none clipped, with `.hint` and `.progress` hidden per the existing `@media print` rule (unchanged from before — this is a regression check, not new functionality).

- [ ] **Step 3: Push and confirm live**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git push
```

Wait for Render to redeploy, then reload the live `deck.html` URL and repeat the slide-1-to-21 click-through to confirm the deployed version matches.
