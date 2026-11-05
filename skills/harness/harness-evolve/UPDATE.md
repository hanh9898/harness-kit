# Update (step 5)

Entry and index formats: `../harness-setup/RECORD-FORMAT.md` (relative to this skill's folder). Same safe writing: each file to `<name>.tmp` in the same folder, then rename over the target; an entry or index line already present is updated in place, never appended twice.

## Record

For every entry the change touched: new body, `status`, `verified_on` from this run's check, the pasted result. A new entry also needs its `gate_*` keys from step 2. Drift settled in step 0 is written here too.

## Lessons

`harness/lessons.md`, append only, one block per change. Skip a block already there for the same change.

```
## <date> <change sentence>
- learned: <what the change taught about the harness>
- standard: <a missing or wrong rule, or "none">
```

A standard change is only a proposal: show the user the exact text. Edit `harness/STANDARDS.md` only after they say yes; then the matching `standard-*` entry follows the same step 4 rules.

## Retro

Remind the user that Matt's `retro` can review the session, by hand or on a schedule if the platform supports one. Do not run it.

## Log

Append to `harness/progress.log`, one line per finished step, never edited. Take the timestamp from running `date -u +%FT%TZ`.

```
<timestamp> step=<read|change|gate|work|check|update> <key=value ...>
```

`read` carries `drift=`, `overdue=`, `failing=`, `open=` (counts); `change` carries `change=` and `pieces=`; `gate` carries `items=` and `dropped=`; `work` carries `tickets=` (and `round=` from the second round); `check` carries `entry=` and `result=` (`passing`, `failing`, `waived`); `update` carries `entries=` and `lesson=`.

A return to step 3 after a failed check logs `work` again with `round=<n>`. Before logging, read the last line: a line for the same step and the same change already there is not logged again. A `read` identical to the last `read` is not logged again. A rerun with nothing to change ends after step 0; its only write is that `read` line.
