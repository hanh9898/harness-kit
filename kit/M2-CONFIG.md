# M2 target profile and runtime mode

These are two values in existing approved decision and host configuration
records, not new required files or a second registry. The decision owns the
target profile; the host owns effective runtime configuration. A host may
render JSON for interchange; update the authoritative record, not its render.
Do not add these fields to [stage handoffs](STAGE-CONTRACTS.md) or require an M2
file when consuming existing handoffs.

## Schema

JSON Schema 2020-12 in YAML 1.2's JSON-compatible form. Interchange values are
UTF-8 JSON. In addition to schema validation, the boundary must reject duplicate
keys and non-standard numbers (`NaN`, `Infinity`, `-Infinity`), require an
actual integer for `version` (not a boolean or float), and apply the stage
contract's non-empty, printable, trimmed reference rule to every ref and ID.
The schema describes shape; it does not resolve references or grant authority.

```yaml
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "oneOf": [
    {"$ref": "#/$defs/targetProfile"},
    {"$ref": "#/$defs/runtimeConfig"}
  ],
  "$defs": {
    "ref": {"type": "string", "minLength": 1},
    "targetProfile": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "version": {"const": 1, "type": "integer"},
        "target_profile": {"enum": ["repo-only", "bot-only", "repo-and-bot"]},
        "scope_ref": {"$ref": "#/$defs/ref"},
        "owner_ref": {"$ref": "#/$defs/ref"},
        "repo_ref": {"$ref": "#/$defs/ref"},
        "bot_ref": {"$ref": "#/$defs/ref"}
      },
      "required": ["version", "target_profile", "scope_ref", "owner_ref"],
      "oneOf": [
        {"properties": {"target_profile": {"const": "repo-only"}},
         "required": ["repo_ref"], "not": {"required": ["bot_ref"]}},
        {"properties": {"target_profile": {"const": "bot-only"}},
         "required": ["bot_ref"], "not": {"required": ["repo_ref"]}},
        {"properties": {"target_profile": {"const": "repo-and-bot"}},
         "required": ["repo_ref", "bot_ref"]}
      ]
    },
    "runtimeConfig": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "version": {"const": 1, "type": "integer"},
        "mode": {"enum": ["interactive", "persistent-bot"]},
        "scope_ref": {"$ref": "#/$defs/ref"},
        "instance_id": {"$ref": "#/$defs/ref"},
        "adapter_ref": {"$ref": "#/$defs/ref"},
        "checkpoint_ref": {"$ref": "#/$defs/ref"}
      },
      "required": ["version", "mode", "scope_ref"],
      "oneOf": [
        {"properties": {"mode": {"const": "interactive"}},
         "not": {"anyOf": [{"required": ["instance_id"]}, {"required": ["checkpoint_ref"]}]}},
        {"properties": {"mode": {"const": "persistent-bot"}},
         "required": ["instance_id", "adapter_ref", "checkpoint_ref"]}
      ]
    }
  }
}
```

## Target profile examples

For an ordinary repo request, default to `repo-only` and `interactive` unless
the existing caller mode is known. Do not ask Bot questions, load Inbox or
Memory, write to a store for this default, or emit a `bot-setup` handoff.
`repo_ref` identifies the repo, its Harness destination and Product location
if present; do not derive the destination from the current directory.

```json
{
  "version": 1,
  "target_profile": "repo-only",
  "scope_ref": "scope:docs",
  "owner_ref": "owner:maintainer",
  "repo_ref": "repo:docs/harness"
}
```

For `bot-only`, use the real workspace, owner and scope; no repo or Product
tracker is required. `bot_ref` identifies the selected configuration target
or creation intent (host, workspace and owner); read back the real instance
ID before treating a created instance as configured.

```json
{
  "version": 1,
  "target_profile": "bot-only",
  "scope_ref": "scope:editorial",
  "owner_ref": "owner:editor",
  "bot_ref": "bot-target:editorial"
}
```

Use `repo-and-bot` only if both targets are to change. `repo_ref` and
`bot_ref` must differ. Each target has its own binding, revision, grant,
effect and result. Block a dependent Bot change when its Repo prerequisite
has not been met. A Bot denial does not roll back independent Repo work.

```json
{
  "version": 1,
  "target_profile": "repo-and-bot",
  "scope_ref": "scope:docs-and-editorial",
  "owner_ref": "owner:maintainer",
  "repo_ref": "repo:docs/harness",
  "bot_ref": "bot-target:editorial"
}
```

## Runtime mode examples

Mode describes the caller, not the target. A Bot target can be designed or
tried interactively; an existing persistent Bot can work on a repo-only target
under its Repo authority without changing Bot configuration. The runtime
scope must match the decision scope or have a documented containment relation
covering the intended work; do not infer it from names.

```json
{
  "version": 1,
  "mode": "interactive",
  "scope_ref": "scope:editorial"
}
```

Until the durable instance ID, chosen adapter and checkpoint readable by a
worker with the correct ACL are verified, persistent mode is intent only.
Even effective `persistent-bot` does not activate any trigger.

```json
{
  "version": 1,
  "mode": "persistent-bot",
  "scope_ref": "scope:docs",
  "instance_id": "instance:docs-assistant",
  "adapter_ref": "binding:docs-worker@4",
  "checkpoint_ref": "checkpoint:docs-assistant"
}
```

## Route binding

The adapter reference points to an existing binding, not a second config
file. An `AdapterBinding` carries integer `version: 1`, `host` (`devin`,
`pi`, `claude-code` or `codex`), `scope_ref`, `caller_ref` and `routes`.
A `BoundRoute` contains:

| Fields | Contract |
| --- | --- |
| `capability` | One of `work-workers`, `inbox`, `memory`, `domain-targets`, `wake`, `evidence-write-gate`. No duplicate capability in a binding. |
| `mode`, `status` | Mode: `native`, `external`, `manual`, `unsupported`. Status: `verified`, `ambiguous`, `unavailable`. An unsupported route is unavailable and must not be called. |
| `target_ref`, `exact_id`, `source_ref`, `source_revision`, `digest` | Optional in an unselected route. A selected route requires target, exact route ID (or native identifier/command path), source and at least one revision or digest. Revision is a nonnegative integer or a reference. |
| `grantor_ref`, `precedence_ref` | Optional; record applicable grantor and precedence information for a route that writes. |
| `evidence_refs`, `missing_requirement` | Required evidence array; for unavailable routes name the missing requirement in non-blank text. |

Use printable trimmed refs/IDs as in the schema. Verify in the exact caller
and revision, separately for read, supervised write and unattended write.
Do not assume equivalence across hosts. Reverify affected evidence when the
binding, source, caller or target changes.

## Readiness and authority gates

| Transition | Evidence and authority required |
| --- | --- |
| Draft → DesignReady | Current approved decision/revision, basis, acceptance, dependencies and read/preparation authority. Allows `prepare`, not publishing or execution. |
| DesignReady → Published | Live grant for the exact draft and [Harness destination](STAGE-CONTRACTS.md), stable `work_id` and canonical ticket readback. Never fall back to Product. On timeout, look up the same work ID rather than sending again. |
| Published → DispatchReady | Reread the current decision, dependencies, exclusive claim/epoch, caller/source, applicable selections and bound authority. Readiness is derived from live state, never from parsing a handoff. |
| DispatchReady → Applied / Denied / Unknown | At commit, the destination checks authority, applicable claim/epoch, expected revision and effect. A prior read, process lock or tracker grant is not a substitute. If a required fence is missing, stop; only if policy allows a non-atomic route may an authorized person supervise and confirm each send, never unattended. A timeout after send is Unknown. |
| Unknown → Applied / Denied | Reconcile the exact effect using sufficient destination evidence (receipt, history or readback). Absence alone is not proof of no effect. Until resolved, keep the checkpoint and do not retry, roll back, republish, transfer the claim, advance the affected cursor or start a competing wake. Independent work may continue. |
| Applied → Verified → Closed | The owner checks the assignment, criteria and accessible evidence. Closing needs separate authority. Application, verification, activation and measured improvement are distinct. |
| Configured-disabled → Manual-qualified → Resume-qualified → Active | Read back configuration, run manually within authority, verify a fresh worker can resume and deduplicate, then obtain a separate grant and read back each enabled trigger. Keep unqualified routes disabled; missing offline access, ACL or fencing limits use to an approved manual route. Revocation disables the affected authority. |
| Active → Draining → Rebound-disabled | Confirm old triggers are off, wait for or fence old runs and reconcile Unknown effects before the owner rebinds and reads back. While draining, the new host only inspects or uses isolated fixtures. Never allow two hosts to send for the same scope. Keep the instance only if the approved original state is accessible; otherwise use a new instance after stopping the old one or separating scope. Do not import secrets, grants, transcripts or schedules. |

For wake deduplication, use `(instance_id, event_source_id, provider_event_id)`
or, if a schedule has no stable event ID,
`(instance_id, schedule_id, scheduled_utc_instant)`. Persist the occurrence
key and claim atomically in an approved existing record before acknowledging
delivery or advancing its cursor. Duplicate wakes reopen the same checkpoint
and receipt; do not advance the effect checkpoint before reconciliation. A
checkpoint carries `instance_id`, `occurrence_key`, `scope_ref`, optional
`assignment_ref`, `history_ref` and `receipt_ref`, and `next_step`. Keep the
dependent trigger off if uniqueness or the destination fence cannot be proven.

A deliberately unconfigured Library store permits catalog reads, not
effective selections. A configured store that is missing (including a broken
link), unreadable under read-only access or the wrong identity blocks only
dependent work. Only a ready store can supply selection and history; no row
there is valid revision zero. Do not silently fall back to unconfigured or
create a replacement store. Restore the selected binding or authorize and read
back a different one. Verify `store_ref`, `scope_ref`, `owner_ref`,
`canonical_target_ref` and `continuity_ref` using existing identity and
history; path or basename alone is insufficient. For local SQLite, use
owner-pinned real paths and same-host continuity evidence (such as device and
inode, plus the required revision/history), not a mutable database checksum
or an inode copied between hosts. Missing continuity requires owner
reconciliation. Check grant and revision at write time in the same verified
store. See [Library](LIBRARY.md) and [durable state](PERSISTENCE.md).
