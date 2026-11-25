---
name: harness-m2-to-tickets
description: Draft missing tickets in the Devin fixture.
---

# Draft only missing tickets

Use only via the [opt-in Devin fixture](../../../skills/harness/harness-implement/ROUTES.md#devin-prepare-fixture).
Stop before authoring if the actual project, exact ID, source, revision, caller
or effective invocation policy does not match the verified binding.

Recheck [H5](../../../skills/harness/harness-implement/WORK.md#spec-approval-h5)
at the authoritative spec or decision source. Stop with `AwaitSpecApproval`
if the spec is missing, stale or not explicitly approved at its current
revision. A matching, current approval needs no new question.

Keep any compatible existing ticket. Draft only missing slices of the approved
spec. Each slice cites the decision and spec revisions and states its target,
observable acceptance checks and real dependencies. Use one slice if it can
be completed and verified independently.

Return the draft inline. Do not assume a `draft_ref` is durable or emit a
`publish` handoff. Do not load an upstream original, write files, publish,
claim, change Git or add labels.
