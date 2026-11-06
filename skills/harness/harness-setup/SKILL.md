---
name: harness-setup
description: Set up a project's harness: observe how work really flows, turn a need into a kit piece, record it, run its check. Run after setup-matt-pocock-skills.
disable-model-invocation: true
---

# Harness Setup

Build the project's **harness** (the frame around a coding agent that adds capability) one **tracer bullet** at a time: one need, one kit piece, one record entry, one check that has actually run. Terms: **kit** is the shared read-only store of pieces (**legos**); **record** is `harness/record/`, this project's harness choices, one file per entry; both are defined in the kit README. Speak to the user in their own language. Ask **one question per turn**, then wait. Read [ASKING.md](ASKING.md) before your first message: overview message, question forms, rules, sheets S01 to S31. Each step names its sheets; write every question from its sheet.

Stages (the "k/6" of every question; the overview message lists them first):

| Stage | Plain name | Steps | The user |
|---|---|---|---|
| 1 | Understand how your team works | 0, 1 | tells one recent piece of work, names the agent app, labels items, confirms the flow |
| 2 | Pick one thing to improve and the lightest way to do it | 2, 3, 4 | picks a need, approves evidence, settles tools, folders, team shape |
| 3 | Record it and try it out | 5, 6 | agrees one check and sees it run |
| 4 | Decide who may decide what | 7, 8 | names roles, gives a recent decision per role, picks levels and profiles |
| 5 | Rules, keeping the tooling apart from your product, wiring it in | 9, 10, 11 | picks rules, says yes or no to isolation, confirms hook files |
| 6 | Final check | 12 | reads the report; no question |

Before the first question send the overview message (ASKING.md), short. Everything you say is in the user's words: the rule on words not to say is in ASKING.md, once. The user may ask to start at stage 5 (steps 9 to 12).

## Process

### 0. Preflight and resume

Setup is a prerequisite: look for an `## Agent skills` block in `AGENTS.md` or `CLAUDE.md` and for `docs/agents/`. Both there: `matt_config: present`. Neither: tell the user to run `setup-matt-pocock-skills` first, write nothing, stop. `docs/agents/issue-tracker.md` there but no `## Agent skills` heading: `matt_config: partial`; propose a block (sub-headings Issue tracker, Triage labels, Domain docs; one summary line and a pointer to each file under `docs/agents/`), show the draft, write it only after the user approves, change nothing else in the file. This does not relax the prerequisite: the block must exist before step 1.

`harness/progress.log` exists: read its last line, say which step it logged and that you continue after it. Take platform, flow, labels, the card and approved gate evidence (`harness/gate.md`) from the files; ask nothing a logged line already answers. Resume at the first step without its log line, except:

| The log shows | Resume at |
|---|---|
| a `record` line, no `check` line | 6 |
| every entry checked, no `delegation` line | 7 (a `delegation-draft` line without its `delegation` line: continue at the first field not settled, say what was kept) |
| a `delegation` line, no `roles` line | 8 |
| `roles` done | the first of 9 to 12 without its line |

`harness/record/` exists: **edit mode**. Ask only what differs from the record; start at step 2 for the new need unless the flow changed; if the user names a later step (9 to 12), start there. Otherwise **fresh mode**.

### 1. Observe

Learn how work really flows here. Write `harness/situation.md`, the situation card: nine lines `field: value`, facts you looked up (fields and values: [RECORD-FORMAT.md](RECORD-FORMAT.md)); draft it from the repo with `platform: unknown` and `confirmed: no`. Before the first question read `AGENTS.md`, `docs/agents/`, the repo and every local folder in the card's `code_home`; ask only what they leave open. Ask which agent app the team uses (S01) and write it into the card. Run `python3 <skill-dir>/../../../tools/check_kit.py --situation harness/situation.md`: it prints the branch each sheet takes (meanings in [BOUNDARY.md](BOUNDARY.md)). Sheets read the card, never a kind of repo.

Read [BOUNDARY.md](BOUNDARY.md). Label the items as its `s03_labels` branch says; you suggest, the user decides. Every item ends as `shared` or `project`. Learn the flow (S02, in BOUNDARY.md), then read its description back (S06), labels and card included. Set `confirmed: yes` when the user says it is right. Append the log line for `observe` (keys in RECORD-FORMAT.md) and run `check_kit.py --log harness/progress.log`, so a later run resumes from the log alone.

### 2. Need to piece

Take **one** need from the flow, the one the user names or the most painful. Look it up in the kit, never by loading the store:

```
<skill-dir>/../../../kit/scripts/kit list            # groups
<skill-dir>/../../../kit/scripts/kit list <group>    # one line per piece
<skill-dir>/../../../kit/scripts/kit show <id>       # one piece in full
```

(`<skill-dir>` is the folder holding this SKILL.md as you were given it, three levels below the plugin root; substitute it before running.) Run `kit list` for every group that could touch the need ("automatic" touches schedules too) and tell the user the group names you looked at. Pick the piece whose `needed_when` matches; none fits: `outside the kit`. Ask which need hurts most (S07, in ASKING.md; branch `pain` asked it in stage 1: take the `pain=` of the `observe` line, never ask again), show the need and the piece and wait for a yes (S08). Append the log line for `need-to-piece`, with the letters of the groups you looked at.

### 3. Simplicity gate

Nothing is recorded or installed until it passes the gate. Items: the pieces of step 2, the folder and team items of step 4 when proposed, and in edit mode every item you add or change. For **each** item, find the next lighter step on the ladder (instruction file, skill, script/CLI, MCP) and the evidence that it is not enough. Read the platform's docs or `--help` now, never from memory. Write url or command, date and the answer. Method and format: [GATE.md](GATE.md). Show the whole evidence list as an evidence block (ASKING.md; S09 in GATE.md) and wait; only the user approves it. An item without approved evidence is dropped, not recorded. Append the log line for `gate`.

### 4. Propose, one part at a time

Three parts, in this order: tools to install (with their rung), folder layout, agent team shape. Propose one, wait for the user to settle it, then move on. The tools were gated in step 3; folder and team items go through the gate as you propose them, evidence shown with the proposal. Method and sheets S10 to S12: [PROPOSALS.md](PROPOSALS.md); the card's `s11` branch says how an existing harness is handled. Append one log line per settled part.

### 5. Record

Write each settled item as an entry and update the index as set out in [RECORD-FORMAT.md](RECORD-FORMAT.md): temp file first, then rename. Status starts `unverified`. A `kind: team` entry carries `check_scope: structural`. Check for an existing entry for this need first and update it in place. Append the log line for `record` per entry.

### 6. Install and run the check

Create what the settled parts name (the script, the folders) and nothing else. Then propose one check per entry (S13, in ASKING.md; one command each, and say the number of entries first): a command that proves the piece works (start from the piece's `detail`; with `outside the kit`, design it with the user). Run only the command the user agreed to, no probe commands to "see what happens". Paste the real output into the entry. Set `status: passing` and `verified_on` only after the check ran and passed; a failure is `failing`. A piece the kit marks as unchecked on this platform needs its own check before `passing`. Append the log line for `check` once, after the final result.

### 7. Delegation

Its own step, never mixed into the team shape. It is the longest stage: announce its length first (DELEGATION.md). For each role and each kind of decision, ask the four axes and agree one level from 1 to 7. Fetch the framework piece by piece, never the whole file. Write one `delegation-<role>` entry per role. Turning delegation on or off later is changing a level, nothing rebuilt. Method, format and sheets S14 to S20: [DELEGATION.md](DELEGATION.md). Append the log line for `delegation` per entry.

### 8. Roles and profiles

One `role-<role>` entry per role, four cells (tools, docs, skills, delegation level), each pointing to something that exists. A cell pointing at nothing sends you back to fix it; the entry is never `passing` until every pointer resolves. Method and sheet S21: [ROLES.md](ROLES.md). Append the log line for `roles` per entry.

### 9. Standards

Choose the checkable standard for the pieces chosen, from the kit's rules, never by loading them. Write `harness/STANDARDS.md` (first line: it applies only to changes under `harness/`) and one `standard-*` entry per chosen rule, each pointing at its section. Method and sheet S22: [STANDARDS-STEP.md](STANDARDS-STEP.md). Append the log line for `standards`.

### 10. Isolation

Its own question, always asked: should the harness stay out of the product's commits, comments and PRs? If yes, propose rule, checker and review; the user chooses. Suggest, never edit, a scope line for the product's coding standards. Method and sheets S23 to S27: [ISOLATION.md](ISOLATION.md). Append the log line for `isolation`.

### 11. Map, entry point and hooks

Register the contexts in `GLOSSARY-MAP.md`, create the harness glossary and ADR folder, replace the block between the two markers in `AGENTS.md` or `CLAUDE.md`, and wire and trigger every hook. Method and sheets S28 to S31: [WIRING.md](WIRING.md). Append the log line for `wiring`.

### 12. Final check

List every entry in `record/` with its status. Verify with a command, not from memory, that each `passing` entry has a pasted check result with a date, and re-run any that does not. An entry whose check cannot run stays `unverified` or `failing`, and you say so. Append the log line for `final`, then report: entry paths, check results, and the log's last line.

