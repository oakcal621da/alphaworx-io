---
title: Model deprecation is a reliability risk, not an IT ticket
category: Reliability
date: 2026-07-07
excerpt: A model change is a change to the service your business relies on. Plan the evaluation, cutover, and fallback before the deadline.
slug: model-deprecation-reliability-risk
updated: 2026-09-05
---

A retirement notice may arrive as a technical update, but its consequences belong to the business workflow. A replacement can connect successfully and still alter the quality, cost, latency, or behavior of the service. The useful question is not simply whether the application runs. It is whether the new configuration remains acceptable for the work it performs.

## Track the actual dependency and its lifecycle

Record the provider, deployment, model identifier, version where available, region, and update behavior for each production workflow. Distinguish an alias that may change from an explicitly selected version. Assign an owner to notices and link the dependency to the service that would be affected.

Microsoft’s [Foundry lifecycle policy](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements) and [retirement schedule](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule) show why dates and replacement paths need to be checked for the actual deployment. There is no single retirement window that applies to every provider and model. Pinning can make behavior more reproducible while the version remains available; it does not create an indefinite entitlement to that service.

## Re-evaluate the work, not just the connection

Build a representative set of cases with the people who own the workflow. Include difficult inputs, retrieval failures, refusals, formatting requirements, and the decisions that must remain with a person. Keep the evidence used to define an acceptable answer so that reviewers are comparing against a stable task rather than their memory of a good demo.

Run the candidate configuration against the current one where possible. Examine quality, completion time, operating cost, tool use, and the amount of human correction required. A higher average result can coexist with unacceptable behavior on a small but consequential slice of work. Review those differences explicitly and record which tradeoffs the owner accepts.

## Make the cutover a controlled release

Choose a release path that fits the consequence of failure. A small internal drafting workflow may allow a straightforward supervised trial. A customer-facing operation may need staged traffic, parallel review, or a narrower initial task. Define monitoring and stop conditions before switching the default.

For Meridian’s service assistant, the acceptance record could include policy accuracy, appropriate escalation, permitted tool actions, latency, and reviewer workload. Engineering owns the release mechanism; the business owner accepts the service behavior. Both need to know who will make the decision if early results differ from the evaluation. A calendar reminder alone cannot make that decision for them.

## Prepare a fallback that survives retirement

“Roll back to the old model” stops being an option once the old service is unavailable. Rehearse the fallback you will actually have: a validated alternate configuration, a reduced feature set, a human queue, or a controlled pause. State the capacity and limitations of that route so operations can make realistic commitments.

After cutover, keep the decision record and compare live observations with the evaluation. Feed new failure cases into future tests. The migration is complete when the organization can explain what changed, who accepted it, and how it will detect a regression. That evidence makes the next provider update a managed dependency change rather than a repeat of the same urgent discovery exercise.
