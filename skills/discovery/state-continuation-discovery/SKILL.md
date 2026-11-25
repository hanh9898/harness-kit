---
name: state-continuation-discovery
description: Identify authoritative records, safe handoff references and resume checks.
---

# State and continuation discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass one. Return findings and intent inline, without writes.

**Core question:** Where can the next run recover its current state?

- Identify owners and authoritative decision, checkpoint and effect records. Verify which sources a fresh authorized session can open; a transcript is not a durability substitute.
- Separate applied, verified, blocked and unknown work. Return references, the next action and owner, and any access or persistence limit. Do not write the checkpoint here.
