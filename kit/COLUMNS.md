# Columns of legos.csv

| Column | Meaning |
|---|---|
| id | Unique. Group letter plus a number, for example `B01`. |
| group | Group letter. |
| name | Short name. `show` also accepts it, case-insensitive. |
| summary | One sentence: what the piece is. |
| needed_when | One sentence: the situation that calls for it. |
| rung | `instruction-file`, `skill`, `script-cli` or `mcp`. |
| certainty | How well the sources support the piece. |
| sources | Where the claim comes from. |
| detail | How to use it. Only `show` prints this. |

Every cell is required. `tools/check_kit.py` reports missing columns, empty cells, a rung outside the four values, and duplicate ids.

The kit names no project. `boundary-tokens.txt` at the repo root lists the forbidden strings; keep it outside `kit/` so the kit stays clean. `tools/check_boundary.py` reads it.
