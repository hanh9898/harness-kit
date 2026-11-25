# Read and verify reusable resources

Identify the relevant authorized store, owner and scope. Personal, project
and shared scopes are distinct, even when they refer to the same catalog.
Confirm the actual consumer and distribution/revision, not the invoking
checkout by default. Report unreadable or unverified stores as such. Do not
create a store for discovery. If current configuration confirms that no store
is configured for the requested scope, report that condition separately from
an unreadable store or an unverified scope. Inspect only supplied provenance
without a store and report that selection was not verified.

Resolve the skill's real directory; `library` and `kit` below mean the
executables in `<skill-dir>/../../../kit/scripts/`, not assumed PATH entries.
For an inspected store, use `library --store <selected-path> search <term>`:
text matching is literal, not semantic. Narrow queries on truncation; an
empty result proves nothing beyond that scope. Open only useful candidates via
`kit show` for supplied resources or `library show` for saved resources.
Use targeted `kit list <group>`, `kit list rules <topic>`, `kit list P` or
`kit list delegation` for summaries where relevant. The group index classifies
resources, not discovery nodes. Raw kit output is provenance, not evidence
of current selection.

For [Bot role templates](../../../kit/README.md#bot-role-templates), look up
the exact role by slug or use the literal query `bot role template` with
`--limit 30`. Open only the selected role section and its portable contract
as needed, from the pinned distribution revision. The selection snapshot
covers the catalog row, not the linked instructions. Treat both pieces as
guidance, not installed Bots, grants, schedules or proof of host readiness.

For a supplied resource use `library --store <selected-path> selection <id> --source supplied`.
If the pinned distribution is not the bundled one, add
`--kit-dir <pinned-catalog>` pointing to its verified kit directory. Do not
use the bundled catalog as a fallback. Use `--source saved` for saved resources.
Check effective state, source, exact ID and revision (content or catalog
revision and selection revision as applicable); open scoped history only
as needed. The same ID in `supplied` and `saved` means distinct resources.

## Selection handoff

Use the live read in the consumer's authorized store and scope. Return a v1
[`selection`](../../../kit/STAGE-CONTRACTS.md#library--consumer-selection)
with `store_ref`, `scope_ref`, the CLI's `source` and canonical `id`,
`revision` as `selection_revision`, and the observed `enabled`, `available`
and `effective` (`enabled` and `available`) state. Include `evidence_refs`
for the readback and provenance plus `lineage_ref` or `hold_ref` when relevant.

| Source | Revision and snapshot evidence |
| --- | --- |
| `supplied` | Use the revision of the catalog actually read as `distribution_revision`. For an available snapshot from that same read, use `current_snapshot.sha256` as `digest`. |
| `saved` | Use `current_snapshot.revision` as `content_revision`; omit it if unavailable. A saved snapshot does not require a digest. |

Keep selection revision separate from content/distribution revision. A supplied
CSV snapshot covers the row, not linked content; pin the template and linked
content to the same distribution revision. If store, scope, revision or
identity is unverified, return the blocker rather than guessing a handoff.
A possible rename is a hold, not proof of lineage.

The consumer must reread the live selection before application. Disabled,
unavailable or unreconciled choices do not confer permission to use raw catalog
content. Return source evidence and its limits, not approval, applied state
or a claim about the current external consumer inventory.

## Lineage

During a known or suspected catalog, ID or source migration, use attributable
source history or an authorized confirmed mapping. Never infer lineage merely
from the same ID, name, text or CLI default. If identity may have moved and is
not reconciled, return unverified for that candidate, even if the new ID appears
enabled. Do not block unrelated verified candidates. A verified equivalent must
retain the old exclusion in the same authorized scope; never auto-restore.

For the [shipped piece-slug upgrade](../../../kit/LIBRARY.md#upgrading-from-letter-number-piece-ids),
the catalog's explicit alias resolves to one selection stream even after content
edits. Read the live selection via the slug and use it for writes and grants.

The [supplied rename guard](../../../kit/LIBRARY.md#renaming-an-excluded-supplied-piece-or-rule)
only holds exact ID-only supplied piece/rule matches to absent predecessors in
the **same store**. `possible_previous_ids` is evidence of a hold, not proof
of identity. Confirm the predecessor from source evidence and inspect its
selection/history. With explicit authority to record the migration, use
`disable` on the replacement with a top-level `confirm_rename_from` equal
to the exact predecessor ID and preserve predecessor owner/scope. Use the live
replacement selection revision and the [write guard](WRITE.md#write-guard).
Read back `inherit-disable` and its predecessor/revision, the replacement's
ineffective selection and the unchanged old history. Keep the candidate
unselectable without authorization to record the migration.

The CLI does not infer lineage for non-ID edits, across sources, across stores
or across distributors, or for Markdown resources. Where the CLI confirmation
is unsupported, keep a known or suspected replacement out of selection until
an authorized equivalent exclusion is recorded and verified in the intended
scope; for a verified replacement this may be an explicit authorized disable
with separate lineage evidence, not a claimed CLI inheritance. Keep the
predecessor history. Restoring requires explicit authority for the current
identity, and does not apply it to a consumer.
