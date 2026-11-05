# Kit

Read-only store of lego pieces for building an agent harness, plus the rules, team patterns and delegation framework that go with them. Terms (harness, record, rung) are defined once, in the project's harness glossary; this kit only adds the ones below.

**The CSV files are the source of truth.** Edit `legos.csv` and `rules.csv` directly. They were generated once from research reports; nothing regenerates them, and the generator refuses to overwrite them (see "Where the data came from").

## Vocabulary

- **Lego**: one row of `legos.csv`.
- **Rule**: one row of `rules.csv`, a checkable instruction with its source.
- **Pattern**: one row of the table in `patterns.md`, a way to shape a team of agents.
- **Rung**: how heavy a piece is. One of `instruction-file | skill | script-cli | mcp`, lightest first. The values are the English forms of the four rungs: instruction file, skill, script or CLI, MCP.
- **Certainty**: how well sources support a row. One of `stated | inferred | open | partial`.
  - `stated`: a source says it in so many words.
  - `inferred`: the research drew it from sources that do not say it directly.
  - `open`: not checked, or sources disagree.
  - `partial`: support comes from a source that was read only in part. A row with such a source is never marked higher than `partial`.
- **Verified on**: date a rule was last re-checked against its source. Empty until someone checks it.

## Files

| File | What it holds | Rows |
|---|---|---|
| `legos.csv` | Pieces, 14 groups (columns in [COLUMNS.md](COLUMNS.md)) | 162 |
| `rules.csv` | Rules for skills, agent documents, prompts, configuration, workflow, tools, testing | 211 |
| `patterns.md` | Team architecture patterns | 14 |
| `delegation.md` | Delegation framework: four axes and a seven-step scale, all `partial` | 4 axes, 7 steps |

Row counts differ from the first plan in one place (14 patterns, not 13); see `docs/generation-notes.md` at the repository root.

Groups: A Intake, B Knowledge and context, C Agent behavior, D Enforcement and safety, E State and progress, F Tools and connections, G Communication and coordination, H Check and measure, I Learn and improve, J Operations and schedules, K Team organization and distribution, L Environment and isolation, M Observation and interface, N Written output and writing standard.

In `sources`, `note:R24` means "research note 24", an internal note, not a link. `practice:` means the piece is supported only by observed use. In `rules.csv`, a bare source id such as `K08` is the id used in the research; most carry a link next to them.

## Look something up

```
scripts/kit list            # groups and piece counts
scripts/kit list A          # one line per piece in group A
scripts/kit show B01        # one piece in full, by id or exact name
scripts/kit list P          # team patterns, one line each; scripts/kit show P6 for one
scripts/kit list delegation # four axes and seven steps, one line each
scripts/kit show axis1      # one axis; step3 for one step; combine for how the axes combine
```

There is no command that prints the whole store, on purpose. Ask for a group, then a piece. Rules have their own commands: `kit list rules` (gate rules only), `kit list rules <topic>`, `kit show <rule id>` (for example `4.06`). Do not load `rules.csv` whole.

## Where the data came from

A one-time script, `skills/harness/harness-evolve/scripts/generate_kit.py`, read the research reports and wrote the four data files. Numbers, ids, certainty and source links are parsed from the reports. The free text was Vietnamese, so it was translated by hand block by block into `skills/harness/harness-evolve/scripts/seed/`; the script stops if a seed block does not match a report id or count. Run it again only into an empty directory:

```
python3 skills/harness/harness-evolve/scripts/generate_kit.py --reports <reports dir> --dest <new dir>
```

It refuses to write if any output file already exists, so a hand-edited kit is never replaced.

## More

- Columns and rules for editing the CSV: [COLUMNS.md](COLUMNS.md)
- Checks (run from the repo root): `python3 -I tools/check_kit.py`, `python3 -I tools/check_boundary.py --strict`, `python3 -m pytest`
