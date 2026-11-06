# Boundary: three questions, two labels

Classify every item the flow turned up (tool, document, data, role, script). Two labels only:

- `shared`: names nothing about this project; works unchanged in another project.
- `project`: carries this project's name, data, paths, tools or roles. Business documents, data snapshots and tools that process them are `project` harness too.

Write each question from its sheet below, in the forms of [ASKING.md](ASKING.md). Put these to the user in order, one per turn, for the items not yet settled; stop at the first answer that settles each item. A suggested label is a proposal until the user answers.

1. **Own names or values?** Project name, machine path, entry from a project log, project-only tool or role. Yes: `project`.
2. **Delete test.** Carry it into another project: still true and still runs? Yes: `shared`.
3. **Direction.** Does the `shared` part point back at the project? Yes: the dependency is upside down. Move the pointer into the `project` side, or split the item.

Where people can see the item (its visibility) is a note on the item, never a third label.

A `shared` tool stays under `harness/tools/` and the record notes it as a candidate for the kit; kit changes go through a change to the plugin.

## Question sheets (step 1)

Forms and rules: [ASKING.md](ASKING.md). Stage 1 opens with S01 (full form); S02-S06 are compact. Order: S01, S02, then S03-S05 per unsettled item, then S06. With no history, ask S03-S05 only about existing items beyond original guidance files; otherwise explain the skip and log `labels=none`. User-facing labels are "shared across projects" and "specific to this project"; the log retains `shared` and `project`.

### [S01] Which agent app the team uses

- Stage: 1/6 Understand how your team works
- Helps: the tools and files I set up are the ones your agent app really reads
- If skipped: I take the app the repo's config folders point to and say which; a wrong guess means files in the wrong place
- Why: folders and settings differ from one agent app to another
- Ask: Which agent app did your team use for the last piece of work in this repo? (Repo with no history: "Which agent app will your team use for the work you plan?")
- Terms: agent app = the program in which an AI agent works on your code; if you name a folder such as the settings folder of the app, say what it is
- Enough: one name
- Unsure: say "not sure"; I use the app named under Suggest and tell you which; with no Suggest (empty repo, no config folder), I record no app yet and ask again at stage 5 when files are wired
- Suggest: "The repo has <config folder> and commits signed <trailer>, so I think it is <app>. Is that right?" Look at config folders and commit trailers first; the platform of the answer is what the log records. Leave out the trailer part when git has none

### [S02] How one piece of work went from start to finish

Before turn 1, read the repo's own flow documents (files named like project-flow, workflow or process under `docs/`, and `docs/agents/issue-tracker.md`) and the tracker they name. If the current repo's git holds no product work because the code lives in another repo (a control repo: the work sits in a tracker), say so in one line and take the recent piece of work from the tracker or from the user, never from this repo's git. Ask the "who" chain (turns 2 to 5) only when the evidence for it is clear. If it is not, replace it with one question: which step of the flow hurts most, built from the steps in the flow document. A run showed users reject "who wrote, who merged": it names three people and is not yet a process.

- Stage: 1/6 Understand how your team works
- Helps: the rules about who does what match how your team really works, so stage 4 does not start over
- If skipped: I use what git shows for the latest piece of work and mark the flow as not confirmed by you
- Why: I build the path of work from one real example instead of guessing
- Ask (one turn each, in this order; skip any turn the chain confirmation of ASKING.md already settled):
  1. Work: Which piece of work did you finish most recently (merged or closed)? Enough: its title. Unsure: I take the last one in git history. Suggest: "<title> (merge <date>). Use it?"
  2. Request: For "<title>", who wrote the description of what to do: you, or an agent? Enough: one name. Unsure: I take the author of the first commit. Suggest: author of the spec or ticket file's first commit, with a co-author trailer if there is one
  3. Code: For that piece of work, who wrote the code: you, or an agent (which)? Enough: one name. Unsure: the author of most commits in the change. Suggest: that author
  4. Review: For that piece of work, who looked at the code before it was merged? Enough: a name or "nobody". Unsure: whoever commented or approved on the pull request. Suggest: that name, or "nobody I can see"
  5. Merge: For that piece of work, who pressed merge? Enough: one name. Unsure: the name on the merge commit. Suggest: that name
  6. Different: In those steps, which one went differently this time than you usually do it? Enough: "none" or one step. Unsure: I write the flow from this one piece and note that it is based on this one piece. Suggest: none differed
- Terms: description of what to do (spec) = the document saying what to build; ticket = one small task cut from it; both live in the folder where this repo keeps them
- Enough: per turn, above
- Unsure: per turn, above
- Suggest: per turn, above. If git shows all four of turns 2 to 5 clearly, use the chain confirmation instead of those four turns. Empty history: the "Repo with no history" branch of ASKING.md replaces turn 1 and drops turn 6. If the user's account differs from git, follow "Contradiction between git and the account" in ASKING.md

### [S03] Does it carry this project's own names or values

- Stage: 1/6 Understand how your team works
- Helps: things that belong to this project stay here, and shared things can be reused elsewhere
- If skipped: I label it `project`; a wrong `project` label costs only a move later, no data is lost
- Why: this answer decides whether the item goes in the shared store or stays in this project
- Ask: In "<item>" I found "<concrete detail: a project name, a machine path, a line from a project log>". Is that specific to this project?
- Terms: label = a tag saying whether the item could be copied unchanged into another project ("shared") or would need editing there ("this project's own"); the project's own = carries this project's name, paths, data, tools or roles
- Enough: yes or no
- Unsure: say "not sure"; I label it `project`
- Suggest: "Yes, it names this project, so I label it project."

### [S04] Would it work unchanged in another project

- Stage: 1/6 Understand how your team works
- Helps: whatever works anywhere is kept apart so other projects can use it
- If skipped: I label it `project`; mislabelling costs only a move later
- Why: asked only for items S03 did not settle; it decides shared or project
- Ask: In "<item>" there is "<concrete detail, with file and line>". If you copied the whole file into another project, would that line need changing?
- Terms: shared and project as in S03
- Enough: "needs changing" or "no change needed"
- Unsure: say "not sure"; I label it `project`
- Suggest: "It needs changing, so I label it project. Agree?"

### [S05] Does the shared part depend on the project

- Stage: 1/6 Understand how your team works
- Helps: shared parts stay free of project details, so they really can be reused
- If skipped: I label the item `project`, the safe side
- Why: asked only for an item labelled shared in which I found a pointer to something of this project; I grep for the pointer first and ask only when I find one
- Ask: In "<shared item>" I found a pointer to "<project thing>" (<file>:<line>). Does the shared item need that pointer to work?
- Terms: pointer = a path, name or reference from one file to another thing
- Enough: yes or no
- Unsure: say "not sure"; I label the item `project`
- Suggest: "No, it can go; I move the pointer to the project side. Agree?" If yes (it needs the pointer): split the item or move the pointer

### [S06] Read the description of the flow back

- Stage: 1/6 Understand how your team works
- Helps: everything later is built on a description of your flow that you have confirmed
- If skipped: I do not move on; I point at the one line I am least sure of and ask about that line only
- Why: this is the last check of stage 1 before we choose what to improve
- Ask: Is this description of how work moves in your team right? <description with the labels>
- Terms: label = "shared across projects" or "this project's own", as in the earlier question
- Enough: "right", or the line that is wrong
- Unsure: say "not sure"; I ask only about the line I am least sure of
- Suggest: "Right." Say which parts came from your answers and which from the repo
