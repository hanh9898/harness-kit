# RFC 006: Optional pinned verification methods

**Status:** Proposed with implementation. **Baseline:** `main` at `81ba733`.

## Problem and decision

Verification discovery should find a relevant method without installing a
skill or suggesting every result of a literal search. The prototype's
predicate index returned exactly the expected 0, 2 and 1 IDs on the three
primary fixtures. Its nine cases used human-labeled facts; this does not
measure host fact extraction or method effectiveness.

Distribute `packs/verification-methods/` independently of the core `kit/`
catalog. A consumer explicitly enables it with a Library binding that pins its
index bytes. Never import it into core search, an install inventory, or a
default discovery entry. Use the existing Library selection ledger, not a
second database or a directory of host skills. Present neutral capability
names. Keep upstream identity in the index's validated provenance, not in
the discovery or browse output.

| Stable ID | Display name | Suggest only when |
| --- | --- | --- |
| `opt-blind-comparison` | Blind comparison with one rubric | Comparing variants requires subjective grading and is not fully objective. |
| `opt-shared-premise-probe` | Test the shared premise before another fix | At least two fixes fail the same gate and rest on a demonstrated common assumption. |
| `opt-formal-model-resync` | Resync a formal model to covered code | An existing formal model covers code changed since its recorded sync. |

Browse any effective method individually or use the **Eval comparison** and
**Formal model checking** scenario views. A scenario references the same IDs;
choosing a scenario does not enable its members or bypass their predicates.

## Index and binding contracts

The UTF-8 JSON index has exactly `schema: 1`, `scenarios` and `items`.
The maps have distinct kebab-case keys; item IDs start with `opt-`. Each
scenario has `name` and a nonempty array of distinct `ids` present in
`items`. Every item belongs to at least one scenario. Each item has:

| Field | Contract |
| --- | --- |
| `name`, `summary`, `needed_when` | Nonempty single-line text, free of upstream branding. |
| `kind` | `playbook` or `principle`; both are read-only instruction files, not execution routes. |
| `node` | Exactly `Verification & feedback`. |
| `all`, `none` | Distinct known fact strings; `all` is nonempty. The lists do not overlap. |
| `body_sha256` | Lowercase SHA-256 of raw UTF-8 bytes at `guidance/<id>.md`; no arbitrary path in the index. |
| `provenance` | Exactly `url` and `license`; a canonical HTTPS GitHub blob URL with a full lowercase commit and safe path segments; license `MIT`. |

Allowed facts: `compare-variants`, `subjective-grading`, `fully-objective`,
`repeated-same-gate`, `shared-assumption`, `formal-model-exists`, and
`covered-code-changed`. A confirmed user need or static observation supplies
each fact. Unconfirmed required facts are absent. A method matches when the
node is exact, all required facts are present, and none of its exclusions are
present. Scenario grouping operates on the already filtered IDs.

The explicit Library binding is UTF-8 JSON: `schema: 1`, nonempty `owner`
and `scope`, plus these exact objects:

- `store: {path, device, inode}` is the authorized canonical SQLite target
  and same-host file identity. The CLI's `--store` must resolve to that target.
- `catalog: {path, files}` is the verified absolute core `kit/` path and a
  SHA-256 map for exactly `legos.csv`, `rules.csv`, and `piece-aliases.csv`.
  The host verifies the core distribution revision before recording these pins.
- `pack: {path, index_sha256}` is the verified absolute pack path and its
  exact index SHA-256. The index commits to every body digest.

Reject duplicate or unknown fields, malformed data, and pin mismatches.
Paths must be absolute and canonical in the binding; validate pins against
the bytes used. Reject IDs that collide with core pieces, rules or aliases.
Never follow symlinked pack entries. Body bytes are read and verified only
on a selected open. Pack changes or moves require a newly reviewed binding;
keep stable IDs so existing exclusions survive a reviewed update. A
consumer without a pack binding is unaffected by a broken pack.

## Library and discovery flow

1. Pass the consumer's verified binding as `--pack-binding FILE` before
   `pack-discover --node NODE [--fact FACT ...] [--view methods|scenarios]`.
   No binding means zero suggestions without touching the pack or store.
   A supplied but invalid binding fails closed with exit 2 and no stdout.
2. Read effective selection for candidate IDs in one existing strict
   read-only SQLite transaction. Compare the bound store identity and stored
   record owner/scope. Disabled or wrong-scope records never become usable
   suggestions. No raw-catalog fallback, SQLite sidecar, or new store.
3. Use `pack-browse [--view methods|scenarios] [--scenario ID]` for explicit
   browsing without trigger facts. Browse and discover return `total`,
   `matches` and `groups`; groups reference method IDs, not copies. Use
   `pack-show ID` to recheck selection and read only that ID's verified body.
   None of these commands applies or installs guidance.
4. Use the existing exact `selection` or `selection-history` with
   `--source supplied` and the same binding for readback. Only separately
   authorized `disable` / `restore` and matching `grant-write` can mutate the
   existing ledger, with the exact ID, scope and revision. Pack grants also
   bind the binding bytes. The first grant enables the existing store-wide
   guard; discovery never issues a grant. No schema migration.
5. Setup's pass-one verification topic can ask Library about that node
   after the existing caller and prerequisite checks. No changes to pass order,
   H gates, Evolve routing, default skills, adoption, wake, ACK or dispatch.

## File whitelist and strict checks

| Scope | Allowed additions or edits |
| --- | --- |
| Design and caller | This RFC, `kit/LIBRARY.md`, `skills/harness/harness-library/{READ,WRITE}.md`, `skills/discovery/verification-discovery/SKILL.md` |
| Runtime | `kit/scripts/library`, `kit/scripts/method_pack.py`, `kit/scripts/piece_ids.py` |
| Pack | `packs/verification-methods/index.json`, `LICENSE`, and exactly three `guidance/<id>.md` files named above |
| Gates | `tools/check_method_pack.py`, `tests/test_library_method_pack.py`, `.github/workflows/v1-guard.yml` |

Keep `tools/check_boundary.py --strict` and its token list unchanged for
core. Check the pack separately. First validate its exact file inventory,
schema and digests, including a digest of the reviewed provenance map for
the three shipped IDs. Scan the license, guidance bodies and decoded index
keys and values, omitting only the validated and allowlisted
`provenance.url` values. Do not normalize display content, paths or body
text. In a second temporary view,
map methods to ordinary catalog rows and use `check_kit.py` to catch
invalid rows and collisions. Neither temporary view ships or becomes a
runtime catalog. A pack path is not a boundary exemption.

Required gates: full pytest, core `check_kit.py --dir kit`, isolated
`python3 -I tools/check_boundary.py --strict`, `skill_budget.py`, the pack
checker, and the GitHub `v1-guard` and Devin Review checks. Cover the nine
prototype inputs, both views, exact body open, malformed pins and boundaries,
scoped disable/restore, and byte-for-byte no-write checks for ready, missing
and WAL stores. Do not claim host fact extraction, native ACL enforcement or
non-Linux support from these local fixtures.
