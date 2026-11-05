# Isolation (step 10)

Ask the user in one turn: do you want the harness kept out of the product's commits, comments and PRs? This is a question, not a label from step 1. Do not assume the answer.

- **No.** Write no entry. Log `isolation outcome=none`.
- **Yes.** Propose, then wait. Three parts, one turn each, user chooses among options for each:
  1. **Rule.** What may not appear in product artefacts (harness paths, record entry names, harness terms in commit messages, code comments and PR bodies, harness files in a product commit). Offer a narrow and a broad wording.
  2. **Checker.** A command that detects a breach: for example a scan of the staged diff and the commit message for the listed strings. Offer the lightest form that works (a gate step in the simplicity ladder). The checker must be runnable now.
  3. **Review.** A line for a reviewer or review skill to check what a script cannot (comments and PR text). The user may decline it.

Write the rule and checker into `harness/STANDARDS.md` as a section, and record `isolation-<slug>` with `kind: isolation`: `choice` is the chosen option, `check` the checker command. Run the check on a real case (a throwaway commit that contains a breach must be reported; a clean one must not), paste both outputs, and only then set `status`. Gate keys as in step 9.

## The product's coding standards

If the product has a coding-standards file, propose one line for the user to add to it, saying those standards do not apply to changes under `harness/`. Show the exact text and the file. Never edit or create that file yourself; the user decides and edits. Record in the entry body that the line was proposed and whether the user said they would add it.
