# Check (step 4)

## Run

Run each ticket's check and each affected entry's check. Paste command, exit code and output into the entry's `## Check result`. Mark `passing` and set `verified_on` (`date -u +%F`) only after the check ran and passed; a failure is `failing`.

## Review with `code-review`

When the change touches `harness/`, review it with `code-review`. That skill has no standards parameter, so put it in the prompt: name `harness/STANDARDS.md` as the standard for this change, and say the product's coding standards do not apply to harness files. Also give the absolute path of the repo (the review may start in another folder) and a fixed point that makes the diff non-empty, such as the last commit before the change. For a product-code diff, say nothing about the harness standard.

## Fail

A check fails and is not waived: do not write `passing`. Go back to step 3 with the failing output, rework, run the check again. Repeat until it passes or the user waives.

## Waiver

Only the user waives. Ask for the reason (sheet V09 below; forms in [ASKING.md](../harness-setup/ASKING.md)); never write one on their behalf. Record in the entry: `waived_on` (date), `waived_reason` (the user's words), `waived_by: user`. The entry keeps `status: failing`; a waived entry is never `passing`. Say in the final report which entries are waived.

## Team entries

An entry with `kind: team` and `check_scope: structural` only proves the pattern and the folders exist. When the change touches one, ask the user for one verification that actually runs outside that check (sheet V08 below) (for example, run a small task through the team and look at the result). Run it and paste the result into the entry. If the user cannot run it now, write `not run` in the entry and do not describe the team as working.

## Question sheets (step 4)

### [V08] A real run of the team

- Stage: 3/4 Do it and check it
- Helps: you learn whether the team really works, not only that its files exist
- If skipped: I write "not run" in the entry and do not say the team works
- Why: the automatic check only proves that the pattern and folders exist
- Ask: Shall we run one small task through the team now, for example "<small task from the latest piece of work>", and look at the result?
- Terms: team = the agents set up together for this repo; structural check = proves only that files and folders exist
- Enough: yes, or another task
- Unsure: say "not sure"; I write "not run"
- Suggest: yes, with a small task taken from the latest piece of work

### [V09] The reason for waiving a failing check

- Stage: 3/4 Do it and check it
- Helps: the record shows honestly why a failure was accepted
- If skipped: there is no waiver; the entry stays failing and we go back to rework
- Why: only you may waive, and the reason is written in your words
- Ask: The check `<command>` fails with "<one line of output>". In your own words, why do you accept that for now?
- Terms: waive = accept a failing check knowingly; the entry stays "failing", marked as waived
- Enough: one sentence in your words
- Unsure: say "not sure"; no waiver is written
- Suggest: none; I never write a reason for you. I may say what the failure seems to be
