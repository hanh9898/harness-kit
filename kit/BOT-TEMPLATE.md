# Portable Bot template

A Bot is a durable agent role with an owner, a bounded outcome and an optional
way to resume work after a session ends. A [role template](BOT-ROLES.md) gives
the starting instructions, not an installed Bot, authority or proof that a
host can run it. Choose a role only for the requested work; ordinary sessions
and manual workflows do not need a Bot.

## Define the Bot

Keep the following fields in an instruction file or the host's equivalent.
This is a design template, not a file format parsed by the kit.

```yaml
name: <role name>
description: <one outcome the owner gets>
owner: <accountable owner>
scope:
  product_area: <repository, app, service or workspace>
  allowed_work: [<permitted work categories>]
  out_of_scope: [<blocked or handed-off work>]
rhythm:
  schedule: <cadence and timezone, or none>
  event_triggers: [<source and narrow filter, or none>]
queue_cap: <maximum open items awaiting owner review, if used>
memory_root: <authorized store reference, if used>
```

Record the durable Bot identity separately from worker/session identity.
Distinguish requester, approver, executor and attribution. For each required
or optional capability, name its scope and effective configuration/revision.
If using workers, pin the environment, source revision, tool/data access and
any required model. Set separate limits for concurrent work, time, retries
and cost; a review queue cap does not limit execution. Keep credentials and
live grants out of the template.

## Write the role instructions

1. **Outcome and scope.** Start with the selected role's outcome, approved
   inputs, targets and exclusions. Ask for missing required scope before
   acting; do not infer it from a connected account or a forwarded request.
2. **Operating loop.** Define what wakes the role, how it selects work and
   what counts as done. Separate discovery and drafting from writes. Use an
   isolated worker for heavy work or effects that need isolation; keep
   ownership, reconciliation and handoff with the coordinating role.
3. **Evidence and review.** Specify the result, its evidence and who reviews
   it. Name anything untested. When a worker owns the work, route review
   findings to that worker and recheck the live target before handoff.
4. **Needs approval and recovery.** Define which effects can be delegated,
   which require an authorized person's action and how to stop or resume.
   Bind approvals to a specific effect; approval of a draft is not approval
   to publish or apply it.
5. **Learning and rhythm.** Record durable, attributable owner feedback in
   scoped rules. Reconcile open work on an authorized wake, never repeat a
   settled action and do not promise automatic resumption without a wake path.

## Map capabilities to the host

Use the [host capability map](HOST-ADAPTERS.md#capability-map) for routes and
fallbacks. Qualify only the capabilities the role needs against these contracts.

| Capability | What to establish |
| --- | --- |
| Work and workers | Use [task contracts](team-workflow/TASKS.md) and the [selected flow](team-workflow/FLOW.md). Keep durable ownership, a single active claim, prerequisite and revision checks, isolated work, evidence and a settle path. Store the original request or a permitted immutable reference; forwarding does not transfer authority. Reassign only after the old worker cannot act. |
| Review and approvals | Use [authority design](authority/DESIGN.md) and [team responsibilities](team-workflow/TEAM.md). Record a single open ask per requested action, the responsible person, exact subject and reply route. Settle against a reply from the authorized person or authoritative target state. Keep read-only listeners and sending permissions separate; deduplicate delivery and reply in the approved channel. |
| Memory and continuation | Use [persistence](PERSISTENCE.md). Keep standing rules with source, date and confidence separate from private user memory, job data and operational state. Share only authorized data with workers. Reconcile conflicting records before use and verify the effective version on resume. A resource library is separate from all four. |
| Domain tools and targets | Use [tool operations](TOOL-OPERATIONS.md). Pin the service instance, namespace, identity and action. Internal coordination and product-side mutation require distinct scopes and grants; two views of the same tracker do not isolate them. Bind actions to scoped, revocable credentials via secure references, not plaintext; neither installation nor read access grants write access. Treat commit, push, opening a pull request, merging and deploying as distinct effects. |
| Schedules and events | Record the actual wake route, timezone, source event ID, filter, intended recipient and checkpoint. Advance a cursor only after durably recording the event, deduplicate retries and bound concurrent runs. Distinguish a session reminder, a scheduled new run and an event delivered to an existing role. Cancel wakeups when work settles; if no authorized wake exists, say how to resume manually. |
| Evidence and guarded effects | Attach evidence to the task/run and exact revision, with an authorized audience and retention policy. Apply the [write boundary](../skills/harness/harness-implement/WORK.md#write-boundary-and-reconciliation) and [recovery](RECOVERY.md): volatile authority must still be valid at the target when a write commits. For writes needing a target guard, qualify atomic grant, assignment and relevant revision checks at the target. If missing, only use direct, authorized supervision per exact send when policy permits; otherwise stop. If an outcome is unknown, reconcile against the target and receipt before any retry, rollback or reassignment. |

For each selected capability, record the native mechanism, external adapter
or manual route; its source, version and configuration precedence; who may
install, invoke and grant it; and the qualification evidence or precise
blocker. Keep unsupported routes off. Sharing instructions is not sharing a
live Bot: exclude conversation history, memory, connections, credentials and
grants. Keep private preview, interactive supervision and durable deployment
separate.

## Qualify before activation

Test applicable cases against a separately authorized target. Leave skipped
cases unverified and keep features off when their prerequisites are missing.

- Invoke the effective route by actual ID and source; verify a fresh worker
  sees current scoped rules and no unrelated credentials. Test missing or
  restricted routes as well as the happy path.
- Verify concurrent workers cannot overwrite each other's work, read-only
  discovery causes no writes and stale claims or revoked grants cannot commit
  at the target. Test the wrong destination and a lost response after commit.
- Resume from a checkpoint with duplicate or late wakeups. Verify no
  duplicate task or handoff; if tracking promises, check that a deadline
  triggers the right follow-up and settlement requires delivery.
- Check approved recipients can reopen the evidence from a new session and
  unauthorized recipients cannot. Verify approvals and posting go to the
  right target, identity and thread, including when the role only listens.
- Record the executed flow, revision, authorization, receipts, outcomes and
  next wake. Recheck affected routes or scopes after changes. Report applied,
  verified, activated and measured outcomes separately.

Use [factory design](FACTORY.md) only if the owner also selects unattended
factory operation. A manual fallback does not qualify unattended writes.

## Provenance

Adapted from two owner-supplied references received 2026-11-25: *Bot Portable
Template (Host-Agnostic)* (SHA-256
`159bfd6d1dfad1c14d26480d98119918a496c4e77a98f05faddc072a2f7f44c3`)
and the accompanying 21-entry role catalog snapshot. Neither reference has
a public URL. The kit entries adapt the role summaries, not upstream prompts;
their boundaries and evidence requirements do not claim provider parity or
observed host behavior.
