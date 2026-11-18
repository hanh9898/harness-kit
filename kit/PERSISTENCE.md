# Persistence recovery

Use when setup, adoption or library work cannot read/write required records,
loses a write acknowledgement, or resumes after interruption. The owning entry
keeps the result contract; [coordinated recovery](RECOVERY.md) orders affected
work. Use the existing [record procedure](../skills/harness/harness-evolve/UPDATE.md)
for grants, pre-action capture, scratch and serialization. This branch qualifies
continuation with available facilities; it creates no alternative record authority.

## 1. Establish what is known

Begin with read-only inspection of the discovery pointer, current view, linked
history and relevant live consumer state. Enter write serialization only for a
permitted mutation whose lock/scratch scope is granted. A recorded lock location
is not a grant to create it; read-only diagnosis needs no new record lock. Carry forward the objective, logical record/operation identity,
targets, settled answers, prior grants and revocations, selected provider/methods,
standards, reviews, remaining limits and original evidence conditions. Recheck
changing prerequisites for the next effect; a record's authority text is a
reference to an actual grant, not permission by itself.

Identify the failed read/write, destination, expected revision and acknowledgement
status from observed errors and native evidence. Distinguish a location never
created from a previously used store that is now missing. Missing storage is
not an empty history, and a timeout or failed readback is not proof of no effect.
Preserve source data and failed attempts; recovery does not authorize replacing,
reinitializing, deleting or unlocking inaccessible material.

Inspect the operation's live content, selection and histories or native receipt
at its original identity. Compare intended data and authority references with
what actually persisted, including each target's current bytes and checks.
A matching label alone cannot establish identity or completed application.

**Done:** each affected write/effect is observed completed, observed absent under
a sufficient native view, or unresolved. Unknown outcomes stay explicit.

## 2. Qualify capture for the same logical record

First reuse adequate existing durable references. Check their actual content,
version, accessibility to future consumers, authority, required timing and
survival scope. A prior accepted choice may satisfy pre-action capture without
another event. It does not establish application or replace missing result evidence.

If an alternative is needed, establish all of these before dependent effects:

- The actual grant covers its destination, writes, discovery pointer and needed
  locks/replacements. Provider and selected standards still apply.
- The alternate continues the same logical record, preserving identity, linked
  history, per-target state and prior authority. It references library-owned facts
  and live effects without copying them into competing authorities.
- The intended future consumer can find and read it through an existing or
  authorized updated pointer even while the primary destination is unavailable.
- The native facility meets the required survival and concurrency conditions.
  Observe write/readback and fresh-consumer access as applicable. State precisely
  what was checked: retained local files, a commit, an acknowledged remote write
  and survival after runner disposal are different claims. A writable path or a
  successful probe alone does not establish the required durability.
- One integration writer or suitable native transaction serializes the record
  across both locations. Reuse its canonical lock identity. A second independent
  lock or copied database does not coordinate writers of the original record.

An unresolved original write requires outcome reconciliation before a mutation
that could duplicate it. An alternate can retain an explicitly unresolved status
under the same identity when qualified; it cannot turn unknown into absent or
create a competing library revision. If the primary cannot be inspected, preserve
its uncertainty and stop the potentially duplicate operation.

**Done:** required facts are recoverable and read back through qualified existing
references or the authorized alternate. Otherwise hold only effects requiring
that capture, name the exact missing evidence/grant/facility and complete valid
independent work. If no writable durable continuation is available, point to the
existing recoverable request/history and report that the new status is unsaved;
conversation text alone is not a qualified persistence replacement.

## 3. Continue from live effects

Keep serialization across the reread–capture–effect–result interval. Reconcile
stopped-owner state before an authorized lock recovery; never take over a live
owner. Immediately before acting, compare live state with the captured basis.

| Observation | Continuation |
| --- | --- |
| Interrupted before effect; native evidence establishes absence | Apply only the still-authorized missing action after its prerequisites and capture pass. |
| Effect completed; result record missing | Preserve the effect. Complete only the missing attributable record/checks. |
| Write acknowledgement lost | Read the original destination and histories. Reuse a matching committed result; reconcile conflicts. Retry only after sufficient evidence establishes absence and current authority permits it. |
| Store inaccessible or evidence incomplete | Hold the potentially duplicate mutation. Keep completed targets and independent work usable under their own contracts. |
| State changed since the plan | Reconcile the changed target, source, selection, grant or provider. Preserve valid late work and history; the old plan does not override it. |

Keep application, review and outcome separate for every target. Preserve earlier
questions and answers; ask only for a material unresolved prerequisite. For native
library operations, use [the library contract](LIBRARY.md)'s revision checks and
transaction boundary; replaying at a newer revision without reconciliation can
still duplicate a logical operation.

When the primary returns, compare both histories and actual effects under the
same integration ownership. Link the alternate's events and resolve disagreement
explicitly before changing the discovery pointer. Retain required history; restoring
access neither authorizes copying a stale snapshot over current work nor creates
a second active writer. No migration or cleanup is implied by recovery.

**Done:** discoverable current state identifies completed and blocked targets,
actual evidence, unknown outcomes, selected context/grants/methods/standards and
who can perform the next action under what trigger. A fresh unchanged continuation
adds no effect, duplicate event or repeated settled question. Claim only the
storage conditions actually observed; unknown required durability stays blocked.

Inferred application of [spec 15](https://github.com/hanh9898/harness-kit/issues/15),
record requirements 26–30 and A17/A19, within [ticket 35](https://github.com/hanh9898/harness-kit/issues/35).
