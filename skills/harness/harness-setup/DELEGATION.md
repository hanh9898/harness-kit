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

Write each question from its sheet at the end of this file, in the forms of [ASKING.md](ASKING.md). Say "axis", "level" and the 70 percent threshold in plain words; they are your working terms. The list of roles and the table below are the same questions as before, only worded from the sheets.

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

## Question sheets (step 7)

Stage 4 opens with S14 (full form); S15 to S20 follow in compact form. A new role restarts the loop at S15.

### [S14] The roles

- Stage: 4/6 Decide who may decide what
- Helps: the permissions below are given to the roles your team really has
- If skipped: I use the roles I proposed from your flow
- Why: each role gets its own level of freedom, so I need the list of roles first
- Ask: In "<recent piece of work>" I see these roles: <roles from the flow and the team shape, in plain words>. Are those the roles?
- Terms: role = a job in the flow done by a person or an agent, for example the one who writes requests, who codes, who reviews
- Enough: yes, or the names to add or remove
- Unsure: say "not sure"; I use my list
- Suggest: the roles of the chain seen in stage 1

### [S15] What a role decided on its own

- Stage: 4/6 Decide who may decide what
- Helps: freedom is set for real choices the role makes, not for guesses
- If skipped: I use the choices I find in the pull request and commits for that role
- Why: each kind of decision gets its own level
- Ask: In "<recent piece of work>", what did <role> have to decide on its own? (After each answer: Was there another? Stop when the user says no.)
- Terms: kind of decision = a group of similar choices, for example choosing a column name or merging a change
- Enough: one decision per answer, in the user's words
- Unsure: say "not sure"; I use the choices found in the history
- Suggest: "<example from the pull request, for instance choosing the name of a column>"

### [S16] Hard or easy to undo

- Stage: 4/6 Decide who may decide what
- Helps: hard-to-undo choices stay under your control
- If skipped: I treat it as hard to undo, which keeps the freedom low
- Why: how hard a mistake is to undo decides how much freedom is safe
- Ask: Last time <role> decided "<decision>" (<pull request or commit>): if it had been wrong, would undoing it have been hard or easy?
- Terms: hard to undo = one-way, for example data lost or already shipped; easy = two-way, a cheap revert
- Enough: hard or easy
- Unsure: say "not sure"; I treat it as hard to undo
- Suggest: the answer the history suggests (for example "easy: it was a single commit that can be reverted"), stated as a guess

### [S17] Did the role have enough information

- Stage: 4/6 Decide who may decide what
- Helps: a role that often lacked information proposes and waits; one with enough may act
- If skipped: I treat it as not enough, which lowers the level; you can raise it later
- Why: this decides whether the role acts alone or proposes
- Ask: Last time <role> had to decide "<decision>" (<pull request>): did it have enough information to decide right?
- Terms: none
- Enough: enough, not enough, or don't know
- Unsure: say "don't know"; I treat it as not enough
- Suggest: "Not enough: it had not read <document> yet." Name what you found

### [S18] How much it may decide alone

- Stage: 4/6 Decide who may decide what
- Helps: the number you pick is what the agent is allowed to do without asking you
- If skipped: I use my suggested level, capped at 3 when the decision is hard to undo
- Why: this is the final level for this kind of decision
- Ask: For "<decision>" I suggest level <n> of 7: "<meaning of that level in plain words, from the framework piece>". Is that how much you want <role> to decide alone?
- Terms: level = from 1 (the role only reports) to 7 (the role decides and acts alone, you are told afterwards); the meaning of the level is read from the framework, said in plain words
- Enough: yes, or another number from 1 to 7
- Unsure: say "not sure"; I use the suggested level (capped at 3 when hard to undo)
- Suggest: the level the framework gives for this answer of S16 and S17. A hard-to-undo choice above 3 needs your stated reason, which I write in the entry

### [S19] Where it may act alone and when it must stop (level 5 or higher)

- Stage: 4/6 Decide who may decide what
- Helps: at high freedom the agent has clear limits, so it cannot wander
- If skipped: I keep this decision at level 4 until you give both limits
- Why: from level 5 on I need both a place it may act and a point where it must stop and ask
- Ask (two turns, in this order):
  1. Zone: Which places may <role> change alone for "<decision>": which folders, commands or systems? Enough: a concrete list. Unsure: level stays at 4. Suggest: the paths changed in "<recent piece of work>"
  2. Stop point: When should <role> stop and ask you: after how many refused attempts, when something is unknown, or when the cost passes what amount? Enough: one concrete trigger. Unsure: level stays at 4. Suggest: "after 2 refusals, or when something it needs is unknown". "When unsure" is not a trigger; ask again once
- Terms: zone = the places it may act alone; stop point = what makes it stop and ask
- Enough: per turn
- Unsure: per turn
- Suggest: per turn

### [S20] Confirm the table of one role

- Stage: 4/6 Decide who may decide what
- Helps: you see all levels of this role in one place before they are written
- If skipped: the table stays a draft and nothing is written
- Why: one yes covers the table and the evidence for it
- Ask: Is this table right for <role>? <the table>
- Terms: level, zone and stop point as in S18 and S19
- Enough: yes, or the row to change
- Unsure: say "not sure"; the table stays a draft
- Suggest: yes
