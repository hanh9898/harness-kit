# Checklist: harness-setup, thin slice and simplicity gate

Manual behavior checklist (seam 2). Every row is externally observable through messages, repo files, or file contents. Rerun and paste results into the ticket whenever the skill changes.

C1-C20 come from ticket 08; ticket 09 strengthens C7, C11 and C13 and adds C21-C31; ticket 10 adds C32-C43 (delegation, roles and profiles); ticket 11 adds C44 onward (standards, isolation, map, marker, hooks and final checks). C18 now permits those items but excludes coding standards and paths outside harness/ unless a step names them.

Prepare a clean sample repo with setup-matt-pocock-skills output (AGENTS.md Agent skills block and docs/agents/), without harness/; another copy lacks docs/agents/. A stand-in user follows a prepared response script.

| # | Observation | Evidence | Pass condition |
|---|---|---|---|
| C1 | Explicit-invocation frontmatter | Read skill and provider config | disable-model-invocation=true; allow_implicit_invocation=false; only name and description as other keys |
| C2 | Require Matt setup | Repo copy without agent docs | Asks for setup-matt-pocock-skills first and creates no harness directory |
| C3 | One question per turn | Count unanswered questions | Exactly one question per agent turn |
| C4 | Do not ask known facts | Compare questions with root and agent docs | No questions about already configured tracker or domain document locations |
| C5 | Ask the agent platform | Platform question | Asks and records the platform from the user's answer |
| C6 | Confirm the workflow | Turn before step 2 | Reads back the workflow and waits for confirmation |
| C7 | List-accepting classification | Classification turn | Presents one table with suggested labels and one-line reasons; S03-S05 only for disputed or unknown rows; user determines shared/project labels |
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
| C44 | Select standards through kit | Command history | Lists and shows individual rules; never loads rules.csv; offers verified gate rules first and only topics relevant to selected groups |
| C45 | Harness standard starts with scope | harness/STANDARDS.md | First line limits scope to harness changes in the user's language; each rule has a kit ID and check method |
| C46 | Standard entry is a pointer | Standard record files | Correct kind, points to a standards section, includes check and gate fields, and does not copy rule text |
| C47 | Execute standard checks | Standard entries | Actual results recorded; passing and verification date follow execution |
| C48 | Isolation is a separate question | Transcript | After standards, asks whether harness content should stay out of product commits, comments and PRs; records nothing before asking |
| C49 | User selects isolation | Transcript | Offers rules, checker and review for approval; if rejected, creates no isolation entry and logs outcome=none |
| C50 | Isolation check runs on a real case | Isolation entry | Executable check actually tests an operation with harness traces, records evidence, and never claims unexecuted verification passed |
| C51 | Only propose coding-standard scope | Transcript, Git status and hashes | Shows exact proposed text for the user to add; never edits or creates CODING_STANDARDS.md |
| C52 | Create map with product context | Glossary map | Adds root product glossary and ADR pointers; preserves existing rows and adds only the harness row |
| C53 | Harness map row includes both paths | Glossary map | One description with harness glossary AND ADR paths; no copied terms |
| C54 | Context relationships | Glossary map | Relationships section states harness reads product and product does not name harness; notes known same-name/different-meaning terms |
| C55 | Domain docs become multi-context | Root and domain agent docs | Domain summary points to glossary map; domain doc includes harness ADR paths exactly once |
| C56 | Harness context foundations | Harness glossary and ADR directory | Both exist; glossary opens with kit README link; preserves existing contents |
| C57 | Harness block contains only pointers | Root instructions | One marked Harness block inside Agent skills; only record index, standards and ADR pointers |
| C58 | Preserve outside markers | Before/after diff | All lines outside markers unchanged except the separately assessed domain summary |
| C59 | Replace rather than append | Rerun marker writing after manual edits | Exactly one marker pair and Harness block; restores expected contents; no duplicate map rows, sections, entries or logs |
| C60 | Structural team checks are labelled | Team entry and record format | check_scope=structural; documentation says passing does not prove the team runs |
| C61 | Hook is actually wired | Platform config and command history | Uses selected platform, writes hook into the entry's named config, preserves existing config |
| C62 | Hook actually triggers | Entry evidence | Triggers and records a real event; if unavailable, names the unverified platform and does not mark wiring passing |
| C63 | Final verification | Transcript and records | Lists every entry/status, checks actual evidence for each passing entry, and reports failures |
| C64 | Resume within steps 9-12 | Interrupt after standards, isolation or wiring logs | Reads log, resumes correct step, reuses answers and creates no duplicates |
| C65 | Edit only differences | Rerun a completed setup | Announces edit mode; no-change run does not repeat standards, isolation or map questions; files unchanged |
| C66 | Boundaries and short body | Boundary checker and line counts | No platform/project names; SKILL.md below 170 lines; body links explain standards, isolation and wiring siblings |
| C67 | Harness standards in code review | Review a sample product diff | Records loaded standards and whether harness standards affected product code as an observation, not a pass criterion |

## Question layer (ticket 19): C80 to C93

C68-C78 are reserved for ticket 20 (routing multiple needs); ticket 19 starts at C80. Also prepare one repo with history and another with one commit. The stand-in user follows a response script and records whether each question's purpose was clear and whether the first answer was sufficient.

| # | Observation | Evidence | Pass condition |
|---|---|---|---|
| C80 | Asking document sections | Document and question-layer tests | Overview, full/compact forms, rules, grouped confirmations, list-accepting conditions and incomplete answers; no absolute paths |
| C81 | Overview before first question | Opening transcript | Describes visible outcome, six stage lines and user actions, effort and method, uncertainty and resume behavior in the user's language |
| C82 | Honest effort estimate | Opening turn | Says time is not measured, invents no minutes, and notes a real-user run will measure it |
| C83 | Full form opens each stage | Transcript | Includes Stage k/6, benefit, skip consequence, purpose, question, sufficient answer, uncertainty default and suggestion |
| C84 | Later questions are compact | Transcript | At most five lines with stage, combined purpose/impact, question, sufficient-answer/default line and suggestion |
| C85 | One idea and plain language | Transcript | One idea per question; no unexplained framework jargon; unfamiliar terms receive plain definitions |
| C86 | Ask about concrete recent work | Transcript | Process questions name a real task, PR or commit rather than asking about usual behavior |
| C87 | Look up facts before asking | Commands and suggestions | Reads Git, PRs and files first; suggestions cite findings; does not ask facts the repo already supplies |
| C88 | Grouped chain confirmation | Clear Git evidence for request/code/review/merge | States the entire four-step chain and asks once; asks only missing links when evidence is incomplete |
| C89 | Situation card selects planned work | One-commit repo with history=none | Situation checker selects s02_work=planned; asks about future work and roles instead of recent completed work |
| C90 | Handle incomplete answers | General, partial, uncertain and why-ask cases | Refocuses on the same task; accepts supplied parts; uses stated defaults; explains purpose in one sentence; at most one follow-up |
| C91 | Full form after mid-stage resume | Interrupt stage 4 and rerun | First resumed question uses the full form even within an existing stage |
| C92 | Complete question sheets | Question-layer tests and line counts | S01-S31 and V01-V10 have nine fields each; setup SKILL.md at most 110 lines; each question step links to its sheet |
| C93 | Stand-in user comprehension | Compare the new run with the earlier transcript | Records clarification and incomplete-answer counts against the old run; acknowledges stand-in agent limitations |
| C94 | Readable gate evidence | Steps 3 and 4 messages | Consistent language, conclusion first, plain needs, explained unfamiliar terms, stage/name, and one reliability line per source |
| C95 | One approval with consequences | Evidence block | Exactly one decision question last before suggestion; names next step or rejection result; full details only on request; stored evidence remains complete |

## Two-reader question-layer revisions (ticket 22): C96 to C108

Each row corresponds to an issue found by two unscripted readers (question-19-reader-A.md and -B.md). Replay sessions for a repo with history and a one-commit repo using stand-in user agents, then have two other agents read only assistant messages. Anything readers cannot infer without user messages counts as a message defect.

| # | Observation | Evidence | Pass condition |
|---|---|---|---|
| C96 | Consistent user-facing language | Reader-assessed transcript | Avoids unexplained foreign labels and jargon; describes unfamiliar commands/files once; uses no piece IDs or untranslated quotes; record/log keys remain English |
| C97 | Short opening | Opening turn | About 150 words maximum; one outcome sentence; at most two filenames beyond harness/; one line per stage; reader overload at most moderate |
| C98 | Explain all seven levels | Autonomy question | One plain line per level identifying the decision maker; readers can distinguish adjacent levels without extra framework jargon |
| C99 | Preserve the selected level | Selection, readback and record | Table matches the user's stated level and cites the answer; inapplicable or unknown cells use plain explanations |
| C100 | Announce and group stage 4 | First stage 4 turn | Announces questions per role, defaults to one decision type, permits one role first; at most eight questions per role/type below level 5; combines evidenced reversibility and information questions; groups all four known profile cells |
| C101 | Git/account contradictions | User account differs from Git | States both once, records the user's account and discrepancy, allows one correction without arguing |
| C102 | Incomplete answers remain one idea | General or partial answers | Rephrases the same concrete question without adding an idea; never requests an already supplied answer |
| C103 | Assumptions are not user choices | Questions after uncertainty | Calls the choice an assumption from a named source, never attributes unspoken choices to the user |
| C104 | One check is one command | Step 6 | Announces N entries with one check each and asks per entry; may explicitly group read-only checks |
| C105 | Shared/project labels | Stage 1 and log | Explains reuse unchanged versus project-specific editing in one sentence; user-facing labels are plain; log retains shared/project |
| C106 | Empty repo questions | One-commit repo | S01 still asks, based on guidance files if present; S03-S05 only for real items beyond root instructions; otherwise explains no items need labels and logs labels=none |
| C107 | Voice and unnecessary lines | Reports and need selection | No apologetic voice for planned work; no suggestion references without a suggestion; no irrelevant missing-Git-evidence remarks |
| C108 | Two new readers | question-22-reader reports | Each reader finds unfamiliar terms in at most 10% of questions, none in gate evidence blocks; zero ambiguous or contradictory questions |
| C109 | Hand off an existing harness without moving it | prior_harness is not none and user requests reorganization | Setup creates adopted or needs-change folder records, makes no move plan and moves nothing; evolve receives needs-change entries |
| C110 | Control repo uses tracker work | Git contains no product work | Reads flow and tracker, explains that code is elsewhere, gets work from tracker or user; asks for the painful step rather than an unsupported author/merger chain |
| C111 | Step 0 Agent skills block | Agent docs exist but root heading is absent | Shows the three-section draft, waits for approval, preserves surrounding content and setup prerequisites |
| C112 | Revise a logged decision | User changes a prior decision | Appends the same step with revised=<old timestamp>; original stays unchanged; log checker passes |
| C113 | Update question estimates | A section exceeds the estimate | Explains why once, announces the remaining count, and uses the new estimate |
| C114 | Inspect and name every relevant kit group | Step 2 CLI history | Lists every kit group related to the need, including scheduling for automation; logs groups=; log checker passes |
| C115 | Situation card | After step 1 | Nine factual key:value lines; situation checker passes; confirmed=yes only after flow approval; sheets and step 10 follow printed branches |