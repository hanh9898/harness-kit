# Drift, overdue, unfinished work (step 0)

## Compare the record with reality

Each entry names things that must exist. For every entry in `index.md`:

- run its `check` field if it is a read-only command; otherwise test that each path it names exists (`test -e`)
- for a hook entry, open the platform config file the entry names and confirm the hook is there
- for a `kind: standard` or `kind: isolation` entry, confirm the section it points at exists in `harness/STANDARDS.md`
- for a `role-*` entry, confirm each of the four cells points at something that exists

Also look the other way: a file under `harness/tools/` or a `standard` section that no entry covers. Run commands, do not judge from memory.

Count an entry once, under the first class that fits: drift, then failing, then overdue. Report each mismatch as: entry, what it claims, what is on disk. Ask one question per mismatch: fix the record, or fix reality? Write nothing until the user answers. Then do only that, through step 1 to 5 if it is a change. If the record alone is wrong, edit the record directly (step 5 rules), rerun that entry's check, and log `read`, `check` and `update` only; there is no change, gate or work to log.

## Overdue

An entry is **overdue** when `verified_on` is empty on a non-`unverified` entry, or older than 30 days (`date -u +%F` against the field). The user may name another limit; use it for this run and say so. Overdue and `failing` entries go on the findings list. Rerunning an overdue entry's check is offered, not assumed.

## Unfinished work

Read the log's last lines. A `change` line with no later `update` for the same change is unfinished. Take the change text, gate evidence (`harness/gate.md`) and tickets from the files; ask nothing a logged line already answers.
