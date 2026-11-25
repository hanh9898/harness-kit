---
name: bot-memory
description: Read or update scoped, durable Bot rules in an opted-in instance without mixing in private memory or run state.
---

# Bot memory

Use the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md) before
choosing an operation. A scoped start or resume that calls for a Memory
read goes direct. A bare invocation is not opt-in to inspect a store.

Read on start or resume. Refresh before relying on an old session's view.
Resolve the exact skill and source. Confirm opt-in and use the
[qualified host route](HOST.md) before accessing a store.

## Keep storage scopes separate

| Layer | Contents and access |
| --- | --- |
| Durable Bot rules | Shared within the authorized Bot instance. Read `MEMORY.md` and relevant topic files; write global Bot rules to the index and topic-specific rules to their own files. |
| Personal memory | Separate private store and explicit consent; never read or share it through the Bot rules route. |
| Job files | `files/<job>/` for job inputs and outputs under the job owner's access and retention policy. |
| Operational state | Checkpoints, cursors, Inbox cards and promises belong to the Bot or host, not durable rules. |

Library is a separate resource catalog. Keep secrets in the vault and grants
at the authority boundary; never copy either into memory, or turn chat
transcripts, personal memory or in-flight task state into shared rules.

## Read and apply

Resolve the binding for this Bot. Verify caller access and store identity
before reading the published index and only the authorized, requested topic.

| Store state | Read outcome |
| --- | --- |
| Confirmed unconfigured | No rules. |
| Configuration unknown | `Blocked`. |
| Configured store missing | `Blocked`. |
| Configured store unreadable | `Blocked`. |
| Configured store identity mismatch | `Blocked`. |
| Ready store, no matching rule | No rules. |

On `Blocked`, report the unmet requirement without disclosing store contents.
Do not fall back to another store or a cached rule. On a read or unchanged
request, never create a store, file, directory or write-side sync.

Only auto-apply an in-scope, uncontested `high` rule. A `low` rule is a
candidate to verify, not an instruction. Treat other or missing confidence
as non-binding. Current scope, instructions and target authorization still
take precedence. Memory does not grant access or permission to act.

## Record and reconcile

1. Write only for an authorized standing instruction or verified evidence.
   Write only to a ready store. Verify write authority for the owner, caller,
   instance and topic. The session owning the original conversation records an
   authorized standing instruction once. A worker receiving it in a forwarded
   message must not record it again.
   Directly received corrections and verified evidence still need scoped write
   authority. Check existing rules and the original event before writing.
2. Record one rule per entry with a source reference, ISO date and confidence,
   for example `- Use the project formatter. [source: <event>; added: YYYY-MM-DD; confidence: high]`.
   Use `high` for an explicit standing instruction from the owner or an
   owner-authorized promotion supported by verified evidence. Start observations
   at `low`; add confirming sources without dropping prior provenance. Revise
   or downgrade a contradicted rule only through reconciliation. If the
   instruction is temporary or the effective entry is unchanged, do not write.
3. Prefer separate topic files or keys; serialize changes to `MEMORY.md`.
   Publish against the revision read. Sync one batch immediately per accepted
   change. Use a fresh authorized worker on the same Bot instance, store, and topic
   to verify the published revision, rule, and provenance before reporting the
   rule effective. If the outcome is `Unknown`, check the same destination's
   revision and receipt before any further write. Do not replay.
4. On conflict, preserve the published revision and the local draft. Do not
   auto-apply or overwrite the disputed rule before reconciliation. Leave
   unrelated rules available. Have the scoped writer reconcile with the owner
   against the current revision, preserving provenance, then verify readback.
