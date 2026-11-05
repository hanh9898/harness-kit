# Record format

Files `harness-setup` writes under `harness/`.

## `record/<entry>.md`

`<entry>` is a short kebab-case slug of the need.

```
---
kind: tool            # tool | folder | team | delegation | role-profile | standard | isolation
choice: <kit id and name, or "outside the kit">
reason: <why this piece, one or two lines>
check: <the exact command; for a generated file, its path>
status: unverified    # unverified | passing | failing
verified_on:          # date; empty until the check ran
---

## Check result

<command, exit code, pasted output; empty until run>
```

## `record/index.md`

Read first. One line per entry, no detail:

```
# Harness record

- [<entry>](<entry>.md): <kind>, <status>
```

## `progress.log`

Append only; one line per finished step, never edited:

```
<UTC timestamp from `date -u +%FT%TZ`> step=<observe|need-to-piece|record|check> <key=value ...>
```

`observe` carries `platform=`, `flow=` and `labels=`; `need-to-piece` carries `need=` and `piece=`; `record` and `check` carry `entry=`. Before logging a step, read the last line: a line for the same step and entry already there is not logged again.

## Writing safely

Write each file to `<name>.tmp` in the same folder, then rename over the target; remove no other file. An entry or index line already present is updated in place, never appended twice.
