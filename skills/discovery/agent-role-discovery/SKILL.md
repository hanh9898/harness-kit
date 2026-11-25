---
name: agent-role-discovery
description: Identify agent profiles, responsibility boundaries and per-Bot role intent.
---

# Agent and role discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass one. Return findings and intent inline, without writes.

**Core question:** Who should do which work, with which profile?

- Compare available model profiles, quality and budget against actual responsibilities, handoffs, scope and fallback. Name a consumer check for each proposed override.
- For requested Bot work, use the proposed or bound inventory and pinned Library candidates. Return role and contract intent for each `bot_id` with its work scope and handoffs; keep unknown bindings explicit.
- Do not infer a grant, binding or wake mapping from a role. Keep each Bot's Inbox, Memory and authority separate; do not add a Bot to ordinary repo onboarding.
