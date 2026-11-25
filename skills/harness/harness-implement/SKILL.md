---
name: harness-implement
description: Prepare, publish or execute Harness work from a settled Setup or Evolve decision. Reuse valid specs and tickets; require a verified route and target authority before effects. Not for ordinary product work.
---

# Harness Implement

Setup and Evolve call this skill by exact ID through the host. Accept the requested operation, the authority and source references it requires, and only the relevant context. Do not install providers, change a decision or start a different operation on your own. The first v1 pilot host is Devin, within an approved project scope. A skill call or an approved design is not permission to write.

Read the [work contract](WORK.md) for the requested operation and [route contract](ROUTES.md) only for a step that needs a skill. Keep these gates independent:

| Operation | Gate | If missing |
| --- | --- | --- |
| Prepare | `DesignReady`: current decision, decision basis, scope, measurable acceptance, dependencies and read/process authority. | Return material choices to Setup or Evolve. With no storage grant, return drafts in the session. No tracker or effect grant is needed. |
| Publish or update | Verified Harness namespace and permission for the exact write, or an authorized local Harness record for small work. | Keep drafts; never fall back to a product tracker. Published tickets can remain waiting. |
| Execute | `DispatchReady`: a read-back Harness ticket, current decision and prerequisites, exclusive assignment, verified execution route and current authority for the exact target effect. | Block only dependent work. No execution from a chat draft, label or publish grant. |

Reuse a compatible spec and ticket even if created manually. For missing artifacts, call only the verified `to-spec` and/or `to-tickets` routes, in that order when both are needed. They produce drafts, not tracker writes. Select the execution route only for execution; use [execution methods](EXECUTION.md) for the work at hand.

Before applying a library resource, call `harness-library` for current store, scope, source, ID, revision, exclusion and lineage. An excluded, stale, unavailable or unreconciled selection blocks its dependents. A library write also goes through that skill under separate store authority. An inspection is not a cross-system fence.

At every write boundary use the [late-write gate](WORK.md#write-boundary-and-reconciliation). Do not run non-atomic writes unattended. If an effect is uncertain, keep `Unknown`, reconcile at the target and do not retry or undo. Return assignment, target/revision, actual effects, checks and accessible evidence, unknowns and next step. The caller checks the assignment and evidence before marking `Verified` and closing; it alone updates its decision map.
