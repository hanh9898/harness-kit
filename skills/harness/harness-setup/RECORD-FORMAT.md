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
gate_lighter_rung: <next lighter rung, or "none">
gate_why_not_enough: <one or two lines>
gate_source: <url, or the exact `--help` command>
gate_read_on: <date the source was read>
gate_answer: <what the source said>
gate_approved: user   # always "user"; an entry without it is not written
---

## Check result

<command, exit code, pasted output; empty until run>
```

Entries written before the gate existed have no `gate_*` keys. Read them as `gate: not run`; never delete or reject them. Run the gate for such an entry before you change it, then add the keys.

Entries of `kind: delegation` (one per role) and `kind: role-profile` (one per role, named `role-<role>`) use the same keys. Their body is set out in [DELEGATION.md](DELEGATION.md) and [ROLES.md](ROLES.md); the `check` of a role profile tests that every pointer exists. Older entries are read as before.

## `gate.md`

Hand-off from step 3 to step 5, so an interrupted run keeps the approved evidence. One `## <item>` section per approved item with the five evidence fields (`lighter_rung`, `why_not_enough`, `source`, `read_on`, `answer`). The entry holds the lasting copy; later runs read the entry.

## `record/index.md`

Read first. One line per entry, no detail:

```
# Harness record

- [<entry>](<entry>.md): <kind>, <status>
```

## `progress.log`

Append only; one line per finished step, never edited:

```
<UTC timestamp from `date -u +%FT%TZ`> step=<observe|need-to-piece|gate|proposal|record|check|delegation|roles> <key=value ...>
```

`observe` carries `platform=`, `flow=` and `labels=`; `need-to-piece` carries `need=` and `piece=`; `gate` carries `items=` (approved) and `dropped=`; `proposal` carries `part=` (tools, folders or team) and `outcome=`; `record` and `check` carry `entry=` (`check` also `result=`); `delegation` and `roles` carry `entry=` and `result=`, and the first `delegation` line also `roles=` (all role names). Always take the timestamp from running `date -u`, never from memory. Before logging a step, read the last line: a line for the same step and the same entry (or, for `need-to-piece`, the same need) already there is not logged again.

## Writing safely

Write each file to `<name>.tmp` in the same folder, then rename over the target; remove no other file. An entry or index line already present is updated in place, never appended twice.
