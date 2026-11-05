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

Use the roles of step 7. Ask the user for each cell, one cell per turn; propose from the record and the repo (tools from `record/` tool entries, docs from `AGENTS.md` and `docs/agents/`, skills from the installed ones). A skill cell holds the skill name and the path of its `SKILL.md` (ask the user or look in the installed skill folders; do not guess). `gate_*` keys: an instruction-file item like the delegation entry (`gate_lighter_rung: none`, `gate_source` the command you ran), approved by the user's yes to the profile. `none` is allowed for tools, docs and skills if the user says so; the delegation cell is never `none`.

## Gate: every cell points at something real

`check`: a command that tests each pointer exists (`test -e` for paths and skill files, and for the delegation cell, the entry file and its line in `record/index.md`). Run it; paste the output.

- Every pointer resolves: `passing`.
- Any pointer does not: name the cell and the pointer to the user, go back and fix it (change the pointer, or create the missing thing through the earlier steps and its gate). Write the entry as `failing` with the output first, so the state before the fix is on disk; never write `passing`. Re-run the check after the fix.

Add a profile line to `record/index.md`. Append one `roles` log line per entry, after the check result (no separate `record` or `check` lines); the run is done when every role has one. A role already recorded is updated in place.
