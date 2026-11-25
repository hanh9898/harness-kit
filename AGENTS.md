# Working agreements

## Carry work through completion

Continue authorized work until the user's acceptance criteria are met. Resolve routine implementation choices yourself using available evidence and existing grants. Treat status questions and preferences as steering of the current objective unless the user changes or cancels it.

Keep a discoverable checkpoint for multi-run work in git, the ticket tracker, or the orchestrator. Record the objective, acceptance criteria, completed work and evidence, outstanding work, active task identifiers, blockers, and next trigger. Reconcile that state at the start of a new run and after context compaction. Temporary files may cache context; essential continuation must remain recoverable without them.

Before ending a run with unfinished work, record what will resume it. Follow the orchestrator's completion-event instructions for running delegates; preserve one active claim per ticket and serialize integration writes. Report completion only when the acceptance criteria and required checks are satisfied.

## Subagent model

Use Codex `gpt-6.1-sol` explicitly for every newly started subagent, including implementers, mergers and reviewers. Do not inherit another model or silently fall back if Sol is unavailable; report the blocker. This applies to orchestration agents, not the product host/model intentionally exercised by a qualification test. Existing runs may finish with their original model unless the user asks to stop or replace them.

## Ask the user only when needed

Use the available user-input tool for material questions that existing sources cannot answer. Include the decision, relevant context, recommendation, and whether an answer is required. Continue independent work while the question is pending.

For an optional preference with a reasonable default within existing authority, state that default and a deadline two minutes after the question is presented. If no answer arrives by the deadline, proceed with the stated default and record the assumption. A late answer steers remaining work; inspect completed effects before changing them.

If ending the run while awaiting an optional answer in T3, create a one-time `schedule_task` bound to the current thread for the deadline. Its prompt must identify the question, default, scope, and checkpoint; it must first check for an answer, cancellation, completion, or an already-applied default. Disable an obsolete timer when the answer is handled early. Use delegate completion events for delegate waits, not scheduled polling. If scheduling is unavailable or fails, report that automatic resumption is not armed.

Required permission, indispensable missing facts, secrets, and required human review remain prerequisites. Silence does not supply them. Keep only dependent work blocked, preserve a concrete continuation, and complete independent authorized work. A user pause or cancellation takes precedence over a timeout.

## v1 structural guard

Run `python3 -m pytest -q tests/test_v1_structural_contract.py tests/test_library_read_no_write.py`.
Each gate has one owner and one `v1-gates` JSON block of `{id, requires}` records
per owner. Keep alternative routes in separate leaves. A root is an observed
fact, not authority by itself. When a contract intentionally changes, update
its owner, caller links and the guard together.
Use plain top-level frontmatter keys and a single-line `name:` for skill IDs
so the guard can check them without a YAML dependency.

| Rule | Check |
| --- | --- |
| Apply, override readiness, spec revision, publication and continuation keep their prerequisites. | Gate owners, required edges and caller links. |
| Only an automation for the exact Bot can claim; durable dedupe precedes ACK. Configuring, rebinding, piloting and enabling remain separate. | Wake and lifecycle edges, no chat ingress, and the Tasks/Inbox boundary. |
| Discovery and override routes do not become default entries. | Entry inventories, proposal links, discovery order and parents, and override IDs. |
| Library reads do not write; Inbox and Memory retain distinct authority and store gates. | Public Library CLI no-write tests, and Library, Inbox and Memory edges. |

The `v1-guard` PR job is a structural and CLI regression check, not proof of
host behavior, TLC properties, or live ACL enforcement. Reproduce red cases in
a scratch checkout, never on the review branch. The repository owner sets the
required check on the protected branch; do not bypass this gate.
