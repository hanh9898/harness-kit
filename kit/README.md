# Kit

Read-only store of lego pieces for building an agent harness. Terms (harness, record, rung) are defined once, in the project's harness glossary; this kit only adds the ones below.

- **Lego**: one row of `legos.csv`.
- **Rung**: how heavy a piece is. One of `instruction-file | skill | script-cli | mcp`, lightest first. The values are the English forms of the four rungs: instruction file, skill, script or CLI, MCP.
- `legos.csv` is the source of truth. Edit the CSV; nothing regenerates it.

## Look something up

```
scripts/kit list            # groups and piece counts
scripts/kit list A          # one line per piece in group A
scripts/kit show B01        # one piece in full, by id or exact name
```

There is no command that prints the whole store, on purpose. Ask for a group, then a piece.

## More

- Columns and rules for editing the CSV: [COLUMNS.md](COLUMNS.md)
- Checks (run from the repo root): `python3 -I tools/check_kit.py`, `python3 -I tools/check_boundary.py --strict`, `python3 -m pytest`
