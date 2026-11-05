# Proposals, one part at a time

Three parts, in order. Present a part, wait, change it until the user settles it, then start the next. Never present two together. Tools were gated in step 3. Every folder or team item, and anything new that comes up while proposing, goes through the gate ([GATE.md](GATE.md)) before the part is settled: show the evidence with the proposal, and append the approved blocks to `harness/gate.md` once the user settles the part.

1. **Tools to install.** The pieces from the gated items, each with its rung. Name what gets installed or generated, where, and nothing else.
2. **Folder layout.** Where the project's harness files live under `harness/`, and which existing folders are left alone. Take names from the repo survey.
3. **Agent team shape.** Take it from the team patterns in the kit, never by loading them all:

```
<skill-dir>/../../../kit/scripts/kit list P       # one line per pattern
<skill-dir>/../../../kit/scripts/kit show P<n>    # one pattern in full
```

(Substitute `<skill-dir>` as in SKILL.md.) The patterns favour the simplest shape. Start from the single agent, show `Use when` and `Avoid when` of the pattern you propose, and pick a heavier one only if the flow you observed matches its `Use when`. State any condition the pattern carries (some are experimental on their platform).

Settled parts are logged one line each (`proposal part=tools|folders|team`). A part the user rejects entirely is logged with `outcome=none`.
