# Replay of harness-setup steps 0 and 1 (brief for a fresh sub-agent)

The lead fills the four values below, then hands this whole file to one fresh sub-agent. The grading lives in `replay-step0-1-assertions.md` next to this file; the runner never opens it.

- `<plugin>`: the harness-kit checkout to test
- `<target>`: the repo to run on (read only)
- `<out>`: an empty folder for everything the run writes
- `<language>`: the user's language (default: Vietnamese)

---

You run the `harness-setup` skill of the plugin at `<plugin>` on the repo `<target>`, steps 0 and 1 only, as a dry run. There is no live user: you write every message you would send, and a simulated user answers it.

## Rules

1. `<target>` is read only. Do not create, edit, move or delete anything under it; no `git` command that writes (no commit, checkout, stash, branch). Everything the skill would write under `<target>/harness/` goes to `<out>/harness/` instead.
2. Write only under `<out>`.
3. Read only these plugin files: `<plugin>/skills/harness/harness-setup/SKILL.md` (the overview and steps 0 and 1), `ASKING.md`, `BOUNDARY.md` and `RECORD-FORMAT.md` in the same folder. Run `<plugin>/tools/check_kit.py` and `<plugin>/kit/scripts/kit` as the skill says; do not read their source. Do not open anything else in `<plugin>`: not `checks/` (beyond this file), not `CHECKLIST.md`, not `tests/`, not `docs/`.
4. Do not open `replay-step0-1-assertions.md`.
5. In `<target>`, read what the skill tells you to read, plus anything you need to look up a fact before asking. Folders named in the card's `code_home` are read the same way, read only.
6. The simulated user answers every question with "yes" when the question carries a suggestion line, and "not sure" when it does not. Apply the skill's rule for that answer and go on. Stop after the `observe` log line, or where the skill tells you to stop.
7. Messages are in `<language>`; record and log keys stay in English, as the skill says.

## Write these files

- `<out>/transcript.md`: every message you would send, in order, the overview message first. After each question, one line `> user: yes` or `> user: not sure`. Before each question, one line `<!-- sheet: <id>, branch: <name>=<value> or none -->`.
- `<out>/harness/situation.md` and `<out>/harness/progress.log`: the files the skill would write, as they stand at the end.
- `<out>/check-situation.txt`: each `check_kit.py --situation` command you ran and its full output.
- `<out>/check-log.txt`: the command `python3 <plugin>/tools/check_kit.py --log <out>/harness/progress.log` and its output.
- `<out>/files-read.txt`: every file and folder you opened or listed, in order, one per line, plus every command you ran; put the line `--- first question sent ---` where you sent the first question.
- `<out>/ambiguities.md`: each place where the skill left you unsure what to do: the file and line, what was unclear, what you chose. Write "none" if there was none.

Report back in at most ten lines: the card's values, the branches printed, the number of questions you asked, and the number of ambiguities.
