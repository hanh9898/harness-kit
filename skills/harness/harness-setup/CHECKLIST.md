# Checklist: harness-setup, thin slice

Manual behavior checklist (seam 2). Every row is externally observable through messages, repo files, or file contents. Rerun and paste results into the ticket whenever the skill changes.

Prepare a clean sample repo with setup-matt-pocock-skills output (AGENTS.md Agent skills block and docs/agents/), without harness/; another copy lacks docs/agents/. A stand-in user follows a prepared response script.

| # | Observation | Evidence | Pass condition |
|---|---|---|---|
| C1 | Explicit-invocation frontmatter | Read skill and provider config | disable-model-invocation=true; allow_implicit_invocation=false; only name and description as other keys |
| C2 | Require Matt setup | Repo copy without agent docs | Asks for setup-matt-pocock-skills first and creates no harness directory |
| C3 | One question per turn | Count unanswered questions | Exactly one question per agent turn |
| C4 | Do not ask known facts | Compare questions with root and agent docs | No questions about already configured tracker or domain document locations |
| C5 | Ask the agent platform | Platform question | Asks and records the platform from the user's answer |
| C6 | Confirm the workflow | Turn before step 2 | Reads back the workflow and waits for confirmation |
| C7 | Three questions classify two labels | Classification turns | Applies the three questions and shows shared/project labels in the readback |
| C8 | Query the kit through CLI | Command history | Uses list then show; never reads the entire lego CSV |
| C9 | Record index | Record index file | Exists with one pointer per entry |
| C10 | One record entry | harness/record/<entry>.md | Contains kind, choice, reason, check, status and verified_on |
| C11 | One log line per completed step | Progress log | Exactly one chronological line for every completed step |
| C12 | Executed check | Record entry | Pastes actual results; status passing with verified_on |
| C13 | No passing before execution | Interrupt before checking | Status remains unverified and verified_on stays empty |
| C14 | Temporary file then rename | Messages or mv command | No temporary files remain in the record directory |
| C15 | Resume after interruption | Interrupt after step 1 and rerun | Reads the last log line, names the resume point, and does not repeat finished steps |
| C16 | No duplicates | Rerun | One file per entry; no duplicate index lines or completed step logs |
| C17 | Edit mode | Third run with an existing record | Announces edit mode and asks only about differences |
| C18 | Thin-slice scope | Resulting tree | No new glossary map, Harness block, role profiles or standards |
| C19 | Generic skill boundaries | Boundary checker on skills | No specific platform or project names |
| C20 | Progressive disclosure | File line counts | SKILL.md below 170 lines; branches in sibling files; body links state when to open them |
