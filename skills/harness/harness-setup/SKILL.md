---
name: harness-setup
description: Set up or resume a project Harness. Discover its operating needs in two passes, settle a minimum design and hand authorized work to Harness Implement. Existing-harness advice and scoped changes belong to Harness Evolve.
---

# Harness Setup

Deliver a minimum working Harness and a usable continuation, not a fixed set
of files. Setup owns the decision map and assignment verification; decision
contexts discover choices and implementation contexts deliver eligible tickets.
Use existing records and grants. The first v1 pilot host is Devin in approved
project scope; do not start a pilot or install anything by default.

Select [the target profile and caller mode](FOUNDATION.md#target-profile-and-caller-mode)
from the request and existing context before asking questions. Ordinary repo
onboarding adds no Bot questions or opt-ins. A Bot workspace can be the only target.

## Phase A: settle the design

1. Reconcile the [environment](ENVIRONMENT.md), active authority and prior
   work. For interrupted or legacy setup, use [resume](RESUME.md). Read
   authorized context for the selected targets, settled choices, open tickets,
   Glossary/ADR pointers and relevant drafts. Call `harness-library` by exact
   ID before setting the goal: resolve the relevant store/scope and inspect only
   resources that could change the goal or its acceptance. Do not create a
   store for a read. Record the goal, acceptance and scope before the first
   node; lack of operational history does not block discovery.
2. Check the original foundation methods and [install missing prerequisites
   when authorized](ACTIVATION.md#install-required-upstream-skills) before
   opening dependent discovery nodes. Follow the [discovery tree and node
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
   questions only for requested Bot work. Review the remaining branches, then
   batch only actionable unanswered questions (authority first) and clear
   proposals for review. No questions means no empty turn.
3. In pass two, visit domains of non-deferred branches in order of readiness,
   using the earliest ready node in tree order. Carry only relevant parent
   direction, choices and artifact pointers. Use one working context per
   node, not one per method. Ask groups of ready questions and route answers
   back to the nodes. At each node in both passes, call `harness-library`
   internally for the scoped need; do not substitute raw catalog or CLI.
   If a dependency blocks one node, continue independent authorized work.
4. Follow the [decision map](DECISION-MAP.md) for ticket types, checkpoints
   and evidence of confirmation. Present a synthesis of choices, open and
   deferred items, proposed implementation tickets and draft Glossary/ADRs.
   Approval does not authorize activation or target writes. Run the scoped
   `DesignReady` check; when advising only or blocked, return the design and
   checkpoint without calling execution.

## Phase B: implement and verify

1. [Check and install missing prerequisites for the selected routes when
   authorized](ACTIVATION.md#install-required-upstream-skills) before authoring
   their overrides. If the selected routes need overrides in an approved Devin
   project, prepare and when authorized register the needed `to-spec`,
   `to-tickets` and execution
   overrides via [activation](ACTIVATION.md). Registration can use a separate
   authorized bootstrap; it does not depend on an override that is not yet installed.
   Keep a small catalog with actual resolution and invocation evidence.
2. Follow [v1 stage handoffs](RECORD-FORMAT.md#current-stage-handoffs) and invoke
   `harness-implement` by exact host ID. For a scoped `DesignReady` decision,
   emit `prepare` to draft or reuse artifacts. Emit `publish` only for an exact
   draft with a current grant and a verified Harness destination (including an
   authorized canonical local Harness record for small work). The coordinator
   builds `execute` only at `DispatchReady` with the current exclusive claim.
   Use the independent [Implement gates](../harness-implement/WORK.md);
   do not use Product issues as fallback.
   When separately asked to change reusable material, call `harness-library`
   for the exact operation and store grant, via the same write gate. No raw
   CLI fallback if a skill is blocked.
3. Receive `result` and reconcile the owning assignment, actual effects and
   accessible evidence before marking `Verified`. Close only passed work
   under separate authority and update the map through one writer. Check the
   [minimum foundation](FOUNDATION.md) and exercise authorized initial use
   through its real consumer route. Keep product
   verification separate from Harness verification; if no app exists, state
   how it can be tested later. Distinguish selected, applied, verified and
   still waiting; do not treat an uncertain effect as success. Only for work
   that changes a Bot target, emit `bot-setup` after authorized configuration
   and readback, never on `repo-only`. The operator owns separate activation.

Hand off references to settled choices, revisions, live authority, evidence and
the next actionable item. For a session transfer, suggest the user run
`/handoff` only if available; temporary handoff output does not replace an
authorized durable record. Do not auto-start Evolve, open a PR or schedule work.
Use the [qualification checklist](CHECKLIST.md) when authorized to test the route.
