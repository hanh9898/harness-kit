#!/usr/bin/env python3
"""check_kit: validate legos.csv data in a kit directory.

  check_kit.py [--dir DIR]

Check required columns and cells; rung must be instruction-file | skill | script-cli | mcp,
IDs are unique. Print one legos.csv:line error per line; exit 1 on errors, 0 when clean.
"""
import argparse
import csv
import sys
from pathlib import Path

COLUMNS = ["id", "group", "name", "summary", "needed_when", "rung", "certainty", "sources", "detail"]
RUNGS = ["instruction-file", "skill", "script-cli", "mcp"]


def check(kit_dir):
    path = kit_dir / "legos.csv"
    try:
        f = path.open(encoding="utf-8", newline="")
    except OSError as e:
        return [f"legos.csv: cannot read file ({e}); fix: create legos.csv in {kit_dir}"]
    with f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [f"legos.csv:1: missing columns {', '.join(missing)}; fix: include all columns {', '.join(COLUMNS)}"]
        errs, seen = [], {}
        for n, r in enumerate(reader, 2):
            for c in COLUMNS:
                if not (r.get(c) or "").strip():
                    errs.append(f"legos.csv:{n}: {r.get('id') or '?'} has an empty `{c}` cell; fix: supply a value")
            if r["rung"] and r["rung"] not in RUNGS:
                errs.append(f"legos.csv:{n}: {r['id']} rung `{r['rung']}` is not in {' | '.join(RUNGS)}; fix: choose one of these four values")
            if r["id"] in seen:
                errs.append(f"legos.csv:{n}: duplicate id {r['id']} from line {seen[r['id']]}; fix: choose another ID")
            seen.setdefault(r["id"], n)
        return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent.parent / "kit"))
    a = ap.parse_args(argv)
    errs = check(Path(a.dir))
    for e in errs:
        print(f"ERROR: {e}")
    print(f"{len(errs)} data errors." if errs else "Kit data clean.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
