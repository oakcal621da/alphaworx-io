---
title: Excessive agency — the AI risk that doesn't need an attacker
category: Security
date: 2026-07-14
excerpt: OWASP's 2026 ranking moved this risk from sixth to third. No adversary required — just an agent with permissions nobody scoped down.
slug: excessive-agency-ai-risk-no-attacker
---
Most AI security conversations start from an attacker: someone crafting a malicious prompt, planting instructions in a document the model will read. That framing misses a risk that jumped from sixth to third place in the 2026 OWASP ranking of AI risks — and it requires no attacker at all.

Excessive agency is what happens when an AI agent has more capability, more access, or more autonomy than the task in front of it actually needs. A tool built to summarize email that can also send and delete it. A read-only research task granted broad database access because that was the credential already sitting around. A high-impact action taken without a human checkpoint, not because anyone approved skipping the checkpoint, but because nobody thought to require one. The trigger can be a hallucinated instruction from a poorly written prompt just as easily as a genuine attack — the failure mode doesn't care which one it was.

That's what makes this risk different from the ones security teams are trained to look for. There's no intrusion to detect, no malicious payload to scan for. The system did exactly what it was built to do, with permissions nobody had scoped down, and eventually used them for something nobody predicted.

> Excessive agency earns its position because it does not require an adversary at all. An agent with delete permissions it never needed will eventually use them for a reason nobody predicted.

The control isn't a smarter model or a better prompt filter. It's the unglamorous work of permission scoping — deciding, before an agent goes live, exactly what it's allowed to touch and confirming that boundary in the architecture rather than in a policy document. As agentic AI moves from pilot to production faster than most companies' governance does, that scoping work is quickly becoming the actual security perimeter, whether or not anyone's treating it that way yet.
