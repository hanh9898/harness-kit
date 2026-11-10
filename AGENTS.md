# harness-kit

Write repository files, comments, examples, commit messages, issues, pull requests,
and GitHub metadata in English. Run the language checker before committing;
review unaccented prose for English meaning as well.

Keep session notes, as-is snapshots, and unfinished design drafts in `.scratch/`.
Document implemented behavior and accepted decisions; update the affected documentation in the same change.

## Design principle

Design every capability, the software factory and harness-kit's own behavior included, as kit pieces that a project assembles: each function offers alternative pieces, the kit fixes only conditional mandatory requirements, and the project records its chosen pieces and values with the reason. See `docs/adr/0005-assemble-harnesses-from-pieces.md`.

## Agent skills

### Issue tracker

Specs and tickets are GitHub Issues in `hanh9898/harness-kit`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the five standard Matt triage labels with English descriptions. See `docs/agents/triage-labels.md`.

### Domain docs

Single context: `GLOSSARY.md` and `docs/adr/` at the repo root; create them when terms or decisions need recording. See `docs/agents/domain.md`.
