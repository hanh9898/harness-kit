# Delegation (step 7)

How much each role may decide for the user. Done after the tracer-bullet entries are recorded and checked, so there is something to delegate over. Separate from the team shape: the team says who exists, this says who decides what.

## Take the framework in pieces

```
<skill-dir>/../../../kit/scripts/kit list delegation     # four axes, seven steps, one line each
<skill-dir>/../../../kit/scripts/kit show axis<n>        # one axis in full (1 to 4)
<skill-dir>/../../../kit/scripts/kit show step<n>        # one step in full (1 to 7)
<skill-dir>/../../../kit/scripts/kit show combine        # how the axes combine
```

(Substitute `<skill-dir>` as in SKILL.md.) Never open `delegation.md` whole. Its rows are marked `partial`; say so to the user. The four-axis combination is this project's design, not a published standard; do not credit it to a source.

## Ask, one question per turn

First ask the user to name the roles (propose from the flow in step 1 and the team shape of step 4; the log may name none). The first `delegation` log line lists all of them in `roles=`. For each role, list the kinds of decision it makes (a few, in the user's words). For each pair (role, decision kind):

1. **Reversibility.** One-way (hard to undo) or two-way (cheap to undo)? Use `axis1`.
2. **Information.** Does the role usually have enough to decide (about 70 percent)? Use `axis2`. For a one-way choice held at level 3 or lower, `unknown` is an accepted answer; it can only lower the level.
3. **Level.** Suggest a level from `combine` and read `step<n>` for it; the user decides the number 1 to 7. One-way choices stay at 3 or lower unless the user states a reason; say the reason in the entry.
4. **Zone and escalation.** Only for level 5 or higher: where may the role act alone (paths, commands, systems) and what makes it stop and ask (a count of refusals, an unknown, a cost)? Both must be concrete. An answer like "when unsure" is not a threshold; ask again. Below level 5 write `n/a`.

Show the filled table for the role and wait for a yes before the next role.

## Entry

One entry per role, `record/delegation-<role>.md`, `kind: delegation`, other keys as in [RECORD-FORMAT.md](RECORD-FORMAT.md). It is an instruction-file item, the lightest rung: `gate_lighter_rung: none`, `gate_source` is the `kit show` command you ran this turn, `gate_answer` one line of what it said, `gate_approved: user` once the user said yes. Show this evidence in the same turn as the table, so one yes covers both; an edit to the table is shown again. Body:

```
## Levels by kind

| Decision kind | Reversibility | Information | Level (1-7) | Zone | Escalation |
|---|---|---|---|---|---|
```

`check`: a command that fails if any row lacks a field, has a level outside 1 to 7, or has level 5 or more with `n/a` zone or escalation. Run it and paste the output before `passing`. Example (columns 2 to 7 of the table; fields are the cells):

```
awk -F'|' '/^## Levels by kind/{t=1;next} t&&/^\|/{n++; if(n>2){rows++; for(i=2;i<=7;i++){gsub(/^ +| +$/,"",$i); if($i=="")bad=1} if(!($5 ~ /^[1-7]$/))bad=1; if($5>=5&&($6=="n/a"||$7=="n/a"))bad=1}} END{if(!rows||bad){print "FAIL";exit 1} print "OK rows=" rows}' <entry>
```

A check with `|` or quotes goes in the YAML key as a block scalar (`check: |-`).

Append one `delegation` log line per entry, after the check result (no separate `record` or `check` lines for it). The run is done when every role in `roles=` has such a line; resume with the roles that lack one.

## Switching on or off

Changing delegation is editing the Level cells of the existing entry (edit mode): off is every level to 3 or lower, on is level 6 for reversible kinds, per `combine`. Leave Zone and Escalation as they are (a level below 5 may keep them; the check still passes). Turning on moves a kind to the level the user names, or back to its earlier level if the user says so; ask when unclear. Update `verified_on` after the check reruns. A level change adds no log line (the entry is the same, the step is the same). Create no new entry, delete none, rebuild neither roles nor team; the role profiles point at the entry and need no change. Level 5 or higher still needs zone and escalation.
