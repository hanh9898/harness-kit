---
name: harness-setup
description: Set up or resume a project Harness. Discover its operating needs in two passes, settle a minimum design and hand authorized work to Harness Implement. Existing-harness advice and scoped changes belong to Harness Evolve.
---

# Harness Setup

Start with the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md):
an explicit request goes straight to Setup; otherwise offer only read-only
research-backed choices before starting either phase.

Deliver a minimum working Harness and a usable continuation, not a fixed set
of files. Setup owns the decision map and assignment verification; decision
contexts discover choices and implementation contexts deliver eligible tickets.
Use existing records and grants. Do not start a pilot or install anything by
default.

## Required path

Follow these steps in order. Continue past a stop only after the missing fact,
grant or evidence exists.

| Step | Read | Do | Expected output | Stop when |
| --- | --- | --- | --- | --- |
| 1. Enter | [PROPOSAL-ENTRY](../../../kit/PROPOSAL-ENTRY.md) | Choose Direct or the proposal lane. | Explicit request or selected proposal. | The requested effect or requester is unclear. |
| 2. Frame | [FOUNDATION](FOUNDATION.md#target-profile-and-caller-mode), [ENVIRONMENT](ENVIRONMENT.md), [RESUME](RESUME.md) | Choose or leave open the visible target scope, then reconcile target facts and prior records. | Goal, acceptance, user-visible scope, target facts, authority gaps. | Intent, target role, write destination or permission scope is unclear. |
| 3. Preflight | [ACTIVATION](ACTIVATION.md#verify-upstream-prerequisites) | Run the read-only target preflight and probe required methods once. | Tool, target, writer and grant blockers named before effects. | Node/npx, exact grant, target-role evidence or writer evidence is missing. |
| 4. Pass one | [DISCOVERY](DISCOVERY.md) | Visit all seven branch contexts in order. | One outcome and checkpoint per branch. | A route, method, Library read or branch answer is blocked. |
| 5. Ask | [DECISION-MAP](DECISION-MAP.md) | Batch only actionable branch questions; map every answer to exact branch paths. | Confirmations name every branch they settle. | A blanket yes or unmapped answer arrives. |
| 6. Pass two | [DISCOVERY](DISCOVERY.md) | Open only applicable child topics, one at a time. | Child outcomes linked to settled parents. | The parent is deferred, blocked or unsettled. |
| 7. DesignReady | [DECISION-MAP](DECISION-MAP.md#check-designready-for-each-scope) | Validate the transition record before reporting readiness. | `check-setup-transition` exits 0. | Any branch decision, confirmation or checkpoint is missing. |
| 8. Prepare | [RECORD-FORMAT](RECORD-FORMAT.md#current-stage-handoffs), [Implement WORK](../harness-implement/WORK.md#prepare) | Build and shape-check one `prepare`; invoke `harness-implement` by exact ID. | Draft refs, reused artifact refs or a named blocker. | The checker fails or drafting authority is unclear; missing H5 stops ticket drafting, not first spec drafting. |
| 9. Publish | [Implement WORK](../harness-implement/WORK.md#publish-or-update) | Build and shape-check one `publish` only with the exact live grant. | Canonical Harness ticket readback or no write. | Target, split approval or publish grant is missing. |
| 10. Execute | [Implement WORK](../harness-implement/WORK.md#dispatch-and-integrate) | The coordinator builds one `execute` at current `DispatchReady`. | A result handoff or `Unknown` checkpoint. | Claim, route, selection or effect authority is stale. |
| 11. Verify | [CHECKLIST](CHECKLIST.md), [DECISION-MAP](DECISION-MAP.md) | Reconcile result, acceptance evidence and close authority; validate the transition record. | `check-setup-transition` exits 0 before `Verified`. | Evidence is unreadable, result is not Applied or close authority is missing. |
| 12. Continue | [PERSISTENCE](../../../kit/PERSISTENCE.md#continuation-handoff) | Hand off refs, live authority, evidence and next trigger. | Receiver-readable continuation. | A durable readable record does not exist. |

## Entry, target scope and mode

Choose the target scope from the user's intent, never from the current Git
directory or from whether Claude Code, Devin or Codex is the agent host. Show
the scope in plain language before recording it, and include it in the design
summary so the user can correct it before approval. Use these three choices:

1. Only this repository (`repo-only`).
2. Only a Bot (`bot-only`).
3. Both the repository and a Bot (`repo-and-bot`).

A clearly repo-only request names that scope briefly and continues without Bot
questions or opt-ins. A bare `/harness-setup` or otherwise unclear intent stays
undecided: show the three choices and wait for a selection before recording a
profile. A Bot or mixed choice may be recorded as intent before a real Bot
identity exists. Verify the exact Bot, durable instance, binding and grant
before any Bot configuration or activation; missing identity blocks only those
Bot effects. Selecting a scope grants nothing and never installs a Bot, writes
configuration or enables a schedule.

Validate the local scope selection fixture or record before relying on it:

```sh
<skill-dir>/../../../kit/scripts/check-setup-scope <scope.json>
```

The record must show what the user saw, what was recorded, the basis, Bot
identity state and effects. It writes nothing. A nonzero result means the scope
is not usable: keep it undecided or correct the record before continuing.

Choose Inspect, Advice or Apply from the request before probing prerequisites.
Default to Inspect if the requested mode is unclear. Apply must be explicit.
Inspect and Advice never install or activate anything, even with a prior install grant.
Apply does not itself authorize writes. Approval of the design is approval to
prepare only; it never publishes, executes, installs or activates.

Before any Apply effect, run the read-only preflight from the real skill
directory. This example is for an upstream install effect that needs Node tools:

```sh
<skill-dir>/../../../kit/scripts/check-setup-preflight \
  --target /path/to/project --mode apply \
  --effect install-upstream=grant:install@1 \
  --requires-tool node --requires-tool npx --json
```

Use one `--effect name=grant-ref` pair per exact effect. Reopen each grant at
its authoritative source. If the report is blocked, name the missing tool,
target-role evidence, writer evidence or grant and make no effect. Never use
sudo, a system package manager or a machine-wide install to clear a missing
Node/npx blocker.

## Concrete internal calls

Use exact host IDs and scoped inputs. Do not substitute raw files, raw catalog
output or a different installation.

| Call | Input example | Expected output | Stop when |
| --- | --- | --- | --- |
| `harness-library` | scope `project:docs`; need `choose a writing method for override guidance`; pin the approved distribution. | One selection handoff, or `Blocked` with the missing store, source, pin or access. | No configured store, wrong pin or denied read. |
| `harness-implement` `prepare` | JSON with operation `prepare`, original request, scope, decision revision, acceptance and needed routes. Shape-check it first. | Spec or ticket draft refs, compatible existing refs or `AwaitSpecApproval`. | Shape check fails, routes are unverified, or H5 is missing for ticket drafting. |
| `harness-implement` `publish` | JSON with operation `publish`, exact draft revision, Harness target, work ID and publish grant ref. Shape-check it first. | Canonical Harness `ticket_ref` after destination readback. | Grant, target or split approval is missing. |
| `harness-implement` `execute` | JSON with operation `execute`, canonical ticket, assignment epoch, route, effect authority and expected target revision. | `Applied`, `Denied` or `Unknown` result with evidence refs. | Claim, route, target revision or effect grant is stale. |

Shape-check a JSON handoff before using it:

```sh
<skill-dir>/../../../kit/scripts/check-stage-handoff --expect-operation <operation> <file>
```

## Phase A: settle the design

1. Reconcile the [environment](ENVIRONMENT.md), active authority and prior
   work. For interrupted or legacy setup, use [resume](RESUME.md). Read
   authorized context for the selected targets, settled choices, open tickets,
   Glossary/ADR pointers and relevant drafts. Call `harness-library` by exact
   ID before setting the goal: resolve the relevant store/scope and inspect only
   resources that could change the goal or its acceptance. Do not create a
   store for a read. Record the goal, acceptance and scope before the first
   node; lack of operational history does not block discovery.
2. [Verify upstream prerequisites](ACTIVATION.md#verify-upstream-prerequisites)
   before opening dependent discovery nodes. Follow the [discovery tree and node
   contract](DISCOVERY.md). In pass one, visit all seven branches in order
   without opening child domains. Start with Environment & authority: settle
   context boundaries, autonomy, where authorized setup records and Harness
   Glossary/ADRs live, and the applicable issue spaces. Keep Harness and
   Product work separate when both apply; never require a repo or Product
   tracker for `bot-only`. Record each applicable tracker role,
   system/instance, namespace, permission and confirming source;
   use the [tracker contract](../harness-implement/WORK.md#publish-or-update).
   In both passes, skip node inputs that do not apply to the selected targets,
   including repo inputs for a Bot-only workspace. Open Bot role and runtime
   questions only for requested Bot work.
3. After each branch, save a checkpoint that names the branch path, outcome,
   open questions, blocker or deferral, and the exact confirmation ref when
   settled. A batch confirmation may cover several branches only when its
   record lists those exact branch paths. An unmapped yes closes nothing.
4. In pass two, visit applicable topics of non-deferred branches in order of readiness,
   using the earliest ready node in tree order. Carry only relevant parent
   direction, choices and artifact pointers. Use one working context per
   node, not one per method. Ask groups of ready questions and route answers
   back to the nodes. Let each topic use Library for the scoped need. If a
   dependency blocks one node, continue independent authorized work.
5. Follow the [decision map](DECISION-MAP.md) for ticket types, checkpoints
   and evidence of confirmation. Present a synthesis of choices, open and
   deferred items, proposed implementation tickets and draft Glossary/ADRs.
   Approval does not authorize activation or target writes. Run the scoped
   `DesignReady` check and validate the transition record before reporting
   readiness. In Inspect or Advice, or when blocked, return the
   design and checkpoint without entering Phase B.

## Phase B: implement and verify

Apply only. Require separate authority for each effect.

1. [Verify upstream prerequisites](ACTIVATION.md#verify-upstream-prerequisites)
   before authoring overrides. If the selected routes need overrides in an
   approved Devin project, prepare the needed `to-spec`, `to-tickets` and
   execution overrides and register them only when authorized. See
   [activation](ACTIVATION.md). Registration can use a separate
   authorized bootstrap; it does not depend on an override that is not yet installed.
   Keep a small catalog with actual resolution and invocation evidence.
2. Follow [v1 stage handoffs](RECORD-FORMAT.md#current-stage-handoffs) and invoke
   `harness-implement` by exact host ID. For a scoped `DesignReady` decision,
   shape-check and validate the transition record before sending `prepare` to draft or reuse artifacts. Shape-check and
   send `publish` only for an exact draft with a current grant and a verified
   Harness destination. The coordinator builds `execute` only at
   `DispatchReady` with the current exclusive claim. Use the independent
   [Implement gates](../harness-implement/WORK.md); do not use Product issues
   as fallback. When separately asked to change reusable material, call
   `harness-library` for the exact operation and store grant, via the same
   write gate. No raw CLI fallback if a skill is blocked.
3. Receive `result` and reconcile the owning assignment, actual effects and
   accessible evidence before marking `Verified`. Validate the `verified`
   transition record first. Close only passed work under separate authority
   and update the map through one writer. Check the
   [minimum foundation](FOUNDATION.md) and exercise authorized initial use
   through its real consumer route. Keep product
   verification separate from Harness verification; if no app exists, state
   how it can be tested later. Distinguish selected, applied, verified and
   still waiting; do not treat an uncertain effect as success. Only for work
   that changes a Bot target, emit `bot-setup` after authorized configuration
   and readback, never on `repo-only`. The operator owns separate activation.

Hand off references to settled choices, revisions, live authority, evidence and
the next actionable item. For a session transfer, follow the
[continuation handoff](../../../kit/PERSISTENCE.md#continuation-handoff).
Do not auto-start Evolve, open a PR or schedule work.
Use the [qualification checklist](CHECKLIST.md) when authorized to test the route.
