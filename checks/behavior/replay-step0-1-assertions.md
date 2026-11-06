# Grading the replay of steps 0 and 1

For the lead only; the runner of `replay-step0-1.md` never sees this file. Grade each line PASS or FAIL with one line of evidence (file and line, or command output). Before grading, write down the facts of `<target>` yourself (Agent skills block, flow documents, tracker, code folders, existing harness parts, latest finished work of the user) so the card is judged against the repo, not against the runner's claims.

## Machine checks

| # | Command | Pass when |
|---|---|---|
| M1 | `git -C <target> status --porcelain` and a file listing of `<target>` taken before and after the run | no change at all |
| M2 | `python3 <plugin>/tools/check_kit.py --situation <out>/harness/situation.md` | exit 0; the branches match `<out>/check-situation.txt` |
| M3 | `python3 <plugin>/tools/check_kit.py --log <out>/harness/progress.log` | exit 0 |
| M4 | `grep -c "step=observe" <out>/harness/progress.log` | exactly 1 |

## Reading checks

| # | Look at | Pass when |
|---|---|---|
| A1 | transcript, card | Step 0 matches the repo: with an `## Agent skills` block and `docs/agents/`, `matt_config: present`, no block is proposed and the run does not stop; without them the run stops and writes nothing but the transcript |
| A2 | card | every value matches the facts you wrote down; `platform` is the app S01 settled (or `<app>@<host>` when it runs through a host), `unknown` only when S01 had no suggestion and the answer was "not sure"; `confirmed: yes` after S06 |
| A3 | `files-read.txt` | every local folder in `code_home` other than `.` is read before `--- first question sent ---` |
| A4 | transcript | the overview message comes first; each message holds one question; each question carries its stage line (stage 1 of 6); the first question of the stage uses the full form, later ones the compact form |
| A5 | transcript | no harness words in what the user reads: no piece id (A01, P1), no `kit show`, no "rung", "lego", "gate" without its plain version |
| A6 | transcript, branch comments | the suggested recent work follows `s02_work`: `git` from this repo's git history; `tracker` a closed ticket assigned to the user, never this repo's git and never another person's ticket; `planned` a planned piece in the future tense |
| A7 | transcript | `s02_chain=pain`: S02 turn 1 is asked, then S07 with the steps of the flow document as choices, and no question about who wrote, coded, reviewed or merged. `s02_chain=who`: one chain confirmation when git is clear, otherwise one question per unclear link |
| A8 | transcript | `s03_labels=ask`: one list-accepting question holds every item to label, each with a suggested label and a one-line reason; S03 to S05 appear only for an item without a suggestion; no run of one question per item. `skip`: one line, and `labels=none` in the log |
| A9 | transcript, log | S06 reads back the flow with the labels and the card; the `observe` line carries `platform=`, `flow=` (in double quotes when it has spaces) and `labels=` |
| A10 | transcript | no question asks what the repo, git, the tracker files or the `code_home` folders already answer |

## Recorded, not graded

- R1: number of questions in stage 1, by sheet.
- R2: every entry of `ambiguities.md`, each marked as a gap in the skill or a misreading by the runner.

The grade is the count of PASS out of 14 (M1 to M4, A1 to A10), with each FAIL named.
