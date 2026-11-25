> Historical reference for interpreting existing setup artifacts. Current onboarding
> follows [SKILL.md](SKILL.md) and [RESUME.md](RESUME.md); the sequence and
> prerequisites below are not requirements for new or resumed onboarding.

# Asking the user

How `harness-setup` talks to the user. Evolve uses its own proportional workflow. Read this file before the first message of a run. Every message and question is in the user's own language; the forms below are in English with placeholders in `<angle brackets>`.

Two layers. Layer one: one **overview message** at the start of the run (where this is going). Layer two: every **question** says where it sits, what it buys the user, and what happens if skipped. The per-question data lives in **question sheets** next to the step they belong to; this file holds the forms and the rules.

## Overview message

Send once, before the first question, in plain words. Four parts, in this order:

1. **Final result**: ONE sentence: what the user will see in the repo when the run ends, naming at most the folder `harness/` and one other file. Say what "harness" means in a few words (the rules, tools and checks around an agent in this repo); do not list record, log, glossary or other file names, they come up later when needed.
2. **Stages**: one line per stage, taken from the stage table in the skill's `SKILL.md`: the plain name, then what the user does there. Say how many stages there are.
3. **Effort**: `{effort}`. Not measured yet, so say so: "I have not timed this." Give no minutes and no count of questions you cannot back. Name what to have ready (one piece of work finished recently).
4. **How it goes**: one question per turn; "not sure" is an answer and I say which default I use; stop any time, the next run continues from `harness/progress.log`. Setup only: the user may ask to jump to stage 5.

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

1. **One idea per question.** No "and" or "or" joining two different asks. A choice between two options is one idea. The named exception is the **list-accepting question**: one question over a table of items, each with a suggested value and a one-line reason; "yes" accepts every row and the user names only the wrong ones; the table does not count toward the five lines of the compact form (labels of step 1, BOUNDARY.md).
2. **Ask about ONE concrete recent thing**: "the last time", the latest merged piece of work, the latest change, a named file or commit. Never "usually", "in general", "would you".
3. **No harness words, anywhere the user reads**: the question, "Why I ask", the suggested answer, "Because", the evidence block. The words in the table "Words the user sees" below, a piece id (pre-tool-gate, P1), a command (`kit show`), and the words rung, kit, lego, tracer bullet, check scope, record entry id are not said; say what the thing is ("a ready-made way to block dangerous commands", "the lightest way that works"). A file or term the user has not met gets a short plain description at its first appearance; if a word cannot be avoided, put it in "Terms" with one line. Do not quote source text in another language; paraphrase. Rule ids shown in brackets in sheet S22 are the one exception.
4. **Look it up, do not ask, and open the file before you name anything in it.** A run said "Codex adds `ship()`" before reading the code; the function was named otherwise. Anything the repo, git history, the pull requests, the tracker files, `harness/` or the log can answer, you read first. Ask only what stays open. Facts are your job, never the user's.
5. **The suggested answer comes from what you looked up** (a name, a commit, a path), stated as an assumption the user can correct. When you found nothing, say so in the suggestion line instead of guessing.
6. **"Not sure" always names the default** you will use, and it must be safe: it keeps the level low, writes nothing, or changes the least. On every yes-gate the default is: the step stays a draft and nothing is written.
7. **Word it so that "yes" accepts your suggestion.**
8. **Stage k/N is the stage table of the skill**, repeated on every question. Do not renumber.
9. **Read the sheet, then render.** The sheet for the step holds the data (Stage, Helps, If skipped, Why, Ask, Terms, Enough, Unsure, Suggest); you fill the placeholders from the repo and pick the form. Translate to the user's language; keep paths, commands and ids as they are.
10. **Translate every label**, not only sentences: Stage, Helps you, If skipped, Why I ask, My suggestion, Because and Decide use the user's language; Terms, Enough and Not sure become plain sentences. Reader runs found untranslated labels embedded in localized messages; translate them consistently.
11. **Evidence block stays short**: the conclusion, then at most three lines per item. A reader run found a 6-line item with command examples unreadable.
12. **Say only what is true.** "If skipped" and "Helps you" come from what the skill really does; no threat, no pressure to answer.
13. **Never present an assumption as the user's word.** After "not sure" or "don't remember", later questions say "assuming <X>, from <PR or file>", never "you chose <X>" or "you said <X>". Never say the user said something (for example "the other roles come later") that they did not say.
14. **A suggestion line exists or it does not.** If you have nothing to suggest, leave the line out and do not mention a suggestion anywhere else in the message. No filler about what the repo lacks ("no revert commit found") unless the user can use it to answer.
15. **No apologetic voice when `s02_work` is `planned`.** Say "planned" and "as you describe it", not "not observed" or "not checked".
16. **Each message stands alone.** The user may have a bad memory and a reader cannot see earlier replies: when a question depends on an earlier answer, restate it in the question ("You told me the pain is <X>"). Use one name per thing for the whole run (do not say "bash" in one place and "shell" in another; do not call the same person "Lan" and "Claude Code" for the same role: say "Lan asked Claude Code to write it").
17. **Counts come with names.** Never say "3 entries" or "2 items" without naming them in plain words in the same message.
18. **Commands in a question are rare and short.** Say first, in a plain sentence, what the command proves and that it changes nothing. Show the command only if it is under about 60 characters with no pipe; otherwise say "I can show you the exact command if you want".
19. **Name what you mean.** "I checked 1 thing" with no thing named, or "about 8 questions" with no reason, left readers guessing. Say which thing, or which questions. A stage over about five questions announces in its first question how many to expect for one item, and that the user may stop after the first item. When a part runs past the number of questions you announced, say once "this part is longer than expected because <reason>, about <n> questions left" and announce the new number; the full and compact forms then use the new number.

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
| building block, shared store | "a ready-made solution included with this tool" (first explain that the tool is the running plugin) |
| context, trust boundary, role card | say what it does in one clause or leave it out |
| fail open, exit 2 | describe behavior: "if the script fails, the operation still runs" |

The opening message explains `harness/` and `AGENTS.md` (the repo's agent instructions). Describe unfamiliar files and commands in plain words at first mention. Use descriptions rather than piece IDs, kit commands or untranslated quotes. "Shared" means reusable unchanged in another project; "project-specific" means it needs editing. The log retains `shared` and `project`.

## Echo the user's own choice

When an answer goes into a table, a summary or a record, show the user's answer, not your suggestion, and say where it came from ("you chose level 4 in the last question"). If the user's answer differs from your suggestion, the user's answer wins; say it once in the echo: "you chose level 4, not my suggestion of 5, so I write 4". The question number does not restart after a resume: take it from the last question you can count in the log, or drop the number and keep the stage line. In tables, "n/a" becomes "not needed" with the reason in a few words, and "unclear" becomes "not known yet".

## Contradiction between git and the account

If what the user tells differs from what git or the pull request shows (for example the user says they wrote the request, git shows an agent as author), do not argue and do not pick silently. Say both in one line, record the user's account, add the git view as a note in the log (`git_differs=<step>`), and ask once whether to keep the user's account. If the user keeps it, move on.

## Confirming a chain

Applies to "who wrote the request, who wrote the code, who reviewed, who merged" (sheet S02) when the card's `s02_chain` is `who` and the evidence is clear. Look the four up in git and the pull request first. If the evidence is clear for all four, do not ask four questions. State the whole chain and ask one idea:

```
For "<title>" I see: request written by <A> (<evidence>), code by <B> (<evidence>), reviewed by <C> (<evidence>), merged by <D> (<evidence>). Is that the chain for that piece of work?
```

If the user says no, ask only which link is wrong, one link per turn. If the evidence is unclear for some links, state the clear ones and ask only about each unclear link, one per turn. With `s02_work` `planned` there is no git evidence: state the chain in the future tense as an assumption built from what the user already said ("For <plan> I assume: request written by <A>, ...") and cite none.

## Incomplete answers

At most one follow-up per question, one question per turn:

1. **General answer** ("usually...", "it depends"): say the same question again, now about the one concrete piece of work already named. It is the same question reworded, not a second one: no new idea, no extra "and".
2. **Partly answered**: accept what was given, say in one sentence what is still missing, and offer your suggested answer for it. Never re-ask what was answered.
3. **"Not sure" or "don't remember"**: use the suggested answer as an assumption, say which one you used, write `unclear` where the record or log takes it, and leave it to edit mode. This is information, not a failure.
4. **"Why do you ask?"**: answer with exactly the one line from "Why I ask", then repeat the question. Add no new question.
5. **Second time without a usable answer**: use the default in "Not sure", say so, move on.

## Evidence block

The simplicity-gate evidence (setup step 3) and any proposal that carries evidence (setup step 4) are shown to the user in this form, not as the raw block of `GATE.md`. It is a question too: full form at the first one of a stage, compact after. The record keeps its English keys (`gate_*`) exactly as before; only what you SAY to the user is in the user's language, and no English label (lighter rung, why not enough, source, answer) is spoken.

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
2. "How sure I am" in one short line per item: whether the documentation says it directly, or whether I could only read a summary of it, and what that means for the user (can they trust the proposal). Do not talk about quotations.
3. Full detail (piece id, url, date read, exact answer) is shown only when the user asks to see it ("show me the sources"); it is always written to `harness/gate.md` and the entry keys as before.
4. Words like "simple way" and "heavier way" replace rung terms. The first time, say the four kinds in plain words in one clause: a rule written in a text file, a reusable instruction, a small command, an outside service.
5. A proposal (tools, folders, team shape) that carries evidence puts its evidence in one line "Because: <...>" and keeps the full block for when the user asks.

## Question sheets

A sheet is the data of one question; the form is above. Sheets live in the sibling file of the step they belong to. Every sheet is a heading `### [Sxx] <title>` (setup) followed by nine fields: Stage, Helps, If skipped, Why, Ask, Terms, Enough, Unsure, Suggest. Where a question has several turns, `Ask` lists them as numbered sub-bullets and each turn carries its own enough, unsure and suggest.

Where each sheet is: S01 to S06 in `BOUNDARY.md`; S09 in `GATE.md`; S10 to S12 in `PROPOSALS.md`; S14 to S20 in `DELEGATION.md`; S21 in `ROLES.md`; S22 in `STANDARDS-STEP.md`; S23 to S27 in `ISOLATION.md`; S28 to S31 in `WIRING.md`. Steps that have no file of their own keep their sheets here, below.

### [S07] Pick the need to work on (step 2)

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: the one thing we set up first is the one that hurts your team most, so the first result you see is worth having
- If skipped: I pick the step of the flow where the repo shows the most rework (reverted or fixed-up commits), else the first step; you can change it at the next question
- Why: I take one need at a time, and this answer decides which one
- Ask: In "<the recent piece of work from stage 1>", where did you or an agent lose the most time or have to redo something?
- Terms: need = one thing you want easier, safer or faster in the flow
- Enough: one place, one or two sentences
- Unsure: say "not sure"; I use the rework spot named under Suggest
- Suggest: "I see <fix commit / reverted change / reopened ticket> after <step>. Is that the spot?" Name what you found; if nothing, leave the suggestion line out entirely and say nothing about it. With branch `pain` (BOUNDARY.md) it is asked in stage 1 (Stage 1/6) and offers the steps of the flow document as choices

### [S08] Confirm the need and the building block (step 2)

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: what gets set up is chosen for the need you named, not guessed
- If skipped: nothing is recorded or installed for this need yet
- Why: this is the proposal for the need you just named; only a yes lets me look at its evidence
- Ask: Shall I deal with "<need in plain words>" with "<the ready-made building block, in plain words>"?
- Terms: building block = a ready-made, described way of doing it from the shared store of this tool; if none fits I say "no ready-made block fits, we design one together"
- Enough: yes, or what to change
- Unsure: say "not sure"; I keep this as a draft and write nothing
- Suggest: yes, with the one-line reason the block's "needed when" text matches your need. If the need goes against a rule written in `AGENTS.md` or `docs/agents/`, quote that rule with its file:line; the user decides

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
