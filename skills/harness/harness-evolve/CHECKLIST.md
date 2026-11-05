# Checklist: harness-evolve (seam 3)

Manual behavior checklist. Every row is externally observable through agent messages, repo files, or file contents. Prepared ahead of skill implementation (ticket 12); rerun and paste results into the ticket whenever the skill changes.

Prepare a Git repo copy that has completed `harness-setup` (with `harness/record/`, `harness/progress.log`, `harness/STANDARDS.md`, the `### Harness` block in `AGENTS.md`, and a local Markdown tracker), plus another copy without `harness/record/`. A stand-in user follows a prepared script. The coordinator prepares drift, overdue, and failing-check cases before the session.

| # | Observation | Evidence | Pass condition |
|---|---|---|---|
| E1 | Explicit-invocation frontmatter | Read `SKILL.md` and `agents/openai.yaml` | `disable-model-invocation: true`; `allow_implicit_invocation: false`; only `name` and `description` as other keys |
| E2 | Preflight | Run without `harness/record/` | Asks the user to run `harness-setup`, stops, and creates no files |
| E3 | One question per turn | Count unanswered questions in each turn | Exactly one question awaits an answer per turn |
| E4 | Read record and log first | Commands and messages | Reads the index, entries and final log lines before questions; names the logged step and resume point |
| E5 | Report drift before editing | Remove or modify a referenced file and inspect hashes | Names the entry and mismatch; asks whether to fix record or reality; neither changes before the answer |
| E6 | Apply the chosen drift resolution | User chooses a side | Changes only the selected side |
| E7 | Detect overdue entries | Prepare an old verification date | Reports the entry, date and overdue state; asks what to handle |
| E8 | Detect failed checks | Prepare a failing entry or command | Reports it, reruns or lists the check; never retains passing for a failed check |
| E9 | Detect unfinished work | Log a change or work without an update | Reports unfinished work, asks whether to continue or start new, and reuses logged answers |
| E10 | One-sentence change with role and piece | Step 1 message | Names the change, affected role, and piece (kit ID or record entry); user confirms |
| E11 | Query the kit through its CLI | Command history | Uses `kit list` and `kit show`; does not load entire `legos.csv`, `rules.csv`, or `patterns.md` |
| E12 | Rerun the simplicity gate | Messages and record entry | For each added or changed item, names a lighter rung, reads docs or runs `--help` in that turn, records source, date and answer, and waits for user approval |
| E13 | A sufficient lighter rung returns to step 1 | Prepare a case where the lighter rung suffices | Agent revises the change and reruns the gate rather than implementing the heavier option |
| E14 | Reuse setup's GATE.md | List skill files and inspect links | Evolve has no GATE.md copy; its body links to the setup file by a relative skill path |
| E15 | Complete the Matt flow | Spec, tickets, implementation and transcript | `to-spec` writes the spec; `to-tickets` writes tickets; `implement` completes them; each has a check; order is correct |
| E16 | Actual or fallback skill invocation | Transcript | States which Matt skills could be invoked; if unavailable, explains why and produces the same artifacts manually with lower confidence |
| E17 | Run checks and record results | Final record entry | Each real command, exit code and output is recorded; `passing` and today's `verified_on` follow successful execution |
| E18 | Review prompt names the harness standard | Prompt to `code-review` or reviewer | Names `harness/STANDARDS.md` and excludes product standards for the harness diff |
| E19 | Rework an unwaived failure | Prepare a failing check | Does not mark passing; returns to step 3, reworks and reruns until passing |
| E20 | Record waiver reasons | User waives | Records the user's reason, date and identity; status stays failing; asks for a missing reason without inventing one |
| E21 | Run an additional team verification | Change a structural `kind: team` entry | Explains the structural check's limits; runs an additional task or records "not run"; never claims an untested team works |
| E22 | Safe record updates | Record files and command history | No leftover temporary files or duplicate index lines; `verified_on` is the actual check date |
| E23 | Real log timestamps | Log and agent's `date -u` command | One increasing timestamped line per completed step, within the observed time window |
| E24 | Lessons and proposed standard changes | Lessons file and messages | Appends lessons; proposes missing rules as text; edits `harness/STANDARDS.md` only after approval |
| E25 | Remind the user about Matt's retro | Final message | Mentions manual or supported scheduled `retro`; never invokes it automatically |
| E26 | Resume after interruption | Interrupt after each change, work, or check log line, then restart | Reads the last log line, resumes the correct step, and does not repeat settled questions |
| E27 | Idempotent rerun | Rerun a completed session with no changes | No duplicate entries, index lines, lessons, or step logs; files unchanged; identical final read lines are not repeated |
| E28 | Stay within scope | Git status and hashes | Does not change kit, coding standards, or product code outside the agreed change; writes only harness files and explicitly affected paths |
| E29 | Boundaries and length | Boundary checker and line counts | No fixed platform or project names; SKILL.md below 170 lines; body links explain when to open sibling files |
