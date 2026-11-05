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

Use the roles of step 7. Ask the user for each cell, one cell per turn; propose from the record and the repo (tools from `record/` tool entries, docs from `AGENTS.md` and `docs/agents/`, skills from the installed ones). `none` is allowed for tools, docs and skills if the user says so; the delegation cell is never `none`.

## Gate: every cell points at something real

`check`: a command that tests each pointer exists (`test -e` for paths and skill files, and for the delegation cell, the entry file and its line in `record/index.md`). Run it; paste the output.

- Every pointer resolves: `passing`.
- Any pointer does not: name the cell and the pointer to the user, go back and fix it (change the pointer, or create the missing thing through the earlier steps and its gate). Status stays `failing`; never write `passing`. Re-run the check after the fix.

Add a profile line to `record/index.md`. A role already recorded is updated in place.
