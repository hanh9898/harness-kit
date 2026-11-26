---
name: verification-discovery
description: Identify separate Product and Harness checks, evidence and access.
---

# Verification discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass one. Return findings and intent inline, without writes.

**Core question:** What evidence would verify the result?

- Identify Product checks and separate Harness behavior checks. Name a successful case and a rejected or non-triggering case where it matters.
- Specify environment, cleanup, usable receipts or readback, and who can read the evidence. Distinguish observed, unrun and inconclusive checks.
- If the consumer has enabled a pinned optional method pack, pass this node and confirmed facts to [Library](../../harness/harness-library/READ.md) through the existing topic route. An unconfigured pack adds no suggestions. Open only a selected ID; keep all results advisory.
- Return acceptance checks without installing checks or adding telemetry.
