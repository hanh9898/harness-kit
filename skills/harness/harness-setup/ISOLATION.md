# Isolation (step 10)

Ask the user in one turn: do you want the harness kept out of the product's commits, comments and PRs? This is a question, not a label from step 1. Do not assume the answer. Write every question from the sheets below, in the forms of [ASKING.md](ASKING.md).

- **No.** Write no entry. Log `isolation outcome=none`.
- **Yes.** Propose, then wait. Three parts, one turn each, user chooses among options for each:
  1. **Rule.** What may not appear in product artefacts (harness paths, record entry names, harness terms in commit messages, code comments and PR bodies, harness files in a product commit). Offer a narrow and a broad wording.
  2. **Checker.** A command that detects a breach: for example a scan of the staged diff and the commit message for the listed strings. Offer the lightest form that works (a gate step in the simplicity ladder). The checker must be runnable now. It must not flag the harness's own pointers in shared files (step 11 writes the block between the markers, the map line and the multi-context section): list those files and the marker block as exempt in the rule.
  3. **Review.** A line for a reviewer or review skill to check what a script cannot (comments and PR text). The user may decline it.

Write the rule and checker into `harness/STANDARDS.md` as a section, and record `isolation-<slug>` with `kind: isolation`: `choice` is the chosen option, `check` the checker command. After the user agrees to the check, run it on a real case, on a throwaway branch you delete afterwards (a throwaway commit that contains a breach must be reported; a clean one must not), paste both outputs, and only then set `status`. Gate keys as in step 9, except `gate_source`: the `--help` or docs page of the tool the checker uses, read this turn.

## The product's coding standards

If the product has a coding-standards file, propose one line for the user to add to it, saying those standards do not apply to changes under `harness/`. Show the exact text and the file. Never edit or create that file yourself; the user decides and edits. Record in the entry body that the line was proposed and whether the user said they would add it.

## Question sheets (step 10)

Stage 5 continues with S23; the first question of the stage that you ask uses the full form.

### [S23] Keep the tooling out of the product's commits

- Stage: 5/6 Rules, keeping the tooling apart from your product, wiring it in
- Helps: your product's history stays free of traces of the harness files, if you want that
- If skipped: I write nothing and log that isolation was declined; you can add it later
- Why: this is your choice, not something I assume; it decides whether I propose a rule and a checker
- Ask: Looking at your last merged change, do you want changes like it to carry no trace of the harness in the commit message, code comments or pull request text?
- Terms: harness = the rules, tools and records this setup created; product = the code your team ships
- Enough: yes or no
- Unsure: say "not sure"; I treat it as no and write nothing
- Suggest: say what the last change shows, for example "its commit message mentions <harness path>" or "no trace in the last change"

### [S24] Narrow or broad wording of the rule

- Stage: 5/6 Rules, keeping the tooling apart from your product, wiring it in
- Helps: the rule flags real breaches and not harmless text
- If skipped: I use the narrow wording (fewer false alarms)
- Why: this decides what counts as a breach
- Ask: Which wording do you want: narrow ("<text>") or broad ("<text>")? Your last commit would be flagged under <both | the broad one | neither>.
- Terms: narrow = only the harness's own paths; broad = also harness terms in messages and comments
- Enough: narrow or broad
- Unsure: say "not sure"; I use the narrow one
- Suggest: narrow, with the result of running both on your last commit

### [S25] The checker

- Stage: 5/6 Rules, keeping the tooling apart from your product, wiring it in
- Helps: breaches are caught by a command, not by someone's memory
- If skipped: the rule has no checker and its entry stays unverified
- Why: this fixes which command detects a breach; I will run it on a throwaway case before I trust it
- Ask: Shall I use `<command>` to detect a breach? On your last commit it would say <result>.
- Terms: checker = a command that detects traces of the harness in a commit
- Enough: yes, or another command
- Unsure: say "not sure"; I add no checker
- Suggest: yes; the lightest command that works, with what the tool's own help or docs said today. It must not flag the harness's own pointers in shared files

### [S26] A line for the reviewer

- Stage: 5/6 Rules, keeping the tooling apart from your product, wiring it in
- Helps: a reviewer catches what a command cannot see: comments and pull request text
- If skipped: no review line is written
- Why: it is optional; you may decline
- Ask: Do you want this line given to whoever reviews your changes: "<line>"?
- Terms: reviewer = the person or skill that reviews a change before it is merged
- Enough: yes or no
- Unsure: say "not sure"; I do not add it
- Suggest: yes, if your last change had a review; no, if nobody reviews

### [S27] A line for the product's coding standards

- Stage: 5/6 Rules, keeping the tooling apart from your product, wiring it in
- Helps: your product's standards say they do not apply to harness files
- If skipped: I note in the entry that I proposed it and that you did not confirm
- Why: I never edit that file; you do
- Ask: Do you want to add this line to <file>: "<exact text>"?
- Terms: coding standards = the file in which your product's code rules are written
- Enough: "I will add it" or "I will not"
- Unsure: say "not sure"; I note it as proposed, not confirmed
- Suggest: "I will add it", since without it a reviewer may apply product rules to harness files. If the product has no such file, I do not ask
