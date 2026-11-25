---
name: workflow-discovery
description: Identify workflow order, owners, handoffs and recovery checks.
---

# Workflow discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass two under `coordination-discovery`. Return findings and intent inline, without writes.

**Core question:** What order, ownership and handoffs does this work need?

- Trace producer outputs, consumer inputs, prerequisites and owners. Compare the proposed route with a simpler manual path.
- For a native repo schedule that does not wake a Bot, check the trigger, overlap, failure owner and stop path. Do not select a Bot or enable the schedule.
- Return the entry, handoff and completion criteria plus a recovery check for a failed or missing step. Do not publish or dispatch work.
