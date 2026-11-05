# Delegation (step 7)

How much each role may decide for the user. Done after the tracer-bullet entries are recorded and checked, so there is something to delegate over. Separate from the team shape: the team says who exists, this says who decides what.

## Take the framework in pieces

```
../../../kit/scripts/kit list delegation     # four axes, seven steps, one line each
../../../kit/scripts/kit show axis<n>        # one axis in full (1 to 4)
../../../kit/scripts/kit show step<n>        # one step in full (1 to 7)
../../../kit/scripts/kit show combine        # how the axes combine
```

(Resolve the path to the plugin's `kit/scripts/kit`.) Never open `delegation.md` whole. Its rows are marked `partial`; say so to the user. The four-axis combination is this project's design, not a published standard; do not credit it to a source.

## Ask, one question per turn

List the roles from the flow in step 1 and the team shape of step 4. For each role, list the kinds of decision it makes (a few, in the user's words). For each pair (role, decision kind):

1. **Reversibility.** One-way (hard to undo) or two-way (cheap to undo)? Use `axis1`.
2. **Information.** Does the role usually have enough to decide (about 70 percent)? Use `axis2`.
3. **Level.** Suggest a level from `combine` and read `step<n>` for it; the user decides the number 1 to 7. One-way choices stay at 3 or lower unless the user states a reason; say the reason in the entry.
4. **Zone and escalation.** Only for level 5 or higher: where may the role act alone (paths, commands, systems) and what makes it stop and ask (a count of refusals, an unknown, a cost)? Both must be concrete. An answer like "when unsure" is not a threshold; ask again. Below level 5 write `n/a`.

Show the filled table for the role and wait for a yes before the next role.

## Entry

One entry per role, `record/delegation-<role>.md`, `kind: delegation`, other keys as in [RECORD-FORMAT.md](RECORD-FORMAT.md). It is an instruction-file item, the lightest rung: `gate_lighter_rung: none`, `gate_source` is the `kit show` command you ran this turn, `gate_answer` one line of what it said, `gate_approved: user` once the user said yes to the table. Body:

```
## Levels by kind

| Decision kind | Reversibility | Information | Level (1-7) | Zone | Escalation |
|---|---|---|---|---|---|
```

`check`: a command that fails if any row lacks a field, has a level outside 1 to 7, or has level 5 or more with `n/a` zone or escalation. Run it and paste the output before `passing`.

## Switching on or off

Changing delegation is editing the Level cells of the existing entry (edit mode): off is every level to 3 or lower, on is level 6 for reversible kinds, per `combine`. Update `verified_on` after the check reruns. Create no new entry, delete none, rebuild neither roles nor team; the role profiles point at the entry and need no change. Level 5 or higher still needs zone and escalation.
