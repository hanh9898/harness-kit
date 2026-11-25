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

- Enforce caller, instance and topic access before any read. Resolve the
  published revision through a read-only refresh or read the available published
  snapshot; do not use a sync operation that could publish, initialize a store,
  or flush local changes on a read. Missing stores are not provisioned by this
  skill. Provisioning is a separate authorized effect.
- Before enabling writes, verify that the store can publish an authorized
  batch only if its expected revision is still current, or use an authorized
  single-writer route that checks the revision and publishes under the same
  exclusive access. Recheck write authority at publication; do not automate
  writes if the route cannot prove these checks hold at the target.
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
   pinned source. Exercise an absent store and a no-op read of an existing
   store; audit zero store creation, writes and write-side syncs.
2. Record one owner-authorized standing rule at `high`; sync and verify its
   exact revision and effect in a fresh worker. Forward the same instruction
   to a worker and verify no duplicate rule or batch. The accepted change
   must account for at most one sync batch in the store log.
3. Put a `low` candidate in the scoped test data and verify it is not
   auto-applied. Attempt a stale conflicting write and check that the
   published revision and draft are preserved, the disputed rule is blocked,
   and unrelated rules are unaffected until reconciliation.
4. Try an out-of-scope read and verify access is denied before disclosure.
   Seed only synthetic private data; verify none of it appears in the
   worker's context, shared rules or receipts.

Save revision, caller, scoped receipt and outcome evidence without private
data. Report skipped cases and the route exercised; package checks do not
qualify a live host.
