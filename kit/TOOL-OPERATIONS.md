# Tool operations

Use for a direct tool/integration result through evolve, or a selected operation during setup. Deliver a usable route and demonstrated result within grants. Advice may finish with a concrete operation contract and precise missing prerequisites; installation, deployment and future-call authority are separate effects. Reuse the calling workflow's [original-method selection](../skills/harness/harness-evolve/CHANGE-FLOW.md) and [pre-action capture and continuation](../skills/harness/harness-evolve/UPDATE.md), including scratch scope and serialization.

## Select the operation

Identify the consumer's operation and actual target/account, inputs, needed output and allowed effects before selecting a facility. Inspect available tools, current CLI help, API contracts or UI controls. Compare adequate existing routes by operation coverage, access, verification and maintenance cost. A connected server, installed executable or visible page proves neither operation support nor permission.

Retrieve agent-invoked-cli and actionable-tool-errors through the kit CLI: use an adequate existing command and make failures name the next step. Read external-systems-through-mcp for an actual MCP choice, pinned-external-tool-versions for a version-dependent integration, and the relevant platform detail only when selected. Preserve source certainty: actionable-tool-errors is inferred practice, not a requirement to add a wrapper or rewrite external errors. Native API, CLI and UI routes are alternatives; select by demonstrated fit, not a mandatory ladder. Add a helper only for a demonstrated gap that the granted existing facility cannot cover.

Before execution, make the contract usable directly or through authoritative references:

| Contract | Concrete meaning to establish |
| --- | --- |
| Route and prerequisites | Callable tool/command or UI action; active target/account; available version; authentication, resource access and operation-specific grant. Keep secrets out of records. |
| Input | Required values, identifiers, types, target scope and preconditions; use an existing revision or idempotency mechanism when supported. |
| Output | Expected response/error shape, identifiers and status meanings; required content and completeness for this consumer. |
| Effects | Which resources may change, including logs, record and scratch artifacts; irreversible or uncertain effects; available readback and compensation limits. |
| Check and continuation | How to inspect the actual result, what would invalidate dependent use, bounded repair and the condition/actor that resumes blocked work. |

For selected tasks, consume effective values and controls from [task workflows](team-workflow/TASKS.md). Workflow owns limits and rationale; tools verifies actual mechanisms. A declared limit or instruction is not native enforcement. Keep applicable claim, stop, give-up and trigger-loop controls; capability selection alone does not install them.

**Done:** the operation can be invoked and checked under actual prerequisites, or each missing condition has a concrete continuation. An unavailable route can still yield useful independent preparation.

## Execute and check

Load the applicable original methods before dependent authoring or repair. Use the caller's existing record procedure for required pre-action choice/scope/rationale/authority, and read back capture before the effect. Reconcile live target state and earlier attempts first. Use sufficient grants without another blanket confirmation; an unavailable provider or missing material grant blocks only dependent work.

Invoke the selected native operation. Retain request/action identity, target, version, time and relevant output/exit status without secrets. Check exchanged data against the operation's real contract: parseability, required fields/types, schema/version, matching request/resource identity, status/error meaning and completeness. A UI route needs corresponding visible resource identity/state evidence. Transport success or exit zero alone is insufficient; conversely, a failed response does not prove the effect did not happen.

Keep three conclusions separate: the exchange is valid; the intended target effect is observed; the model's conclusion is supported. Well-formed data can carry a false model claim. Instruction/response design owns model-result form/content criteria; apply its selected checks and source facts before dependent consumption. Preserve its failed judgment instead of changing the protocol to make it pass. [Assessment](../skills/harness/harness-evolve/ASSESS.md) interprets the resulting evidence; [observation](../skills/harness/harness-evolve/OBSERVE.md) supplies correlated operating facts when needed.

Read back the affected resource through an adequate native operation. Compare intended scope and relevant unchanged state. Save observed application separately from review and outcome, retain useful partial results, and name the remaining action and prerequisite. Qualification covers the actual host/provider/version/grant and operation tested; a local fixture or metadata check does not qualify an external service.

## Classify before repair

Retain the raw failure and independently classify both the exchange and the effect. More than one condition can hold: a refusal may have a malformed envelope, and a failed response may accompany a completed write.

| Observed condition | Next action within existing authority |
| --- | --- |
| Unavailable prerequisite | Name the missing executable, source, authentication, target access or required provider. Finish independent preparation; resume when the named prerequisite is available through an authorized route. |
| Refused operation | Preserve the reason and any audit/partial effect. A policy or permission refusal is a stop for that effect. An alternate API, account or UI must satisfy the same authority; route switching cannot bypass refusal. |
| Unsupported operation | Confirm the operation/version against actual help/schema/UI capability. Offer an adequate supported alternative only if its effects and prerequisites fit the grant; otherwise name the needed facility. Connection success is insufficient. |
| Invalid exchange | Stop dependent consumption. Locate the contract mismatch (input, version, identity, shape, truncation or error envelope), retaining valid independent data. An invocation correction may be sufficient; do not rewrite service contracts or model conclusions to manufacture validity. |
| Uncertain effect | Inspect native status, receipt, target revision/content or audit evidence using the original operation identity. A timeout, malformed reply or missing receipt from an incomplete/stale view proves neither success nor absence. If adequate inspection is unavailable, preserve uncertainty and block a potentially duplicate mutation. |
| Valid exchange, failed model/content check | Retain transport success separately from the failed instruction/content criterion. Return the artifact and evidence for its owning response/assessment work; changing tool transport is not a remedy for an unsupported conclusion. |
| Partial or mismatched effect | Preserve completed valid work and identify each unresolved resource. Reconcile conflicts before dependent use. Restore or compensate only the specifically authorized effects with an adequate native route; compensation is a new effect, not universal rollback. |

An error's claimed “no effect” may exclude audit records or downstream work. Inspect the relevant scope rather than widening that claim. When effect evidence establishes success despite a failed response, complete the missing record/check instead of repeating the mutation. When evidence establishes absence, retry only if the cause, grant and duplicate-safety conditions allow it. Use existing idempotency/revision controls where adequate; a reused key alone does not prove their semantics or enforcement.

## Bound a specific repair

Before a repair attempt, state the evidenced cause, smallest permitted change, progress check and stop bound. Reuse the selected task's limits and rationale; for interactive work choose a finite bound proportional to the concrete hypothesis and grant. There is no universal attempt count. Carry spent attempts and unresolved effects into continuation; resuming or changing routes does not reset the budget or create authority.

Repair only that cause: correct an input or supported format, obtain a missing authorized prerequisite, or reconcile observed effects. Check required original methods for code/guidance changes. Inspect uncertain effects before a potentially duplicate call, capture consequential repair choices under the caller's record procedure, and rerun the affected check. Progress means new verified state or evidence toward the requested outcome, not a new phrasing, repeated output or another invocation.

Stop on exhausted scope/budget, refusal, unchanged failure, unresolved uncertainty or a required human condition. Continue only independent authorized work. Provider quota or access failure names that actual condition; repeated calls or unrequested provider switching do not repair it. Keep useful partial outputs and successful checks instead of restarting the whole task.

Hand back the operation/target and actual grant, completed effects and evidence, failed or unknown checks, attempts and repair scope already consumed, remaining work, responsible actor and exact next trigger. Reopen changing live state before the next dependent action. Save this continuation only in the authorized discoverable record; advice may return it without a write. Separate restoration achieved from proposed compensation and broader unverified service support.

**Done:** the usable result and its limits are demonstrated, or useful partial work and a precise resumable blocker remain. No generic retry loop, dispatcher or enforcement platform is required.

This is inferred operating guidance implementing [spec 15](https://github.com/hanh9898/harness-kit/issues/15), implementation requirements 15, 18 and 34, and [ticket 27](https://github.com/hanh9898/harness-kit/issues/27). agent-invoked-cli/actionable-tool-errors inform facility reuse and actionable failures; the shared record, task and assessment contracts remain authoritative for their own responsibilities. Qualification requires actual operation evidence under the selected host and grant.
