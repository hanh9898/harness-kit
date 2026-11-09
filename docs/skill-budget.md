# Skill description budget

The `tools/skill_budget.py` tool measures the fixed context cost of frontmatter `description` fields per session. It is read-only: measure before editing.

## Run

Paths below are relative to the kit repo root; `--root` selects the repo to measure and defaults to the current directory.

```
python3 tools/skill_budget.py --root <repo-root>                 # scan .claude/skills and .agents/skills under this root
python3 tools/skill_budget.py --root <repo-root> --top 10        # only the 10 largest skills per directory
python3 tools/skill_budget.py --root <repo-root> --dir skills    # another skill directory; repeatable
python3 tools/skill_budget.py --root <repo-root> --json          # machine-readable output
python3 tools/skill_budget.py --root <repo-root> --max-total 20000 --strict
```

By default it warns with exit 0; `--strict` exits 1 on warnings (name/folder mismatch, missing `description`, unreadable SKILL.md, or totals exceeding `--max-total`). Every warning gives a next step. Exit 2 means `--root` is not a directory. Token counts use characters / 4, not a model tokenizer.

## Reading the output

- Each directory reports skill count, total description characters, estimated tokens, folder/name mismatches, then skills in descending description length.
- Both skill directories may contain the same skill through symlinks or copies. Adding their totals can double-count; actual loading depends on which sources the session uses.
- Run before and after editing descriptions; record both measurements in the commit message.

## Measurement limits

- Only `description` is measured, not `name` or other fields added by the skill loader.
- The built-in frontmatter parser uses no YAML dependency and supports double-quoted, single-quoted, plain, and `>`/`|` block scalars. Other formats may introduce small errors.
