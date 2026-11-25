# Bot Inbox host routes

## Resolve the route

Choose this capability only by explicit opt-in. Record mode (`native`,
`external`, `manual`, or `unsupported`), exact ID, source and pinned revision or
digest, caller, target scope, who grants each operation, configuration
precedence, and evidence status. Check access as the actual Bot or worker doing
the action; an owner or parent session seeing the route does not qualify it for
another caller.

| Mode | Use it when |
| --- | --- |
| `native` | Invoke exact `bot-inbox` and verify the resolved source in an isolated Devin project. Prefer the native route when it meets the contract and the caller can use it. |
| `external` | Explicitly select a qualified adapter to an existing Inbox; pin and verify its source, target and caller. Register the portable skill by exact ID only on a path that does not shadow the native skill. |
| `manual` | Explicitly select the pinned portable runbook and an authorized operator using the existing Inbox or tracker record. The operator verifies the card key and prior delivery in that record and reconciles PRs against the live target. A manual run is not background qualification. |
| `unsupported` | Keep dependent operations off; retain only an authorized draft and report the missing prerequisite. |

Do not enable default registration, shadow a same-ID skill, or fall back
silently. Stop the dependent operation on unresolved ID/source conflicts. If a
selected route is missing or unqualified, report the gap and only use a
different route after explicit selection and verification. A read probe must
not create a record, grant, registration, subscription, or scheduled wake.

On native Devin, use the PR subject's server-managed settlement on merge or
close. Verify the card against live PR state; do not manually close it for that
transition. Report inconsistent or unavailable state without substituting a
different write path.

## Qualify in an isolated Bot

Before activation, obtain scope for the test Bot and Inbox, recipients and
threads, and for each actual send, grant-gate check, PR write and wake setup.
Record the skill's resolved ID/source/revision, caller, project, targets and
authority. With two permitted people or threads, run these cases and inspect
the Inbox and destination audit rather than inferring results from instructions:

| Case | Evidence to collect |
| --- | --- |
| Trigger the same ask twice, including a replay after resume. | One active card for the action and at most one delivery to its approved recipient and thread. |
| Reply as the wrong person or in the wrong thread, then reply on the correct route as the authorized person. | Invalid replies leave the card open and produce zero effect grants; the valid reply settles it once. Zero results delivered across routes. |
| Try queue ranking as a worker and as the Bot; check sending with read-only access and a send-scoped grant. | Only the Bot can set priority or defer; read-only access cannot send; send permission cannot issue effect grants. |
| Close a test PR only if separately authorized at the target. Exercise a verified wake, then replay it. | Live terminal state closes the matching review card once; no extra delivery or PR write. |

For automatic reconciliation, verify the event or schedule actually wakes the
appropriate Bot and that it re-reads live state. When consuming events, record
the source and event ID durably before advancing an existing checkpoint. Do not
create a polling loop or a new store. Keep background operation off if wake,
scope, dedupe or delivery evidence is missing. Mark unrun cases unverified;
manual reconciliation is evidence only for the manual route.
