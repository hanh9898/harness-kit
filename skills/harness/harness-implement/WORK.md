# Harness work contract

Use existing authorized records. This contract does not install a tracker, workflow engine or new store. A ticket may share an existing artifact with a short spec, but the decision, spec, ticket, assignment and outcome remain distinguishable.

## Prepare

Receive the decision and its version, confirmation or explicit delegated-choice reference, affected scope, protected scope, prerequisites and acceptance criteria. Setup requires user confirmation; Evolve may cite actual delegation of that choice. Verify that acceptance seams and dependencies still fit the decision. Changes to behavior, scope, target, authority, criteria or accepted risk go back to the caller.

- **Spec:** reuse a current one or invoke the verified preparation route to produce a short problem, target behavior, protected scope, design choices and checks through agreed public seams. Confirm only missing details that do not reopen the decision. The spec does not replace an ADR or decision.
- **Tickets:** reuse compatible tickets or invoke the verified split route for a draft graph. Each implementation ticket cites one decision/revision and its spec, has a target and acceptance check, and states real dependencies. One small spec and one ticket can be enough. Split into independently checkable slices; for a mechanical migration, stage compatibility, migrate, then remove the old path. State any checks that require the integrated result.
- Return the spec/graph and unresolved points. Persist drafts only where a separate grant allows it. Do not pass posting credentials or effect authority to draft methods. Confirm any changed split before publishing.

## Publish or update

Keep three destinations distinct: **Harness work records**, **product references** and **effect targets**. Harness records own work on agent behavior, skills, rules, hooks and workflow, even in a product repository. Product feature or bug work stays in its own workflow; read a related product issue only with read authority and pass its full URL only when disclosure is allowed. Do not create, sync, update, change status or close a product issue in this flow; separate product authorization belongs to the product workflow.

Resolve the effective tracker instance and namespace, its Harness role and exact action grant before each write. Two issue spaces may share a provider, but labels, views and filtered boards of the same issue set are not separation. Do not inherit the target from the checkout, product link, upstream defaults or orchestration board. Missing, equal, ambiguous or unpinnable destinations mean no external write. Reuse an authorized local Harness record for small work or keep a draft; never improvise a different store. Apply the write gate below before publishing, status changes and closure as well as execution.

Check for duplicates at the authoritative write boundary by node, question and intended outcome, not title. Publish prerequisites first; link dependencies by stable Harness IDs. Product predecessors are read-only references, not tracker links that update the other side. Read back the exact destination, ID, content, links and state. A local ticket is canonical only if it is durable in the selected, authorized location and readable by the receiving session. Both local and external tickets need the same contract.

## Dispatch and integrate

Record a stable ticket ID, node, decision/revision and spec, target and expected state/revision, protected scope, authority references, prerequisites, checks and result destination. Record the owning session and unique assignment before dispatch; verify exclusive ownership. Require the current canonical ticket and route, live prerequisites and authority at the actual effect target. Do not reassign until the old session has stopped or its assignment cannot still write. Isolate and serialize effects to overlapping targets; use one integration owner for dependent tickets.

Before each effect or closure, reopen mutable inputs from authoritative sources and compare the current assignment, decision, scope, route, selection and target state. A missing source, a denied read and an unverified result are different blockers. If a premise changes, hold affected tickets, notify the current owner and preserve independent progress. A new policy cannot authorize its own activation. Commit, branch/worktree creation, cleanup, push, PR and merge are separate effects; do not inherit them from upstream methods.

## Write boundary and reconciliation

- **Automatic:** use a condition enforced by the destination when it accepts the write. It must reject expired or revoked authority, stale assignment or relevant revision for the effect. A read just before sending, an orchestrator claim, local serialization, or a version check in another system is not sufficient. Where approval or assignment lives elsewhere, prove the target's gate reflects its revocation; do not assume propagation.
- **Non-atomic:** when the policy allows this gap, an authorized person must be present, see the exact destination and effect, confirm each individual send in real time and be able to stop the next effect. Recheck that current authority still applies. Do not run in the background or rely on prior approval or silence. If no valid supervisor route exists or policy requires atomic enforcement, stop. Supervision does not make the write atomic.
- **Uncertain effect:** retain `Unknown`, request/receipt ID, target and assignment. Inspect authoritative receipts, history and state before resuming. No automatic replay, reassign, close or rollback. If a stale assignment did write, report the actual effect, stop dependent work and seek a separate recovery decision.

Return durable evidence references a receiving session can open for the exact revision, not just logs or a transient worktree. Report applied state, tested behavior, activation and measured improvement separately. Verify Harness behavior and at-risk product behavior separately; route product findings back, without writing product issues.
