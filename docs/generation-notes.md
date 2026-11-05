# Generation notes

How `kit/` was produced and why its row counts differ from the planning figures. Planning figures were 162 legos, 211 rules and 13 patterns.

Counts below come from headings and table rows in the source reports, counted by a test that does not call the generator.

| Item | Planned | Counted in sources | Result |
|---|---|---|---|
| Groups | 14 | 14 (group headings A to N in report 25) | 14 |
| legos | 162 | 162 (`### A1.` to `### N6.` headings in report 25) | 162 rows in `legos.csv` |
| rules | 211 | 211 (table rows numbered 1.01 to 7.31 in the synthesis) | 211 rows in `rules.csv` |
| patterns | 13 | 14 (rows of the convergence matrix, section 3 of report 26) | 14 rows in `patterns.md` |
| delegation | 4 axes, 7 steps | 7 steps quoted in report 27; 4 axes grouped by the kit design | 4 axes, 7 steps |

## patterns: 13 planned, 14 counted

The planning figure of 13 appears only in design notes; report 26 itself never states a total. Its section 3 matrix has 14 rows, the last being the free-running ReAct loop. The kit uses the counted number and lists all 14. No row was merged or split, so the difference is one pattern the plan did not count.

## legos: ids

Source ids such as `A1` are written as `A01` so ids sort. Nothing was merged or split.

## delegation: why four axes

Report 27 has a 7-row axis matrix and report 28 a 9-row one. The kit groups them into four axes (reversibility, information level, the seven-step scale, permitted zone with escalation threshold). Every row of `delegation.md` is `partial` because reports 27 and 28 were read only in part; the file lists what was not read.

## Certainty values

`stated`: the source says it. `inferred`: the research inferred it. `open`: unchecked or sources disagree. `partial`: any row whose support comes from a source read only in part (reports 17, 27, 28), never anything higher.

## What was translated by hand

Free text in the reports is Vietnamese. The generator does not translate. Names, summaries, rule text, pattern text and the delegation text were translated block by block into `skills/harness/harness-evolve/scripts/seed/`. The generator parses ids, groups, certainty, sources, ordering and counts from the reports, and stops when a seed block does not match a report id or count.

## After the first generation: the CSV is the source of truth

`generate_kit.py` ran once. From then on `kit/legos.csv` and `kit/rules.csv` are edited by hand and are the source of truth; the generator and its `seed/` are not updated to follow them (the generator refuses to overwrite a hand-edited kit).

Rows added after the first generation, all at the end of the file so later merges stay clean: lego `H18` (review checklist), rules `2.24` and `7.32`, giving 163 legos and 213 rules in the committed kit. The extra detail text on `D04`, `L08` and `I04` was edited in place. The independent count test still compares the generator against the source reports (162 and 211); only the committed-kit check adds `ADDED_AFTER_GENERATION`.
