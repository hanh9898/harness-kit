# Bot Inbox host routes

## Resolve the route

Choose this capability only by explicit opt-in. Record mode (`native`,
`external`, `manual`, or `unsupported`), exact ID, source and pinned revision or
digest, `bot_id`, bound Inbox, caller, target scope, who grants each operation,
configuration precedence, and evidence status. A Devin child uses the Inbox of
the Bot that started it, not the Inbox of another Bot on the same thread.
Check access as the actual Bot or worker doing the action; an owner or parent
session seeing the route does not qualify it for another caller.

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
different write path. If native cannot prove the reply's subject revision,
require manual review with no effect: leave the ask unresolved and do not
submit a grant request. An Inbox item represented by a board ticket is still
an Inbox item, not a Tasks record or proof of Tasks or GitHub authority.

## Qualify in an isolated Bot

Before activation, obtain scope for the test Bot and Inbox, recipients and
threads, and for each actual send, grant-gate check, PR write and wake setup.
Record the resolved ID/source/revision, Bot binding, caller, project, targets
and authority separately for the owner and worker. Use two isolated test Bots
and scoped respondents and threads for the mismatch cases. Inspect the Inbox
and destination audit:

| Case | Evidence to collect |
| --- | --- |
| With send authority and cadence permitting delivery, send two current asks as a group. Confirm delivery, then replay the trigger after resume with a nonmaterial edit and regrouping. | One active card per action and one initial delivery to the approved recipient and thread. Zero additional deliveries on replay. The receipt covers both asks. A held or failed first send does not qualify dedupe. |
| Regroup a delivered ask with an authorized, undelivered ask on the same route, with cadence permitting delivery. | Only the undelivered ask is sent. Its receipt covers only that ask; the earlier receipt stays unchanged. |
| Create a similar ask in each Bot. Try wrong Bot, actor, thread, subject, revision or action separately. Supersede a card and replay its old reply. | Neither Bot settles the other's ask. Invalid or stale replies leave the current card open and produce zero effect grants. The superseded card stays closed and its pending delivery is suppressed. |
| Change action A to B, then back to A at the same subject revision. Repeat with a new authoritative subject revision. | At the old revision, A stays in manual review with no new card or send. At the new revision, a new A card can open. The original A card stays closed in both cases. |
| Reply to the current card on the approved route, then replay the reply. Exercise both a decline and an authenticated yes on separate asks. | Each valid reply settles once. Decline submits no request; yes submits one request to the independent gate. No reply, card or receipt mints a grant or wakes a Bot. Zero results delivered across routes. Tasks and GitHub state stay unchanged. |
| Try the native route without trustworthy subject revision evidence. | Manual review only: no settlement, grant request or effect. |
| Try queue ranking as a worker and as the Bot; check sending with read-only access and a send-scoped grant. | Only the Bot can set priority or defer; read-only access cannot send; send permission cannot issue effect grants. |
| Start with an open test PR and review card. Close the test PR only if separately authorized at the target. Exercise a verified wake, then replay it. | Live terminal state closes the matching review card once; no extra delivery or PR write. |

Record upsert, lookup, delivery and reconciliation counts for the initial run
and replay, by Bot and caller. Use the destination audit to verify that replay
adds zero sends.

For automatic reconciliation, verify the event or schedule actually wakes the
appropriate Bot and that it re-reads live state. When consuming events, record
the source and event ID durably before advancing an existing checkpoint. Do not
create a polling loop or a new store. Keep background operation off if wake,
scope, dedupe or delivery evidence is missing. Mark unrun cases unverified;
manual reconciliation is evidence only for the manual route.
