# Stage handoffs (v1)

Pass only the inputs for one operation, not copies of specs, tickets, decision
maps or logs. In one session, pass the structure through the host. Across
sessions, use an authorized handoff or existing record; use the JSON form below
when a machine must read it. If you cannot save it, return a draft in the
session and do not promise automatic continuation. The original records remain
authoritative. This contract does not require a new store or migration.

Keep the [M2 target profile and runtime mode](M2-CONFIG.md) in their owning
records, not in these envelopes.

## Envelope and local check

Use one UTF-8 JSON object with integer `version: 1`, string `operation`, and
the fields listed for that operation. Unknown fields, duplicate keys, and
`null` are not allowed. Omit optional fields when unused. A reference or ID
is a non-empty printable string with no surrounding whitespace; its format and
resolution belong to the host. A revision is a nonnegative integer or a
non-empty reference string unless specified otherwise. Reference arrays may
be empty unless noted.

```sh
kit/scripts/check-stage-handoff --expect-operation execute tests/fixtures/stage-handoffs/execute.json
```

The checker reads one local file and exits 0 for valid shape, 1 for a read or
validation error, and 2 for incorrect command usage. Pass `--expect-operation`
when the receiver expects a specific operation, to reject even a correctly
formed handoff for a different operation. The checker does not resolve
references, access the network or SQLite, write files, or assess authority.
A valid shape is not proof that a reference exists, is current, agrees with
another reference, or grants any permission. Send references, never
credentials or live grant tokens.

The receiver reopens the authoritative inputs in its own scope. On an unknown
version, wrong operation, missing field, conflicting identity or unreadable
required reference, preserve the draft or stop the dependent step. This
contract does not turn unversioned legacy records into invalid payloads or
change what any existing skill runs.

## Setup or Evolve → Implement: `prepare`

Required: exactly one of `request` (original non-blank text) or `request_ref`
(immutable original request); `scope_ref` (selected repo or workspace scope);
`decision_ref` (decision ID, revision and basis);
`acceptance` (one or more non-blank criteria);
`dependency_refs`; `needed_route_refs` (evidence for only the still-needed
drafting routes).

Optional: compatible `spec_ref` and `ticket_ref`. A `ticket_ref` is an object
with `instance`, `namespace`, `id` (references), and `revision`.

`DesignReady` only marks the design ready to draft. Check artifact compatibility; if both
artifacts are missing, resolve `to-spec` then `to-tickets`. If only one is
missing, produce only that artifact. Drafting routes get no publication or
effect authority.

## Setup or Evolve → Implement: `publish`

Required: `draft_ref` (ID and revision), `target` (object with `instance`,
`namespace` and `role` references), stable deduplication `work_id`, and
`grant_ref` for this exact publish or update.

The checker validates shape only. Emit only for an exact draft revision with
the owner's decision on any material split (H6) and a separate exact publish
grant (H7). The receiver reopens the authoritative records under the
[publish gate](../skills/harness/harness-implement/WORK.md#publish-or-update).
Resolve split approval through the draft and decision; do not add approval
fields to the envelope or infer approval from `grant_ref`.

Use the selected Harness destination's own instance, namespace and role. A
selected local Harness record must be durable and readable by the receiver.
It is not a fallback after a tracker error. Never publish to Product or
switch destinations after an error. Read back the canonical ticket at the
selected destination. A timeout after send is `Unknown`; reconcile there
without resending.

## Coordinator → Implement: `execute`

Required: `request_ref`, `scope_ref`, `decision_ref` (including basis),
canonical `ticket_ref` (same object as in `prepare`), `assignment_ref`
(ID and epoch), `route_ref` (ID, resolved source, digest and caller),
`effect_ref` (exact proposed effect and its authority reference), and
`expected_target_revision`. Include `selection_ref` when the task uses a
Library selection.

Recompute `DispatchReady` from current dependency, claim, authority, destination
and route state. Use [route resolution](../skills/harness/harness-implement/ROUTES.md)
in the intended caller context. Do not invoke user-only routes on the user's
behalf or reuse preparation evidence as execution evidence. Apply the
[destination write gate](../skills/harness/harness-implement/WORK.md#write-boundary-and-reconciliation);
a grant reference is not a grant.

## Library → consumer: `selection`

Required: `store_ref`, `scope_ref`, `source` (`supplied` or `saved`),
canonical `id`, integer `selection_revision`, booleans `enabled`, `available`,
and `effective` (equal to `enabled` and `available`), and `evidence_refs` for
provenance. Include a `distribution_revision` for supplied content, or a
`content_revision` for saved content (which may be omitted if unavailable);
never use both. Include the snapshot `digest` for available supplied content;
the saved snapshot uses its content revision and does not require a digest.
Include `lineage_ref` or `hold_ref` when relevant.

Reread the [Library selection](LIBRARY.md) before applying it. A supplied
snapshot pins the catalog row, not the linked content: pin the template and
linked content to the same distribution revision. Selection is not adoption.

## Implement → Setup or Evolve: `result`

Required: `assignment_ref`, `target_ref`, `target_revision` (the observed
revision, or the expected revision if no observed one is known), `effect_id`
or `request_id` (or both), `outcome` (`Applied`, `Denied` or `Unknown`),
`receipt_ref` or `history_ref` (or both), `verification_refs`,
`evidence_refs` the recipient can open, and a non-blank `next_step`.

For `Unknown`, a history reference can point to the authoritative place to
reconcile; it does not imply a confirmed receipt. Do not replay, roll back or
reassign before reconciliation. The owner checks the assignment and acceptance
criteria before marking `Verified`, closing under separate authority, or
updating the decision map. Keep applied, verified, activated and measured
improvement separate.

## Setup or Evolve → Bot operator: `bot-setup`

Required: `instance_id`, pinned `template_ref` and `contract_ref`, `scope_ref`,
`adapter_ref` (adapter profile and caller), `configuration_ref` (observed
readback), `evidence_refs`, and `disabled_capabilities` (actual disabled
capability IDs from readback).

Emit only after an authorized change to a Bot target and actual configuration
readback, never for a repo-only change. The operator evaluates activation;
configuration and this handoff authorize no trigger. Read back the configuration,
exercise a permitted manual route and verify fresh-worker resume and deduplication
before obtaining a separate grant and reading back activation for each trigger.
