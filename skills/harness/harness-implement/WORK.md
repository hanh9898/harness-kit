# Harness work contract

Use existing authorized records. This contract does not install a tracker, workflow engine or new store. A ticket may share an existing artifact with a short spec, but the decision, spec, ticket, assignment and outcome remain distinguishable.

## Handoff intake

Use [stage handoffs v1](../../../kit/STAGE-CONTRACTS.md) for `prepare`, `publish` and `execute`. For a versioned handoff, check shape and match the operation to the caller's request before resolving references or loading routes. For an existing JSON file, use the real skill directory to locate `../../../kit/scripts/check-stage-handoff --expect-operation <operation> <file>`. For an in-session handoff, compare against the same contract without requiring a file. Unknown version, wrong operation or invalid shape stops the dependent step; do not reinterpret a rejected handoff as legacy input.

For v1 `prepare`, `needed_route_refs` can identify the ticket drafting route but do not authorize invocation. Apply [H5](#spec-approval-h5) before resolving or invoking it.

For an unversioned legacy caller or manual record, gather existing references for the requested operation and fill gaps only from authoritative sources you can read. Do not require a migration or invent authority. Both inputs use the same operation checks below: reopen the original records, hold the draft or stop dependent work on missing, conflicting or unreadable required evidence, and do not treat a reference as a grant.

## Prepare

Resolve the original request, decision ID, revision and basis, affected and protected scope, acceptance criteria and prerequisites. Setup requires user confirmation; Evolve may cite actual delegation of that choice. `DesignReady` permits preparation only, with read and drafting authority in scope. Verify that acceptance seams and dependencies still fit the decision. Changes to behavior, scope, target, authority, criteria or accepted risk go back to the caller.

Check both artifacts for compatibility before resolving any drafting route, including manually authored artifacts. Use the [preparation route choices](ROUTES.md#prepare-only-missing-artifacts) and only the evidence for the routes still needed.

- **Spec:** describe the problem, target behavior, protected scope, design choices and checks through agreed public seams. Confirm only missing details that do not reopen the decision. The spec does not replace an ADR or decision.
- **Tickets:** each implementation ticket cites one decision/revision and its spec, has a target and acceptance check, and states real dependencies. One small spec and one ticket can be enough. Split into independently checkable slices; for a mechanical migration, stage compatibility, migrate, then remove the old path. State any checks that require the integrated result.
- Return compatible artifact references or in-session drafts, plus unresolved points. Persist drafts only where a separate grant allows it. Do not pass posting credentials or effect authority to draft methods. Resolve material split changes at [publication](#publish-or-update).

### Spec approval (H5)

Apply H5 to direct or legacy preparation and v1 `prepare` handoffs. It covers both the legacy `to-tickets` route and `harness-project-to-tickets`. A compatible spec, `DesignReady`, or valid handoff shape does not prove approval.

Before resolving or invoking the ticket drafting route, reopen the spec, decision, and approval evidence at the selected authoritative spec or decision source. Verify explicit approval by the authorized spec owner. Match the exact spec reference and revision, decision reference and basis, and scope. Confirm the acceptance criteria and dependencies still match. Do not infer approval from general assent, ticket status, an Inbox card, or a publish grant.

A changed basis or a material change to ownership, acceptance, dependencies, scope, or impact invalidates approval. Check revocation and current approver authority at the source.

| Approval | Next step when a ticket is missing |
| --- | --- |
| Current and matching | Use the [verified drafting route](ROUTES.md#prepare-only-missing-artifacts) without asking again. |
| Missing, stale, revoked, or unverifiable | Hold the draft and return `AwaitSpecApproval`. Do not resolve or invoke a ticket drafting route. |

For `AwaitSpecApproval`, return the spec reference, revision, basis, scope, and blocker to the caller. The caller resolves the blocker and requests H5 from the authorized spec owner only if a new approval is needed. Resume only on a new `prepare` request. Recheck approval on resume.

## Publish or update

Direct publish, v1 handoffs and legacy records use the same gate. Preflight is read-only; no step below authorizes a write on its own.

Keep three destinations distinct: **Harness work records**, **product references** and **effect targets**. Harness records own work on agent behavior, skills, rules, hooks and workflow, even in a product repository. Product feature or bug work stays in its own workflow; read a related product issue only with read authority and pass its full URL only when disclosure is allowed. Do not create, sync, update, change status or close a product issue in this flow; separate product authorization belongs to the product workflow.

1. Reopen the current draft at its authoritative source. Match the requested draft reference and revision. Compare its split with the current authoritative decision. Changes to ownership, acceptance, dependencies, scope or impact are material. An unchanged split may reuse the current decision if its basis and scope still match. If the basis has changed or evidence cannot be opened, hold the draft rather than infer a match.
2. **H6: split approval.** For a material change, verify a current decision by the authorized decision owner at the authoritative source. It must cover the exact draft reference and revision, material diff, decision basis and scope, including acceptance and dependency or independence changes. General assent, ticket status, an Inbox card or a publish grant is not split approval. H6 does not replace H5 or H7.
3. **H7: publish authority.** Resolve the selected target's exact instance, namespace and Harness role at the destination, not from the handoff alone. Two issue spaces may share a provider, but labels, views and filtered boards of the same issue set are not separation. Do not inherit the target from the checkout, product link, upstream defaults or orchestration board. A wrong, missing, shared, ambiguous or unpinnable namespace blocks the write. For a selected local Harness destination, use the local record's own instance, namespace and role; require durable, receiver-readable storage at that locator. Never switch to Product or fall back to local after a tracker error.
4. Resolve the live grant for the exact draft revision, publish or update action, payload and selected destination. Check prerequisites and apply the [write boundary](#write-boundary-and-reconciliation) before each send, including revision and revocation checks. Recheck the draft, split approval and target binding before sending; a changed premise stops publication.

| Condition | Outcome |
| --- | --- |
| Draft revision changed | Keep the draft; do not publish. |
| Material split with missing, mismatched or revoked owner approval | Keep the draft; do not publish. |
| Product role or mismatched Harness locator | Keep the draft; do not write to any destination. |
| Missing, stale, revoked or mismatched publish grant | Keep the draft; do not publish. |
| Timeout after send | Record `Unknown`; reconcile at the same destination without resending. |

Deduplicate at the authoritative write boundary. In the exact Harness namespace, look up the stable `work_id` once and search by node, question and intended outcome, including legacy records without a `work_id`. An ID hit must match all three; a semantic hit with a different recorded `work_id` is also a conflict. Reuse only a single compatible ticket after readback, without changing its identity. If the keys disagree, multiple candidates match or the lookup is incomplete, stop; only create when both checks rule out an existing ticket. Update an existing record only if the requested action and grant cover that revision.

Publish prerequisites first under their own approvals and grants; link dependencies by stable Harness IDs. Product predecessors are read-only references, not tracker links that update the other side. Return canonical `ticket_ref` only after reading back the exact destination, ID, revision, content, links and state. Resolve an `Unknown` attempt by its effect or request ID and stable `work_id` at the same destination. The write boundary also applies to status changes and closure.

## Tasks board and Inbox

Use the bound Tasks board for canonical work. Distinguish a human assignee
from a session claim. Before claiming or dispatching, read back the canonical
ticket, current claim and dependencies and verify authority on that board.
Inbox cards and replies do not authorize a Tasks claim or replace canonical
work, PR status, or an effect grant.

## Dispatch and integrate

For a Bot work claim, apply the [Tasks board and Inbox boundary](#tasks-board-and-inbox).

Recompute `DispatchReady` from the read-back Harness ticket and its current decision/revision, scope, spec and prerequisites; the exclusive, live assignment ID and epoch; the exact execution route in the assigned caller context; and the live authority for the planned effect at the expected target revision. A stale claim, wrong route or revoked grant blocks the write. Do not reassign until the old session has stopped or its assignment cannot still write. Isolate and serialize effects to overlapping targets; use one integration owner for dependent tickets.

If the effect uses a Library selection, require `selection_ref` and call `harness-library` before applying it. Reread its [selection handoff](../harness-library/READ.md#selection-handoff) against the intended store, scope, source, ID, revisions, digest and lineage as applicable. Stop dependent work on a stale, disabled, unavailable or unreconciled selection; do not fall back to the raw catalog. A Library write also goes through that skill under separate store authority. Selection readback is not proof of adoption or a cross-system fence.

On resume and before use, return to the original authorized store binding and
verify its identity. Put `--require-existing-store` before `selection` or
`selection-history`. Missing, unreadable and wrong-identity each block dependent
work; do not treat them as revision 0, empty history or no configured store.

Before each effect or closure, reopen mutable inputs from authoritative sources and compare the current assignment, decision, scope, route, selection and target state. A missing source, a denied read and an unverified result are different blockers. If a premise changes, hold affected tickets, notify the current owner and preserve independent progress. A new policy cannot authorize its own activation. Commit, branch/worktree creation, cleanup, push, PR and merge are separate effects; do not inherit them from upstream methods.

## Write boundary and reconciliation

Use the live exact-effect grant: match principal, operation, target and scope, payload or digest, assignment where applicable, expected revision and expiry. Bind the stable effect or request ID to the effect before sending. Send at most once for that authorized attempt; if the ID already has a result or unresolved attempt, read back or reconcile instead of sending again.

- **Automatic:** use a condition enforced by the destination when it accepts the write. It must reject expired or revoked authority, stale assignment or relevant revision for the effect. A read just before sending, an orchestrator claim, local serialization, or a version check in another system is not sufficient. Where approval or assignment lives elsewhere, prove the target's gate reflects its revocation; do not assume propagation. This applies to tracker and bootstrap effects too. A Library store grant does not by itself fence an external assignment.
- **Non-atomic:** when the policy allows this gap, an authorized person must be present, see the exact destination and effect, confirm each individual send in real time and be able to stop the next effect. Recheck that current authority still applies. Do not run in the background or rely on prior approval or silence. If no valid supervisor route exists or policy requires atomic enforcement, stop. Supervision does not make the write atomic.
- **Uncertain effect:** retain `Unknown`, request/receipt ID, target and assignment. Inspect destination receipts, history and state before resuming. An absent record is not proof of no write while delivery is unresolved. Do not replay, reassign, close or roll back pending reconciliation even under supervision. A proven no-write requires a fresh gate and applicable grant for any new attempt. If a stale assignment did write, report the actual effect, stop dependent work and seek a separate recovery decision.

## Execution result

Return a v1 [`result`](../../../kit/STAGE-CONTRACTS.md#implement--setup-or-evolve-result): assignment and target references, observed revision (expected if not known), effect or request ID, `Applied`, `Denied` or `Unknown`, receipt or authoritative history reference, separate verification and accessible evidence references, and the next step. For `Unknown`, a history reference can be where to reconcile, not proof of a receipt. If required evidence is missing, report the gap; do not invent a complete result.

Verify Harness behavior and at-risk product behavior separately. Report applied state, verified behavior, activation and measured improvement separately; route product findings back without writing product issues. Setup or Evolve checks the assignment and acceptance before marking `Verified`, closes under separate authority and updates its own decision map.

```v1-gates
[
  {"id": "authority.spec-decision", "requires": []},
  {"id": "authority.work-claim", "requires": []},
  {"id": "prepare.spec-approved", "requires": ["spec.exact-revision", "authority.spec-decision"]},
  {"id": "prepare.tickets", "requires": ["prepare.spec-approved"]},
  {"id": "publish.apply", "requires": ["publish.split-current", "publish.exact-grant", "publish.harness-target"]},
  {"id": "publish.exact-grant", "requires": []},
  {"id": "publish.harness-target", "requires": []},
  {"id": "publish.split-current", "requires": []},
  {"id": "spec.exact-revision", "requires": []},
  {"id": "work.canonical-task", "requires": []},
  {"id": "work.claim", "requires": ["work.canonical-task", "authority.work-claim"]}
]
```
