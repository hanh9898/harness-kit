# Resource formats

## Topic hierarchy and assignments

`categories.csv` contains `id,parent,name`. Root identifiers are `01` through `05`; leaves use identifiers such as `1.3` and name their root in `parent`. Root rows have an empty parent. Resources are assigned to leaves.

`catalog.csv` contains `kind,id,category,rationale`. The pair `kind,id` identifies one source resource; each source resource has exactly one primary category. A rationale explains the semantic fit without changing the resource's evidence or provider scope. Pieces use `lego`, numbered team patterns use `pattern` with identifiers such as `P6`, and delegation entries use `delegation` with `axis1`, `step3`, or `combine`. Rules use `rule`; richer resources use their declared kind.

## Guides and workflows

`resources.json` is an array of resource objects. Each object carries:

- `id`: stable lowercase slug; `kind`: `guide`, `workflow`, `rule`, or `piece`.
- `name`, `summary`, `when_to_use`: identity, purpose, and applicability.
- `prerequisites`, `instructions`, `applicable_standards`, `verification`: arrays describing the resource contract.
- `sources`: primary-source URLs; `certainty`: `stated`, `inferred`, or `partial`.
- `checked_on`: date the documentation was checked; `host_scope` and `limitations`: applicability and evidence limits.

Category assignments live only in the catalog. Verification arrays are instructions for checking the resource, not evidence that those checks have run. Core catalog validation checks references, unique identifiers, assignments, and field structure; content quality still requires review.

## Columns of legos.csv

| Column | Meaning |
|---|---|
| id | Unique. Group letter plus a number, for example `B01`. |
| group | Group letter. |
| name | Short name. `show` also accepts it, case-insensitive. |
| summary | One sentence: what the piece is. |
| needed_when | One sentence: the situation that calls for it. |
| rung | `instruction-file`, `skill`, `script-cli` or `mcp`. |
| certainty | `stated`, `inferred`, `open` or `partial`; see the README. |
| sources | Where the claim comes from. |
| detail | How to use it. Only `show` prints this. |

Every cell is required. `tools/check_kit.py` reports missing columns, empty cells, a rung outside the four values, and duplicate ids.

The kit names no project. `boundary-tokens.txt` at the repo root lists the forbidden strings; keep it outside `kit/` so the kit stays clean. `tools/check_boundary.py` reads it.

## Columns of rules.csv

| Column | Meaning |
|---|---|
| id | Unique, standard number and rule number, for example `4.07`. |
| topic | `skill-writing`, `agent-docs`, `prompts-and-roles`, `configuration`, `workflow`, `tools-and-cli` or `testing-and-review`. |
| rule | The rule, one or two sentences. |
| source | Source ids with links, separated by ` | `. |
| certainty | Same four values as `legos.csv`. |
| check | `machine`, `review` or `machine+review`: how the rule can be checked. |
| verified_on | Date of the last re-check against the source page. Empty until checked. Only gate rules carry it. |

## Columns of gates.csv

One row per rule proposed as a gate (a check the harness may rely on). A rule is a gate only when its row says `gate=yes`.

| Column | Meaning |
|---|---|
| id | A rule id from `rules.csv`. |
| gate | `yes` or `no`. |
| verify_method | `raw-grep` (raw page fetched with curl, tags stripped, exact sentence searched; whitespace and backticks ignored), `webfetch` (summary by a small model; not enough for a gate) or `unreadable`. |
| verified_quote | The sentence copied from the source page. Separate several with ` | `. |
| note | Source page, what differed, and limits. Required when `gate=no`. |

A `gate=yes` rule needs `certainty` = `stated`, a `verified_on` date in `rules.csv`, a non-empty `verified_quote` and `verify_method` = `raw-grep`. A rule that does not match is set to `gate=no`, its `certainty` is lowered and its `verified_on` stays empty. `tools/check_kit.py` enforces this when `gates.csv` exists.
