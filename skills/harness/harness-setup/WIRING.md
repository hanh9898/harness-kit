# Map, entry point and hooks (step 11)

Three parts; do them in order. Every write is a temp file then rename. Every part can run again: it converges, it never appends a second copy.

## A. Glossary map

`GLOSSARY-MAP.md` at the repo root registers one line per context. The harness is its own context; the product is another.

1. Missing: create it and register the product's root `GLOSSARY.md` (and `docs/adr/` if it exists). The product line is the only thing you add for the product.
2. Present: keep every existing line. Add only the harness line if absent; update it in place if present.
3. Harness line: one line of description, no terms copied. It names both paths: `harness/GLOSSARY.md` and `harness/docs/adr/`.
4. `## Relationships`: the harness reads the product's vocabulary and code; the product never mentions the harness. If you know a term used in both contexts with different meanings, name it here.
5. `docs/agents/domain.md`: add (once) a "This repo: multi-context" section that says to read `GLOSSARY-MAP.md` and gives the harness ADR path. In `AGENTS.md` or `CLAUDE.md`, change the `### Domain docs` line to say multi-context (see `GLOSSARY-MAP.md`).
6. Create `harness/GLOSSARY.md` if missing, its first line pointing to the kit README (next to this plugin's `kit/` folder); create `harness/docs/adr/`. Never overwrite an existing file's content.

## B. Entry point

In the `## Agent skills` block of `AGENTS.md` (or `CLAUDE.md`, whichever the project uses), the harness owns exactly the text between two marker lines:

```
<!-- harness:begin -->
### Harness

- Record: harness/record/index.md
- Standards: harness/STANDARDS.md
- Decisions: harness/docs/adr/
<!-- harness:end -->
```

Pointers only: no description, no rule text. No markers yet: append the pair at the end of the block. Markers present: replace everything between them with the text above, even if someone edited it; never add a second pair. If the text between the markers differs from the text above, show the user the lines that will be dropped before replacing. Leave every line outside the markers as it is. Afterwards `grep -c` each marker: exactly one of each.

## C. Hooks

For each entry whose piece is a hook (ask the user if unsure), on the platform taken from the user's answer in step 1:

0. A hook whose entry is `passing`, whose config file already holds the hook and has a `verified_platform`, is not re-triggered and not asked about again; run its check once and move on.
1. Name the platform's config file for hooks (read the platform's docs or `--help` now, as in the gate). Ask the user to confirm the file.
2. Show the exact addition. After a yes, merge it into that file: keep everything already there. Missing file: create it. Put the file's path in the entry's `check`.
3. Trigger the hook for real: run the platform so that the hooked event fires (a command the hook blocks, or one it logs). Paste the real output. Use the platform's non-interactive mode if it has one.
4. Fired as expected: `passing`, and set `verified_platform` to the platform, event, matcher and date. Could not fire it on this platform here: leave the wiring `unverified`, set `verified_platform: not verified on <platform>`, tell the user, and do not call it `passing`.
5. Any `kind: team` entry written before this step existed and lacking `check_scope: structural` gets it added now (see [RECORD-FORMAT.md](RECORD-FORMAT.md)).
