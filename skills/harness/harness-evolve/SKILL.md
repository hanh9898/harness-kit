---
name: harness-evolve
description: Diagnose, assess or improve an existing Harness. Use for drift, agent guidance, tools, workflows, authority, costs, experiments and resource adoption. Change only the affected scope; ordinary product work belongs elsewhere.
---

# Harness Evolve

An explicit request takes the direct path. Otherwise, start with silent,
read-only research under the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md).

Start from the requested result, the actual consuming host and its current
authority. Keep existing records, including `needs-change` work, and reopen only
what affects this request. A missing setup catalog or `harness/record/` does not
require onboarding. New foundations belong to Setup; library-only work belongs
to `harness-library`. Classify a change by what it changes, not where it was
reported or where its files live.

Use the existing decision and live configuration to identify the affected target
and caller. A request about the repo alone stays `repo-only`, with `interactive`
as the default when no persistent runtime is bound. Do not add Bot questions or
opt-ins, Inbox/Memory access or store writes to the repo path.
Use [Adoption](ADOPTION.md#1-reconcile-selections-and-live-targets) to reconcile
an affected binding, not to bootstrap or reinstall it.

| Intent | Path |
| --- | --- |
| Observe, advise, assess or retrospect | Read current evidence and open only relevant questions. Return findings, limits and the next step. Do not create a record, schedule, activation or implementation ticket for advice. |
| Repair a small, understood problem | Confirm the failure, current basis, exact target and check. Use a minimal implementation ticket without another grill. |
| Design a change with unresolved choices or multiple consumers | Track affected nodes and real dependencies. Settle the decision before preparing implementation. |
| Diagnose or run a bounded experiment | Define question, baseline, quality floor, allowed effects and stop rule. Report negative or inconclusive results; no automatic adoption. |

Use the appropriate reference, not the bundle:

| Need | Reference |
| --- | --- |
| Drift or recovery | [Drift](DRIFT.md), [coordinated recovery](../../../kit/RECOVERY.md) |
| Existing selection, upgrade, replacement or carry-forward | [Adoption](ADOPTION.md) |
| Access to task-specific knowledge or instruction design | [Context](CONTEXT.md), [instruction and response](../../../kit/instruction-response/DESIGN.md) |
| Tools, failures or uncertain tool effects | [Tool operations](../../../kit/TOOL-OPERATIONS.md) |
| Status, spend, assessment, learning or comparison | [Observation](OBSERVE.md), [assessment](ASSESS.md), [retrospective](RETROSPECTIVE.md), [experiment](EXPERIMENT.md) |
| Authority, team, standards or an explicitly selected factory | [Authority](../../../kit/authority/DESIGN.md), [team](../../../kit/team-workflow/TEAM.md), [task workflow](../../../kit/team-workflow/TASKS.md), [standards](../../../kit/standards/SELECT.md), [factory](../../../kit/FACTORY.md) |
| Record repair, supersession, archival or cleanup | [Record maintenance](../../../kit/MAINTENANCE.md) |

For any catalog ID named by a runbook, call `harness-library` internally to
check current selection and retrieve only relevant details. If an item is
excluded or unverified, do not use it as guidance; continue independent work
and state any dependent limitation. No raw catalog fallback.

## Phase A: decide in the affected scope

1. Record desired outcome, acceptance, consuming targets, protected scope and
   current grants. For multi-step work, use the shared [decision map](../harness-setup/DECISION-MAP.md).
   A simple case can use an existing record or an in-session summary.
   Check the Harness and product destinations when trackers are relevant;
   use the [tracker contract](../harness-implement/WORK.md#publish-or-update).
   Product references may inform the work when readable, but are not a write
   destination. No substitute using repo defaults, filtered views or labels.
2. Use the [discovery map](../harness-setup/DISCOVERY.md) to identify affected
   nodes and dependencies. Do not invoke Setup's topic routes.
   Pass one checks current context and widens only for dependencies that could
   alter the result. Use relevant authorized runtime evidence; its absence is
   not a blocker for static cases or a basis for invented improvements. Revisit
   a deferred choice only if the new objective or its trigger makes it relevant.
3. Pass two resolves actionable questions in dependency order. Use one context
   per affected node that needs grilling, with both foundation skills and
   only relevant Harness Glossary/ADR pointers. Group unanswered choices;
   respect current choices and constraints. Apply [method selection](CHANGE-FLOW.md)
   before recommendations or effects. Call `harness-library` by exact host ID
   for the scoped discovery need. For separately authorized library changes
   call the exact operation; applying in the repo remains a separate decision
   and permission.
4. Separate facts, proposals and choices; cite user confirmation or actual
   delegation for that exact choice. Check `DesignReady` against the map and
   target; hold unresolved, incompatible or unproven dependencies. Advice
   alone stops here, without a stage handoff. For a repair with settled scope,
   the evidence and prior decision can satisfy this phase without open discovery.

## Phase B: prepare, apply and verify

Read [UPDATE.md](UPDATE.md) before effects. Reuse the existing durable record,
integration owner and current adoption procedure. A proposed rule does not
authorize itself. Document timing, active grants and pre-action state.

Independently verify only needed skill routes in the actual host and caller
using the [route contract](../harness-implement/ROUTES.md). Reuse current evidence
or inspect effective host configuration and run a permitted no-write probe. Use
the resulting ID/revision, scope, invocation context, status and evidence; do
not rerun Setup, install a route, or invoke a user-only upstream method.
Valid artifacts eliminate their preparation routes. An unavailable or
ambiguous execution route blocks execution, not drafting or independent work.

For the current change only, send one [v1 stage handoff](../../../kit/STAGE-CONTRACTS.md)
per requested operation. [Reuse compatible artifacts and prepare or publish](DESIGN-WRITEBACK.md#hand-off-the-current-change)
through `harness-implement`. The authorized coordinator builds `execute` only
at live `DispatchReady`: reopen the canonical ticket, decision, dependencies,
selection if used, exclusive claim and epoch, exact route, target revision and
authority for the effect.
A missing, stale or conflicting claim blocks dispatch. Use the
[destination write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation):
target-enforced atomic conditions, or direct authorized supervision of each
non-atomic send only where policy allows. Otherwise stop.

Use [CHECK-STEP.md](CHECK-STEP.md) to receive `result` and verify the actual
assignment, behavior, affected target and protected scope. Check Harness
behavior and relevant product regressions separately. Update Evolve's map
only after checking the criteria and with writeback authority; closing passed
work needs separate authority.
Distinguish selected, applied, observed working and measured improvement.
Report what remains open, untested or blocked and the next action. Do not
reapply finished effects on resume or create a new loop or schedule. See the
[qualification checklist](CHECKLIST.md) for authorized behavior checks.
