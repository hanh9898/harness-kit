---
name: bot-inbox
description: Reconcile Bot Inbox cards for owner input, approvals, and PR review without duplicate asks or delivery.
---

# Bot Inbox

Load this opt-in skill before asking or blocking on an authorized person, when
an answer arrives or the card's purpose changes, and before handing off work
with an open ask. Use [host routes](HOST.md#resolve-the-route) to find the pinned
Inbox for this Bot and caller. Read related cards and current target state before
writing; continue work that does not need an ask. Do not keep an Inbox in memory,
the resource Library, or a separate queue.

## Keep one active card per action

Use the existing Inbox to record the Bot owner, authorized respondent, ask kind
(`ask`, `approval`, or `review`), canonical subject, exact requested operation,
source and stable issue/PR/request ID, and approved delivery and reply routes.
Use authenticated identities and target IDs, not display names or message text.

- Deduplicate by authorized respondent, canonical subject and requested action
  within the Bot's Inbox. The action includes the ask kind and operation. Resolve
  aliases before building the key; retries and thread changes do not create a
  new action. A deferred card still owns its key. Upsert using store-enforced
  uniqueness or a verified single writer that serializes reads and writes for
  the key. If neither exists, keep a draft and do not create a card or send an
  ask.
- The Bot creates or updates its own cards and ranks them by priority, urgency,
  effort and engagement. The Bot may defer a card with an explicit expiry. A
  worker proposes a card to the Bot or edits/closes a card within its current
  delegation; it cannot set priority or defer cards. Ranking never authorizes a
  send.
- Close a card when answered, declined, superseded or no longer needed, with the
  reason and evidence. Suppress any pending delivery when its ask is no longer
  current. Check settled card history as well as active cards; a repeated or late
  event does not reopen a settled ask. Verify that a new decision is needed
  before creating another card.

## Deliver and handle replies separately

1. **Send:** Check separate send authority for the sender, audience, channel,
   exact thread and current payload. Read/listen access and card write access do
   not allow sending. Check cadence independently of rank, per person and
   channel; hold or group only current asks for the same approved audience and
   route. Do not send periodic status pings or move delivery to another thread.
2. **Deduplicate delivery:** Use a stable delivery key per logical delivery on an
   approved route, separate from the card key. Replays reuse that key; a card
   edit is not a new delivery. Track which asks a grouped delivery covers so
   regrouping cannot resend them. Check the destination receipt/history and
   use destination dedupe or a verified serialized sender with durable receipts.
   On unknown outcome, reconcile before retrying; if the effect cannot be read
   back or deduplicated, stop automatic retries.
3. **Validate the reply:** Match the authenticated respondent, subject, exact
   action, active card and configured reply route, including the thread. A reply
   from the wrong person or thread, a forwarded reply without provenance, or an
   answer to a superseded request does not settle the card. Do not disclose the
   result or acknowledge it on a different route.
4. **Gate the effect:** Record a matching answer once. If it is an approval,
   route it to the independent grant gate with the stable request ID and exact
   actor and operation. The gate verifies current authority, target scope and
   payload before issuing a grant. Read back the gate's receipt before retrying
   an uncertain handoff. Neither the reply, a button click, a card, nor send
   permission is itself a grant. Replying back, when needed, requires its own
   send check on the approved route.

## Reconcile PR review cards

On a verified wake or when the Bot resumes, use the canonical PR ID and read
live state from the authoritative target. An event is a hint to reconcile, not
proof that the PR is terminal.

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
