# Columns of legos.csv

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
