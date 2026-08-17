# Deck v3 Comprehensive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `deck.html` (currently 12 slides on `main`) with a comprehensive 41-slide presentation combining a new value-creation narrative (from AI Strategy Playbook v2) with the existing risk/control material, in a richer table-driven visual template.

**Architecture:** `deck.html` stays a single, self-contained, dependency-free HTML/CSS/JS file, built fresh from `main`'s current 12-slide version (NOT from the `deck-expansion` branch, which is discarded). New CSS adds a "rich" slide template (header + takeaway callout + data table/chip-row/narrative content + footline) alongside the existing "simple" template (used for title/dividers/closing) and the chart components from the discarded v2 branch (bar-chart, timeline, split-compare, stat-pair, matrix — ported in fresh, including the print-mode fix already discovered on that branch). Content is built in 3 sequential append tasks (each growing the file), followed by full verification.

**Tech Stack:** Plain HTML/CSS/JS — no chart library, no build step, no new dependencies.

---

## Reference

- Design spec: [`docs/superpowers/specs/2026-08-17-deck-v3-comprehensive-design.md`](../specs/2026-08-17-deck-v3-comprehensive-design.md)
- Source material: `/Users/DSA/Seneca Projects/AI Strategy Playbook/AI Strategy Playbook v2.html` (read-only reference, not part of this repo)
- **Content depth policy (from the spec — keep this in mind across every task):** the 8 risk findings and the 4 narrative walkthroughs get full detail. The 6 "framework" slides (Portfolio Scoring, Data Foundation, Ownership & RACI, Metrics & ROI, Workforce Adoption, Industry Overlays) show the shape of the framework (names, one example) and deliberately withhold the complete operational worksheet — this is intentional, not incomplete content. Do not "fill in" these slides with more detail from the source document even if it's tempting to be thorough — the trimmed version is the spec.

## File Structure

- Modify: `deck.html` (full replacement, then two subsequent append edits)

All paths relative to repo root: `/Users/DSA/Seneca Projects/Alphaworx Website`.

---

## Task 1: CSS framework + Open + Part 1 + Part 2 (slides 1-13)

**Files:**
- Modify: `deck.html` (full replacement)

- [ ] **Step 1: Replace `deck.html` entirely with the content below**

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
  .slide.dark .findings-list div { color:#ccc; }
  .slide.dark .findings-list b { color:#fff; }
  .num { position:absolute; bottom:3vh; right:4vw; font-size:0.75vw; color:#ccc; }
  .slide.dark .num { color:#555; }
  .progress { position:fixed; bottom:0; left:0; height:3px; background:#111; transition:width 0.2s; }
  .hint { position:fixed; bottom:16px; left:50%; transform:translateX(-50%); font-size:11px; color:#999; letter-spacing:0.04em; }

  /* ===== chart components ===== */
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
  .slide.dark .chart-caption { color:#999; }

  .timeline { display:flex; align-items:center; margin:3vh 0 2vh; max-width:600px; position:relative; height:2px; background:#ddd; }
  .timeline .pt { position:absolute; top:-4px; width:10px; height:10px; border-radius:50%; background:#111; }
  .timeline-labels { display:flex; justify-content:space-between; max-width:600px; font-size:0.8vw; color:#666; }
  .timeline-labels div { max-width:33%; }

  .split-compare { display:flex; gap:3vw; margin-top:3vh; max-width:640px; }
  .split-compare .col { flex:1; }
  .split-compare .col-label { font-size:0.85vw; text-transform:uppercase; letter-spacing:0.08em; color:#111; font-weight:600; margin-bottom:1vh; }
  .split-compare .col-body { font-size:1.05vw; color:#5b5b5e; line-height:1.6; }
  .slide.dark .split-compare .col-label { color:#fff; }
  .slide.dark .split-compare .col-body { color:#aaa; }

  .stat-pair { display:flex; gap:4vw; margin-top:3vh; }
  .stat-pair .item { flex:1; }
  .stat-pair .item .val { font-size:3.2vw; font-weight:200; letter-spacing:-0.02em; }
  .stat-pair .item .lbl { font-size:0.9vw; color:#666; margin-top:0.8vh; max-width:260px; }
  .slide.dark .stat-pair .item .lbl { color:#999; }

  .matrix { display:flex; flex-direction:column; max-width:640px; margin-top:2.5vh; }
  .matrix-row { display:flex; justify-content:space-between; align-items:center; padding:1vh 0; border-top:1px solid #ececec; }
  .matrix-row:last-child { border-bottom:1px solid #ececec; }
  .matrix-row .cat { font-size:0.95vw; color:#333; }
  .matrix-row .status { font-size:0.75vw; letter-spacing:0.04em; text-transform:uppercase; color:#888; font-weight:600; }
  .slide.dark .matrix-row { border-top-color:#333; }
  .slide.dark .matrix-row:last-child { border-bottom-color:#333; }
  .slide.dark .matrix-row .cat { color:#ccc; }

  /* ===== v3 rich template ===== */
  .slide.rich { padding:4vh 5.5vw 3vh; }
  .rich-top { display:flex; justify-content:space-between; align-items:flex-start; gap:3vw; margin-bottom:1.6vh; }
  .rich-top .htext { max-width:58%; }
  .rich-top h2.rh { font-size:1.9vw; font-weight:600; letter-spacing:-0.01em; line-height:1.28; margin-bottom:0; }
  .takeaway { max-width:32%; font-size:0.78vw; color:#666; line-height:1.55; border-left:2px solid #111; padding-left:1vw; flex:none; }
  .slide.dark .takeaway { color:#aaa; border-left-color:#fff; }

  .data-table { width:100%; border-collapse:collapse; font-size:0.8vw; margin-top:1vh; }
  .data-table th { text-align:left; font-size:0.62vw; letter-spacing:0.06em; text-transform:uppercase; color:#999; font-weight:700; padding:0.9vh 1vw 0.9vh 0; border-bottom:2px solid #111; }
  .data-table td { padding:1vh 1vw 1vh 0; border-bottom:1px solid #ececec; vertical-align:top; color:#333; line-height:1.42; }
  .data-table tr:last-child td { border-bottom:none; }
  .data-table td.label { font-weight:700; color:#111; white-space:nowrap; }
  .slide.dark .data-table th { color:#888; border-bottom-color:#fff; }
  .slide.dark .data-table td { color:#ccc; border-bottom-color:#333; }
  .slide.dark .data-table td.label { color:#fff; }

  .footline { margin-top:auto; padding-top:1.4vh; display:flex; justify-content:space-between; align-items:center; border-top:1px solid #ececec; }
  .footline .brand { font-size:0.62vw; color:#999; letter-spacing:0.04em; }
  .footline .n { font-size:0.62vw; color:#bbb; }
  .slide.dark .footline { border-top-color:#333; }
  .slide.dark .footline .brand, .slide.dark .footline .n { color:#666; }

  .chip-row { display:flex; flex-wrap:wrap; gap:0.7vw; margin-top:1.8vh; }
  .chip { border:1px solid #ddd; border-radius:20px; padding:0.7vh 1.1vw; font-size:0.85vw; color:#333; white-space:nowrap; }
  .slide.dark .chip { border-color:#444; color:#ddd; }

  .narrative { font-size:0.98vw; line-height:1.68; color:#3d3d40; max-width:680px; margin-top:1.2vh; }
  .slide.dark .narrative { color:#bbb; }

  .two-col { display:flex; gap:3vw; margin-top:1.6vh; }
  .two-col .col { flex:1; }
  .two-col .col h4 { font-size:0.85vw; text-transform:uppercase; letter-spacing:0.06em; color:#111; font-weight:700; margin-bottom:0.8vh; }
  .slide.dark .two-col .col h4 { color:#fff; }
  .two-col .col p { font-size:0.85vw; color:#5b5b5e; line-height:1.6; max-width:none; }
  .slide.dark .two-col .col p { color:#aaa; }

  @media print {
    html, body { height:auto; overflow:visible; background:#fff; }
    .deck { display:block; height:auto; }
    .slide { display:flex !important; width:100%; aspect-ratio:16/9; page-break-after:always; box-shadow:none; }
    .progress, .hint { display:none; }
    .bar-chart { height:16vw; margin-top:2vw; }
    .timeline { margin:2vw 0 1.5vw; }
    .split-compare, .stat-pair, .matrix { margin-top:2vw; }
    .chart-caption { margin-top:1vw; }
    .footline { margin-top:1vw; padding-top:1vw; }
    .rich-top { margin-bottom:1vw; }
    .chip-row, .narrative, .two-col { margin-top:1vw; }
  }
</style>
</head>
<body>
  <div class="deck">

    <div class="slide dark active" data-slide="1">
      <div class="kicker">Alphaworx</div>
      <h1>The AI Strategy Gap</h1>
      <p>Why the businesses winning right now aren't the ones with the best model.</p>
      <div class="num">1 / 41</div>
    </div>

    <div class="slide" data-slide="2">
      <div class="kicker">The Stakes</div>
      <div class="big">3</div>
      <div class="lab">years old. AI as a serious enterprise capability is barely three years into its cycle — the gap between the companies getting it right and the ones improvising is just starting to open.</div>
      <div class="num">2 / 41</div>
    </div>

    <div class="slide dark" data-slide="3">
      <div class="kicker">The Executive Promise</div>
      <h2>Five commitments,<br>not a transformation slogan.</h2>
      <div class="findings-list">
        <div><b>Strategy —</b> decide where AI should create advantage, not just where it can be demonstrated.</div>
        <div><b>Portfolio —</b> fund the few use cases, platform capabilities, and controls that matter most.</div>
        <div><b>Control —</b> make cost, data movement, model behavior, and vendor dependency visible and governable.</div>
        <div><b>Change —</b> redesign work so adoption becomes operational value, not optional tool usage.</div>
        <div><b>Evidence —</b> measure benefits, risks, and decision quality in a form executives can act on.</div>
      </div>
      <div class="num">3 / 41</div>
    </div>

    <div class="slide dark" data-slide="4">
      <div class="kicker">Part 1</div>
      <h2>Where AI Creates Value.</h2>
      <p>Value concentrates where knowledge work is high-volume, decision cycles are slow, and proprietary context changes the answer. Discovery starts with work systems, not tool ideas.</p>
      <div class="num">4 / 41</div>
    </div>

    <div class="slide rich" data-slide="5">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 1 — The AI Value Thesis</div>
          <h2 class="rh">A testable statement,<br>not a slogan.</h2>
        </div>
        <div class="takeaway">"Become AI-first" is not a strategy. A real value thesis names the workflow, the metric, and the guardrail.</div>
      </div>
      <table class="data-table">
        <tr><th>Weak statement</th><th>Better statement</th><th>Why it's better</th></tr>
        <tr><td>Use AI to improve productivity</td><td>Cut customer-support after-call work by 50% while holding QA scores flat</td><td>Names workflow, metric, and quality guardrail</td></tr>
        <tr><td>Deploy AI across the enterprise</td><td>Prioritize sales, support, and engineering — high-volume knowledge work with measurable baselines</td><td>Creates portfolio boundaries</td></tr>
        <tr><td>Build an AI assistant for employees</td><td>Build a policy assistant only after HR, legal, and IT sources of truth are cleaned and permissioned</td><td>Ties ambition to data readiness</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">5 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="6">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 1 — Value Thesis</div>
          <h2 class="rh">Three categories,<br>funded differently.</h2>
        </div>
      </div>
      <div class="two-col">
        <div class="col"><h4>Table-stakes</h4><p>Capabilities the firm needs to remain operationally current — employee copilots, support drafting, research assistance.</p></div>
        <div class="col"><h4>Differentiating</h4><p>Capabilities tied to proprietary data, workflow depth, or domain expertise that competitors can't copy quickly.</p></div>
        <div class="col"><h4>Strategic options</h4><p>Higher-uncertainty experiments that could become new products, channels, or operating models if the economics prove out.</p></div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">6 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="7">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 1 — Walkthrough</div>
          <h2 class="rh">"We want AI for operations"<br>is not a strategy.</h2>
        </div>
      </div>
      <div class="narrative">A mid-market logistics company starts there. After assessment, the real thesis becomes: use AI to compress exception resolution in freight operations by giving coordinators a governed assistant that reads shipment status, customer commitments, and carrier communications, then drafts next actions for human approval.<br><br>That focuses the portfolio. Generic employee chat becomes table stakes. Freight exception management becomes the strategic bet. Data cleanup now has a business reason. The metric isn't "AI usage" — it's exception cycle time, escalation rate, and margin leakage on delayed shipments.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">7 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="8">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 1 — Value Pools</div>
          <h2 class="rh">Value concentrates<br>in six pools.</h2>
        </div>
      </div>
      <table class="data-table">
        <tr><th>Value pool</th><th>Typical opportunities</th><th>What to measure</th></tr>
        <tr><td class="label">Revenue Growth</td><td>Sales research, next-best action, proposal generation</td><td>Conversion, win rate, deal size</td></tr>
        <tr><td class="label">Margin &amp; Productivity</td><td>Document processing, engineering copilots, finance close</td><td>Cycle time, throughput, cost</td></tr>
        <tr><td class="label">Customer Experience</td><td>Support agents, personalization, onboarding</td><td>First-contact resolution, CSAT</td></tr>
        <tr><td class="label">Risk &amp; Compliance</td><td>Contract review, policy monitoring, audit prep</td><td>Error detection, time to remediate</td></tr>
        <tr><td class="label">Product Differentiation</td><td>In-product AI features, domain assistants</td><td>Activation, retention, adoption</td></tr>
        <tr><td class="label">Strategic Learning</td><td>Frontier experiments, agentic workflows</td><td>Validated assumptions, option value</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">8 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="9">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 1 — Discovery</div>
          <h2 class="rh">Map the workflow<br>before collecting ideas.</h2>
        </div>
        <div class="takeaway">"Build a chatbot" is not a use case. "Reduce Tier 2 escalations by drafting grounded answers from approved sources" is.</div>
      </div>
      <div class="narrative">Discovery starts with the current workflow on the wall — trigger, inputs, human decisions, handoffs, rework, approvals, and final outcome. Then: where could AI reduce search, summarization, classification, or decision support? And just as important — where would AI be dangerous, legally sensitive, or economically irrelevant?</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">9 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="10">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 1 — Portfolio Scoring</div>
          <h2 class="rh">Every use case scored<br>across ten dimensions.</h2>
        </div>
        <div class="takeaway">The scoring discussion is more valuable than the arithmetic — it's where a wishlist becomes a fundable portfolio.</div>
      </div>
      <div class="chip-row">
        <div class="chip">Enterprise value</div>
        <div class="chip">Measurability</div>
        <div class="chip">Feasibility</div>
        <div class="chip">Data readiness</div>
        <div class="chip">Risk level</div>
        <div class="chip">Adoption readiness</div>
        <div class="chip">Reusability</div>
        <div class="chip">Time to impact</div>
        <div class="chip">Sponsor strength</div>
        <div class="chip">Strategic fit</div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">10 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="11">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 2 — Building the Portfolio</div>
          <h2 class="rh">Six classes,<br>funded differently.</h2>
        </div>
      </div>
      <table class="data-table">
        <tr><th>Class</th><th>What it is</th></tr>
        <tr><td class="label">Quick Wins</td><td>Low-to-moderate risk, measurable value, fast adoption — builds confidence and operating muscle.</td></tr>
        <tr><td class="label">Strategic Bets</td><td>High-value, high-sponsorship initiatives tied to differentiation. Senior attention, real platform support.</td></tr>
        <tr><td class="label">Platform Investments</td><td>Gateways, evaluation, identity, retrieval. Rarely win demo day; determine whether scale is possible.</td></tr>
        <tr><td class="label">Risk Necessities</td><td>Compliance, auditability, security work — funded even when the ROI is avoided loss.</td></tr>
        <tr><td class="label">Experiments</td><td>Uncertain but learnable ideas with explicit kill criteria.</td></tr>
        <tr><td class="label">Park or Kill</td><td>Weak ownership, vague metrics, poor data, or risk disproportionate to value.</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">11 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="12">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 2 — Walkthrough</div>
          <h2 class="rh">Twenty-eight ideas.<br>One fundable portfolio.</h2>
        </div>
      </div>
      <div class="narrative">A company arrives with twenty-eight AI ideas. The loudest sponsor wants a customer-facing agent — high value, but low data readiness and real risk exposure. Under the ten-dimension scoring, that's not a "no." It means the platform and data work has to be funded before the use case can be promised, not launched on hope.<br><br>Meanwhile a low-visibility idea — a reusable document-retrieval pattern — scores modestly on enterprise value but high on reusability and platform leverage. It gets funded first. The flashy idea gets its platform dependency scheduled honestly instead of quietly slipping. That's what portfolio discipline actually buys: not fewer ideas, but a funding order the organization can defend.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">12 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="13">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 2 — Data Foundation</div>
          <h2 class="rh">A model is a confident<br>interface to your data.</h2>
        </div>
        <div class="takeaway">Good or bad, the model amplifies whatever it's sitting on. AI programs need governed data products, not one-off extracts.</div>
      </div>
      <div class="chip-row">
        <div class="chip">Ownership</div>
        <div class="chip">Quality</div>
        <div class="chip">Permissioning</div>
        <div class="chip">Lineage</div>
        <div class="chip">Unstructured content</div>
        <div class="chip">Retention</div>
        <div class="chip">Semantic layer</div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">13 / 41</div></div>
    </div>

  </div>

  <div class="progress" id="progress" style="width:2.4%"></div>
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

Note: the `.progress` bar and `.num` labels reference `/ 41` and `2.4%` (1/41) even though this task only produces 13 slides — this is expected and intentional (later tasks append the remaining 28 slides; `slides.length` in the live DOM will actually be 13 until Task 2/3 land, so the progress bar will visually reach 100% at slide 13 until then — this is a known, temporary intermediate state, not a bug to fix in this task).

- [ ] **Step 2: Verify structurally**

Read the file back and confirm:
- 13 `<div class="slide` elements, `data-slide="1"` through `"13"`, in order, inside `.deck`.
- Dark slides at exactly `data-slide="1"`, `"3"`, `"4"` — no others in this range.
- All new CSS component classes present: `.bar-chart`, `.timeline`, `.split-compare`, `.stat-pair`, `.matrix`, `.rich-top`, `.data-table`, `.footline`, `.chip-row`, `.narrative`, `.two-col`, plus their `.slide.dark` overrides and the `@media print` block.
- The `<script>` block matches the version from the previous deck builds exactly (unchanged navigation logic).

- [ ] **Step 3: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/.worktrees/deck-v3"
git add deck.html
git commit -m "Deck v3: new CSS framework + Open, Part 1, Part 2 (slides 1-13)"
```

---

## Task 2: Part 3 + Part 4 (slides 14-32)

**Files:**
- Modify: `deck.html` (append)

- [ ] **Step 1: Insert the following 19 slides between the closing `</div>` of `data-slide="13"` and the closing `</div>` of the `.deck` container**

```html
    <div class="slide dark" data-slide="14">
      <div class="kicker">Part 3</div>
      <h2>What Puts That Value at Risk.</h2>
      <p>Every control that measurably works does so by removing capability. Guardrails are a design constraint, not something you bolt on later.</p>
      <div class="num">14 / 41</div>
    </div>

    <div class="slide rich" data-slide="15">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 01 — Economics</div>
          <h2 class="rh">Token prices fall.<br>The bill still rises.</h2>
        </div>
        <div class="takeaway">A 9.2× swing driven by caching, batching, and tokenizer settings — before a single line of business logic changes.</div>
      </div>
      <div class="bar-chart">
        <div class="bar-col"><div class="bar-val">$0.06</div><div class="bar" style="height:12%;"></div><div class="bar-label">Cheapest config</div></div>
        <div class="bar-col"><div class="bar-val">$0.55</div><div class="bar hi" style="height:100%;"></div><div class="bar-label">Priciest config</div></div>
      </div>
      <div class="chart-caption">Same 50k-input, 2k-output job.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">15 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="16">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 02 — Data Exposure</div>
          <h2 class="rh">Shadow AI is your<br>biggest exposure.</h2>
        </div>
        <div class="takeaway">The one number moving the right way: personal-account use fell from 78% to 47% in a year, as governed alternatives rolled out.</div>
      </div>
      <div class="big">43%</div>
      <div class="lab">of breached organizations had a shadow-AI incident in 2026 — up from 20% the year before. Average cost: $5.39M per incident.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">16 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="17">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 03 — Vendor Strategy</div>
          <h2 class="rh">You don't control<br>the control plane.</h2>
        </div>
      </div>
      <div class="split-compare">
        <div class="col"><div class="col-label">You control</div><div class="col-body">Orchestration, retrieval pipeline, agent wiring, prompts.</div></div>
        <div class="col"><div class="col-label">The vendor controls</div><div class="col-body">Pricing, deprecation schedule, rate limits, data-use terms.</div></div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">17 / 41</div></div>
    </div>

    <div class="slide rich dark" data-slide="18">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 04 — Adoption vs. Governance</div>
          <h2 class="rh">Everyone has adopted AI.<br>Almost no one has governed it.</h2>
        </div>
      </div>
      <div class="bar-chart">
        <div class="bar-col"><div class="bar-val">74%</div><div class="bar hi" style="height:100%;"></div><div class="bar-label">Expect substantial agent use by 2027</div></div>
        <div class="bar-col"><div class="bar-val">21%</div><div class="bar" style="height:28%;"></div><div class="bar-label">Report mature agent governance today</div></div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">18 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="19">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 05 — Security</div>
          <h2 class="rh">Excessive agency jumped<br>from 6th to 3rd.</h2>
        </div>
        <div class="takeaway">No attacker required — just an agent with permissions nobody scoped down.</div>
      </div>
      <div class="stat-pair">
        <div class="item"><div class="val">6th → 3rd</div><div class="lbl">OWASP GenAI/LLM Top 10 rank, 2025 to 2026</div></div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">19 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="20">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 06 — Security</div>
          <h2 class="rh">Your AI's supply chain<br>is an attack surface.</h2>
        </div>
      </div>
      <div class="big">200,000+</div>
      <div class="lab">vulnerable instances of the protocol connecting AI assistants to outside tools — model files that can execute code the moment they're loaded.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">20 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="21">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 07 — Reliability</div>
          <h2 class="rh">Model deprecation is a<br>reliability risk, not an IT ticket.</h2>
        </div>
      </div>
      <div class="split-compare">
        <div class="col"><div class="col-label">What vendors give you</div><div class="col-body">An observed ~60-day retirement window once a successor ships.</div></div>
        <div class="col"><div class="col-label">What regulated workflows need</div><div class="col-body">Explicit version pinning and golden-set regression suites — before the clock runs out.</div></div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">21 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="22">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Finding 08 — Governance &amp; Law</div>
          <h2 class="rh">The AI Act timeline.</h2>
        </div>
      </div>
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
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">22 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="23">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 3 — Vendor Reality Check</div>
          <h2 class="rh">Five things the vendor<br>pitch leaves out.</h2>
        </div>
        <div class="takeaway">Each one contradicts a piece of consensus and can be proven wrong by a specific, named piece of counter-evidence.</div>
      </div>
      <table class="data-table">
        <tr><th>Consensus claim</th><th>What's actually true</th></tr>
        <tr><td>Inference is exponentially cheaper, so cost is transitional</td><td>Frontier model run cost rises 3–18×/yr even as fixed-capability cost falls 5–10×/yr</td></tr>
        <tr><td>Reserve capacity and the cost problem is solved</td><td>Reservations guarantee a price, not that capacity is actually available</td></tr>
        <tr><td>"We don't train on your data" is the guarantee that matters</td><td>Retention scope is the real instrument — and it's narrower than most buyers assume</td></tr>
        <tr><td>Guardrails are a feature you add</td><td>Every control that measurably works does so by removing capability</td></tr>
        <tr><td>AI creates a new data-leakage risk</td><td>It mostly makes decades of permission drift searchable in plain English</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">23 / 41</div></div>
    </div>

    <div class="slide dark" data-slide="24">
      <div class="kicker">Part 4</div>
      <h2>The Operating System.</h2>
      <p>Buying access to a model isn't a strategy. The organizations closing the gap are the ones installing an actual operating system around their AI use.</p>
      <div class="num">24 / 41</div>
    </div>

    <div class="slide rich" data-slide="25">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — The Fix</div>
          <h2 class="rh">A governed operating system,<br>not a subscription.</h2>
        </div>
      </div>
      <div class="narrative">Buying access to a model isn't a strategy. The organizations closing the gap are the ones installing an actual operating system around their AI use — not the ones with the newest model.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">25 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="26">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Step 1</div>
          <h2 class="rh">Initial Assessment</h2>
        </div>
      </div>
      <div class="narrative">The same diagnostic we'd run on ourselves — cost, data exposure, security, and ownership — to find what's actually broken before recommending anything. Most engagements start here because most companies genuinely don't know their own exposure yet.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">26 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="27">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Step 2 — Ownership</div>
          <h2 class="rh">Ambiguous ownership stalls<br>more programs than bad models do.</h2>
        </div>
        <div class="takeaway">A title alone doesn't fix it. A Chief AI Officer without budget or veto rights just reproduces the same turf problem one level up.</div>
      </div>
      <table class="data-table">
        <tr><th>Decision</th><th>Accountable</th><th>Common failure</th></tr>
        <tr><td class="label">Production deployment approval</td><td>AI platform owner or delegated council</td><td>Everyone can object, nobody can decide</td></tr>
        <tr><td class="label">Data-source approval</td><td>Data owner</td><td>AI team assumes access equals permission</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">27 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="28">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Step 3</div>
          <h2 class="rh">Thin Platform Hub Design</h2>
        </div>
      </div>
      <div class="narrative">A thin platform hub with real mandate — 4 to 8 people, senior enough to say no. The structure that turns scattered pilots into a governed system, funded as a service rather than run as a toll booth.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">28 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="29">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Step 4</div>
          <h2 class="rh">The 90-day stand-up.</h2>
        </div>
      </div>
      <table class="data-table">
        <tr><th>Phase</th><th>Focus</th></tr>
        <tr><td class="label">Days 0–30</td><td>Finish the assessment. Secure mandate. Land two or three visible quick wins.</td></tr>
        <tr><td class="label">Days 31–60</td><td>Stand up the core control-plane pieces. Start cost show-back so teams see their own usage.</td></tr>
        <tr><td class="label">Days 61–90</td><td>Get the first governed production use cases live. Establish the executive narrative.</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">29 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="30">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Beyond 90 Days</div>
          <h2 class="rh">Control, then repeatability,<br>then a managed capability.</h2>
        </div>
      </div>
      <table class="data-table">
        <tr><th>Horizon</th><th>Management question</th><th>Proof point</th></tr>
        <tr><td class="label">90 days</td><td>Do we know what's happening and who owns it?</td><td>Assessment, mandate, hub, first governed use case</td></tr>
        <tr><td class="label">180 days</td><td>Can we repeatedly move ideas to governed production?</td><td>Portfolio council, benefit tracker, service catalog</td></tr>
        <tr><td class="label">12 months</td><td>Has AI become a managed business capability?</td><td>Budget-cycle integration, executive dashboard, mature controls</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">30 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="31">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Step 5</div>
          <h2 class="rh">Operating Cadence</h2>
        </div>
      </div>
      <div class="narrative">Portfolio discipline, vendor strategy, agent readiness — the ongoing rhythm that keeps the system defensible as it scales, not a one-time stand-up that quietly decays.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">31 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="32">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 4 — Agent Readiness</div>
          <h2 class="rh">Treat agents as identities,<br>not features.</h2>
        </div>
        <div class="takeaway">Shared API keys for agents are a critical finding on their own — and should be eliminated on sight.</div>
      </div>
      <div class="narrative">Agents need joiner-mover-leaver processes like any other identity, and coverage mapped against OWASP's Top 10 for Agentic Applications — a security program that only checks the LLM Top 10 has, by construction, covered half the risk surface. 74% of leaders expect substantial agentic use by 2027. About 21% report a mature agent-governance practice today. That gap is what a new AI strategy lead inherits on day one.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">32 / 41</div></div>
    </div>
```

- [ ] **Step 2: Verify structurally**

Read the file back and confirm:
- Total slide count is now 32 (`data-slide="1"` through `"32"`), all in order, still inside the one `.deck` container, with slides 1-13 from Task 1 unchanged.
- Dark slides in this new range: exactly `data-slide="14"`, `"18"` (note: `"18"` has both `rich` and `dark` classes together), `"24"`. No others among 14-32.
- Every `.num` and footline `.n` in this range reads `N / 41` matching its own slide.

- [ ] **Step 3: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/.worktrees/deck-v3"
git add deck.html
git commit -m "Deck v3: Part 3 and Part 4 (slides 14-32)"
```

---

## Task 3: Part 5 + Close (slides 33-41)

**Files:**
- Modify: `deck.html` (append)

- [ ] **Step 1: Insert the following 9 slides between the closing `</div>` of `data-slide="32"` and the closing `</div>` of the `.deck` container**

```html
    <div class="slide dark" data-slide="33">
      <div class="kicker">Part 5</div>
      <h2>Making Value Real.</h2>
      <p>AI adoption is not the same as AI value. Value appears only when work changes, managers reinforce it, and benefits are measured against a baseline.</p>
      <div class="num">33 / 41</div>
    </div>

    <div class="slide rich" data-slide="34">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 5 — Workforce Adoption</div>
          <h2 class="rh">Segment by role,<br>not by generic literacy.</h2>
        </div>
        <div class="takeaway">Employees don't adopt AI because a policy says they may. They adopt it when the tool fits the work and the manager expects the new workflow.</div>
      </div>
      <div class="chip-row">
        <div class="chip">Executives</div>
        <div class="chip">Managers</div>
        <div class="chip">Frontline knowledge workers</div>
        <div class="chip">Technical builders</div>
        <div class="chip">Control functions</div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">34 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="35">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 5 — Walkthrough</div>
          <h2 class="rh">High usage for two weeks.<br>Then it fades.</h2>
        </div>
      </div>
      <div class="narrative">A claims team gets an AI summarization tool. Usage spikes, then fades. The issue isn't the model — managers still evaluate adjusters on old throughput measures, quality reviewers don't trust the summaries, and nobody changed the claim-note standard.<br><br>The fix redesigns the workflow: AI drafts the summary, the adjuster verifies required fields, quality reviews a sample against a rubric, and managers track cycle time instead of raw usage. Adoption becomes durable only when the operating system around the tool changes — not before.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">35 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="36">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 5 — Metrics &amp; ROI</div>
          <h2 class="rh">Usage is easy to count.<br>Value is not.</h2>
        </div>
      </div>
      <table class="data-table">
        <tr><th>Good measure</th><th>Bad proxy</th></tr>
        <tr><td>Revenue lift, cost avoided, cycle-time reduction</td><td>Number of AI ideas submitted</td></tr>
        <tr><td>Workflow penetration, manager-confirmed change</td><td>Login counts</td></tr>
        <tr><td>Unit cost per completed task</td><td>Total token spend alone</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">36 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="37">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Part 5 — Walkthrough</div>
          <h2 class="rh">"We save two hours<br>per contract." Prove it.</h2>
        </div>
      </div>
      <div class="narrative">A legal team claims an AI contract-review tool saves two hours per contract. Finance asks whether outside counsel spend fell, cycle time improved, or lawyers handled more volume. None of that was measured.<br><br>The corrected benefits case uses a real baseline: review time, outside counsel spend, cycle time by contract type, and risk exceptions. After launch, the team measures cost per reviewed contract while sampling quality. If the hours saved become faster contracting, that's value. If they just become untracked slack, the ROI was never proved.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">37 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="38">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Same System, Different Risk</div>
          <h2 class="rh">The method is the same.<br>The acceptable design isn't.</h2>
        </div>
        <div class="takeaway">A support chatbot means something different by sector — brand voice in retail, patient safety in healthcare, adverse-action rules in financial services.</div>
      </div>
      <table class="data-table">
        <tr><th>Industry</th><th>High-value themes</th><th>Special caution</th></tr>
        <tr><td class="label">Financial Services</td><td>Advisor enablement, underwriting support, fraud</td><td>Model risk management, adverse action, explainability</td></tr>
        <tr><td class="label">Healthcare / Life Sciences</td><td>Clinical documentation, prior authorization</td><td>Protected health information, clinical safety</td></tr>
        <tr><td class="label">Professional Services</td><td>Research, drafting, diligence, knowledge retrieval</td><td>Confidentiality, citation accuracy, work-product liability</td></tr>
      </table>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">38 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="39">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Where Things Stand</div>
          <h2 class="rh">Ten categories.<br>Uneven maturity.</h2>
        </div>
      </div>
      <div class="matrix">
        <div class="matrix-row"><div class="cat">Value Thesis &amp; Portfolio</div><div class="status">Emerging discipline</div></div>
        <div class="matrix-row"><div class="cat">Economics</div><div class="status">Emerging</div></div>
        <div class="matrix-row"><div class="cat">Data Exposure</div><div class="status">Known controls, thin adoption</div></div>
        <div class="matrix-row"><div class="cat">Vendor Strategy</div><div class="status">Unsolved</div></div>
        <div class="matrix-row"><div class="cat">Adoption vs. Governance</div><div class="status">Emerging consensus</div></div>
        <div class="matrix-row"><div class="cat">Security</div><div class="status">Partial by design</div></div>
        <div class="matrix-row"><div class="cat">Reliability</div><div class="status">Mature, under-adopted</div></div>
        <div class="matrix-row"><div class="cat">Governance &amp; Law</div><div class="status">Mature instruments</div></div>
        <div class="matrix-row"><div class="cat">Workforce Adoption</div><div class="status">Emerging discipline</div></div>
        <div class="matrix-row"><div class="cat">Metrics &amp; ROI</div><div class="status">Known controls, thin adoption</div></div>
      </div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">39 / 41</div></div>
    </div>

    <div class="slide rich" data-slide="40">
      <div class="rich-top">
        <div class="htext">
          <div class="kicker">Proof</div>
          <h2 class="rh">We don't just advise.<br>We build and validate.</h2>
        </div>
      </div>
      <div class="narrative">AIR and ATRE are AI systems we've architected ourselves, each gated by the same adversarial-review and out-of-sample validation discipline we bring to every engagement.</div>
      <div class="footline"><div class="brand">alphaworx.io — Enterprise AI Strategy</div><div class="n">40 / 41</div></div>
    </div>

    <div class="slide dark" data-slide="41">
      <div class="kicker">Work With Us</div>
      <h2>The gap is closeable.<br>It won't stay small.</h2>
      <p>Alphaworx installs the operating system that turns AI access into a governed, defensible advantage. info@alphaworx.io</p>
      <div class="num">41 / 41</div>
    </div>
```

- [ ] **Step 2: Verify structurally**

Read the file back and confirm:
- Exactly 41 `<div class="slide` elements total, `data-slide="1"` through `"41"`, in order, all inside the one `.deck` container, nothing from Tasks 1-2 altered.
- Dark slides across the WHOLE file: `data-slide="1"`, `"3"`, `"4"`, `"14"`, `"18"` (rich+dark), `"24"`, `"33"`, `"41"` — exactly 8, no others.
- Every `.num` and footline `.n` across the whole file reads `N / 41` matching its own slide, spot-checking at least slides 1, 13, 14, 32, 33, and 41.
- The `#progress` div's inline `style="width:2.4%"` is present (this is `1/41`).

- [ ] **Step 3: Commit**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/.worktrees/deck-v3"
git add deck.html
git commit -m "Deck v3: Part 5 and Close (slides 33-41) — complete 41-slide deck"
```

---

## Task 4: Full verification, push, and branch cleanup

**Files:** none (verification only)

- [ ] **Step 1: Click through all 41 slides in the Browser pane**

Serve `deck.html` via a locally running static server (not a raw `file://` open — that has repeatedly failed to be interactive in this environment; a simple local HTTP server, e.g. Python's `http.server`, works) and click through slide 1 to slide 41, confirming:
- The progress bar fills smoothly from ~2.4% to 100%.
- Every rich-template slide's header (kicker + headline + optional takeaway), content (data table / chip row / narrative / chart / two-col), and footline render without overflow or clipped text at the deck's `min(92vw, 960px)` width.
- Dark slides (1, 3, 4, 14, 18, 24, 33, 41) all have correct contrast — no dark-on-dark or light-on-light text (this exercises every new `.slide.dark` override added in Task 1).
- Left-arrow navigation steps backward correctly.

- [ ] **Step 2: Check print output**

Open the browser's print preview (Cmd+P) and confirm all 41 slides render one per page, none clipped, with `.hint` and `.progress` hidden. Pay particular attention to the chart-heavy slides (15, 18, 19, 20, 22) and the longest data-table slides (5, 8, 23, 30, 38) for overflow, since these combine the most content with the print-mode vw-based spacing overrides.

- [ ] **Step 3: Content-depth spot check**

Re-read the design spec's "Content depth policy" section and confirm the 6 "shape, not the tool" slides (10, 13, 27, 34, 36, 38) actually stayed trimmed — i.e., they show named categories/chips or 1-3 illustrative rows, not the complete operational table from the source document. This is a content-fidelity check, not just a code check.

- [ ] **Step 4: Push and confirm live**

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website/.worktrees/deck-v3"
git push -u origin deck-v3
```

Then follow `superpowers:finishing-a-development-branch` to merge to `main` and push. Once live, reload the deployed `deck.html` URL and repeat the slide-1-to-41 click-through to confirm the deployed version matches.

- [ ] **Step 5: Clean up the discarded `deck-expansion` branch**

The 21-slide v2 deck on the `deck-expansion` branch/worktree is superseded by this work and was never merged. Remove it:

```bash
cd "/Users/DSA/Seneca Projects/Alphaworx Website"
git worktree remove .worktrees/deck-expansion
git branch -D deck-expansion
```
