# Kit

Supplied store of lego pieces for building an agent harness, plus the rules, team patterns and delegation framework that go with them. Terms (harness, record, rung) are defined once, in the project's harness glossary; this kit only adds the ones below.

**The CSV files are the source of truth.** Edit `legos.csv`, `groups.csv` and `rules.csv` directly. They were generated once from research reports; nothing regenerates them, and the generator refuses to overwrite them (see "Where the data came from").

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
| `legos.csv` | Pieces (columns in [COLUMNS.md](COLUMNS.md)) | 191 |
| `piece-aliases.csv` | Former piece IDs and their canonical slugs | 169 |
| `groups.csv` | Group letter and name of the pieces; `scripts/kit list` prints both | 14 |
| `rules.csv` | Rules for skills, agent documents, prompts, configuration, workflow, tools, testing | 219 |
| `patterns.md` | Team architecture patterns | 14 |
| `delegation.md` | Historical four-axis/seven-step material with migration notice; current route: authority-design-and-calibration | 4 axes, 7 steps |

Row counts differ from the first plan in one place (14 patterns, not 13); see `docs/generation-notes.md` at the repository root.

In `sources`, `note:R24` means "research note 24", an internal note, not a link. `practice:` means the piece is supported only by observed use. In `rules.csv`, a bare source id such as `K08` is the id used in the research; most carry a link next to them.

## Look something up

```
scripts/kit list            # groups: letter, name, piece count
scripts/kit list A          # one line per piece in group A
scripts/kit show project-instructions        # one piece in full, by id or exact name
scripts/kit list P          # team patterns, one line each; scripts/kit show P6 for one
scripts/kit show authority-design-and-calibration        # current authority design, review/calibration and effect grants
scripts/kit list delegation # historical partial four axes/seven steps, with migration notice
scripts/kit show axis1      # one axis; step3 for one step; combine for how the axes combine
```

Use the slug for new references. Former letter-number IDs are [read aliases](LIBRARY.md#upgrading-from-letter-number-piece-ids).

There is no command that prints the whole store, on purpose. Ask for a group, then a piece. Rules have their own commands: `kit list rules` (gate rules only), `kit list rules <topic>`, `kit show <rule id>` (for example `4.06`). Do not load `rules.csv` whole.

## Team and workflow guidance

team-responsibilities-and-review provides [responsibilities and reviewers](team-workflow/TEAM.md). task-contracts-and-workflow provides [task contracts and workflows](team-workflow/TASKS.md), with selected flow and tracker references. Both are inferred supplied guidance, useful independently through setup/evolve. See [provenance](team-workflow/SOURCES.md) for source scope and limits.

## Bot role templates

Group C (Agent behavior) includes [Bot role templates](BOT-ROLES.md) such as
Software Factory, Chief of Staff, Product Engineer and QA Engineer. Each role
is a supplied instruction-file piece, with the shared [portable template
contract](BOT-TEMPLATE.md) as a separate piece. Run from this directory; set
`store` to the authorized library path for the `library` commands:

```sh
scripts/kit list C
scripts/kit show software-factory
scripts/library --store "$store" search "bot role template" --limit 30
scripts/library --store "$store" selection software-factory --source supplied
```

Without an authorized store, use `kit show` for provenance only. A supplied
selection snapshot identifies the CSV row, not the linked Markdown. Pin the
kit distribution revision (for example, the Git commit) and read both the
role and contract from it before using them. Lookup and selection do not
create or install a Bot, activate a schedule, grant access or qualify a host.

## Optional factory

optional-factory-arrangement provides a [connected factory arrangement](FACTORY.md) only when selected. It composes existing capability contracts and service choices, with design, authorized application and observed unattended readiness kept separate. Manual work remains independent. [Provenance](FACTORY-SOURCES.md) retains original-method and source limits.

## Authority

authority-design-and-calibration delivers [authority design and effect grants](authority/DESIGN.md), with the
recommended ten-level PSW reference, delegated-choice review and evidence-based
calibration. It reuses team/task and assessment ownership. Selected grants,
controls and prior adoption authority remain binding; legacy rows stay available
with explicit historical status. [Sources](authority/SOURCES.md) distinguish
research from adaptation; these sources do not establish host qualification.

## Tool operations

[Operation guidance](TOOL-OPERATIONS.md) composes agent-invoked-cli/actionable-tool-errors and existing native facilities through setup/evolve. It distinguishes exchanged-data validity, observed effects and model-result truth, with operation-specific prerequisites and continuation.

[Coordinated recovery](RECOVERY.md) connects actual task dependencies, observation,
assessment and bounded local repair. Valid independent work remains usable;
restoration, recreation, compensation and partial blockers remain distinct.
[Persistence recovery](PERSISTENCE.md) qualifies existing evidence or an authorized
alternate for the same logical record when storage is unavailable or write outcome
is uncertain. Unknown required durability remains a dependent blocker.

## Instruction and response guidance

instruction-and-response-design provides [instruction and response design](instruction-response/DESIGN.md)
through setup/evolve. It includes source reconciliation, scoped writing guidance,
examples and external content/form criteria, with exchanged tool protocol
validity assessed separately. The procedure is inferred from accepted product
requirements; those requirements establish no host-specific precedence or
runtime support. See the reference's source scope; actual host behavior needs its own evidence.

## Standards guidance

standards-selection-and-document-checks provides [standards selection](standards/SELECT.md) through setup/evolve, with six document-check families and honest machine/human evidence. Selected criteria, performed checks and satisfied requirements are separate; team/workflow retain review ownership and assessment interprets evidence.

## Personal and project resources

Use the public `harness-library` skill to retrieve, research, save or edit reusable drafts, and disable or explicitly restore resources. [Library operations](LIBRARY.md) describes focused search, explicit storage scope, attributable saves and revision-safe editing. Supplied CSVs stay authoritative for supplied material; saved drafts are separate and do not adopt into projects.

## Where the data came from

A one-time script, `skills/harness/harness-evolve/scripts/generate_kit.py`, read the research reports and wrote the five data files. Numbers, ids, certainty and source links are parsed from the reports. The free text was Vietnamese, so it was translated by hand block by block into `skills/harness/harness-evolve/scripts/seed/`; the script stops if a seed block does not match a report id or count. Run it again only into an empty directory:

```
python3 skills/harness/harness-evolve/scripts/generate_kit.py --reports <reports dir> --dest <new dir>
```

It refuses to write if any output file already exists, so a hand-edited kit is never replaced.

## More

- Columns and rules for editing the CSV: [COLUMNS.md](COLUMNS.md)
- Checks (run from the repo root): `python3 -I tools/check_kit.py`, `python3 -I tools/check_boundary.py --strict`, `python3 -m pytest`
