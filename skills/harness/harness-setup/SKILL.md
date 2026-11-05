---
name: harness-setup
description: Set up a project's harness: observe how work really flows, turn a need into a kit piece, record it, run its check. Run after setup-matt-pocock-skills.
disable-model-invocation: true
---

# Harness Setup

Build the project's **harness** (the frame around a coding agent that adds capability) one **tracer bullet** at a time: one need, one kit piece, one record entry, one check that has actually run. This is a prompt-driven skill. Explore, ask, confirm, then write.

Terms: **kit** is the shared read-only store of pieces (**legos**); **record** is `harness/record/`, this project's harness choices, one file per entry. Both are defined in the kit README next to this plugin's `kit/` folder.

Speak to the user in their own language. Ask **one question per turn**, then wait.

## Process

### 0. Preflight

Setup is a prerequisite. Look for an `## Agent skills` block in `AGENTS.md` or `CLAUDE.md` and for `docs/agents/`. Missing either: tell the user to run `setup-matt-pocock-skills` first, then stop. Write nothing.

Then read where the last run stopped. `harness/progress.log` exists: read its last line, say aloud which step it logged and that you continue after it. Resume at the first step without a log line, taking platform, flow and labels from the logged lines; ask nothing a logged line already answers.

Pick the mode. `harness/record/` exists: **edit mode**; ask only about what differs from the record, and start at step 2 for the new need unless the flow itself changed. Otherwise: **fresh mode**.

### 1. Observe

Learn how work really flows here, in plain words: where tasks come from, where the documents live, who hands work to whom. Read `AGENTS.md`, `docs/agents/` and the repo first; ask only what they leave open. Ask which agent platform the team works on; take the platform from the answer.

Read [BOUNDARY.md](BOUNDARY.md) and classify what you learned with its three questions: every item ends as `shared` or `project`.

Read the description of the flow back to the user, labels included. Done when the user says it is right. Append the log line for `observe` (format in [RECORD-FORMAT.md](RECORD-FORMAT.md)); put the platform, a one-line flow summary and the labels in it, so a later run resumes from the log alone.

### 2. Need to piece

Take **one** need from the flow, the one the user names or the most painful. Look it up in the kit, never by loading the store:

```
../../../kit/scripts/kit list            # groups
../../../kit/scripts/kit list <group>    # one line per piece
../../../kit/scripts/kit show <id>       # one piece in full
```

(Paths run from this skill's folder; resolve them to the plugin's `kit/scripts/kit`.) Pick the piece whose `needed_when` matches. No piece fits: record `outside the kit`. Show the user the need and the piece (or `outside the kit`) and wait for a yes. Append the log line for `need-to-piece`.

### 3. Record

Write the entry and the index as set out in [RECORD-FORMAT.md](RECORD-FORMAT.md): temp file first, then rename. Status starts `unverified`. Check for an existing entry for this need first and update it in place. Append the log line for `record`.

### 4. Run the check

Propose one check, a command that proves the piece works (start from the piece's `detail`; with `outside the kit`, design it with the user). Run it once the user agrees. Paste the real output into the entry. Set `status: passing` and `verified_on` only after the check ran and passed; a failure is `failing`. A piece the kit marks as unchecked on this platform needs its own check before `passing`. Append the log line for `check`.

Report: entry path, check result, and the log's last line.

## Next steps

This slice stops here. Later steps (simplicity gate, delegation, roles, standards, isolation, map) are separate; name them in one line and leave them.
