> Historical reference for interpreting existing setup artifacts. Current onboarding
> follows [SKILL.md](SKILL.md) and [RESUME.md](RESUME.md); the sequence and
> prerequisites below are not requirements for new or resumed onboarding.

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
status: unverified    # unverified | passing | failing | adopted | needs-change
verified_on:          # date; empty until the check ran
check_scope:          # optional; "structural" on team entries
verified_platform:    # optional; hook entries: platform, event, matcher, date, or "not verified on <platform>"
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

Entries of `kind: delegation` (one per role) and `kind: role-profile` (one per role, named `role-<role>`) use the same keys. Their body is set out in [DELEGATION.md](DELEGATION.md) and [ROLES.md](ROLES.md); the `check` of a role profile tests that every pointer exists.

`check_scope: structural` on a `kind: team` entry means the check proves the pattern exists in the kit and the folders exist; it does not prove the team works. `passing` on such an entry is never read as "the team runs".

Entries of `kind: standard` and `kind: isolation` point at a section of `harness/STANDARDS.md` (see [STANDARDS-STEP.md](STANDARDS-STEP.md) and [ISOLATION.md](ISOLATION.md)); they never copy the rule text. An entry whose piece is a hook names the platform config file it was wired into in `check` and records `verified_platform` (see [WIRING.md](WIRING.md)).

`adopted` and `needs-change` are for a `kind: folder` entry of a part that already existed (card: `prior_harness`): `adopted` meets the standard and stays; `needs-change` does not, gap in `reason`. Setup moves nothing; `harness-evolve` reconciles relevant `needs-change` entries within the requested scope.

## `situation.md`

Step 1 writes nine lines, `field: value`, facts only, no prose; `python3 tools/check_kit.py --situation harness/situation.md` checks them.

| Field | Value |
|---|---|
| `matt_config` | `present`, `partial` or `absent`: the `## Agent skills` block and `docs/agents/` |
| `work_source` | `git`, `tracker:<name>`, `doc:<path>` or `none`: where finished work is found |
| `code_home` | `.` or paths of the repos the flow writes product files to (code or product documents), comma separated |
| `flow_source` | `doc:<path>`, `sample` (one recent piece of work) or `asked` |
| `prior_harness` | `none`, or paths of harness parts that already exist, comma separated |
| `history` | `yes`, or `none` when no finished work can be named |
| `tree_relation` | `shared`: harness files and product code in one tree; `apart`: the harness repo holds no product code |
| `platform` | the agent app, or `<app>@<host>` when it runs through a host (schedules depend on it); `unknown` until S01 is answered |
| `confirmed` | `no` while drafting, `yes` once the user says the card is right |

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
<UTC timestamp from `date -u +%FT%TZ`> step=<observe|need-to-piece|gate|proposal|record|check|delegation-draft|delegation|roles|standards|isolation|wiring|final> <key=value ...>
```

`observe` carries `platform=`, `work=` (the piece of work of S02 turn 1), `flow=`, `labels=` (`shared=a,b;project=c,d`, an empty side left out, or `none`) and, once S07 is asked, `pain=`; `need-to-piece` carries `need=`, `piece=` and `groups=` (letters of every kit group looked at, comma separated); `gate` carries `items=` (approved) and `dropped=`; `proposal` carries `part=` (tools, folders or team) and `outcome=`; `record` and `check` carry `entry=` (`check` also `result=`); `standards` and `isolation` carry `entry=` (or `outcome=none`) and `result=`; `wiring` carries `map=`, `block=` and `hooks=`; `final` carries `entries=` and `result=`; `delegation-draft` is the one line written in the middle of step 7, after each answer that settles a field of a table row: `role=`, `kind=` and the fields settled so far (`undo=`, `info=`, `level=`, `zone=`, `stop=`); it lets a later run continue inside a stage without asking again; `delegation` and `roles` carry `entry=` and `result=`, and the first `delegation` line also `roles=` (all role names). A value with spaces goes in double quotes (`flow="ticket, code, review"`). Always take the timestamp from running `date -u`, never from memory. Before logging a step, read the last line: a line for the same step and the same entry (or, for `need-to-piece`, the same need) already there is not logged again.

**Revising a decision.** The log is never edited. When the user changes a decision already logged, append a new line with the same `step=` (and the same `part=` or `entry=`) and `revised=<timestamp of the old line>`; leave the old line alone. For each (step, part) the line in force is the last one. `python3 tools/check_kit.py --log harness/progress.log` checks that every `revised=` points to the timestamp of an earlier line with the same step, and lists the line in force for each (step, part) by the same rule.

## Writing safely

Write each file to `<name>.tmp` in the same folder, then rename over the target; remove no other file. An entry or index line already present is updated in place, never appended twice.
