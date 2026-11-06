# Proposals, one part at a time

Three parts, in order. Write each proposal from its sheet below, in the forms of [ASKING.md](ASKING.md); the evidence of a part goes in one "Because" line, with the full evidence block only when the user asks. Present a part, wait, change it until the user settles it, then start the next. Never present two together. Tools were gated in step 3. Every folder or team item, and anything new that comes up while proposing, goes through the gate ([GATE.md](GATE.md)) before the part is settled: show the evidence with the proposal, and append the approved blocks to `harness/gate.md` once the user settles the part.

1. **Tools to install.** The pieces from the gated items, each with its rung. Name what gets installed or generated, where, and nothing else.
2. **Folder layout.** Where the project's harness files live under `harness/`, and which existing folders are left alone. Take names from the repo survey.
3. **Agent team shape.** Take it from the team patterns in the kit, never by loading them all:

```
<skill-dir>/../../../kit/scripts/kit list P       # one line per pattern
<skill-dir>/../../../kit/scripts/kit show P<n>    # one pattern in full
```

(Substitute `<skill-dir>` as in SKILL.md.) The patterns favour the simplest shape. Start from the single agent, show `Use when` and `Avoid when` of the pattern you propose, and pick a heavier one only if the flow you observed matches its `Use when`. A team may combine patterns, each tied to the part of the flow that matches its `Use when`. State any condition the pattern carries (some are experimental on their platform).

**Existing harness (card branch `s11`).** `new`: nothing exists yet; lay out the files in S11. `handoff`: `prior_harness` lists parts that already exist. Setup moves, renames and reorders nothing and plans no move. For each listed part write one `kind: folder` entry with `status: adopted` (it meets the standard) or `needs-change` (it does not; the gap in `reason`, in the user's words), then ask S11 only for the new files. Tell the user in plain words that moving what exists is its own piece of work, done with `harness-evolve`, which takes every `needs-change` entry first, on its first run after setup. Log the part as `proposal part=folders outcome=handoff`; if the user changes their mind later, append a line with `revised=`.

Settled parts are logged one line each (`proposal part=tools|folders|team`). A part the user rejects entirely is logged with `outcome=none`.

## Question sheets (step 4)

### [S10] Tools to install

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: only what you agreed is installed, in the lightest form that works
- If skipped: nothing is installed; this part stays open
- Why: this fixes what gets installed or generated and where
- Ask: Shall I install <the tools in plain words: what, where> to deal with "<need>"?
- Terms: tool = a file, script or setting that adds one capability; its weight (text rule, reusable instruction, script, outside service) is said in plain words
- Enough: yes, or what to change
- Unsure: say "not sure"; I install nothing
- Suggest: yes, with "Because: <the one-line evidence from the approved list>"

### [S11] Folder layout

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: the new files land where your team will look for them, and existing folders stay untouched
- If skipped: I create no new folder and put the files only where the tools need them
- Why: this decides where the harness files live
- Ask: Shall the harness files live in <folders, with names taken from the repo survey>, leaving <existing folders> alone?
- Terms: harness files = the rules, tools and records this setup creates
- Enough: yes, or the names to change
- Unsure: say "not sure"; I add no new folder
- Suggest: yes, names taken from folders the repo already has; never a move of existing parts (branch `handoff` above)

### [S12] Agent team shape

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: you start with the simplest team that fits how your team really works
- If skipped: I start with a single agent
- Why: this decides how many agents work and who hands work to whom
- Ask: Shall we start with <the shape in plain words, for example one agent doing everything>? It fits when "<fits when>" and not when "<avoid when>".
- Terms: team shape = how many agents there are and who passes work to whom
- Enough: yes, or another shape
- Unsure: say "not sure"; I use a single agent
- Suggest: a single agent, unless the flow seen in stage 1 matches the "fits when" of a heavier shape; say which line matched. Several shapes may be combined, each named with the part of the flow it covers. Name any condition (some shapes are experimental on a platform)
