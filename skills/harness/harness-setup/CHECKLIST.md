# Checklist: harness-setup, thin slice and simplicity gate

Manual behavior checklist (seam 2). Every row is externally observable through messages, repo files, or file contents. Rerun and paste results into the ticket whenever the skill changes.

C1-C20 come from ticket 08; ticket 09 strengthens C7, C11 and C13 and adds C21-C31; ticket 10 adds C32 onward (delegation, roles and profiles). C18 now permits delegation and profiles but still excludes GLOSSARY-MAP.md, the Harness block and STANDARDS.md.

Prepare a clean sample repo with setup-matt-pocock-skills output (AGENTS.md Agent skills block and docs/agents/), without harness/; another copy lacks docs/agents/. A stand-in user follows a prepared response script.

| # | Observation | Evidence | Pass condition |
|---|---|---|---|
| C1 | Explicit-invocation frontmatter | Read skill and provider config | disable-model-invocation=true; allow_implicit_invocation=false; only name and description as other keys |
| C2 | Require Matt setup | Repo copy without agent docs | Asks for setup-matt-pocock-skills first and creates no harness directory |
| C3 | One question per turn | Count unanswered questions | Exactly one question per agent turn |
| C4 | Do not ask known facts | Compare questions with root and agent docs | No questions about already configured tracker or domain document locations |
| C5 | Ask the agent platform | Platform question | Asks and records the platform from the user's answer |
| C6 | Confirm the workflow | Turn before step 2 | Reads back the workflow and waits for confirmation |
| C7 | Three questions classify two labels | Classification turns | Asks each question in sequence without self-applying; answers determine shared/project labels shown in the readback |
| C8 | Query the kit through CLI | Command history | Uses list then show; never reads the entire lego CSV |
| C9 | Record index | Record index file | Exists with one pointer per entry |
| C10 | One record entry | harness/record/<entry>.md | Contains kind, choice, reason, check, status and verified_on |
| C11 | One real timestamp per completed step | Log and date -u | Each completed step has one increasing timestamp within the observed session window; agent actually runs date -u |
| C12 | Executed check | Record entry | Pastes actual results; status passing with verified_on |
| C13 | No passing before execution | Interrupt after recording and before checking | Status remains unverified and verified_on stays empty |
| C14 | Temporary file then rename | Messages or mv command | No temporary files remain in the record directory |
| C15 | Resume after interruption | Interrupt after step 1 and rerun | Reads the last log line, names the resume point, and does not repeat finished steps |
| C16 | No duplicates | Rerun | One file per entry; no duplicate index lines or completed step logs |
| C17 | Edit mode | Third run with an existing record | Announces edit mode and asks only about differences |
| C18 | Scope limit | Resulting tree | No new glossary map, Harness block, role profiles, standards or delegation |
| C19 | Generic skill boundaries | Boundary checker on skills | No specific platform or project names |
| C20 | Progressive disclosure | File line counts | SKILL.md below 170 lines; branches in sibling files; body links state when to open them |
| C21 | Simplicity gate for each item | After selecting a piece | Names the next lighter rung in instruction-file, skill, script-cli, mcp and why it is insufficient |
| C22 | Read sources in the current turn | Commands and record | Opens platform docs or runs platform help in the same turn; records source, date and answer per item |
| C23 | User approves evidence | Transcript | Presents the complete evidence list and waits; never self-approves; revises rejected items |
| C24 | Omit unapproved items | User rejects or evidence is absent | No entry file or index line; every recorded item has approved gate evidence |
| C25 | Gate fields | New entry | Includes gate_lighter_rung, gate_why_not_enough, gate_source, gate_read_on, gate_answer and gate_approved |
| C26 | Ordered proposal sections | Transcript | Tools with rungs, folders, then team architecture; waits after each section and re-proposes edited sections |
| C27 | Query team patterns through show | Command history | Uses kit list P and kit show P<number>; never loads complete pattern or lego stores |
| C28 | Legacy ticket-08 entries remain readable | Edit an entry without gate fields | Does not reject or delete it; explains missing gate evidence and runs the gate before changing it |
| C29 | Resume after the gate | Interrupt after evidence approval | New session reads the log and reuses approved evidence without asking again |
| C30 | Generic boundaries | Boundary checker on skills | No fixed platform or project names, including new siblings |
| C31 | Write only approved proposals | Resulting sample repo | Installs and generates only approved items |
| C32 | Delegation follows team architecture | Transcript | Announces separate step 7 after step 4 items are recorded and checked; no delegation questions inside architecture selection |
| C33 | Retrieve framework fragments | Command history | Uses delegation list and axis/step/combine show commands; never loads the entire delegation document |
| C34 | Four axes per role and decision type | Transcript and delegation entries | Covers reversibility, information, level 1-7, permitted zone and escalation threshold; records all four |
| C35 | High levels require zone and threshold | Level 5+ entry | Concrete zone and escalation threshold required before recording; lower levels are not forced to supply them |
| C36 | One-way choices capped at level 3 | One-way decision entry | Level at most 3, or explicit rationale and user confirmation for a higher level |
| C37 | Valid delegation entry and user-selected level | Delegation record files | Correct kind, four axes and approved gate fields; agent suggests but user selects the level |
| C38 | Enable/disable changes the level | Edit delegation for a role | Changes only level and verification date; preserves entry, role and team; no duplicate index or log entries |
| C39 | Four-cell role profiles | Role record files | One file per role with tools, documents, skills and delegation cells |
| C40 | Profile pointers resolve | Prepare a missing file, skill or entry | Executes actual checks, names the broken cell, reworks with user, and marks passing only after a successful rerun |
| C41 | Delegation cell points to a real entry | Passing profile | References a delegation entry present in record files and index |
| C42 | Resume without duplicates | Interrupt after delegation, then rerun twice | Reuses settled answers; no duplicate files, index lines or logs; delegation then roles per role, without redundant record/check lines |
| C43 | Generic boundaries and short body | Boundary checker and line counts | No platform/project names; SKILL.md below 170 lines; body links to DELEGATION.md and ROLES.md |
