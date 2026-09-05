---
title: You don't control the control plane
category: Vendor Strategy
date: 2026-08-16
excerpt: Know which decisions belong to your organization, which belong to your providers, and what it would take to change course.
slug: you-dont-control-the-control-plane
updated: 2026-09-05
---

An enterprise may own its prompts, orchestration, and application code while depending on decisions made outside its boundaries. Model availability, supported features, service limits, and contractual conditions are examples. Vendor strategy begins by making that dependency visible before a service change forces the discussion.

## Separate what you operate from what you depend on

The phrase control plane can hide several different kinds of authority. Your organization decides which workflow to deploy, which data to connect, and which actions to permit. A provider decides which services and model versions it offers, subject to the agreement you have negotiated. Neither set of responsibilities disappears because an architecture diagram contains an abstraction layer.

Create a dependency record for every material workflow. Include provider, service, model or deployment identifier, account owner, data conditions, capacity arrangements, and lifecycle assumptions. Connect that record to a business owner who can explain the consequence of interruption. A dependency becomes strategically important when losing it would stop a meaningful activity or make its operation unacceptable.

## Buy time before you need an alternative

A replacement endpoint is not a replacement service until it has been evaluated in your workflow. Outputs may require different prompts, tools may behave differently, and quality or latency can move even when the integration succeeds. Microsoft publishes a [model retirement schedule](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule) by model and version; it illustrates why lifecycle tracking belongs alongside ordinary operating records.

Test a second route where the business case warrants it. That route may be another provider, a simpler model, a constrained feature set, or a manual process. Record what quality and throughput it can support. An untested multi-provider architecture can add complexity without providing dependable continuity. The important asset is a usable option with known limits.

## Translate the contract into operating questions

Ask what happens when demand exceeds the current allocation, a region becomes unavailable, or a required feature changes. Separate commercial price commitments from technical availability and deployment limits. Seek terms and evidence for the actual service you plan to use rather than general assurances about the vendor’s platform.

Do the same for data. Identify which features create persistent state, which regions process the workload, how access is administered, and how deletion is handled. [OpenAI’s API data controls documentation](https://developers.openai.com/api/docs/guides/your-data) is one example of why these questions need feature-level answers. Product documentation informs the review; the signed agreement and configured service determine the arrangement your organization relies on.

## Make switching costs observable

Estimate the work of leaving before a deadline makes the estimate urgent. Prompts, evaluation sets, business rules, connectors, stored context, access policies, and staff training can all contribute. Keep the parts that represent your business knowledge under your control and test whether they can be exported or recreated.

A vendor review should end with explicit decisions: which dependencies are acceptable, which need mitigation, who monitors changes, and when an alternative will be retested. This does not require duplicating every system. It requires allocating resilience effort according to business consequence. For Meridian’s internal drafting tool, a supervised manual fallback may be enough; a customer-facing operation may justify a different level of preparation.
