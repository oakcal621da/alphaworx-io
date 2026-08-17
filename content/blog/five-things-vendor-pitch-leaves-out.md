---
title: Five things the AI vendor pitch leaves out
category: Vendor Reality Check
date: 2026-08-04
excerpt: Each of these contradicts a piece of vendor consensus, rests on disclosed evidence, and can be proven wrong by a specific, named piece of counter-evidence.
slug: five-things-vendor-pitch-leaves-out
---
Most vendor claims about enterprise AI aren't false. They're incomplete in a specific, predictable direction — true enough to survive a sales call, missing exactly the part that shows up on the invoice or the risk register three months later. Here are five, each stated so it could be proven wrong if the evidence changed.

**One: falling token prices and rising task costs are both true at once.** The industry quotes whichever one suits the conversation. The same body of evidence that shows a steady annual decline in the price of a fixed capability level also shows the price of running frontier models rising several-fold per year. Add the mechanics vendors don't lead with — a tokenizer that produces meaningfully more tokens for the same text, a model's internal reasoning billed as output, a residency multiplier for certain configurations — and a genuine headline price cut can still arrive as a bigger bill.

**Two: the standard fix for unpredictable spend buys a price, not a supply.** Reserved-capacity offerings are pitched as solving cost unpredictability. Read the fine print and most vendors say plainly that a reservation doesn't guarantee capacity is actually available when you need it — only a price if it is. The buyer trades price risk for availability risk and, in most risk registers, that risk doesn't even get a row.

**Three: "we don't train on your data" is the weakest of the guarantees that actually matter.** It's nearly universal on commercial tiers and nearly irrelevant to the incidents that actually cause loss. The guarantee that matters is retention scope — and it's typically narrower than buyers assume, often excluding exactly the stateful, multi-turn features the industry is racing toward.

> Each of these contradicts a specific consensus view, rests on disclosed evidence, and can be falsified.

**Four: security here is bought with capability, and the price is now published.** The best publicly benchmarked defense against prompt injection holds a meaningfully lower task-success rate than an undefended system, at a real token-cost premium. Every control that measurably works does so by removing capability. "We'll add guardrails later" isn't a plan — guardrails are a design constraint, not a feature you bolt on.

**Five: AI deployment is an information-governance audit that arrives whether or not you asked for one.** The common fear is that an AI assistant creates a new data-leakage risk. The more common reality is closer to the opposite: the assistant didn't create the over-permissioned file share, it made two decades of accumulated permission drift searchable in plain English. The remediation isn't an AI control — it's access review and retention cleanup that should have happened years ago, and now has a deadline.

None of these five are reasons to avoid deploying AI. They're reasons to price the whole picture before a vendor's pitch deck prices half of it for you.
