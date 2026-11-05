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

Then read where the last run stopped. `harness/progress.log` exists: read its last line, say aloud which step it logged and that you continue after it. Resume at the first step without a log line (a recorded entry with no `check` line resumes at step 6; every entry checked but no `delegation` line resumes at step 7; a `delegation` line but no `roles` line, step 8; then the first of steps 9 to 12 without its log line), taking platform, flow, labels and approved gate evidence (`harness/gate.md`) from the files; ask nothing a logged line already answers.

Pick the mode. `harness/record/` exists: **edit mode**; ask only about what differs from the record, and start at step 2 for the new need unless the flow itself changed. Entries checked but no delegation or role entries yet: offer step 7. An old entry without gate fields is readable: say it predates the gate, and run step 3 for it before you change it. Otherwise: **fresh mode**.

### 1. Observe

Learn how work really flows here, in plain words: where tasks come from, where the documents live, who hands work to whom. Read `AGENTS.md`, `docs/agents/` and the repo first; ask only what they leave open. Ask which agent platform the team works on; take the platform from the answer.

Read [BOUNDARY.md](BOUNDARY.md). Put its three questions to the user, one per turn, about the items still unsettled; you may suggest an answer, the user decides. Every item ends as `shared` or `project`.

Read the description of the flow back to the user, labels included. Done when the user says it is right. Append the log line for `observe` (format in [RECORD-FORMAT.md](RECORD-FORMAT.md)); put the platform, a one-line flow summary and the labels in it, so a later run resumes from the log alone.

### 2. Need to piece

Take **one** need from the flow, the one the user names or the most painful. Look it up in the kit, never by loading the store:

```
../../../kit/scripts/kit list            # groups
../../../kit/scripts/kit list <group>    # one line per piece
../../../kit/scripts/kit show <id>       # one piece in full
```

(Paths run from this skill's folder; resolve them to the plugin's `kit/scripts/kit`.) Pick the piece whose `needed_when` matches. No piece fits: record `outside the kit`. Show the user the need and the piece (or `outside the kit`) and wait for a yes. Append the log line for `need-to-piece`.

### 3. Simplicity gate

Nothing is recorded or installed until it passes the gate. At this step the items are the pieces chosen in step 2 (the folder and team items of step 4 pass the same gate when proposed; in edit mode, every item you add or change). For **each** item, find the next lighter step on the ladder (instruction file, skill, script/CLI, MCP) and the evidence that it is not enough. Read the platform's docs or `--help` now, never from memory. Write url or command, date and the answer. Method and format: [GATE.md](GATE.md).

Show the user the whole evidence list and wait. Only the user approves it; you never do. An item without approved evidence is dropped, not recorded. Append the log line for `gate`.

### 4. Propose, one part at a time

Three parts, in this order: tools to install (with their rung), folder layout, agent team shape. Propose one, wait for the user to settle it, then move on. The tools were gated in step 3; folder and team items go through the gate as you propose them, evidence shown with the proposal. Method: [PROPOSALS.md](PROPOSALS.md). Append one log line per settled part.

### 5. Record

Write each settled item as an entry and update the index as set out in [RECORD-FORMAT.md](RECORD-FORMAT.md): temp file first, then rename. Status starts `unverified`. A `kind: team` entry carries `check_scope: structural`. Check for an existing entry for this need first and update it in place. Append the log line for `record` per entry.

### 6. Install and run the check

Create what the settled parts name (the script, the folders) and nothing else. Then propose one check, a command that proves the piece works (start from the piece's `detail`; with `outside the kit`, design it with the user). Run it once the user agrees. Paste the real output into the entry. Set `status: passing` and `verified_on` only after the check ran and passed; a failure is `failing`. A piece the kit marks as unchecked on this platform needs its own check before `passing`. Append the log line for `check` once, after the final result.

### 7. Delegation

Its own step, never mixed into the team shape. For each role and each kind of decision, ask the four axes and agree one level from 1 to 7. Fetch the framework piece by piece, never the whole file. Write one `delegation-<role>` entry per role. Turning delegation on or off later is changing a level, nothing rebuilt. Method and format: [DELEGATION.md](DELEGATION.md). Append the log line for `delegation` per entry.

### 8. Roles and profiles

One `role-<role>` entry per role, four cells (tools, docs, skills, delegation level), each pointing to something that exists. A cell pointing at nothing sends you back to fix it; the entry is never `passing` until every pointer resolves. Method: [ROLES.md](ROLES.md). Append the log line for `roles` per entry.

### 9. Standards

Choose the checkable standard for the pieces chosen, from the kit's rules, never by loading them. Write `harness/STANDARDS.md` (first line: it applies only to changes under `harness/`) and one `standard-*` entry that points at it. Method: [STANDARDS-STEP.md](STANDARDS-STEP.md). Append the log line for `standards`.

### 10. Isolation

Its own question: should the harness stay out of the product's commits, comments and PRs? If yes, propose rule, checker and review; the user chooses. Suggest, never edit, a scope line for the product's coding standards. Method: [ISOLATION.md](ISOLATION.md). Append the log line for `isolation`.

### 11. Map, entry point and hooks

Register the contexts in `GLOSSARY-MAP.md`, create the harness glossary and ADR folder, replace the block between the two markers in `AGENTS.md` or `CLAUDE.md`, and wire and trigger every hook. Method: [WIRING.md](WIRING.md). Append the log line for `wiring`.

### 12. Final check

List every entry in `record/` with its status. Verify with a command, not from memory, that each `passing` entry has a pasted check result with a date, and re-run any that does not. An entry whose check cannot run stays `unverified` or `failing`, and you say so. Append the log line for `final`, then report: entry paths, check results, and the log's last line.
