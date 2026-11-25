# Library operations

The public entry is `harness-library`. `scripts/kit` retrieves supplied pieces, rules, patterns and delegation references unchanged. `scripts/library` adds focused search and safe local draft and selection operations for pieces, rules and workflows. Neither command applies resources to consumers.

Choose an existing suitable store first. For the local operation, pass an explicitly authorized SQLite file path with `--store`. Its parent must already exist. Project-governed stores should live in project-versioned storage when appropriate; commit or otherwise sync the store under the project's policy for continuation beyond the current machine. A local file alone does not survive disposal. Personal stores need an authorized durable personal location. No default silently writes outside the invoking project. Local SQLite is supported on a filesystem with working SQLite locks; remote filesystems and synchronization of independently edited database copies are unqualified.

```
<kit>/scripts/library --store <path> --require-existing-store search "focused term"
<kit>/scripts/library --store <path> save --input <resource.json> --expect-revision 0
<kit>/scripts/library --store <path> show report-facts
<kit>/scripts/library --store <path> history report-facts
```

`search` reads effective supplied pieces/rules and that one store, returns at most 12 summaries by default (`--limit` 1–50), and reports truncation. Narrow a truncated query; it is not proof that no reusable material exists. Use `kit list P` and `kit list delegation` for those references. `search --include-disabled` also exposes excluded matches with `enabled: false`; it is inspection, not restoration. Filtering precedes the result limit. `show` retrieves a saved resource by exact ID with its current selection state; supplied IDs use `kit show`. Read-only operations never create a store. Corrupt or inaccessible stores fail visibly rather than masquerading as empty results.

## Configured store reads

Before consuming Library results, resolve the authorized binding: store, scope,
owner, canonical target and continuity references. For local SQLite, compare
the resolved path and owner-pinned target plus same-host file continuity
(for example device/inode) and any required revision/history. Do not carry an
inode across hosts or use a changing database checksum as the store ID.

| Store state | Read behavior |
| --- | --- |
| `unconfigured` | Only when configuration confirms no binding: inspect the raw `kit` catalog. It is provenance, not effective selection. |
| `missing` | The configured path or symlink target is absent. Stop the dependent read. |
| `unreadable` | The target cannot be inspected or queried read-only. Stop the dependent read. |
| `wrong-identity` | The target exists but does not match the authorized binding, or continuity is unverified. Stop before consuming results, even if SQLite opens it. |
| `ready` | The binding matches and the strict read succeeds. A resource with no recorded selection can legitimately have revision 0 and empty selection history. |

Put the global flag `--require-existing-store` before `search`, `selection`
or `selection-history`. Missing or unreadable targets exit 2 with empty stdout
and a path to reconcile. Strict reads require a regular, initialized SQLite
file and reject WAL-mode stores, since SQLite may write sidecars even when
opened read-only. The flag does not verify identity or authority; the
consumer checks those separately. Other commands do not accept it.

Do not treat an invalid binding as unconfigured, create a replacement or fall
back to another path. Recover the original or verify an owner-authorized
rebind before proceeding. A moved or replaced file needs authoritative
continuity evidence; a matching filename or revision 0 is not evidence.
Without the flag, the legacy CLI still allows catalog-only results for a
missing path. Do not use that compatibility path for a configured store.

## Save input

Pass UTF-8 JSON as a file; use a JSON serializer, never shell interpolation of resource content. Duplicate JSON fields are rejected as ambiguous. This is a full resource replacement at an expected revision. Example of a valid unfinished rule:

```json
{
  "id": "report-facts",
  "name": "Identify unresolved report facts",
  "kind": "rule",
  "owner": "Report author",
  "scope": "personal",
  "content": "Before publication, name the owner of each unresolved fact. Check: each unresolved fact has an owner or a visible ownership gap.",
  "sources": [],
  "conditions": ["Human-reviewed reports; publication authority stays with the report owner"],
  "gaps": ["No representative report has been checked"],
  "origin": null,
  "evidence": [],
  "continuation": "Inspect a representative report and test the ownership check.",
  "decision": {
    "authority": "Reference to the actual user request authorizing this personal save",
    "rationale": "Retain useful incomplete guidance for reuse",
    "methods": ["Reference to the original writing-for-agents method actually loaded"],
    "standards": ["Applicable selected rule references"]
  }
}
```

Required operation facts are ID, name, kind (`piece`, `rule`, `workflow`), owner, scope, content, continuation and decision authority/rationale. Scope is `personal` or `project:<absolute project path>`. It is ownership metadata, not permission to edit that project. A source has `reference` and `certainty` (`stated`, `inferred`, `open`, `partial`); optional fields such as claim, accessed date or limitations are retained. `sources`, `conditions`, `gaps`, `evidence`, and decision `methods`/`standards` are lists. Empty lists permit incomplete drafts; record applicable gaps truthfully.

For customization, `origin` holds `reference`, `revision` and the exact `snapshot` used. If unknown, use null and record the missing basis as a gap. Existing origin, owner and scope stay stable during ordinary `save`; a checked `update` can advance origin. To create a differently owned/scoped derivative, use a new ID in the appropriate store, preserve the prior resource as its origin and obtain the actual grant. Additional JSON fields (for example dependencies, known uses and coverage, or research findings) are retained. Referenced consumers remain unchanged.

Warnings suggest repairs for missing sources/conditions/evidence and declared gaps. They do not reject a valid unfinished save or approve later use. The operation validates attributable records, not factual truth or semantic completeness. The host must check grants and applicability; supplying an authority string is not native permission enforcement.

## Conflict, failure and continuation

Creation expects revision 0; editing expects the revision read by `show`. A SQLite immediate transaction serializes writers. The revision comparison and append occur inside that transaction, retaining immutable prior content and decision history. Current content is the newest committed revision. No separate current-file/history write can partially succeed. SQLite journaling and full synchronous commits provide the local transaction boundary; this is not a distributed storage guarantee.

For unavailable persistence or uncertain writes, follow [persistence recovery](PERSISTENCE.md) before selecting another destination or retrying. An inaccessible existing store is not a new empty library; retain its logical identity and unresolved outcome.

On conflict, reread `show`/`history`, reconcile meaning and retry only with the newly inspected revision. On interruption or uncertain output, inspect the live store before retrying. If the requested change already committed, retain it; do not append an identical retry. A persistence error reports no success; check live state before choosing an authorized qualified alternative. Readback is separate from commit, so missing readback does not prove the write failed.

Content, decision references, evidence and continuation commit together. Their fields may reference an existing authoritative decision record for required pre-action facts. Keep consumer application and outcome evidence in the consumer's records. Known-use coverage is limited to inspected records; no global inventory is implied. The local operation does not garbage-collect history. Shared promotion uses adequate native stores and the existing project-scoped save operation under the [promotion contract](../skills/harness/harness-library/PROMOTION.md); the CLI supplies persistence, not a grant or maintenance acceptance.

For later consumer adoption or legacy upgrade, evolve's [adoption procedure](../skills/harness/harness-evolve/ADOPTION.md) reconciles the actual targets, contracts and grants. A saved content or selection revision is not per-target application evidence.

## Guarded writes

Use a guarded store for automated writes whose authority can be withdrawn. A trusted caller with authority to manage grants issues one against the **target store**, after inspecting the target revision and approving the exact input file. The first successful `grant-write` creates or enables guarding on that store. Existing stores that never enabled guarding keep their prior CLI behavior. A guarded store always requires a grant for `save`, `update`, `disable` and `restore`, even when no active grants remain. Reads are unchanged.

```
<kit>/scripts/library --store <path> grant-write disable reread-source-before-write --source supplied --input <decision.json> --expect-revision 0 --ttl-seconds 60
<kit>/scripts/library --store <path> disable reread-source-before-write --source supplied --input <decision.json> --expect-selection-revision 0 --write-grant <write_grant>
<kit>/scripts/library --store <path> revoke-write <write_grant>
```

`grant-write` returns JSON with `write_grant` (the ID to pass to the mutation) and `expires_at` (UTC). Use `--source saved` for content operations. The grant's `--expect-revision` is the selection revision for `disable` and `restore`, and the content revision for `save` and `update`. The grant matches the store, operation, source, exact resource ID, expected revision and input bytes. Issuing another grant for the same operation, source and ID invalidates the old grant. Choose a short lifetime between 1 and 86400 seconds; expiry uses the local clock.

To cancel before the worker writes, use `revoke-write` against the same store with the original grant ID. An old ID cannot revoke its replacement. The mutation checks and consumes the grant in the same SQLite write transaction that compares the revision and appends history. If revocation commits first, the mutation fails with no history change even if its revision is still current. If the mutation commits first, revocation does not undo it. A rolled-back transaction does not consume the grant; when the outcome is uncertain, inspect history before retrying.

This is a local guard for calls through the current Library CLI, not an authentication or permissions boundary. The host must establish who may issue or revoke grants, confirm the route and supplied catalog, and prevent workers from bypassing the CLI or issuing their own grants. An upstream claim or decision changing does not revoke a grant here: revoke it at the target. Do not rely on this guard for older CLIs, raw SQLite writes, independent database copies or non-Library targets.

## Exclusion and explicit restoration

Selection is an overlay in the authorized store, separate from supplied files and saved content revisions. Its identity is `(source, exact resource ID)` in that store: `supplied` denotes this harness-kit catalog, `saved` denotes this store's draft. Matching ID strings in the two sources remain independent. Replacing or moving the supplied distribution, saving or updating content (including parent replacement and carry-forward), or temporarily removing and reintroducing a supplied ID does not clear its exclusion. Keep the authoritative store when updating the distribution. Copying/resetting a store is not a distribution update.

```
<kit>/scripts/library --store <path> --require-existing-store selection reread-source-before-write --source supplied
<kit>/scripts/library --store <path> disable reread-source-before-write --source supplied --input <decision.json> --expect-selection-revision 0
<kit>/scripts/library --store <path> --require-existing-store selection-history reread-source-before-write --source supplied
<kit>/scripts/library --store <path> restore reread-source-before-write --source supplied --input <decision.json> --expect-selection-revision 1
```

Use exact IDs for supplied pieces, rules, patterns (`P6`) and delegation references (`axis1`, `step2`, `combine`), or saved pieces/rules/workflows. Selection commands accept `--kit-dir` to inspect a supplied distribution elsewhere. `kit list/show` remains a raw catalog/provenance interface and has no store context; before selecting a directly retrieved resource, check `library selection` in the intended store. Excluded material remains inspectable for history, comparison and explicit restoration. `enabled` reflects the stored choice, or the default if no choice exists (false during a rename hold); `available` describes whether the current resource exists; `effective` requires both. Neither effective selection nor restoration establishes qualified use or consumer adoption.

Selection JSON contains `owner`, `scope`, `decision`, `evidence` and `continuation`, with the same types and authority rules as saves. Include additional context, alternatives, known-use coverage and pre-action record references as applicable. For example:

```json
{
  "owner": "Report author",
  "scope": "personal",
  "decision": {
    "authority": "Actual request authorizing exclusion in this store",
    "rationale": "Keep this hook out of future library selection",
    "methods": [],
    "standards": ["kit:6.09"]
  },
  "evidence": [],
  "continuation": "Retain exclusion through supplied updates; restore only on explicit request."
}
```

Inspect `selection` and `selection-history` first. Changes compare `--expect-selection-revision` inside an immediate transaction; this revision is independent of content revision. A first disable expects 0. Each change appends its decision, scope, owner, observed source snapshot and timestamp atomically with the effective choice. Supplied snapshots retain their source fields and a content digest; saved snapshots retain the inspected content revision and origin. Restoration appends the current snapshot, preserving every prior disable/restore record and all content history. Owner/scope cannot silently change within that selection identity. Authority strings document grants; the host must establish actual authority before calling the operation.

A stale revision or request for the already-recorded state fails without a duplicate history entry. On uncertain output, inspect the live choice/history and requested effect before retrying. Missing resources cannot be disabled/restored; an existing exclusion remains effective if a resource disappears and returns. Inaccessible/corrupt stores fail visibly. Compatible content updates and selection writes serialize in the same SQLite store but touch separate histories, preserving independent work. This proves local operation behavior, not synchronization between independent database copies.

### Upgrading from letter-number piece IDs

The shipped catalog declares the old IDs in `piece-aliases.csv`. For supplied pieces, reads such as `selection H14` resolve to the slug `reread-source-before-write` and retain its existing selection revision and decision, even if the supplied content has changed. No migration command or database rewrite is needed. Historical records and snapshots retain the IDs they were written with; new records use the slug and continue the same history.

Keep alias rows when retiring pieces: the slug still reads the old history while the piece is unavailable. New records for mapped pieces use the old SQLite key so a catalog from before the slug upgrade sees the same exclusion.

Use the slug for writes and issue a fresh grant for that exact slug and current revision. For a custom catalog, pass the same `--kit-dir` when issuing the grant and writing. Old-ID grants do not authorize slug writes. Saved resource IDs and their origins are unchanged. If a custom catalog already recorded separate choices under both IDs, the library refuses to choose between them; inspect both streams with `selection-history` before reconciling the conflict.

### Renaming an excluded supplied piece or rule

If a new ID has no selection record, the CLI holds it out of selection when all other CSV fields exactly match the latest disable snapshot of a now-absent ID of the same kind. `selection` and `search --include-disabled` show `enabled: false` and `possible_previous_ids`; the hold writes no history. It identifies candidates, not proven lineage. A same-content copy does not trigger the hold while the earlier ID is still present.

Verify the rename in the catalog source and record that evidence in the decision. To confirm `previous-hook` as the predecessor, add the top-level field `"confirm_rename_from": "previous-hook"` to the disable input and use the predecessor's owner and scope:

```
<kit>/scripts/library --store <path> disable replacement-hook --source supplied --kit-dir <renamed-kit> --input <decision.json> --expect-selection-revision 0
```

The new ID starts its own exclusion history with an `inherit-disable` record pointing to the predecessor revision; the old history is unchanged. After confirmation, later content edits do not clear the exclusion, and only an explicit restore on the new ID re-enables it. A predecessor revision can be confirmed once. A plain `disable` records an independent decision, not lineage. The CLI cannot recognize a rename if any non-ID fields differ from the disable snapshot: reconcile ID-only changes first, or explicitly disable the replacement before using it. No lineage is inferred across sources, stores, or distributors, or for Markdown resources.

After changing selection, read it back and inspect actual changed/unchanged scope. Applied consumers remain unchanged; report only inspected known uses and coverage. Record continuation in the same authorized durable store and retain it under the project's storage policy. Restoration selects the currently available resource for future use; it does not roll content back or apply it anywhere.


## Origin comparison and updates

```
<kit>/scripts/library --store <path> compare <id> --candidate <origin.json>
<kit>/scripts/library --store <path> update <id> --input <plan.json> --expect-revision <inspected-revision>
```

Candidate JSON contains `reference`, `revision` and exact `snapshot`, like `origin`. A snapshot is the complete text of the selected resource or assembly, including its selected child contents. The operation does not follow child file links or modify referenced resources. Additional resource fields remain metadata; stores that model active children outside `content` need their own qualified replacement operation.

`compare` is read-only. It returns the exact old origin (or null), current customization, candidate, three textual diffs, missing-basis unknowns and `semantic_compatibility: unchecked`. Its token binds the entire saved resource/revision and candidate. It never infers semantic compatibility from textual non-overlap. The host reads the source/contract and checks meaning. Origin snapshots and review claims are attributable caller assertions, not independently authenticated facts.

`diffs.selection_to_candidate` compares the saved customization (labeled `selection`) against the candidate even when the old origin is unknown. The two diffs against the old origin are null when that origin is unknown.

An update plan has these fields:

```json
{
  "candidate": {"reference": "source:report", "revision": "v2", "snapshot": "Review facts.\nPublish monthly.\n"},
  "comparison_token": "token returned by compare",
  "mode": "update",
  "outcome": "complete",
  "content": "Linh reviews facts.\nPublish monthly.\n",
  "review": {
    "summary": "Reviewer and cadence remain compatible under the inspected report contract.",
    "checks": ["contract.md: Linh is authorized for monthly fact review; checked both requirements against proposed content"],
    "compatible_changes": ["Monthly cadence; retained Linh review"],
    "conflicts": [],
    "unknowns": [],
    "prior_selection_valid": true
  },
  "decision": {"authority": "Actual scoped update request reference", "rationale": "Adopt compatible origin changes", "methods": ["Original writing-for-agents actually loaded"], "standards": ["Selected report contract"]},
  "continuation": "Inspect the saved selection; consumer adoption and representative use remain separate."
}
```

`mode: update` accepts `complete`, `partial` or `blocked`. Complete requires an intact basis, checked compatible changes and no unresolved conflicts/unknowns; it advances origin. Partial requires independent compatible changes plus unresolved issues and a valid retained selection; it keeps the old origin and saves the pending candidate in `origin_update.comparison`. Blocked keeps content unchanged and records unresolved work; an invalid prior selection reports blocked consumption. Missing historical basis is always retained in the comparison, even if the caller omits it from review unknowns. Existing conditions, gaps, sources, ownership, scope and other metadata are preserved; review checks are additional evidence, not a claim that old gaps disappeared.

`mode: replace-parent` requires `complete` with content exactly equal to the candidate snapshot. It can select an independently checked new assembly even with unknown prior origin. It advances origin and retains the old selection in history without transplanting old child edits. A different source reference also requires this deliberate replacement mode. Known-use metadata remains a coverage-limited reference, not adopted consumer state.

`mode: carry-forward` requires `complete`, the exact current origin as candidate, and `carry_forward` containing `from_revision` (an earlier saved revision), `customization` (an exact historical excerpt), `target` (an exact excerpt identifying the target in the new origin), and `contract_check` (actual compatibility evidence/reference). The operation verifies historical and target existence; the host checks that proposed content carries the intended customization and preserves the rest of the new assembly. Semantic conflicts block carry-forward. Record such a blocker with `mode: update`, unchanged content and a precise continuation.

Updates use the same immediate transaction and expected revision protection as saves. Token verification, review validation, historical checks, content, decision and continuation commit atomically as one new revision. `origin_update` stores the full comparison, assessment, prior revision and requested carry-forward provenance. On a stale token/revision, missing target, invalid review or persistence failure, inspect live state and reconcile; no successful update is claimed. Read `show` and `history` after uncertain responses before retrying. No operation grants authority or writes to consumers, user configuration or other stores.



## History maintenance and archival

For material corrections, competing contributions, archival and scoped cleanup,
follow [record maintenance](MAINTENANCE.md). Existing save/history transactions and
selection operations supply local persistence; the host checks the meaning of
correction links, ownership, retention and actual references. Archival through
explicit exclusion keeps content and histories inspectable. No CLI operation
purges history or deletes consumers; a preview is not a disposal grant.
