# Drift, overdue, unfinished work (step 0)

## Compare the record with reality

Each entry names things that must exist. For every entry in `index.md`:

- run its `check` field if it is a read-only command; otherwise test that each path it names exists (`test -e`)
- for a hook entry, open the platform config file the entry names and confirm the hook is there
- for a `kind: standard` or `kind: isolation` entry, confirm the section it points at exists in `harness/STANDARDS.md`
- for a `role-*` entry, confirm each of the four cells points at something that exists

Also look the other way: a file under `harness/tools/` or a `standard` section that no entry covers. Run commands, do not judge from memory.

Count an entry once, under the first class that fits: drift, then failing, then overdue. Report each mismatch as: entry, what it claims, what is on disk. Ask one question per mismatch (sheet V02 below; forms in [ASKING.md](../harness-setup/ASKING.md)): fix the record, or fix reality? Write nothing until the user answers. Then do only that, through step 1 to 5 if it is a change. If the record alone is wrong, edit the record directly (step 5 rules), rerun that entry's check, and log `read`, `check` and `update` only; there is no change, gate or work to log.

## Overdue

An entry is **overdue** when `verified_on` is empty on a non-`unverified` entry, or older than 30 days (`date -u +%F` against the field). The user may name another limit; use it for this run and say so. Overdue and `failing` entries go on the findings list. Rerunning an overdue entry's check is offered, not assumed.

## Unfinished work

Read the log's last lines. A `change` line with no later `update` for the same change is unfinished. Take the change text, gate evidence (`harness/gate.md`) and tickets from the files; ask nothing a logged line already answers.

## Question sheets (step 0)

Forms and rules: [ASKING.md](../harness-setup/ASKING.md). Stage 1 opens with V01 (full form).

### [V01] What to handle first

- Stage: 1/4 See where things stand
- Helps: the first change you make is the most pressing one, and you know the others are waiting
- If skipped: I start with a failing check, else the oldest overdue entry
- Why: I found several things; I handle one at a time
- Ask: Which of these shall we handle first? <one line each: what it is, plain words, with date>
- Terms: mismatch = the record says one thing and the file on disk says another; overdue = not re-checked for more than 30 days; unfinished = a change started earlier and not closed in the log
- Enough: one item
- Unsure: say "not sure"; I use the order named under Suggest
- Suggest: the failing check first, then a mismatch, then the unfinished change, then the oldest overdue entry. Say why

### [V02] Which side is right for one mismatch

- Stage: 1/4 See where things stand
- Helps: the record and the files agree again, the way you want
- If skipped: I change nothing and the mismatch stays on the list
- Why: I never fix either side on my own
- Ask: The record of "<entry>" says "<claim>", but the file <path> says "<what is there>". Which one is right now?
- Terms: record = the notes in `harness/record/` about what the setup holds
- Enough: "the record", "the file", or "neither"
- Unsure: say "not sure"; I change nothing
- Suggest: the side the file's last change points to, for example "the file changed on <date> by <commit> after the record, so I think the file is right"

### [V03] Continue the unfinished change or start a new one

- Stage: 1/4 See where things stand
- Helps: you do not lose work that was started and you do not redo it
- If skipped: I continue the unfinished change
- Why: the log shows a change that was started and not closed
- Ask: On <date> you started "<change sentence>" and it was not closed. Continue that, or start something new?
- Terms: none
- Enough: "continue" or "new"
- Unsure: say "not sure"; I continue the unfinished change
- Suggest: continue; its gate evidence and tickets are already on disk, say which

### [V04] The overdue limit and a re-check

- Stage: 1/4 See where things stand
- Helps: entries that nobody re-checked for long are not trusted by accident
- If skipped: I keep 30 days and do not re-run anything
- Why: overdue entries go on the list; the limit and the re-run are yours to set
- Ask (two turns, only when overdue entries exist):
  1. Limit: I count an entry as overdue after 30 days without a re-check. Do you want another limit for this run? Enough: yes with the number, or no. Unsure: keep 30. Suggest: no, keep 30
  2. Re-check: "<entry>" was last checked on <date> (<n> days ago). Shall I run its check again now? Enough: yes or no. Unsure: do not run it. Suggest: yes, when the check only reads files
- Terms: overdue = not re-checked for longer than the limit
- Enough: per turn
- Unsure: per turn
- Suggest: per turn
