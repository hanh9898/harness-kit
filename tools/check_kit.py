#!/usr/bin/env python3
"""check_kit: validate legos.csv data in a kit directory.

  check_kit.py [--dir DIR]

Check required columns and cells; rung must be instruction-file | skill | script-cli | mcp,
IDs are unique. If gates.csv exists, gate=yes rules need an ISO verified_on date
in rules.csv, stated certainty, a valid verify_method and a nonempty verified_quote; gate=no requires a note.
Print one legos.csv:line error per line; exit 1 on errors, 0 when clean.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

COLUMNS = ["id", "group", "name", "summary", "needed_when", "rung", "certainty", "sources", "detail"]
RUNGS = ["instruction-file", "skill", "script-cli", "mcp"]
GATE_COLUMNS = ["id", "gate", "verify_method", "verified_quote", "note"]
GATE_METHODS = ["raw-grep", "webfetch", "unreadable"]
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


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


def check_gates(kit_dir):
    gpath = kit_dir / "gates.csv"
    if not gpath.exists():
        return []
    try:
        with (kit_dir / "rules.csv").open(encoding="utf-8", newline="") as f:
            rules = {r["id"]: r for r in csv.DictReader(f)}
        with gpath.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            missing = [c for c in GATE_COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                return [f"gates.csv:1: missing columns {', '.join(missing)}; fix: include all columns {', '.join(GATE_COLUMNS)}"]
            gates = list(reader)
    except (OSError, KeyError) as e:
        return [f"gates.csv: cannot cross-check rules.csv ({e}); fix: provide rules.csv with an id column"]
    errs = []
    for n, g in enumerate(gates, 2):
        gid, r = g["id"], rules.get(g["id"])
        if r is None:
            errs.append(f"gates.csv:{n}: {gid} is absent from rules.csv; fix: use an existing ID")
            continue
        if g["gate"] not in ("yes", "no"):
            errs.append(f"gates.csv:{n}: {gid} gate `{g['gate']}` is not yes | no; fix: choose yes or no")
        elif g["gate"] == "yes":
            if not ISO_DATE.fullmatch((r.get("verified_on") or "").strip()):
                errs.append(f"gates.csv:{n}: {gid} is a gate but rules.csv lacks YYYY-MM-DD verified_on; fix: record a verification date or set gate=no")
            if r.get("certainty") != "stated":
                errs.append(f"gates.csv:{n}: {gid} is a gate but certainty `{r.get('certainty')}` is not stated; fix: set gate=no")
            if not (g["verified_quote"] or "").strip():
                errs.append(f"gates.csv:{n}: {gid} is a gate with an empty verified_quote; fix: copy the exact quote from the original source")
            if g["verify_method"] not in GATE_METHODS[:2]:
                errs.append(f"gates.csv:{n}: {gid} verify_method `{g['verify_method']}` is insufficient for a gate; fix: use raw-grep or webfetch")
        else:
            if not (g["note"] or "").strip():
                errs.append(f"gates.csv:{n}: {gid} has gate=no without a note; fix: explain why it is not a gate")
            if (r.get("verified_on") or "").strip():
                errs.append(f"gates.csv:{n}: {gid} has gate=no but rules.csv retains verified_on; fix: clear verified_on")
        if g["verify_method"] not in GATE_METHODS:
            errs.append(f"gates.csv:{n}: {gid} verify_method `{g['verify_method']}` is not in {' | '.join(GATE_METHODS)}; fix: choose a listed value")
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent.parent / "kit"))
    a = ap.parse_args(argv)
    errs = check(Path(a.dir)) + check_gates(Path(a.dir))
    for e in errs:
        print(f"ERROR: {e}")
    print(f"{len(errs)} data errors." if errs else "Kit data clean.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
