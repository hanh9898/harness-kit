# Record maintenance

Use for material record corrections, supersession, integration of competing
updates, archival and scoped cleanup. The owning setup/evolve/library entry
retains its grants, selected original methods and result contract. Reuse the
existing authoritative store and [record procedure](../skills/harness/harness-evolve/UPDATE.md).
The steps below govern logical relationships, not a required physical schema.
Recovery coordinates interrupted work; adoption decides where and when a change
becomes effective. Maintenance preserves their facts and authority without
replacing either procedure.

## 1. Establish the maintenance boundary

Read the live current view, relevant history, source evidence, ownership and
known references. Identify the requested correction or retention action and
its authority under the procedure already in force. Reuse prior grants; a new
record entry cannot grant its own effect. Include scratch artifacts and locks
in the scope. Keep tracker status in its authoritative tracker and reference it
from the record; a local summary is not another tracker.

Select applicable original methods and standards through the owning entry.
For agent-read authoring, use original writing-for-agents with N06; use E07/E08
for current state/history and E16 for retention. Their suggested tools do not
require a new runtime when native operations are adequate. Read the relevant
source detail, not just these summaries.

**Done:** the live identities, actual grants, sources, reference coverage and
selected procedure are known. Unknown ownership or retention blocks disposal
of the affected item; independent authorized maintenance can proceed.

## 2. Integrate attributable corrections

Establish serialization before writing using the native transaction/revision
facility or the canonical lock in the record procedure. One integration writer
must reconcile contributions against the authoritative state while holding that
ownership. A fresh read, separate worktree or task claim alone is insufficient.
Keep each contribution and its actor/source recoverable until integrated or
explicitly rejected with a reason. Never replace a winner with a stale snapshot.

After acquiring ownership, reread current state and history. For each material
correction or supersession, append a logical event that identifies the affected
prior event/revision, corrected assertion or changed choice, actor, rationale,
source evidence, authority, review state and scope. State what remains valid.
Preserve earlier events as they were; their mistaken assertions become historical
facts, not current truth. A wording-only repair needs no invented choice event.
Keep required pre-action facts recoverable and read them back before the effect.

Update the editable current view to reference the new event and live facts.
Record actual effects/checks separately from the choice and human review. Read
back the result and verify prior logical events and independent contributions
remain reachable. For multiple files, record and reconcile partial writes;
individual atomic renames are not a multi-file transaction. Release only owned
locks after the result and continuation are recoverable.

For the [local library](LIBRARY.md), `show` and `history` expose the authoritative
content revisions. Ordinary `save` preserves earlier versions in one transaction
and rejects stale expected revisions. Use the resource's supported additional
metadata for explicit correction/supersession references and actor attribution;
inspect the referenced historical revision before saving. These references are
caller assertions, not CLI-validated semantics. Keep origin/owner/scope stable;
use the checked update contract for origin changes. After a conflict, reconcile
both contributions against live history before an authorized retry. Losing a
race is not permission to discard either contribution.

**Done:** the current view is accurate within inspected evidence, every material
change links to preserved history, and each contribution has an attributable
disposition. Review accepted, change applied and outcome improved remain distinct.

## 3. Preview archive and deletion separately

An archive retains material for retrieval and audit while removing it from active
use where intended. Deletion removes material and requires its own applicable
grant and retention decision. Neither age, a completed ticket nor an archive
label establishes that deletion is safe.

Before either effect, produce a scoped preview against actual sources:

- Exact identities/paths, owner, proposed action and intended archive destination.
- Live incoming references and inspected coverage: current records, active tasks,
  consumers, unresolved choices, evidence and retention requirements.
- For Git material, inspected status, branch/head and merge reachability against
  the actual integration target. Check uncommitted/untracked work and active
  worktree/session ownership too. A clean checkout can still contain unmerged work.
- Items to retain, archive or delete, with the evidence and authority for each;
  unresolved ownership/reference checks remain blockers, not empty reference lists.
- Verification, reversibility/restoration limits and the next action for blocked
  items. Keep required history and evidence reachable after any move.

Use suitable native read-only inventory/dry-run operations. Inspect symlink and
shared-store boundaries; a path name does not establish ownership of its target.
An age glob or worktree list alone is not a safe deletion preview. Protect active,
unmerged and unresolved work and required evidence. When archive moves a file,
preserve bytes/identity and keep or update authorized discovery references. If a
dependent reference cannot be updated safely, retain the original or block the move.
For the local library, explicit `disable` with an archival rationale can retire
future selection while retaining `show`, content/history and selection history.
This is not physical deletion and does not change already-applied consumers.
The local CLI has no history purge operation; use an adequate separately qualified
native cleanup facility only under its own grant and retention contract.

**Done:** the preview distinguishes retained, archived and deletable items using
live evidence, with coverage and blockers visible. Preview-only requests stop
here. Sufficient existing action grants need no additional approval round.

## 4. Apply and reconcile actual effects

Recheck the preview's affected identities, references, ownership and grants under
the selected serialization before each granted effect. A changed basis invalidates
that portion of the preview. Capture required rationale first, perform only the
qualified scoped operation, then inspect both source and destination and required
references. Record actual completion, failure or uncertainty per item.

For interrupted archival or uncertain prior deletion, inspect live paths, archive
destinations, native operation receipts and references before retry. Absence alone
does not prove who deleted an item, what it contained or that deletion was allowed.
Retain the uncertainty and any dangling reference; do not invent a successful
deletion or automatically recreate unknown material. Preserve surviving evidence
and block dependent disposal until ownership/effects can be reconciled. An already
completed move needs only missing record repair, not a second move. A held lock
requires the existing stopped-owner/recovery procedure, not lock theft.

**Done:** readback establishes the actual per-item state and discovery route.
Record completed/remaining work, unresolved facts and the concrete next trigger
or actor. Resume from these facts without duplicate effects. Report enforcement
and durability limits: local cooperating locks/transactions do not qualify remote
writers, independent database copies, or survival after disposal of the only store.
