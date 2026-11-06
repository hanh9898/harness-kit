# Asking the user

How `harness-setup` and `harness-evolve` talk to the user. Read this file before the first message of a run. Every message and question is in the user's own language; the forms below are in English with placeholders in `<angle brackets>`.

Two layers. Layer one: one **overview message** at the start of the run (where this is going). Layer two: every **question** says where it sits, what it buys the user, and what happens if skipped. The per-question data lives in **question sheets** next to the step they belong to; this file holds the forms and the rules.

## Overview message

Send once, before the first question, in plain words. Four parts, in this order:

1. **Final result**: ONE sentence: what the user will see in the repo when the run ends, naming at most the folder `harness/` and one other file. Say what "harness" means in a few words (the rules, tools and checks around an agent in this repo); do not list record, log, glossary or other file names, they come up later when needed.
2. **Stages**: one line per stage, taken from the stage table in the skill's `SKILL.md`: the plain name, then what the user does there. Say how many stages there are.
3. **Effort**: `{effort}`. Not measured yet, so say so: "I have not timed this." Give no minutes and no count of questions you cannot back. Name what to have ready (setup: one piece of work finished recently; evolve: nothing).
4. **How it goes**: one question per turn; "not sure" is an answer and I say which default I use; stop any time, the next run continues from `harness/progress.log`. Setup only: the user may ask to jump to stage 5.

Note for whoever measures: `{effort}` stays a placeholder until a run with a real person gives a number; then replace the sentence in part 3 with that number and its source.

Setup overview, shape (at most 150 words; a reader run found 300 words and five unfamiliar file names too much; a later run needed 200 words because each stage line carried two clauses: write each stage line as its plain name plus at most six words of what the user does):

```
Before I ask anything, here is where this is going.
End result: <ONE sentence: a folder `harness/` in the repo (say what it holds in a few words: rules, small commands and checks around the agent) plus a few lines added to `AGENTS.md` (say: the file where the repo tells agents how to work)>.
<N> stages:
1. <plain name>. <what you do>.
...
Effort: <I have not timed this>. Have ready: <...>.
How: one question per turn; say "not sure" and I use the stated default; stop any time and the next run picks up from the log.
```

Evolve overview: same four parts, 4 stages, at most 120 words, no "have ready".

## Full form

For the first question of each stage, and for the first question after resuming from the log in the middle of a stage (the user may have lost the thread; start with one sentence saying what was kept):

```
❓ **Q<n>** - **<short title>**
Stage <k>/<N>: <stage name>, question <j> of about <m> in this stage
Helps you at the end: <how this answer changes the final result, in what the user will see>
If skipped: <the true consequence: the default used, what must be redone>
Why I ask: <one line: what this answer decides right now>
<What this question relies on, if it relies on an earlier answer: "You told me: <the user's own words, shortened>.">
<The question: one idea, about ONE concrete recent thing>
<Only if a word is unusual: "<word> means <one line>.">
<ONE sentence for enough and unsure: "<how much is enough>. If you are not sure, say so and I will <the default action>.">

My suggestion: <suggested answer, from what I looked up; "yes" accepts it>
```

Use a phrase in the user's language for the suggestion label, never an arrow symbol: a reader could not distinguish the arrow from the user's own reply.

Example (Vietnamese user, first question of stage 1):

```
❓ **Q2** - **A recent completed piece of work**
Stage 1/6: Understand how your team works, question 2 of about 6 in this stage
Helps you at the end: the recorded responsibilities match how your team works, so stage 4 does not need to be redone.
If skipped: I use the latest piece of work in Git history; if it does not match your team's process, you will need to correct stage 4.
Why I ask: I need a real example to reconstruct the steps from request to merge, rather than guessing.
Which piece of work did you recently finish in this repo (merged or closed)?
A title on one line is enough. If you cannot remember, say "not sure"; I use the latest piece of work in Git history.

My suggestion: the latest work is "<title>" (merged <date>). Use that?
```

## Compact form

For the second and later questions in the same stage. Five lines at most, same labels rule; it still carries the question number and "question j of about m":

```
❓ **Q<n>** - **<title>**  ·  Stage <k>/<N>: <stage name>  ·  question <j> of about <m>
<Why and what it helps, merged: "So that <final result the user sees>; it decides <what follows right away>." Add "You told me: <...>" when the question relies on an earlier answer.>
<The question: one idea, one concrete recent thing>
<Unusual word in one clause, if any> <Enough, and "if you are not sure, say so and I will <default>", as ONE sentence>

My suggestion: <suggested answer>
```

When the question is repeated after a "why do you ask", it keeps its own `Q<n>` heading and stage line; never send a bare repeat.

Keep "If skipped" in the compact form only when the consequence is heavy or not obvious from the "not sure" default.

## Rules

1. **One idea per question.** No "and" or "or" joining two different asks. A choice between two options is one idea.
2. **Ask about ONE concrete recent thing**: "the last time", the latest merged piece of work, the latest change, a named file or commit. Never "usually", "in general", "would you".
3. **No harness words** (rung, kit, gate, lego, tracer bullet, check scope, record entry id) in "Why I ask" and in the question. If a word cannot be avoided, put it in "Terms" with a one-line meaning. Say "a ready-made building block" for a kit piece, "the lightest way that works" for a rung.
4. **Look it up, do not ask, and open the file before you name anything in it.** A run said "Codex adds `ship()`" before reading the code; the function was named otherwise. Anything the repo, git history, the pull requests, the tracker files, `harness/` or the log can answer, you read first. Ask only what stays open. Facts are your job, never the user's.
5. **The suggested answer comes from what you looked up** (a name, a commit, a path), stated as an assumption the user can correct. When you found nothing, say so in the suggestion line instead of guessing.
6. **"Not sure" always names the default** you will use, and it must be safe: it keeps the level low, writes nothing, or changes the least. On every yes-gate the default is: the step stays a draft and nothing is written.
7. **Word it so that "yes" accepts your suggestion.**
8. **Stage k/N is the stage table of the skill**, repeated on every question. Do not renumber.
9. **Read the sheet, then render.** The sheet for the step holds the data (Stage, Helps, If skipped, Why, Ask, Terms, Enough, Unsure, Suggest); you fill the placeholders from the repo and pick the form. Translate to the user's language; keep paths, commands and ids as they are.
10. **Translate every label**, not only sentences: Stage, Helps you, If skipped, Why I ask, My suggestion, Because and Decide use the user's language; Terms, Enough and Not sure become plain sentences. Reader runs found untranslated labels embedded in localized messages; translate them consistently.
11. **The no-harness-words rule covers every line the user reads**, including the suggested answer and "Because": no piece id (D02, P1), no command (`kit show`), no word "gate" or "rung". Say what it is: "a ready-made way to block dangerous commands". Rule ids shown in brackets in sheet S22 are the one exception.
12. **Plain words for files and jargon.** A file or term the user has not met (record, progress log, hook, check) gets a short plain description the first time it appears. Do not quote source text in a language other than the user's; paraphrase it. Do not give a reason the user cannot use ("the repo has no spec yet").
13. **Evidence block stays short**: the conclusion, then at most three lines per item. A reader run found a 6-line item with command examples unreadable.
14. **Say only what is true.** "If skipped" and "Helps you" come from what the skill really does; no threat, no pressure to answer.
15. **Never present an assumption as the user's word.** After "not sure" or "don't remember", later questions say "assuming <X>, from <PR or file>", never "you chose <X>" or "you said <X>". Never say the user said something (for example "the other roles come later") that they did not say.
16. **Never re-ask what was just answered, and never call it missing.** Do not send two messages in a row that ask the same thing. When the user answered part of a question, name only the part still open.
17. **A suggestion line exists or it does not.** If you have nothing to suggest, leave the line out and do not mention a suggestion anywhere else in the message. No filler about what the repo lacks ("no revert commit found") unless the user can use it to answer.
18. **No apologetic voice for a repo without history.** Say "planned" and "as you describe it", not "not observed" or "not checked".
19. **Each message stands alone.** The user may have a bad memory and a reader cannot see earlier replies: when a question depends on an earlier answer, restate it in the question ("You told me the pain is <X>"). Use one name per thing for the whole run (do not say "bash" in one place and "shell" in another; do not call the same person "Lan" and "Claude Code" for the same role: say "Lan asked Claude Code to write it").
20. **Counts come with names.** Never say "3 entries" or "2 items" without naming them in plain words in the same message.
21. **Commands in a question are rare and short.** Say first, in a plain sentence, what the command proves and that it changes nothing. Show the command only if it is under about 60 characters with no pipe; otherwise say "I can show you the exact command if you want".
22. **Name what you mean.** "I checked 1 thing" with no thing named, or "about 8 questions" with no reason, left readers guessing. Say which thing, or which questions. When a part runs past the number of questions you announced, say once "this part is longer than expected because <reason>, about <n> questions left" and announce the new number; the full and compact forms then use the new number.

## Words the user sees

The record and the log keep English keys; what you SAY is in the user's language. Say these in plain words, and the first time a name for a thing appears, add what it is in a few words.

| Do not say | Say (Vietnamese user) |
|---|---|
| gate | a check for whether a more complex solution is needed, or a review of sources |
| hook | a small command that runs automatically before an agent operation |
| script | a small command |
| record, entry | files recording the project's individual choices (`harness/record/`) |
| progress log | a progress journal for resuming later |
| unverified | not yet tried |
| fragile | easy to bypass |
| spec | a document describing the work to do |
| merge, pull request | combine changes into the main branch; request to combine changes (PR) |
| shared / project | shared across projects / specific to this project |
| a prior stage's workflow | the steps from request to merge |
| building block, shared store | "a ready-made solution included with this tool" (first explain that the tool is the running plugin) |
| record entries | "files recording individual choices" in `harness/record/`; use distinct names for distinct concepts |
| context, trust boundary, role card | say what it does in one clause or leave it out |
| fail open, exit 2 | describe behavior: "if the script fails, the operation still runs" |

The opening message explains `harness/` and `AGENTS.md` (the repo's agent instructions). Describe unfamiliar files and commands in plain words at first mention. Use descriptions rather than piece IDs, kit commands or untranslated quotes. "Shared" means reusable unchanged in another project; "project-specific" means it needs editing. The log retains `shared` and `project`.

## Long stages

A stage that will take more than about five questions is announced in its first question: say how many questions to expect for one item, that you take one item first, and that the user may stop after it. Where a sheet allows it, put what git already shows into ONE confirmation (as in "Confirming a chain") instead of one question per field; ask separately only about the fields the evidence does not settle. Stage 4 (who decides what) follows this: see `DELEGATION.md`.

## Echo the user's own choice

When an answer goes into a table, a summary or a record, show the user's answer, not your suggestion, and say where it came from ("you chose level 4 in the last question"). If the user's answer differs from your suggestion, the user's answer wins; say it once in the echo: "you chose level 4, not my suggestion of 5, so I write 4". The question number does not restart after a resume: take it from the last question you can count in the log, or drop the number and keep the stage line. In tables, "n/a" becomes "not needed" with the reason in a few words, and "unclear" becomes "not known yet".

## Contradiction between git and the account

If what the user tells differs from what git or the pull request shows (for example the user says they wrote the request, git shows an agent as author), do not argue and do not pick silently. Say both in one line, record the user's account, add the git view as a note in the log (`git_differs=<step>`), and ask once whether to keep the user's account. If the user keeps it, move on.

## Confirming a chain

Applies to "who wrote the request, who wrote the code, who reviewed, who merged" (sheet S02), and only when the evidence is clear; when the code lives in another repo and the work sits in a tracker, read the tracker and the repo's flow document first, and ask which step hurts most instead. Look the four up in git and the pull request first. If the evidence is clear for all four, do not ask four questions. State the whole chain for the piece of work and ask one idea:

```
For "<title>" I see: request written by <A> (<evidence>), code by <B> (<evidence>), reviewed by <C> (<evidence>), merged by <D> (<evidence>). Is that the chain for that piece of work?
```

If the user says no, ask only which link is wrong, one link per turn. If the evidence is unclear for some links, state the clear ones and ask only about each unclear link, one per turn.

## Repo with no history

You cannot name a finished piece of work: the repo has no commits, only an initial commit, or no merged change, closed ticket or pull request. Then there is no "most recent piece of work" and you do not invent one. Say it in one line, then:

1. Ask for **one piece of work the user plans to do next** in this repo (a named, concrete one), with a suggestion taken from the repo's guidance files or open tickets if any.
2. Ask the "who" questions about that plan in ONE turn, and only when the evidence for them is clear (otherwise ask which step of the flow hurts most, as in S02 of BOUNDARY.md), in the future tense, as a proposed chain built from what the user already said (the agent app named, the guidance files): "For <plan> I assume: request written by <A>, code by <B>, review by <C>, merge by <D>. Is that the plan?" A reader run found four separate who-questions pointless for a one-person repo. If the user says no, ask which link is wrong, one per turn. No git evidence exists, so do not cite any.
3. Skip the "was it different from usual?" question; there is nothing to compare. Write the flow summary in the log as planned, not yet observed.

Sheet S01 is still asked, without "the last piece of work": suggest the app from the guidance files or config folders if there are any, and do not mention co-author signatures when git has none. Sheets S03 to S05 (labels) are asked only for items that really exist beyond the original guidance files; if there are none, say in one line that there is nothing to label yet and that the guidance files count as the project's own, and write `labels=none` in the log. Sheet S07 asks which part of the planned work worries the user most. The same applies to any sheet whose "Ask" names a past piece of work: use the planned work instead, and ignore the "Suggest" line that needs git evidence.

## List question

Name reserved: **list question**, a question whose answer is a list (for example several needs named at once). Condition for use: only when the skill's routing of several needs says so. These two skills do not use it yet; until they do, every question is one idea and takes one answer.

## Incomplete answers

At most one follow-up per question, one question per turn:

1. **General answer** ("usually...", "it depends"): say the same question again, now about the one concrete piece of work already named. It is the same question reworded, not a second one: no new idea, no extra "and".
2. **Partly answered**: accept what was given, say in one sentence what is still missing, and offer your suggested answer for it. Never re-ask what was answered.
3. **"Not sure" or "don't remember"**: use the suggested answer as an assumption, say which one you used, write `unclear` where the record or log takes it, and leave it to edit mode. This is information, not a failure.
4. **"Why do you ask?"**: answer with exactly the one line from "Why I ask", then repeat the question. Add no new question.
5. **Second time without a usable answer**: use the default in "Not sure", say so, move on.
6. **Memory is fallible**: where git or a pull request shows the answer, prefer that evidence and ask for confirmation.

## Evidence block

The simplicity-gate evidence (setup step 3, evolve step 2) and any proposal that carries evidence (setup step 4) are shown to the user in this form, not as the raw block of `GATE.md`. It is a question too: full form at the first one of a stage, compact after. The record keeps its English keys (`gate_*`) exactly as before; only what you SAY to the user is in the user's language, and no English label (lighter rung, why not enough, source, answer) is spoken.

```
❓ **Q<n>** - **<short title in plain words>**
Stage <k>/<N>: <stage name in plain words>
I read: <ONE sentence naming the document in plain words and the need: "I read the official page of <the agent app> about <topic>, to find a way to <the need in plain words>."> Conclusion: <ONE sentence: "a plain rule would not be enough, a small command is" or the like>.
<The need in plain words>: I propose <the way, in plain words> instead of <the simpler way>, because <one short reason a non-expert can follow>.
How sure I am: <"sure: the page says so directly" or "partly sure: for <app> I could only read a summary"; one line, naming the page in words, no url>
If you say no: <what is left out of the result>
Decide: <ONE sentence ending in a question mark>? If yes, <next step>; if no, <what is dropped>.

My suggestion: <recommendation, one line>
```

Hard limits for this block: at most 8 lines of text in total; no command, no code, no quoted source text; no word from "Words the user sees" without its plain version; no "Terms" line unless one word truly needs it (then at most one line). A reader run found a block of ten lines with command examples and an English quote only half readable, and a "reliability" line that talked about quotations instead of what the user needs to know (can I trust this?).

Rules for this block:

1. The conclusion comes first and the decision sentence is the last line before the suggestion: ONE ask, one line. Nothing after it except the suggestion.
2. Needs in plain words only. A piece id, a source id or a rung name is "Terms" at most, never the label of an item.
3. "How sure I am" in one short line per item: whether the documentation says it directly, or whether I could only read a summary of it, and what that means for the user (can they trust the proposal). Do not talk about quotations.
4. Full detail (piece id, url, date read, exact answer) is shown only when the user asks to see it ("show me the sources"); it is always written to `harness/gate.md` and the entry keys as before.
5. Words like "simple way" and "heavier way" replace rung terms. The first time, say the four kinds in plain words in one clause: a rule written in a text file, a reusable instruction, a small command, an outside service.
6. A proposal (tools, folders, team shape) that carries evidence puts its evidence in one line "Because: <...>" and keeps the full block for when the user asks.

## Question sheets

A sheet is the data of one question; the form is above. Sheets live in the sibling file of the step they belong to. Every sheet is a heading `### [Sxx] <title>` (setup) or `### [Vxx]` (evolve) followed by nine fields: Stage, Helps, If skipped, Why, Ask, Terms, Enough, Unsure, Suggest. Where a question has several turns, `Ask` lists them as numbered sub-bullets and each turn carries its own enough, unsure and suggest.

Where each sheet is: S01, S02, S06 in `BOUNDARY.md`; S03 to S05 in `BOUNDARY.md`; S09 in `GATE.md`; S10 to S12 in `PROPOSALS.md`; S14 to S20 in `DELEGATION.md`; S21 in `ROLES.md`; S22 in `STANDARDS-STEP.md`; S23 to S27 in `ISOLATION.md`; S28 to S31 in `WIRING.md`; V01 to V04 in `../harness-evolve/DRIFT.md`; V08, V09 in `../harness-evolve/CHECK-STEP.md`; V10 in `../harness-evolve/UPDATE.md`. Steps that have no file of their own keep their sheets here, below.

### [S07] Pick the need to work on (step 2)

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: the one thing we set up first is the one that hurts your team most, so the first result you see is worth having
- If skipped: I pick the step of the flow where the repo shows the most rework (reverted or fixed-up commits), else the first step; you can change it at the next question
- Why: I take one need at a time, and this answer decides which one
- Ask: In "<the recent piece of work from stage 1>", where did you or an agent lose the most time or have to redo something?
- Terms: need = one thing you want easier, safer or faster in the flow
- Enough: one place, one or two sentences
- Unsure: say "not sure"; I use the rework spot named under Suggest
- Suggest: "I see <fix commit / reverted change / reopened ticket> after <step>. Is that the spot?" Name what you found; if nothing, leave the suggestion line out entirely and say nothing about it

### [S08] Confirm the need and the building block (step 2)

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: what gets set up is chosen for the need you named, not guessed
- If skipped: nothing is recorded or installed for this need yet
- Why: this is the proposal for the need you just named; only a yes lets me look at its evidence
- Ask: Shall I deal with "<need in plain words>" with "<the ready-made building block, in plain words>"?
- Terms: building block = a ready-made, described way of doing it from the shared store of this tool; if none fits I say "no ready-made block fits, we design one together"
- Enough: yes, or what to change
- Unsure: say "not sure"; I keep this as a draft and write nothing
- Suggest: yes, with the one-line reason the block's "needed when" text matches your need

### [S13] Run one check (step 6)

- Stage: 3/6 Record it and try it out
- Helps: you see a real pass or fail for what was set up, not my claim that it works
- If skipped: the entry stays "unverified" and I do not call it working
- Why: a check is a command; I run it only with your yes, and its real output goes into the record
- Ask: Shall I run `<command>` to see whether "<piece in plain words>" works? (ONE command for ONE entry. With several entries, say first "there are N entries, one check each" and ask for the entries one by one; read-only commands may be run together only if you say so and the user agrees.)
- Terms: check = a command whose pass or fail shows the piece works; "not yet tried" (unverified) = recorded but never proven
- Enough: yes, or a different command
- Unsure: say "not sure"; I do not run it and the entry stays unverified
- Suggest: yes, the command that comes from the piece's description; say where it comes from

### [V05] Latest snag (evolve step 1)

- Stage: 2/4 Settle one small change
- Helps: the change we make fixes the place where you were stuck, not something nearby
- If skipped: I propose the first mismatch or failing check from stage 1; if there is none I stop and ask what you want to change
- Why: the smallest change worth making is the one that fixes your latest snag
- Ask: When was the last time this setup got you or an agent stuck, and what happened?
- Terms: harness = the rules, tools and checks around an agent in this repo
- Enough: one or two sentences telling what happened
- Unsure: say "not sure"; I propose the first mismatch or failing check I found in stage 1
- Suggest: "Latest I see: the check of '<entry>' has failed since <date>. Is that the spot?" If nothing failed, leave the suggestion out

### [V06] Confirm the change sentence (evolve step 1)

- Stage: 2/4 Settle one small change
- Helps: I change exactly what you just described, no wider
- If skipped: I keep the sentence as a draft and start nothing
- Why: one sentence fixes what changes, for which role, in which entry; I look up role and entry myself
- Ask: Is this the change you mean: "<what changes, for which role, in which entry>"?
- Terms: entry = one file in `harness/record/` describing one choice
- Enough: yes, or what to correct
- Unsure: say "not sure"; I keep the draft and start nothing
- Suggest: yes; the role and entry are taken from the record, say which file
- Note: when the change raises a level of freedom to 5 or more, the places it may act alone and the stop point are asked with sheet S19 of `DELEGATION.md` (compact form) before the change is settled; below 5 they stay "not needed". If the user is not sure, the level stays where it was and the change is kept as a draft in the log.

### [V07] Approve the evidence list (evolve step 2)

- Stage: 2/4 Settle one small change
- Helps: nothing heavier than needed is added; you see why a lighter way does not do
- If skipped: items without your approval are dropped and not recorded
- Why: for every item this change adds or alters I read the documentation today; only you approve what I found
- Ask: Do you approve this evidence for "<item list>"?
- Terms: lighter way = a simpler way to do the job (for example a rule in a text file instead of a script); evidence = the page or command output I read today, with its date
- Enough: ok, or name the items to edit or reject
- Unsure: say "not sure"; I treat those items as not approved: nothing is recorded or installed for them
- Suggest: ok for the items whose source clearly says what I claim; point out any item whose source says less
