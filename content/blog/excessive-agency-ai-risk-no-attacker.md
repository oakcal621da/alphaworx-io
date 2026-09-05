---
title: Excessive agency — the AI risk that doesn't need an attacker
category: Security
date: 2026-07-14
excerpt: A correct login and an authorized tool call can still produce the wrong action. Explore how permissions change an agent’s reach.
slug: excessive-agency-ai-risk-no-attacker
updated: 2026-09-05
---

An agent does not need to be compromised to do something consequential that nobody intended. A mistaken interpretation, incomplete instruction, or misleading input can become an action when the surrounding system allows it. Excessive agency is the mismatch between the work the agent needs to perform and the capabilities, permissions, or autonomy it has been given.

## Start from the task and enumerate the actions

“Help with customer email” is too broad to define an authorization boundary. Break it into operations: read a specified queue, retrieve approved policy, draft a response, send that response, amend an account, or delete a message. Each operation changes what a mistake can do. Approving one does not implicitly approve the others.

[OWASP’s excessive-agency guidance](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) distinguishes excessive functionality, permissions, and autonomy. That distinction is useful because a narrow tool can still run under an overpowered identity, and a limited identity can still act without a needed human checkpoint. Review the whole chain from the user’s request through the agent’s tool call to the downstream authorization decision.

## Enforce the boundary beyond the prompt

A prompt can describe the intended behavior. It cannot replace the controls that decide whether an action is permitted. Scope credentials to the task and require the receiving service to enforce the relevant authorization. Where possible, expose a narrow operation instead of a general-purpose interface with many unrelated capabilities.

For Meridian’s email summarizer, access to an approved queue may be sufficient. Sending messages, modifying customer records, and deleting history belong to different decisions. The permission explorer above illustrates the reachable actions created by granting those tools. It is not a vulnerability scanner or a risk score; real authorization also depends on identity, resource scope, arguments, and service-side checks.

## Make human approval specific enough to matter

A reviewer needs to see the proposed action, its target, the material being sent or changed, and any uncertainty relevant to the decision. A generic “allow the agent to continue” prompt can hide the very consequence the checkpoint was meant to expose. Approval should bind to the action the human actually inspected.

Decide which actions always need review and which can run within a bounded policy. Define limits for repeated calls and unusual volumes as well as individual transactions. A series of small permitted actions can have an aggregate consequence. Test changed recipients, unexpected records, missing evidence, and requests that exceed the approved task.

## Exercise the stop and recovery path

Before release, rehearse how the workflow is paused, how credentials are revoked, and how affected records are identified. Logging should make the action traceable to the initiating request and authorization context without collecting unnecessary sensitive content. A stop button that nobody can find is not an operational fallback.

Choose a survivable test and ask the business owner to participate. Can they tell what happened, decide what to restore, and resume only the acceptable portion of the workflow? Agent safety becomes more concrete when the review includes these recovery decisions. The goal is a capability whose authority can be explained and whose failures can be contained, rather than confidence based entirely on the model’s usual behavior.
