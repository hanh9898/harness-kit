# Durable state and safe continuation

Read before application effects and when updating or resuming the record. Use a suitable existing project record or native store. Prefer project-versioned Markdown for human-reviewed project material when no adequate store exists. Keep the record discoverable from existing project guidance. Choose locations within actual grants; the legacy `harness/record/` layout is supported, not required. Local uncommitted files do not survive disposal of their runner: use the selected durable destination before claiming that guarantee, or state the limitation.

Apply the effect boundary to scratch scripts and temporary artifacts too. Under a record-only grant, run helper code inline and keep required lock/replacement files beside the authorized record; host-writable scratch space is not an additional grant. Check executed actions as well as final file hashes, which miss transient and outside-project writes.

## Before effects

Establish one authoritative current view for each selected piece/assembly and consuming target. Reference library-owned content/origin facts and live state instead of creating competing copies. Capture the objective, target scope, selected material/methods/standards, existing authority, inspected state, pending action and next step. The current view distinguishes selection, application and outcome evidence; decision review is independent of all three.

For a consequential action covered by the selected logging standard, make these facts durably recoverable before the effect, directly or through adequate existing references:

- Context, scope and choice; material alternatives and rationale.
- Actor, authority and review state; consequences and reversibility.
- Source evidence and intended action references, including application timing.

Use the procedure and authority in force before the change. Editing a library resource or containing another harness does not grant authority to revise that harness's core. A new rule cannot approve its own adoption. Do not invent a reviewer, approval, waiver or future-call grant.

Read back required capture before acting. For unavailable persistence, uncertain write results or interrupted cross-flow work, use [persistence recovery](../../../kit/PERSISTENCE.md) to qualify existing evidence or an authorized alternative for the same logical record. Hold only dependent effects when required capture or outcome remains unresolved.

## Serialize ordinary Markdown updates

Use a native transactional/concurrency facility when suitable. Otherwise use one integration writer and an exclusive record lock for the whole read–capture–effect–result interval. A separate worktree, a task claim or a fresh read alone does not prevent lost updates.

Establish one canonical lock identity for the authoritative record and keep its exact location discoverable with the record. Every cooperating writer must use that same identity. If competing writers may exist and no common lock is established, first serialize adoption through one integration writer; independently invented lock names are not exclusion. Preserve the lock reference after releasing ownership.

For local Markdown without such a facility, atomic directory creation in the authorized record location is a sufficient basic exclusion mechanism: `mkdir <record-lock>` must succeed before writing. Store an ownership token there. An existing lock blocks this writer; do not delete or take over another actor's lock. Reconcile an interrupted owner's effects and establish that it has stopped before an authorized recovery releases its lock. This protects only cooperating writers; report that enforcement limit. For shared or remote writers, establish a suitable common serialization facility before dependent effects.

After acquiring ownership, reread current state and history. Use unique same-directory temporary files and atomic replacement for each full-file update. Read back each write. Preserve existing logical history and append only new events; serialize history and current-view changes under the same ownership. Individual renames are not a multi-file transaction. If interrupted between files, reconcile both with live effects before completing the missing update. Release only this writer's lock after required results and continuation are persisted, or retain it with a precise recovery handoff on uncertainty.

## Reconcile an uncertain effect

Before each send, retain the exact target and expected revision, assignment
and claim epoch where applicable, and stable request/effect ID (or `work_id`
for publication) in the authorized record. After a timeout or ambiguous reply,
keep `Unknown`, the same identifiers, any observed revision, and references
for destination readback. A history pointer is not a receipt. On resume,
reopen the original destination and check its receipt, history or live state
for this exact effect; inconclusive absence is not evidence of no write.

While `Unknown`, do not retry, re-publish, roll back, close, transfer the
claim, advance the effect checkpoint, or start a wake that could repeat it.
Keep the affected checkpoint and report what evidence is needed. Independent
targets can proceed under their own authority. If readback confirms application,
verify it and finish only missing evidence or writeback. If it definitively
establishes no write, reevaluate prerequisites, claim and revision and obtain
a fresh exact grant before a new attempt; keep the same logical work identity.

## After effects and checks

Record what actually changed for each target, when, the action/result references, commands and observed output, failures, unknowns and the scope of checks. Keep selected, applied, reviewed and improved meanings distinct. A passing structure check does not establish runtime use or improvement. Update the current view; retain append-only logical choice/review history. Link material corrections and supersession to the prior event; a wording-only repair needs no new choice event.

Retain objective, scope, selected references, relevant inspected state, completed/remaining work, material unknowns and next action. An adequate existing pointer suffices for discovery. Reopen changing live sources before the next dependent action. A fully completed resume does not repeat effects or append duplicate history. For material correction/supersession, competing contributions, archival or cleanup, follow [record maintenance](../../../kit/MAINTENANCE.md), including live reference checks and uncertain prior effects.

**Done:** readback confirms honest per-target state and recoverable history, required pre-action rationale was captured at the right time, and an authorized future consumer can find the next action without reconstructing the chat.
