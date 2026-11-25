---
name: bot-inbox
description: Reconcile Bot Inbox cards for owner input, approvals, and PR review without duplicate asks or delivery.
---

# Bot Inbox

Use the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md) before
choosing an operation. A concrete request goes direct. Without opt-in, do
not probe an Inbox route or use a card to offer choices.

Load this opt-in skill before asking or blocking on an authorized person, when
an answer arrives or the card's purpose changes, and before handing off work
with an open ask. Use [host routes](HOST.md#resolve-the-route) to find the pinned
Inbox for this Bot and caller. Read related cards and current target state before
writing; continue work that does not need an ask. Do not keep an Inbox in memory,
the resource Library, or a separate queue.

## Keep one active card per action

**Card key:** `(bot_id, respondent, subject-id, subject-revision, kind, exact-action)`
within the bound Bot's Inbox. Use the authenticated respondent, canonical
subject ID and authoritative revision, ask kind (`ask`, `approval`, or
`review`), and exact requested operation. Record source, stable ask ID and
approved delivery and reply routes. Resolve aliases before building the key.

- Retries, thread changes and nonmaterial edits do not create a new action.
  A deferred card still owns its key. Upsert using store-enforced uniqueness
  or a verified single writer. If neither exists, keep a draft. Do not create
  a card or send an ask.
- When the revision or requested decision changes materially, supersede the
  old card before opening its replacement under the new key. Suppress its
  pending delivery and keep its history and receipts. Guard supersession and
  reply settlement against concurrent changes to the active card or live
  subject revision. If the route cannot do that, stop automated replacement
  and settlement.
- The Bot creates or updates its own cards and ranks them by priority, urgency,
  effort and engagement. The Bot may defer a card with an explicit expiry. A
  worker proposes a card to the Bot or edits/closes a card within its current
  delegation; it cannot set priority or defer cards. Ranking never authorizes a
  send.
- Use card-close authority to settle a card with its reason and evidence.
  Suppress pending delivery for asks that are no longer current. Check active
  cards and settled history: a repeated or late event does not reopen a settled
  ask. Verify that a new decision is needed before creating a card. If it would
  reuse a settled key, require a new authoritative subject revision before
  opening a card. Without one, keep the new ask in manual review.

## Deliver and handle replies separately

1. **Send:** Check separate send authority for the sender, audience, channel,
   exact thread and current payload. Read/listen access and card write access do
   not allow sending. Check cadence independently of rank, per person and
   channel; hold or group only current asks for the same approved audience and
   route. Do not send periodic status pings or move delivery to another thread.
2. **Delivery key:** `(card-key, logical-delivery-id, approved-route-id)`.
   Replay, card edits, cadence changes and regrouping reuse the same keys.
   Save each destination receipt with the ask IDs and delivery keys it covers,
   including every ask in a group. Check coverage before sending. Do not resend
   covered asks. Use destination dedupe or a verified serialized sender with
   durable receipts. On unknown outcome, reconcile before retrying. Stop
   automatic retries if the original outcome cannot be read back or deduplicated.
   A delivery receipt does not change Tasks status, assignee or session claim,
   or GitHub PR status. It is not a reply, effect receipt or grant.

## Validate and record replies

Resolve the Bot from the verified binding, not the message or thread. Find the
active card in the bound Bot's Inbox. Match the authenticated respondent,
canonical subject, current subject revision, kind, exact action and approved
reply thread to that card. Do not settle on a mismatch, a superseded card or a
forwarded reply without verified provenance. The reply's subject revision
must match both the card and the live subject. Follow the
[host fallback](HOST.md#resolve-the-route) if the revision cannot be proved.

Record a matching answer once. A duplicate does not settle or submit it again.
A decline settles only the card. For an approval, only an authenticated yes
can send the existing request to the independent grant gate. Include the
stable request ID, actor and exact operation. The gate checks authority, scope,
revision and payload. Read back its receipt before retrying an uncertain
handoff. A reply cannot wake a Bot or mint a grant. Neither a card, a button
click nor send authority grants the effect. Any acknowledgment needs its own
send check on the approved route.
Do not disclose the answer on another route.

## Reconcile PR review cards

On a verified wake or when the Bot resumes, use the canonical repo and PR ID.
Read live state from the authoritative target. An event is a hint to reconcile,
not proof that the PR is terminal.

| Live PR state | Card action |
| --- | --- |
| Open | Leave the review card open. |
| Merged or closed | Close the matching review card idempotently, recording the observed state and evidence. |
| Unavailable, stale or wrong target | Leave the card unchanged; mark reconciliation unverified. |

Require card-close authority. If the host owns PR card settlement, verify its
result rather than issuing a second close. Do not settle separate approval or
ask cards from this rule, and never merge or close a PR using authority to close
its card. See [wake and qualification](HOST.md#qualify-in-an-isolated-bot) before enabling
background reconciliation. Without a qualified wake route, reconcile only on
resume or by operator action; do not promise immediate auto-close or poll in a
loop.
