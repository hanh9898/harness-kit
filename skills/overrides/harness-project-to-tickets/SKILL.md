---
name: harness-project-to-tickets
description: Draft Harness tickets from an approved project spec. Return drafts and dependencies without publishing.
---

# Draft Harness tickets

Accept only a verified project binding and caller for this route. Require the
exact spec revision approved at H5, its current decision basis, work scope
and dependencies. Return a blocker for missing or stale approval, conflicting
inputs or a mismatched binding.

Reuse compatible tickets. Draft only missing slices with a target, acceptance
check, actual dependencies and references to the decision and spec revisions.
Return a changed split to the caller for H6.

Return drafts inline unless a separate grant allows storing them at the
selected destination. Do not write to a tracker, dispatch work or apply
changes. Harness Implement owns publication under H7.
