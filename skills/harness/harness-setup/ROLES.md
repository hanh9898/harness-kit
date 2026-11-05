# Roles and profiles (step 8)

One profile per role. A profile is a map of four cells; each cell points to something that exists now.

## Entry

`record/role-<role>.md`, `kind: role-profile`, other keys as in [RECORD-FORMAT.md](RECORD-FORMAT.md). Body is four cells:

```
## Profile

- tools: <paths or record entries, or "none">
- docs: <paths of documents the role reads, or "none">
- skills: <skill names, each with the path of its SKILL.md, or "none">
- delegation: <record/delegation-<role>.md>
```

Use the roles of step 7. Write each question from sheet S21 below, in the forms of [ASKING.md](ASKING.md). Ask the user for each cell, one cell per turn; propose from the record and the repo (tools from `record/` tool entries, docs from `AGENTS.md` and `docs/agents/`, skills from the installed ones). A skill cell holds the skill name and the path of its `SKILL.md` (ask the user or look in the installed skill folders; do not guess). `gate_*` keys: an instruction-file item like the delegation entry (`gate_lighter_rung: none`, `gate_source` the command you ran), approved by the user's yes to the profile. `none` is allowed for tools, docs and skills if the user says so; the delegation cell is never `none`.

## Gate: every cell points at something real

`check`: a command that tests each pointer exists (`test -e` for paths and skill files, and for the delegation cell, the entry file and its line in `record/index.md`). Run it; paste the output.

- Every pointer resolves: `passing`.
- Any pointer does not: name the cell and the pointer to the user, go back and fix it (change the pointer, or create the missing thing through the earlier steps and its gate). Write the entry as `failing` with the output first, so the state before the fix is on disk; never write `passing`. Re-run the check after the fix.

Add a profile line to `record/index.md`. Append one `roles` log line per entry, after the check result (no separate `record` or `check` lines); the run is done when every role has one. A role already recorded is updated in place.

## Question sheets (step 8)

### [S21] What a role needs, one cell per turn

- Stage: 4/6 Decide who may decide what
- Helps: each role starts with the tools, documents and skills it needs and nothing else
- If skipped: I use my suggestion for tools, documents and skills; the delegation cell points at the role's own entry (never none)
- Why: a profile tells the role what it may use; I fill one cell per turn
- Ask (one cell per turn): For "<recent piece of work>", which <tools | documents | skills> does <role> need? (The fourth turn is the delegation cell: confirm the pointer to the role's own entry.)
- Terms: profile = four lists telling a role what it can use: tools, documents, skills, and how much it decides alone
- Enough: a list, or "none"
- Unsure: say "not sure"; I use my suggestion
- Suggest: tools from the tool entries of the record, documents from the guidance files and docs folder of the repo, skills from the installed ones; for a skill give its name and the path of its description file, which I look up, never guess
