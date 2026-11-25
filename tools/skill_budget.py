#!/usr/bin/env python3
"""Measure skill frontmatter description budgets without modifying skills.

  skill_budget.py [--root DIR] [--dir REL ...] [--top N] [--json] [--strict] [--max-total N]

Defaults to .claude/skills and .agents/skills under --root; root defaults to the current directory.
Print total characters, estimated tokens (characters / 4), per-skill rows in descending order, and folders
whose name differs from the folder. Defaults to warnings with exit 0; --strict exits 1 for warnings (
name/folder mismatches, missing descriptions, unreadable SKILL.md, or totals above --max-total).
Uses no personal paths and only the standard library.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_DIRS = [".claude/skills", ".agents/skills"]
CHARS_PER_TOKEN = 4


def _block_scalar(lines, i, style, indicators):
    indent = next((int(c) for c in indicators if c.isdigit()), 0)
    if not indent:
        indent = 1
        for line in lines[i:]:
            indent = max(indent, len(line) - len(line.lstrip(" ")))
            if line.strip(" "):
                break

    prefix = " " * indent
    content = []
    while i < len(lines):
        line = lines[i]
        if (not line and i + 1 == len(lines)) or (not line.startswith(prefix) and line.strip(" ")):
            break
        content.append(line[indent:])
        i += 1

    text = "\n".join(content)
    if content and i < len(lines):
        text += "\n"
    if style == ">":
        # Between ordinary lines, a single break folds to a space; blank lines fold out one break.
        text = re.sub(r"(?m)^([^ \t\n][^\n]*)\n(\n*)(?=[^ \t\n])", lambda m: m[1] + (m[2] or " "), text)

    if "+" in indicators:
        return text, i
    value = text.rstrip("\n")
    if "-" not in indicators and value and text.endswith("\n"):
        value += "\n"
    return value, i


def _scalar(lines, i):
    """Read the YAML scalar at lines[i]; return (value, next line index)."""
    rest = lines[i].split(":", 1)[1].strip()
    if rest.startswith("#"):
        rest = ""
    j = i + 1
    while not rest and j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
        line = lines[j].strip()
        if line and not line.startswith("#"):
            rest = line
        j += 1
    block = re.fullmatch(r"([|>])([1-9][-+]?|[-+][1-9]?)?(?:[ \t]+#.*)?", rest)
    if block:
        return _block_scalar(lines, j, block[1], block[2] or "")

    cont = []
    while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
        cont.append(lines[j].strip())
        j += 1
    while cont and not cont[-1]:
        cont.pop()
    text = " ".join([rest] + cont) if cont else rest
    quoted = re.match(r"""("(?:[^"\\]|\\.)*"|'(?:[^']|'')*')\s+#""", text)
    if quoted:
        text = quoted[1]
    elif not text.startswith(('"', "'")):
        text = re.split(r"[ \t]#", text, maxsplit=1)[0].rstrip(" \t")
    if text.startswith('"'):
        try:
            return json.loads(text), j
        except ValueError:
            return text.strip('"'), j
    if text.startswith("'") and text.endswith("'") and len(text) > 1:
        return text[1:-1].replace("''", "'"), j
    return text, j


def frontmatter(path):
    """Return name/description from SKILL.md; omit missing keys."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    out, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        m = re.match(r"(name|description):", lines[i])
        if m:
            out[m.group(1)], i = _scalar(lines, i)
        else:
            i += 1
    return out


def _discover(folder):
    """Find skill folders, without descending into a skill or following directory symlinks."""
    try:
        (folder / "SKILL.md").lstat()
    except FileNotFoundError:
        if not folder.is_symlink():
            try:
                children = sorted(folder.iterdir())
            except OSError:
                return
            for child in children:
                if child.is_dir():
                    yield from _discover(child)
        return
    except OSError:
        pass  # Let the reader report an inaccessible SKILL.md.
    yield folder


def measure(root, rel):
    base = root / rel
    rows = []
    if not base.is_dir():
        return rows
    candidates = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        # Preserve the missing SKILL.md warning for an unrecognized top-level folder.
        candidates.extend(list(_discover(child)) or [child])
    for d in candidates:
        parent = rel if d.parent == base else str(Path(rel) / d.parent.relative_to(base))
        row = {"dir": parent, "folder": d.name, "name": None, "chars": 0, "problem": None}
        try:
            fm = frontmatter(d / "SKILL.md")
        except (OSError, UnicodeDecodeError) as e:
            row["problem"] = f"cannot read SKILL.md ({type(e).__name__})"
            rows.append(row)
            continue
        row["name"] = fm.get("name")
        desc = fm.get("description")
        if desc is None or not desc.strip():
            row["problem"] = "missing description"
        else:
            row["chars"] = len(desc)
        rows.append(row)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--dir", action="append", help="skill directory relative to --root; repeatable")
    ap.add_argument("--top", type=int, default=0, help="show only the N largest skills per directory; 0 shows all")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--max-total", type=int, default=0, help="warn when total characters exceed the limit; 0 disables it")
    a = ap.parse_args(argv)

    root = Path(a.root)
    dirs = a.dir or DEFAULT_DIRS
    if not root.is_dir():
        print(f"ERROR: --root is not a directory: {a.root}. Next step: supply the harness repository root.", file=sys.stderr)
        return 2
    report, warnings = [], []
    for rel in dirs:
        rows = measure(root, rel)
        if not rows:
            warnings.append(f"No skills found in {rel}. Next step: check --root or --dir.")
        mism = [r for r in rows if r["name"] is not None and r["name"] != r["folder"]]
        noname = [r for r in rows if r["name"] is None and r["problem"] is None]
        for r in rows:
            if r["problem"]:
                warnings.append(f"{r['dir']}/{r['folder']}: {r['problem']}. Next step: check that skill's SKILL.md.")
        report.append({"dir": rel, "skills": len(rows), "chars": sum(r["chars"] for r in rows),
                       "name_mismatch": len(mism), "name_missing": len(noname), "rows": rows})
    total = sum(d["chars"] for d in report)
    if a.max_total and total > a.max_total:
        warnings.append(f"Total {total} characters exceeds limit {a.max_total}. Next step: shorten the largest descriptions above.")
    mism_total = sum(d["name_mismatch"] for d in report)
    if mism_total:
        warnings.append(f"{mism_total} folders have a name/folder mismatch. Next step: inspect the name column and decide whether to rename folders or names; this tool only measures.")

    if a.top or not a.json:
        for d in report:
            ranked = sorted(d["rows"], key=lambda r: (-r["chars"], r["folder"]))
            d["rows"] = ranked[: a.top or None]

    if a.json:
        print(json.dumps({"total_chars": total, "total_tokens_est": total // CHARS_PER_TOKEN,
                          "dirs": report, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for d in report:
            print(f"== {d['dir']}: {d['skills']} skills, {d['chars']} characters (~{d['chars'] // CHARS_PER_TOKEN} tokens), "
                  f"name/folder mismatches: {d['name_mismatch']}, missing name: {d['name_missing']}")
            for r in d["rows"]:
                flag = f"  [name={r['name']}]" if r["name"] not in (None, r["folder"]) else ""
                print(f"{r['chars']:>6}  {r['folder']}{flag}" + (f"  ({r['problem']})" if r["problem"] else ""))
        print(f"TOTAL: {total} characters (~{total // CHARS_PER_TOKEN} estimated tokens, characters/{CHARS_PER_TOKEN})")
        for w in warnings:
            print("WARNING: " + w)
    return 1 if (a.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
