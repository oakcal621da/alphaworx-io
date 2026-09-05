---
title: Enterprise AI: what happens after the demo?
category: Executive briefing
date: 2026-09-05
updated: 2026-09-05
excerpt: Six operating questions that connect AI ambition to cost, data, control, reliability, and accountable decisions.
slug: enterprise-ai-after-the-demo
featured: true
---

A useful demonstration answers an important question: can AI help with this task? Leadership then has to answer several more. Can the workflow use the right information without overreaching? Is the cost acceptable when review and exceptions are included? Who will keep it useful when the provider, the work, or the surrounding rules change?

This briefing adapts the central operating questions from [AIR's enterprise AI risk primer](https://theprimerdesk.onrender.com/reports/understanding-enterprise-ai-risk-the-adoption-problems-hiding-behind-the-hype.html), whose evidence cutoff is August 16, 2026. It is a shorter route into the research, with practical decisions and further reading. The underlying report is a synthesis of published material, not a study of Alphaworx clients. The Meridian examples on this site are fictional.

## Price the completed work

A quoted model rate describes one component of cost. A business workflow may also require retrieval, multiple calls, retries, quality checks, and specialist review. Its useful unit of measurement is the accepted outcome: a resolved request, a reviewed document, or a completed case. Define acceptance before comparing alternatives so that faster but unusable work cannot look like a saving.

Ask the business and finance owners to agree a baseline, a cost boundary, and the evidence needed to recognize a benefit. The [pilot economics explorer](https://alphaworx.io/blog/why-ai-pilots-stall.html) makes one part of that calculation visible. Its adjustable inputs are illustrative assumptions; the broader implementation and operating costs still need to be established for the actual workflow.

## Trace the information and the authority

A familiar product name does not settle the data question. Review the particular account, contract, enabled features, connected sources, and retention settings. Document which information is sent, which copies persist, who can retrieve it, and how access changes are reflected downstream. A training-use commitment answers only one part of that review.

Retrieval introduces another practical boundary: a system must return only material the requesting identity is permitted to access. [Microsoft's RAG documentation](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) describes permission-aware retrieval and query-time filtering. Correctly enforcing existing permissions will not repair permissions that were too broad in the first place. Source access needs its own review.

## Match permissions to the task

An assistant that prepares a draft and an agent that sends it have different authority. The difference becomes more consequential when a workflow can modify records, issue refunds, or delete information. Specify the operations the task needs and the conditions under which a person must approve a consequential action.

[OWASP's excessive-agency guidance](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) identifies functionality, permissions, and autonomy as distinct sources of exposure. Narrow tools and downstream authorization checks can constrain reachable actions. They do not establish that every generated answer is correct. The [permissions exercise](https://alphaworx.io/blog/excessive-agency-ai-risk-no-attacker.html) lets readers explore that distinction without touching a real system.

## Plan for the system to change

A release record should identify the provider, model or service version where available, dependencies, accepted use, and evidence supporting deployment. Assign responsibility for notices and material changes. Test a representative set of cases before expanding use or accepting a replacement, and define a fallback that will remain available when it is needed.

A fallback may be a different service, reduced functionality, or a manual route. Each has its own capacity and quality constraints. Reusing the name of an old model is not a plan if that model will no longer be available. The [migration walkthrough](https://alphaworx.io/blog/model-deprecation-reliability-risk.html) helps structure the review.

## Connect the controls to decision rights

Policies become operational when someone can apply them, supply evidence, handle exceptions, and stop work outside agreed conditions. The business needs an outcome owner; shared AI capabilities need an operating owner; security, data, finance, and relevant specialists need explicit roles. The executive sponsor needs a route for resolving tradeoffs that exceed delegated authority.

Our companion guide, [Who owns the AI decision?](https://alphaworx.io/blog/who-owns-the-ai-decision.html), makes that division concrete. NIST's voluntary [AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) offers a wider set of actions across governance, context, measurement, and management. A framework can organize the work; the organization still has to implement and test its chosen actions.

## Keep the evidence proportional to the claim

The AIR report assembles surveys, vendor documentation, technical research, and editorial judgments. Those sources answer different questions. Adoption across surveyed organizations is not a conversion rate into successful deployment; a benchmark result is not a production guarantee; an observed control is not proof of its effect on every loss event.

For the next investment decision, ask for the evidence closest to the workflow: a verified owner, tested permissions, reviewed outputs, an understood cost range, and a viable response to failure. Record the remaining uncertainty alongside the response. That makes the decision useful today and gives the next review something concrete to challenge.
