---
title: Five things the AI vendor pitch leaves out
category: Vendor Reality Check
date: 2026-08-04
excerpt: Five questions that turn an attractive AI proposal into an operating decision you can defend.
slug: five-things-vendor-pitch-leaves-out
updated: 2026-09-05
---

A vendor presentation is designed to make a capability easy to understand. An enterprise purchase also needs to explain the conditions under which that capability will work, what it costs to operate, and who carries the unresolved risk. These five questions help connect the sales conversation to the service the business will actually receive.

## 1. What does an accepted result cost?

A unit price can be accurate and still be insufficient for comparing two solutions. Define the task, required quality, volume, latency, and review effort before comparing bills. Include the parts of the service that the demonstration did not need: retrieval, integration, exceptions, evaluation, support, and the work of checking the result.

Ask the vendor to run a representative workload with agreed success criteria. Record failed attempts and corrections as well as successes. A low processing cost is useful only in relation to the result being purchased. Keep the underlying assumptions so that a later change in volume, configuration, or review time can be assessed without reconstructing the entire business case.

## 2. What is actually committed when we need capacity?

Separate pricing, quota, capacity availability, service levels, and the behavior during an outage. Different products and agreements handle these differently. Neither a reservation label nor a premium tier is enough to establish the promise your operation relies on.

Bring a concrete scenario to procurement: demand doubles during a business event, a region is unavailable, or a request is delayed beyond the workflow’s tolerance. Ask which term or configuration governs the response. Then decide what your organization will queue, route elsewhere, handle manually, or stop. The useful deliverable is a shared operating expectation rather than an adjective such as “enterprise-grade.”

## 3. What is stored, where, and for how long?

Training use, operational logs, application state, uploaded files, and connected systems are distinct parts of a data review. [OpenAI’s API data controls](https://developers.openai.com/api/docs/guides/your-data) provide a concrete example of endpoint-specific retention and feature conditions. Check the corresponding details for the exact vendor product and agreement being considered.

Draw the data path with the application owner. Include the downstream tools that receive content, the administrators who can access it, deletion procedures, and any special conditions for the features you need. Ask for evidence of the configured arrangement. A general statement about model training should not stand in for answers about everything else that happens to the information.

## 4. What happens to quality when controls are enabled?

Evaluate the configuration you intend to operate. Permission limits, review steps, content filtering, and restricted data access can change completion rate, latency, cost, or the kinds of requests the system can fulfill. Measure those tradeoffs on the workflow; do not assume that a demonstration with different conditions predicts production performance.

Include difficult but legitimate requests as well as misuse cases. A system that blocks necessary work may encourage users to seek another route, while one that completes everything may exceed the intended boundary. Define the acceptable balance with the business and security owners. The result should be a specific configuration with known limits, supported by evidence that can be revisited.

## 5. Which existing data problems will the assistant expose?

An assistant may operate within permissions that are already too broad. Microsoft notes that [overshared content can increase risk in Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/security-microsoft-365-copilot). This makes access review a concrete part of deployment planning rather than an assumption inherited from the existing repository.

Test the experience of different user roles and review stale content, sharing links, ownerless repositories, and unnecessary connectors. Ask who will maintain those conditions after launch. The purchase decision should identify work your organization must do as clearly as work the vendor promises to do. A stronger agreement starts with both sides understanding that boundary.
