---
name: hooks-discovery
description: Assess hook events, local checks, effects and stop paths.
---

# Hooks discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass two under `coordination-discovery`. Return findings and intent inline, without writes.

**Core question:** What should run at which host event?

- Verify the native event and payload. Check overlap with CI, blocking behavior, latency, duplicate delivery and failure. Separate a local check from a hook that writes or notifies.
- Return expected and rejected events, a stop or restore path, and the effect boundary, or recommend no hook. Do not configure the hook.
