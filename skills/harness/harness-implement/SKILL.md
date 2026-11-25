---
name: harness-implement
description: Prepare, publish or execute Harness work from a settled Setup or Evolve decision. Reuse valid specs and tickets; require a verified route and target authority before effects. Not for ordinary product work.
---

# Harness Implement

A clear user request or an authorized internal call with an operation and
scope goes straight to intake, even if an effect grant is missing. With no
request, start with silent, read-only research under the
[proposal entry guard](../../../kit/PROPOSAL-ENTRY.md).

Setup, Evolve and coordinators call `harness-implement` by exact ID through the host. Accept one requested operation and only its relevant context. Do not install providers, change a decision or start another operation on your own. The first v1 pilot host is Devin, within an approved project scope.

Read [handoff intake](WORK.md#handoff-intake) for versioned and legacy inputs, then the work contract for the requested operation. Open the [route contract](ROUTES.md) only for a step that needs a skill. Keep these gates independent:

| Operation | Gate | If missing |
| --- | --- | --- |
| [`prepare`](WORK.md#prepare) | Recheck `DesignReady`; reuse compatible artifacts, draft only what is missing. | Return material choices to Setup or Evolve. With no storage grant, return drafts in the session. |
| [`publish`](WORK.md#publish-or-update) | Pin the Harness namespace and verify authority for the exact publication or update. | Keep drafts; never fall back to a product tracker. |
| [`execute`](WORK.md#dispatch-and-integrate) | Recompute `DispatchReady` from the canonical ticket, dependencies, assignment, route and target authority. | Block dependent work; a published ticket or publish grant is not execution authority. |

For every write use the [late-write gate](WORK.md#write-boundary-and-reconciliation). After execute preflight, use [execution methods](EXECUTION.md) and return the [execution result](WORK.md#execution-result) without claiming the caller's verification or closure.

If work must continue in another session, use the [continuation handoff](../../../kit/PERSISTENCE.md#continuation-handoff) without changing the execution result.
