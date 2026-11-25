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

## Phase A: settle the design

1. Reconcile the [environment](ENVIRONMENT.md), active authority and prior
   work. For interrupted or legacy setup, use [resume](RESUME.md). Read
   authorized repo/host context, settled choices, open tickets, Glossary/ADR
   pointers and relevant drafts. Call `harness-library` by exact ID before
   setting the goal: resolve the relevant store/scope and inspect only
   resources that could change the goal or its acceptance. Do not create a
   store for a read. Record the goal, acceptance and scope before the first
   node; lack of operational history does not block discovery.
2. Follow the [discovery tree and node contract](DISCOVERY.md). Check that
   the host permits both original foundation skills. In pass one, visit all
   seven branches in order without opening child domains. Start with
   Environment & authority: settle context boundaries, autonomy, where
   authorized setup records and Harness Glossary/ADRs live, and which
   distinct issue spaces are for Harness and product work. Record each
   tracker role, system/instance, namespace, permission and confirming source;
   use the [tracker contract](../harness-implement/WORK.md#publish-or-update).
   Review remaining branches under current authority, then batch only
   actionable unanswered questions (authority first) and clear proposals for
   review. No questions means no empty turn.
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

1. For the approved Devin project, prepare and when authorized register the
   needed `to-spec`, `to-tickets` and execution overrides via
   [activation](ACTIVATION.md). Registration can use a separate authorized
   bootstrap; it does not depend on an override that is not yet installed.
   Keep a small catalog with actual resolution and invocation evidence.
2. Invoke `harness-implement` by exact host ID with the operation, scoped
   `DesignReady` decision and required route references. Ask it to prepare or
   reuse the spec and drafts. Only request publication with a verified
   Harness destination or an authorized local record for small work. Only
   request execution for a `DispatchReady` ticket. Use its independent
   [gates](../harness-implement/WORK.md); do not use product issues as fallback.
   When separately asked to change reusable material, call `harness-library`
   for the exact operation and store grant, via the same write gate. No raw
   CLI fallback if a skill is blocked.
3. Reconcile the owning assignment, actual effects and accessible evidence.
   Confirm `Verified` and close only passed work, and update the map through
   one writer. Check the [minimum foundation](FOUNDATION.md) and exercise
   authorized initial use through its real consumer route. Keep product
   verification separate from Harness verification; if no app exists, state
   how it can be tested later. Distinguish selected, applied, verified and
   still waiting; do not treat an uncertain effect as success.

Hand off references to settled choices, revisions, live authority, evidence and
the next actionable item. For a session transfer, suggest the user run
`/handoff` only if available; temporary handoff output does not replace an
authorized durable record. Do not auto-start Evolve, open a PR or schedule work.
Use the [qualification checklist](CHECKLIST.md) when authorized to test the route.
