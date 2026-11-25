---
name: environment-discovery
description: Identify the project boundary, bootstrap, authority and record locations.
---

# Environment discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass one. Return findings and intent inline, without writes.

**Core question:** Where may this Harness work?

- Inspect project and host boundaries, bootstrap, prerequisites, readiness and cleanup. A worktree is not a sandbox. Name file, network, runner and secret-access limits; never record secret values.
- Identify authorized Harness records and Glossary/ADR locations. Separate Harness and Product issue spaces by role, instance, namespace and permission where applicable.
- Return allowed, blocked and stop cases, the decision-maker, and checks for bootstrap and rejected routing. Skip repo or Product inputs for a Bot-only workspace.
