# Checklist: harness-setup, thin slice and simplicity gate

Manual behavior checklist (seam 2). Every row is externally observable through messages, repo files, or file contents. Rerun and paste results into the ticket whenever the skill changes.

C1-C20 come from ticket 08; ticket 09 strengthens C7, C11 and C13 and adds C21 onward.

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
