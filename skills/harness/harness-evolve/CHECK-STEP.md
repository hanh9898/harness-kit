# Check (step 4)

## Run

Run each ticket's check and each affected entry's check. Paste command, exit code and output into the entry's `## Check result`. Mark `passing` and set `verified_on` (`date -u +%F`) only after the check ran and passed; a failure is `failing`.

## Review with `code-review`

When the change touches `harness/`, review it with `code-review`. That skill has no standards parameter, so put it in the prompt: name `harness/STANDARDS.md` as the standard for this change, and say the product's coding standards do not apply to harness files. Also give the absolute path of the repo (the review may start in another folder) and a fixed point that makes the diff non-empty, such as the last commit before the change. For a product-code diff, say nothing about the harness standard.

## Fail

A check fails and is not waived: do not write `passing`. Go back to step 3 with the failing output, rework, run the check again. Repeat until it passes or the user waives.

## Waiver

Only the user waives. Ask for the reason; never write one on their behalf. Record in the entry: `waived_on` (date), `waived_reason` (the user's words), `waived_by: user`. The entry keeps `status: failing`; a waived entry is never `passing`. Say in the final report which entries are waived.

## Team entries

An entry with `kind: team` and `check_scope: structural` only proves the pattern and the folders exist. When the change touches one, ask the user for one verification that actually runs outside that check (for example, run a small task through the team and look at the result). Run it and paste the result into the entry. If the user cannot run it now, write `not run` in the entry and do not describe the team as working.
