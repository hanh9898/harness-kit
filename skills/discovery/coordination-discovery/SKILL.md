---
name: coordination-discovery
description: Decide which workflow, hook, automation or factory topics apply.
---

# Coordination discovery

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md). A
concrete question goes direct. Follow the [topic route and result contract](../../harness/harness-setup/DISCOVERY.md#topic-route-and-result)
for pass one. Return findings and intent inline, without writes.

**Core question:** Where does this work need coordination?

- Inspect existing work intake, owners, dependencies and handoffs. Distinguish Tasks board assignees from session claims and board access from operating scope. Inbox is for owner input, permissions and review, not canonical work or PRs.
- Compare manual work with workflow, hooks and automation. Check whether Software Factory is relevant using intake, claims, cost, human controls, and stop and recovery needs; do not open a separate factory topic.
- Keep native repo schedules that do not wake a Bot in workflow discovery. Open automation discovery only for in-scope Bot wake design; do not ask for a Bot on the repo-only path.
- Return applicable child topics, their boundaries and dependencies, or a deferral. Do not load children in pass one.
