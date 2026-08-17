---
title: Your AI's supply chain is now an attack surface
category: Security
date: 2026-07-21
excerpt: Model files can execute code the moment they're loaded. Researchers have found over 200,000 vulnerable instances of the protocol connecting AI assistants to outside tools.
slug: ai-supply-chain-attack-surface
---
A model file doesn't look like software. That's exactly the problem — because in the formats most teams still use, it is software, and treating it like a data asset instead of executable code is how a supply-chain vulnerability ends up onboarded through a data-procurement process that was never built to catch it.

The mechanism is old and well understood in security circles, just newly relevant here. A common model serialization format is built on a system that can run arbitrary code the moment the file is opened. Researchers have already found real examples on public model-sharing platforms carrying hidden payloads, engineered specifically to evade the scanning tools meant to catch them. The proof-of-concept stage is where this sits today. The technique doesn't require a proof-of-concept stage to stay proven.

The newer version of the same problem lives one layer up, in the protocols that let AI assistants reach outside tools and data sources. A widely used transport mechanism in one such protocol has been found to execute operating system commands without sanitization, across every major SDK implementing it — not as scattered coding mistakes, but as a systemic design choice. Security researchers have identified well over 200,000 vulnerable instances in the wild, with thousands of servers found responding to unauthenticated requests.

> Model files execute code on load; tool protocols place sanitization downstream. Scanners have documented gaps; a protocol designer's risk transfer cannot be undone by the adopter.

The uncomfortable part isn't the vulnerability count — it's who's responsible for closing it. When the organization that designed the protocol confirms the behavior was intentional and assigns sanitization responsibility to whoever adopts it downstream, that's a legitimate engineering decision and a real risk transfer landing on every company that plugs in. The response looks exactly like the controls a mature security team already applies to any third-party executable: signed model registries, process isolation for tool servers, explicit version pinning, and treating every model file and every tool connection as untrusted until proven otherwise. The tooling and vocabulary already exist. What's missing in most companies is the decision to route AI components through a software-procurement process instead of a data one.
