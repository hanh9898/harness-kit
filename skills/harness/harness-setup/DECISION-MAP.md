# Decisions, tickets and the readiness check

Setup and Evolve share this contract. Reuse adequate records with the
[durable-state procedure](../harness-evolve/UPDATE.md). Store only in an
authorized location; use an in-session checkpoint until durable storage is
permitted. Keep a short index: goal, scope, phase, active/next node, one line
and link per decision, waiting and under-specified work, approved deferrals
with reasons, and approved out-of-scope items. Keep detailed rationale,
evidence and results in their own sources.

Entry selection (H1) opens a request, not a settled node or a write grant.
At H2 confirm the actual node decision and, separately, the final design
revision. The [discovery map](DISCOVERY.md) owns route order and parent
eligibility. Topic results are inline input to the map writer, not tickets
or checkpoints of their own. An approved deferral records why and when to
reopen it; a blocker or silence is not a deferral.

## Branch answers and checkpoints

Record every grilling answer against the exact tree path of the branch that
asked it. A confirmation record has a stable ref and a `covered_paths` list.
A batch yes may settle only the branch paths explicitly listed in that record.
It never settles unasked or unlisted branches. Before moving to the next
branch, save a checkpoint with the branch path, outcome, confirmation or
deferral ref, open question or blocker, and the evidence refs needed to reopen it.

Validate the local transition record at each state change:

```sh
<skill-dir>/../../../kit/scripts/check-setup-transition <transition.json>
```

A nonzero exit means the state claim is blocked. Do not report `DesignReady`,
send `prepare`, or report `Verified` from that record. The checker validates
structure and cross-references only; reopen the referenced authority and
evidence at their authoritative sources.

## Record and close by result

| Ticket | Close only when |
| --- | --- |
| Research | Findings, readable sources and unknowns are recorded. Closing research does not settle the decision it informs. |
| Grill | Both foundation skills were used and the node choice is confirmed by the authorized decision-maker. Stop at the choice, constraints and check, not implementation detail. |
| Prototype | The scoped demonstration is available and the user supplied the response needed for the choice. A measurement-only experiment closes with its result and limits, not adoption. |
| Manual prerequisite | There is actual evidence the prerequisite was satisfied, not just a request or acknowledgement. |
| Implementation | A ticket tied to one decision passes its checks with readable evidence for its current assignment. During discovery record implementation work as waiting, never execute it. |

Deduplicate against current records by node, question and outcome. If a question
is concrete but a prerequisite is unresolved, retain a waiting ticket. If the
question is not formed, keep it in **Needs information**, not a fake ticket.
Assign eligible research in either pass, or name its next owner/blocker. Check
the type, processor, prerequisites and authority before dispatch; no agent
can relabel work to close it. Resize at material additions and before handoff;
split independently checkable questions only, not a second grill for one node.

A settled choice must trace to specific user confirmation (a batch review
counts if it included that choice). Only Evolve may cite explicit existing
delegation for that exact class of choice; label it as such. Proposals, facts
and deferred or out-of-scope items are not ready for implementation.
Read back map pointers and confirmation after updates. Setup checkpoints after
every branch in each pass and when answers arrive; Evolve checkpoints changes
proportionally. One map writer integrates returned results and applies the
[write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation)
to durable writes. Serialization prevents competing map updates; it does
not enforce current authority at the destination. If another writer changed
the source, reread and integrate, not overwrite. Read the last entry and
its links to check for truncation; split linked details only within authorized
storage.

## Check `DesignReady` for each scope

Compare the approved goal and decision/revision with the whole relevant map,
including open questions, assumptions, unresolved impacts, compatibility and
unrun checks that could change the decision. Closed tickets do not establish
readiness. A dependent scope waits if impact is unknown. Allow only portions
whose independence can be explained. Check the receiving context can read and
use the minimal inputs with room to execute and verify. Split by checkable
scope and dependency order if needed; do not use a fixed token threshold.
Record readiness and remaining blockers by scope and decision version; redo
the affected check on a change. Readiness permits preparation, not publication
or effect. Before reporting it, validate a `design-ready` transition record
with every applicable branch outcome, branch-specific confirmation and branch
checkpoint. Missing or invalid input means no `DesignReady` claim.

Before closing or handing off, verify actual evidence from the record with
receiving-session access. Use full tracker URLs or paths relative to a named
durable source with the relevant revision. Do not promise resume from transient
files. If evidence or record access is unverified, mark it and preserve a
checkpoint with the next step. Before reporting `Verified`, validate a
`verified` transition record with the required handoffs, an Applied result,
acceptance evidence and separate close authority. Missing or invalid input
means no `Verified` claim.
