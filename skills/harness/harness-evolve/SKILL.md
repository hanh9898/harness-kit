---
name: harness-evolve
description: Change and maintain a project's harness: reconcile the record with reality, take one change through spec, tickets, implement and check, then update the record. Run after harness-setup.
disable-model-invocation: true
---

# Harness Evolve

Change the project's **harness** one **checked change** at a time, and keep its **record** honest. This is a prompt-driven skill. Read, ask, confirm, then write.

Terms: **kit**, **record** and **legos** are as in `harness-setup`; the record is `harness/record/`, one file per entry. A change is one sentence long and ends with a check that has run.

Speak to the user in their own language. Ask **one question per turn**, then wait. Read [ASKING.md](../harness-setup/ASKING.md) before your first message (overview message, question forms, rules, sheets); write every question from its sheet (V01 to V10).

Stages (the "k/4" of every question; the overview message lists them first):

| Stage | Plain name | Steps | The user |
|---|---|---|---|
| 1 | See where things stand | 0 | sees mismatches, overdue and unfinished work; picks what first |
| 2 | Settle one small change | 1, 2 | tells the latest snag, confirms one sentence, approves evidence |
| 3 | Do it and check it | 3, 4 | mostly watches; may waive a failure or run a team check |
| 4 | Write it down | 5 | reads the report; decides on a change to the standard |

Before the first question send the overview message.

Every step ends with one log line; the keys are fixed in the Log section of [UPDATE.md](UPDATE.md). Read that section before you write the first line.

## Process

### 0. Read

Preflight: no `harness/record/` means setup never ran. Say so, tell the user to run `harness-setup`, and stop. Write nothing.

Then read, in this order: `harness/record/index.md`, the entries, the last lines of `harness/progress.log`. Say aloud which step the log last shows and what you will pick up. Method for the three findings below: [DRIFT.md](DRIFT.md).

- **Drift**: an entry says one thing, the real file says another. Report each one and ask whether to fix the record or fix reality. Never fix either on your own.
- **Overdue or failing**: entries whose `verified_on` is older than the limit in DRIFT.md, or whose check fails now.
- **Needs change**: entries with `status: needs-change`, handed over by setup. Offer them first, ahead of the other findings, as the change of step 1; when it is done, the entry becomes `adopted`.
- **Unfinished work**: the log shows a `change` without its `update`. Ask: continue that, or start a new change.

Show the user one list of findings and ask what to do first (V01; V02 to V04 in DRIFT.md). Append the log line for `read`.

### 1. State the change

Before forming a suggestion, use `<skill-dir>/../../../kit/scripts/kit browse` to find relevant categories across resource types, then `inspect <kind:id>` for selected resources. Carry their guidance into implementation and their applicable standards into review; [the kit guide](../../../kit/README.md) explains evidence limits.
One sentence: what changes, which role, which piece (a kit id or a record entry). Ask for the latest snag (V05, in ASKING.md) and confirm the sentence (V06); the role and piece you look up yourself. The user names it, or picks from step 0. Look up the kit, never by loading the store:

```
<skill-dir>/../../../kit/scripts/kit list            # groups
<skill-dir>/../../../kit/scripts/kit list <group>    # one line per piece
<skill-dir>/../../../kit/scripts/kit show <id>       # one piece in full
```

(`<skill-dir>` is the folder holding this SKILL.md as you were given it; substitute the real folder before running.) Read the affected entries from the record. Wait for the user's yes to the sentence. Append the log line for `change`.

### 2. Simplicity gate

Run the gate again for every item the change adds or alters, exactly as set out in `../harness-setup/GATE.md` (relative to this skill's folder; open it, do not work from memory). The user approves the evidence (an evidence block; V07, in ASKING.md); you never do. A lighter rung that is enough sends you back to step 1 with the lighter change. An item without approved evidence is dropped. Append the log line for `gate`.

### 3. Do it through the Matt flow

`to-spec`, then `to-tickets`, then `implement`, as registered in the `## Agent skills` block. Each ticket carries one check: a command that proves the change works. Detail, including what to do when a skill is not available: [CHANGE-FLOW.md](CHANGE-FLOW.md). Append the log line for `work`.

### 4. Check

Run every check; paste command, exit code and output into the entry. Reviewing a harness change with `code-review`: its prompt must name `harness/STANDARDS.md` as the standard. Detail, the two exits (fail, waiver) and sheets V08, V09: [CHECK-STEP.md](CHECK-STEP.md). A failing check that is not waived sends you back to step 3. Changing a **team** entry: ask for one more verification that actually runs, outside the structural check. Append the log line for `check` per entry.

### 5. Update

Write the entries (temp file, then rename), set `verified_on`, add the log line, append the lessons, and offer any change to the standard as text. Remind the user of Matt's `retro`; never run it yourself. A rerun adds nothing twice. Method, formats and sheet V10: the rest of [UPDATE.md](UPDATE.md). Append the log line for `update`, then report: entries changed, check results, the log's last line.
