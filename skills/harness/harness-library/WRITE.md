# Write and reconcile a library operation

Resolve the exact authoritative store, scope, owner, requested effect and
grant. Reuse existing suitable stores and the established governance. A
personal-save grant does not authorize shared promotion, a host installation
or a consumer change. A mutable resource field is not proof of authority.
Capture rationale, authority reference, expected revision and recoverable
continuation before the effect. Do not create an alternative store to get
around a blocker.

For authoring, check existing resources first. Use the original `research`
method only for unresolved factual gaps and `writing-for-agents` for
agent-read content, including its skill mechanics if writing a skill. If a
required method is unavailable, keep dependent work blocked; an authorized
incomplete draft can retain its stated limits. A piece states use, inputs,
results and dependencies; a rule states applicability and a check; a workflow
states roles, handoffs and failure continuation. Preserve attributable source
identity, revision, certainty and actual evidence.

Read only the relevant fields and examples in the [CLI contract](../../../kit/LIBRARY.md):
[save](../../../kit/LIBRARY.md#save-input), [selection](../../../kit/LIBRARY.md#exclusion-and-explicit-restoration)
or [origin update](../../../kit/LIBRARY.md#origin-comparison-and-updates).
Keep content and selection revisions separate. Exclusion is a scoped library
choice, not removal from consumers. Restore only on explicit request after
inspecting current content and selection history.

For supplied resources, carry the verified consumer pin from the
[strict read](READ.md) into issuance, mutation and readback. An unresolved
pin or configured store blocks the effect; do not substitute the bundled
catalog or a new store. Keep each Bot's selection, adoption and grant refs
in its own scope, even when the backing Library is shared.

## Write guard

Use the [write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation)
for each mutation. For local automated `save`, `update`, `disable` and
`restore`, qualify the current [guarded Library CLI](../../../kit/LIBRARY.md#guarded-writes)
on the authoritative SQLite store. Only a trusted, authorized grant manager
may enable guarding or issue/revoke grants; a writer must not mint its own
authority. Enabling guarding is itself a store change. Confirm the host pins
the intended catalog/CLI and prevents bypass via old CLI, direct database
writes, independent copies or unapproved grant issuance. Otherwise the CLI
transaction is not a sufficient automatic boundary.

1. Read the relevant live revision and approve the exact input file. A trusted
   caller uses `library --store <selected-path> grant-write <operation> <id> --source supplied --kit-dir <pinned-catalog> --input <file> --expect-revision <rev> --ttl-seconds <ttl>`
   for a supplied exclusion/restoration. Use the selection revision. For
   saved resources use `--source saved` without a catalog flag (content
   revision for `save`/`update`). Use a short TTL.
   Issuance validates the request and compares the live revision before enabling
   guarding or replacing a grant. On conflict, reread content or selection
   history and reconcile before reissuing. Rejection leaves existing grants intact.
2. Pass the returned `write_grant` ID with `--write-grant` to the exact
   mutation with unchanged input bytes, store, source, resource and revision.
   For supplied resources, run
   `library --store <selected-path> <operation> <id> --source supplied --kit-dir <pinned-catalog> --input <file> --expect-selection-revision <rev> --write-grant <grant-id>`.
   The host must enforce the pin and intended writer; SQLite does not bind
   the grant to the catalog revision or caller. Keep the grant out of handoffs and logs.
   For content mutations use `--expect-revision`. A grant is single-use. A rejection does
   not authorize a retry, a different input, or a downgrade to an unguarded store.
3. Revoke the exact grant at the target with `revoke-write <grant_id>` when
   its underlying authority or assignment ends before the write. An upstream
   revocation does not itself revoke a target grant. The transaction consumes
   the grant with the successful change and history; revocation that wins
   prevents the mutation, not one already committed. Qualify propagation for
   any authority held outside the store before allowing automatic execution.

For targets without a qualified atomic gate, use direct authorized supervision
at each send only if policy permits; otherwise stop. A guarded store still
requires its valid CLI grant even for supervised writes. Do not weaken access
controls to resume work.

After a selection change, [reread selection and history](READ.md) in the same
store, scope and pin. Match the new revision, owner/scope, action and snapshot to
the approved request. For saved content, use `show` and `history` in the
same store. Return durable readback evidence. If uncertain, keep `Unknown`
and reconcile actual history and state before retry or closure. Do not replay,
restore or overwrite to turn uncertainty into success. Preserve independent
content edits and record what remains unverified. Report a save and any
observed consumer impact separately; never imply adoption.
