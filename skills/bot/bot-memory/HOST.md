# Bot memory host routes

Record the selected route (`native`, `external`, `manual`, or `unsupported`),
exact skill ID, source and pinned revision or digest, configuration precedence,
Bot instance/store, allowed caller and read/write scope, who grants access,
and qualification evidence. Check the effective ID and source in the actual
caller, not just in a skill list or the parent. Missing access, stale or
ambiguous sources, and unproven capability block the affected operation; do
not silently switch routes.

| Route | Use |
| --- | --- |
| `native` | On Devin, prefer the built-in `bot-memory` and host sync only if they meet this contract. Do not install a portable skill of the same ID to shadow them. Qualify the native source and fresh-worker access independently. |
| `external` | Register only this package by exact ID from a pinned distribution when selected. Use an authorized existing store with scoped reads and conditional publication. Do not add it to default Harness registration or create a store to satisfy a read. |
| `manual` | An authorized person may inspect an existing scoped snapshot and perform a supervised write through a single writer, with a revision check and readback. Record what was actually checked; this does not qualify unattended writes. |
| `unsupported` | Leave the unsupported capability off. If only writes are unsupported, qualified reads may still use the published snapshot. Unrelated Bot work can continue. |

## Store requirements

- Enforce caller, instance, and topic access before probing the store. The
  same owner does not authorize reads or writes across Bot instances. Resolve
  the configured route and verify the canonical store target and continuity
  against the binding. Report `Blocked` on denied access or when identity,
  continuity, or read access cannot be verified. Confirm unconfigured status
  from the Bot binding, never from a failed store lookup.
- Read the published revision with a read-only refresh or an authorized
  published snapshot. Limit the read to the index and requested topic within
  scope. On a read, do not use a sync operation that could publish, initialize
  a store, or flush local changes. Provisioning is a separate authorized effect.
- Before enabling writes, verify that the store can publish an authorized
  batch only if its expected revision is still current, or use an authorized
  single-writer route that checks the revision and publishes under the same
  exclusive access. Recheck write authority at publication; do not automate
  writes if the route cannot prove these checks hold at the target. A stale
  revision is a conflict, not permission to retry.
- Keep drafts separate from effective rules. Surface an unresolved conflict
  for the affected rule to authorized readers through scoped host state without
  publishing the draft or blocking unrelated rules. Clear it after
  reconciliation and readback.
- Record the original event identity (source and event ID), base and published
  revisions and receipt in scoped host evidence, not in personal memory or as
  additional shared rules. For a repeat event or lost response, check the
  authoritative receipt or history before sending another batch. With no
  conclusive readback, leave the write `Unknown` and escalate rather than retry.

## Qualify on an isolated Bot

1. From the actual Bot and worker, invoke exact `bot-memory` and record its
   pinned source. Check that a confirmed unconfigured binding and a ready
   store with no matching rule return no rules. Check that a configured store
   that is missing, unreadable, or has the wrong identity returns `Blocked`.
   Audit zero store creation, writes, and write-side syncs in these read cases.
2. Open a worker on the old published revision. Record one owner-authorized
   standing rule at `high` and sync it. In a fresh authorized worker on the
   same Bot instance, store, and topic, verify the exact revision, rule, and
   original event provenance. Resume the old worker. Verify that a read-only
   refresh picks up the new revision before applying rules, with no writes or
   write-side syncs. Forward the same instruction to a worker and verify no
   duplicate rule or batch. The accepted change must account for at most one
   sync batch in the store log. Measure readback time from the fresh worker's
   scoped read request to verification. Check that the read accessed no topics
   outside the requested scope.
3. In a separate case, drop the response after a test write commits. From a
   fresh authorized session, reconcile `Unknown` from the authoritative
   receipt or history and verify the published revision. Audit the caller's
   outbound attempts for zero resubmissions and the store history separately
   for exactly one committed batch. If the host cannot inject the failure or
   expose both counts, mark the case unverified.
4. Put a `low` candidate in the scoped test data and verify it is not
   auto-applied. Attempt a stale conflicting write and check that the
   published revision and draft are preserved, the disputed rule is blocked,
   and unrelated rules are unaffected until reconciliation.
5. Use only synthetic private data. Try an out-of-scope read. Attempt both a
   read and a write across two Bots with the same owner. Verify denial before
   disclosure and no changes to either store. Check that no private data appears
   in the worker's context, shared rules, or receipts.

Save revision, caller, scoped receipt and outcome evidence without private
data. Report skipped cases and the route exercised; package checks do not
qualify a live host.
