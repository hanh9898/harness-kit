---
name: automation-discovery
description: Draft one exact Bot target for a schedule or allowed integration event.
---

# Automation discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass two under `coordination-discovery`. Return findings and intent inline, without writes.

**Core question:** What recurring work warrants an automation, and which Bot owns it?

- Compare a manual baseline with a verified schedule or allowed integration event. Chat, @mentions, and Inbox replies are never wake triggers, nor are Bot messages or manual pilots.
- Draft exactly one `target_bot_id` per automation. Record the automation identity, trigger, scope, actor, current binding and occurrence key. Require the explicitly selected Bot; there is no default Bot, role match, chat match or fan-out. If selection or binding is missing, ambiguous or mismatched, return a blocker.
- Require the runner to verify the active trigger and exact binding, then claim the occurrence and secure durable, atomic dedupe before ACK. Replays must not dispatch again. State who owns failures and the stop path: disable and read back the exact trigger, fence or drain work, then reconcile in-flight effects.
- Return a disabled draft and verification conditions only. Do not configure, enable, claim, ACK or dispatch.
