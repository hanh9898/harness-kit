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
