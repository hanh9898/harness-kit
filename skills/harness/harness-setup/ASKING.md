# Asking the user

How `harness-setup` and `harness-evolve` talk to the user. Read this file before the first message of a run. Every message and question is in the user's own language; the forms below are in English with placeholders in `<angle brackets>`.

Two layers. Layer one: one **overview message** at the start of the run (where this is going). Layer two: every **question** says where it sits, what it buys the user, and what happens if skipped. The per-question data lives in **question sheets** next to the step they belong to; this file holds the forms and the rules.

## Overview message

Send once, before the first question, in plain words. Four parts, in this order:

1. **Final result**: what the user will see in the repo when the run ends (files and folders by name), in one or two sentences. Define "harness" in a few words: the rules, tools and checks around an agent in this repo.
2. **Stages**: one line per stage, taken from the stage table in the skill's `SKILL.md`: the plain name, then what the user does there. Say how many stages there are.
3. **Effort**: `{effort}`. Not measured yet, so say so: "I have not timed this." Give no minutes and no count of questions you cannot back. Name what to have ready (setup: one piece of work finished recently; evolve: nothing).
4. **How it goes**: one question per turn; "not sure" is an answer and I say which default I use; stop any time, the next run continues from `harness/progress.log`. Setup only: the user may ask to jump to stage 5.

Note for whoever measures: `{effort}` stays a placeholder until a run with a real person gives a number; then replace the sentence in part 3 with that number and its source.

Setup overview, shape (about 300 words, keep it shorter if the repo is small):

```
Before I ask anything, here is where this is going.
End result: <what exists in the repo afterwards, by name>.
<N> stages:
1. <plain name>. <what you do>.
...
Effort: <I have not timed this>. Have ready: <...>.
How: one question per turn; say "not sure" and I use the stated default; stop any time and the next run picks up from the log.
```

Evolve overview: same four parts, 4 stages, about 160 words, no "have ready".

## Full form

For the first question of each stage, and for the first question after resuming from the log in the middle of a stage (the user may have lost the thread):

```
❓ **Q<n>** - **<short title>**
Stage <k>/<N>: <stage name>
Helps you at the end: <how this answer changes the final result, in what the user will see>
If skipped: <the true consequence: the default used, what must be redone>
Why I ask: <one line: what this answer decides right now>
<The question: one idea, about ONE concrete recent thing>
Terms: <word> = <one line>   (leave out when there is no unusual word)
Enough: <how much is enough>
Not sure: say "not sure"; I will <the default action>.

➡️ <suggested answer, from what I looked up; "yes" accepts it>
```

Example (Vietnamese user, first question of stage 1):

```
❓ **Q1** - **A recent completed piece of work**
Stage 1/6: Understand how your team works
Helps you at the end: the recorded responsibilities match how your team works, so stage 4 does not need to be redone.
If skipped: I use the latest piece of work in Git history; if it does not match your team's process, you will need to correct stage 4.
Why I ask: I need a real example to reconstruct the workflow rather than guessing.
Which piece of work did you recently finish in this repo (merged or closed)?
Enough: a title on one line.
Not sure: if you cannot remember, I use the latest piece of work in Git history.

➡️ The latest work I found is "<title>" (merged <date>). Use that?
```

## Compact form

For the second and later questions in the same stage. Five lines at most:

```
❓ **Q<n>** - **<title>**  ·  Stage <k>/<N>: <stage name>
<Why I ask and what it helps, merged: "So that <final result the user sees>; it decides <what follows right away>.">
<The question: one idea, one concrete recent thing>
<Terms, if any> · Enough: <...> · Not sure: <default>

➡️ <suggested answer>
```

Keep "If skipped" in the compact form only when the consequence is heavy or not obvious from the "Not sure" default.

## Rules

1. **One idea per question.** No "and" or "or" joining two different asks. A choice between two options is one idea.
2. **Ask about ONE concrete recent thing**: "the last time", the latest merged piece of work, the latest change, a named file or commit. Never "usually", "in general", "would you".
3. **No harness words** (rung, kit, gate, lego, tracer bullet, check scope, record entry id) in "Why I ask" and in the question. If a word cannot be avoided, put it in "Terms" with a one-line meaning. Say "a ready-made building block" for a kit piece, "the lightest way that works" for a rung.
4. **Look it up, do not ask.** Anything the repo, git history, the pull requests, the tracker files, `harness/` or the log can answer, you read first. Ask only what stays open. Facts are your job, never the user's.
5. **The suggested answer comes from what you looked up** (a name, a commit, a path), stated as an assumption the user can correct. When you found nothing, say so in the suggestion line instead of guessing.
6. **"Not sure" always names the default** you will use, and it must be safe: it keeps the level low, writes nothing, or changes the least. On every yes-gate the default is: the step stays a draft and nothing is written.
7. **Word it so that "yes" accepts your suggestion.**
8. **Stage k/N is the stage table of the skill**, repeated on every question. Do not renumber.
9. **Read the sheet, then render.** The sheet for the step holds the data (Stage, Helps, If skipped, Why, Ask, Terms, Enough, Unsure, Suggest); you fill the placeholders from the repo and pick the form. Translate to the user's language; keep paths, commands and ids as they are.
10. **Say only what is true.** "If skipped" and "Helps you" come from what the skill really does; no threat, no pressure to answer.

## Confirming a chain

Applies to "who wrote the request, who wrote the code, who reviewed, who merged" (sheet S02). Look the four up in git and the pull request first. If the evidence is clear for all four, do not ask four questions. State the whole chain for the piece of work and ask one idea:

```
For "<title>" I see: request written by <A> (<evidence>), code by <B> (<evidence>), reviewed by <C> (<evidence>), merged by <D> (<evidence>). Is that the chain for that piece of work?
```

If the user says no, ask only which link is wrong, one link per turn. If the evidence is unclear for some links, state the clear ones and ask only about each unclear link, one per turn.

## Repo with no history

You cannot name a finished piece of work: the repo has no commits, only an initial commit, or no merged change, closed ticket or pull request. Then there is no "most recent piece of work" and you do not invent one. Say it in one line, then:

1. Ask for **one piece of work the user plans to do next** in this repo (a named, concrete one), with a suggestion taken from the repo's guidance files or open tickets if any.
2. Ask the "who" questions about that plan, in the future tense ("who will write the request for <plan>?"), suggesting from the guidance files; no git evidence exists, so the chain confirmation does not apply.
3. Skip the "was it different from usual?" question; there is nothing to compare. Write the flow summary in the log as planned, not yet observed.

The same applies to any sheet whose "Ask" names a past piece of work: use the planned work instead, and ignore the "Suggest" line that needs git evidence.

## List question

Name reserved: **list question**, a question whose answer is a list (for example several needs named at once). Condition for use: only when the skill's routing of several needs says so. These two skills do not use it yet; until they do, every question is one idea and takes one answer.

## Incomplete answers

At most one follow-up per question, one question per turn:

1. **General answer** ("usually...", "it depends"): bring it back to the one concrete piece of work already named: "For <the piece of work>, who did that step?"
2. **Partly answered**: accept what was given, say in one sentence what is still missing, and offer your suggested answer for it. Never re-ask what was answered.
3. **"Not sure" or "don't remember"**: use the suggested answer as an assumption, say which one you used, write `unclear` where the record or log takes it, and leave it to edit mode. This is information, not a failure.
4. **"Why do you ask?"**: answer with exactly the one line from "Why I ask", then repeat the question. Add no new question.
5. **Second time without a usable answer**: use the default in "Not sure", say so, move on.
6. **Memory is fallible**: where git or a pull request shows the answer, prefer that evidence and ask for confirmation.

## Evidence block

The simplicity-gate evidence (setup step 3, evolve step 2) and any proposal that carries evidence (setup step 4) are shown to the user in this form, not as the raw block of `GATE.md`. It is a question too: full form at the first one of a stage, compact after. The record keeps its English keys (`gate_*`) exactly as before; only what you SAY to the user is in the user's language, and no English label (lighter rung, why not enough, source, answer) is spoken.

```
❓ **Q<n>** - **Do you approve what I found?**
Stage <k>/<N>: <stage name in plain words>
<I checked: one sentence of conclusion: "I checked <N> things and <M> need nothing heavier than <the lightest way>; <K> need a closer look: <name>.">
For each item, one short group:
  <the need in plain words, never a piece id or code like L05>: <the way I propose, in plain words> instead of <the lighter way>, because <one line>.
  Reliability: <which source I quoted word for word, which one I only have a summary of, in one short line>
Helps you at the end: <what stays out of the result if you say no>
Decide: <ONE sentence: "Do you approve this?"> If yes, the next step is <...>; if you reject an item, I drop it and record nothing for it.
Not sure: <default: items without your approval are dropped; nothing recorded or installed>

➡️ <your recommendation: approve the items whose source says what I claim; name any that say less>
```

Rules for this block:

1. The conclusion comes first and the decision sentence is the last line before the suggestion: ONE ask, one line. Nothing after it except the suggestion.
2. Needs in plain words only. A piece id, a source id or a rung name is "Terms" at most, never the label of an item.
3. Reliability in one short line per item: say which source was quoted word for word and which one only gave a summary.
4. Full detail (piece id, url, date read, exact answer) is shown only when the user asks to see it ("show me the sources"); it is always written to `harness/gate.md` and the entry keys as before.
5. Words like "lighter way" and "heavier way" replace rung terms; explain "way" levels once under Terms the first time: a rule in a text file, a reusable instruction (skill), a small script, an outside service (MCP).
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
- Suggest: "I see <fix commit / reverted change / reopened ticket> after <step>. Is that the spot?" Name what you found; if nothing, say the repo shows no rework

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
- Ask: Shall I run `<command>` to see whether "<piece in plain words>" works?
- Terms: check = a command whose pass or fail shows the piece works; unverified = recorded but never proven
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
- Suggest: "Latest I see: the check of '<entry>' has failed since <date>. Is that the spot?" If nothing failed, say the record and the files agree

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
