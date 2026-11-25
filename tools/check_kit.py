#!/usr/bin/env python3
"""check_kit: validate legos.csv data in a kit directory.

  check_kit.py [--dir DIR]
  check_kit.py --log FILE        check a harness/progress.log for revised=, observe work=/labels=, need-to-piece groups= and double quotes
  check_kit.py --situation FILE  check a nine-field key:value harness/situation.md and print selected branches

Check CSV quoting, required columns and cells; legos.csv and rules.csv rows must not exceed their headers.
Rung must be instruction-file | skill | script-cli | mcp,
IDs in legos.csv, rules.csv and gates.csv are unique and every group has a name in groups.csv (id,name).
If gates.csv exists, gate=yes rules need an ISO verified_on date
in rules.csv, stated certainty, verify_method=raw-grep and a nonempty verified_quote; gate=no requires a note.
When gates.csv exists, only rules with gate=yes may carry verified_on.
Print one error per line; exit 1 on errors, 0 when clean.
"""
import argparse
import csv
import re
import sys
from contextlib import contextmanager
from datetime import date
from pathlib import Path

COLUMNS = ["id", "group", "name", "summary", "needed_when", "rung", "certainty", "sources", "detail"]
RUNGS = ["instruction-file", "skill", "script-cli", "mcp"]
RULE_COLUMNS = ["id", "topic", "rule", "source", "certainty", "check", "verified_on"]
GATE_COLUMNS = ["id", "gate", "verify_method", "verified_quote", "note"]
GATE_METHODS = ["raw-grep", "webfetch", "unreadable"]
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


@contextmanager
def _strict_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, strict=True)
        try:
            yield reader
        except csv.Error as e:
            # DictReader only updates its line number after a successful read.
            raise csv.Error(f"{path.name}:{reader.reader.line_num}: malformed CSV ({e}); fix: check CSV field quoting") from e


def check(kit_dir):
    errs, seen, used_groups = [], {}, {}
    try:
        with _strict_csv(kit_dir / "legos.csv") as reader:
            missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                return [f"legos.csv:1: missing columns {', '.join(missing)}; fix: include all columns {', '.join(COLUMNS)}"]
            for r in reader:
                n = reader.line_num
                if None in r:
                    errs.append(f"legos.csv:{n}: {r.get('id') or '?'} has extra cells beyond the header; fix: match the row to the header")
                for c in COLUMNS:
                    if not (r.get(c) or "").strip():
                        errs.append(f"legos.csv:{n}: {r.get('id') or '?'} has an empty `{c}` cell; fix: supply a value")
                if r["rung"] and r["rung"] not in RUNGS:
                    errs.append(f"legos.csv:{n}: {r['id']} rung `{r['rung']}` is not in {' | '.join(RUNGS)}; fix: choose one of these four values")
                if r["id"] in seen:
                    errs.append(f"legos.csv:{n}: duplicate id {r['id']} from line {seen[r['id']]}; fix: choose another ID")
                seen.setdefault(r["id"], n)
                group = r["group"]
                if group and group.strip():
                    used_groups.setdefault(group, n)
    except csv.Error as e:
        return errs + [str(e)]
    except OSError as e:
        return [f"legos.csv: cannot read file ({e}); fix: create legos.csv in {kit_dir}"]
    return errs + check_groups(kit_dir, used_groups)


def read_groups(kit_dir):
    """{group ID: name} from groups.csv; raise on file or CSV errors."""
    with _strict_csv(kit_dir / "groups.csv") as reader:
        return {(r.get("id") or "").strip(): (r.get("name") or "").strip() for r in reader}


def check_groups(kit_dir, used):
    """Every group used by legos.csv needs a name in groups.csv."""
    try:
        names = read_groups(kit_dir)
    except csv.Error as e:
        return [str(e)]
    except OSError as e:
        return [f"groups.csv: cannot read file ({e}); fix: create groups.csv with id,name columns"]
    return [f"legos.csv:{n}: group `{g}` has no name in groups.csv; fix: add `{g},<group name>`"
            for g, n in sorted(used.items()) if not names.get(g)]


def check_rules_and_gates(kit_dir):
    rpath = kit_dir / "rules.csv"
    gpath = kit_dir / "gates.csv"
    has_gates = gpath.exists()
    if not has_gates and not rpath.exists():
        return []
    errs, rules, rule_lines = [], {}, {}
    try:
        with _strict_csv(rpath) as reader:
            missing = [c for c in RULE_COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                return [f"rules.csv:1: missing columns {', '.join(missing)}; fix: include all columns {', '.join(RULE_COLUMNS)}"]
            for r in reader:
                rid, n = r["id"], reader.line_num
                if None in r:
                    errs.append(f"rules.csv:{n}: {rid or '?'} has extra cells beyond the header; fix: match the row to the header")
                missing_cells = [c for c, value in r.items() if value is None]
                if missing_cells:
                    errs.append(f"rules.csv:{n}: {rid or '?'} is missing cells for {', '.join(missing_cells)}; fix: include a cell for each column")
                if rid is not None and not rid.strip():
                    errs.append(f"rules.csv:{n}: ? has an empty `id` cell; fix: supply a value")
                    continue
                if rid in rule_lines:
                    errs.append(f"rules.csv:{n}: duplicate id {rid} from line {rule_lines[rid]}; fix: keep one row per ID")
                rule_lines.setdefault(rid, n)
                rules[rid] = r
        if not has_gates:
            return errs
        with _strict_csv(gpath) as reader:
            missing = [c for c in GATE_COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                return errs + [f"gates.csv:1: missing columns {', '.join(missing)}; fix: include all columns {', '.join(GATE_COLUMNS)}"]
            gates = [(reader.line_num, g) for g in reader]
    except csv.Error as e:
        return errs + [str(e)]
    except (OSError, KeyError) as e:
        if has_gates:
            return errs + [f"gates.csv: cannot cross-check rules.csv ({e}); fix: provide rules.csv with an id column"]
        return errs + [f"rules.csv: cannot check rule IDs ({e}); fix: provide rules.csv with an id column"]
    gate_lines = {}
    for n, g in gates:
        gid = g["id"]
        if gid in gate_lines:
            errs.append(f"gates.csv:{n}: duplicate id {gid} from line {gate_lines[gid]}; fix: keep one row per ID")
        gate_lines.setdefault(gid, n)
        r = rules.get(gid)
        if r is None:
            errs.append(f"gates.csv:{n}: {gid} is absent from rules.csv; fix: use an existing ID")
            continue
        if g["gate"] not in ("yes", "no"):
            errs.append(f"gates.csv:{n}: {gid} gate `{g['gate']}` is not yes | no; fix: choose yes or no")
        elif g["gate"] == "yes":
            verified_on = (r.get("verified_on") or "").strip()
            if not ISO_DATE.fullmatch(verified_on):
                errs.append(f"gates.csv:{n}: {gid} is a gate but rules.csv lacks YYYY-MM-DD verified_on; fix: record a verification date or set gate=no")
            else:
                try:
                    date.fromisoformat(verified_on)
                except ValueError:
                    errs.append(f"gates.csv:{n}: {gid} rules.csv verified_on `{verified_on}` is not a calendar date; fix: record a valid YYYY-MM-DD date or set gate=no")
            if r.get("certainty") != "stated":
                errs.append(f"gates.csv:{n}: {gid} is a gate but certainty `{r.get('certainty')}` is not stated; fix: set gate=no")
            if not (g["verified_quote"] or "").strip():
                errs.append(f"gates.csv:{n}: {gid} is a gate with an empty verified_quote; fix: copy the exact quote from the original source")
            if g["verify_method"] != "raw-grep":
                errs.append(f"gates.csv:{n}: {gid} verify_method `{g['verify_method']}` is insufficient for a gate; fix: use raw-grep")
        else:
            if not (g["note"] or "").strip():
                errs.append(f"gates.csv:{n}: {gid} has gate=no without a note; fix: explain why it is not a gate")
            if (r.get("verified_on") or "").strip():
                errs.append(f"gates.csv:{n}: {gid} has gate=no but rules.csv retains verified_on; fix: clear verified_on")
        if g["verify_method"] not in GATE_METHODS:
            errs.append(f"gates.csv:{n}: {gid} verify_method `{g['verify_method']}` is not in {' | '.join(GATE_METHODS)}; fix: choose a listed value")
    for rid, r in rules.items():
        if rid not in gate_lines and (r.get("verified_on") or "").strip():
            errs.append(f"rules.csv: {rid} has no gate row but retains verified_on; fix: clear verified_on")
    return errs


LOG_FIELD = re.compile(r'([\w-]+)=("([^"]*)"|\S*)')
LOG_TS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
LABEL_SIDE = re.compile(r"(shared|project)=[^,;=\s][^,;=]*(,\s*[^,;=\s][^,;=]*)*")


def labels_ok(value):
    """none, or shared=a,b and/or project=c,d joined by a semicolon, each label once."""
    sides = [s.strip() for s in value.split(";")]
    names = [s.partition("=")[0] for s in sides]
    return value == "none" or (all(LABEL_SIDE.fullmatch(s) for s in sides) and len(set(names)) == len(names))


def _parse_log(text):
    """Return (rows, errors); values containing whitespace use double quotes: flow="a then b"."""
    rows, errs = [], []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        head, _, rest = line.partition(" ")
        if rest.count('"') % 2:
            errs.append(f"progress.log:{n}: unclosed double quotes; fix: enclose the complete whitespace-containing value in one pair of \"...\"")
            continue
        rows.append((n, head, {k: q if v.startswith('"') else v for k, v, q in LOG_FIELD.findall(rest)}))
    return rows, errs


def _log_key(fields):
    return fields.get("step", ""), fields.get("part") or fields.get("entry") or fields.get("role") or ""


def effective_lines(text):
    """Latest effective line per (step, part); part falls back to entry, then role."""
    return {_log_key(f): dict(f, ts=ts) for _, ts, f in _parse_log(text)[0]}


def check_progress_log(text, groups=None):
    """A revised= line must reference an earlier timestamp with the same step.
    A shared timestamp can be disambiguated by the decision's part or need.
    Superseded lines skip field checks, but their revision links are still checked.
    observe requires work= and correctly formatted labels=. need-to-piece requires groups= with comma-separated inspected group letters, validated against groups when supplied."""
    rows, errs = _parse_log(text)
    seen, superseded = {}, set()
    for n, ts, f in rows:
        step, part = _log_key(f)
        decision = f.get("need", "") if step == "need-to-piece" else part
        rev = f.get("revised")
        if rev is not None:
            earlier = seen.get(rev)
            if not LOG_TS.fullmatch(rev) or not earlier:
                errs.append(f"progress.log:{n}: revised={rev} does not reference an earlier timestamp; fix: copy the original timestamp exactly")
            elif step not in earlier:
                target_step = next(iter(earlier))
                errs.append(f"progress.log:{n}: revised={rev} points to step={target_step}, not step={step}; fix: keep the replacement on the same step")
            else:
                candidates = earlier[step]
                target_lines = candidates.get(decision)
                if target_lines is None and len(earlier) == len(candidates) == 1 and ts != rev:
                    (only_lines,) = candidates.values()
                    if len(only_lines) == 1:
                        target_lines = only_lines
                if target_lines:
                    superseded.update(target_lines)
                else:
                    errs.append(f"progress.log:{n}: revised={rev} does not identify an earlier row for this decision; fix: keep the replacement on the same part, entry, role, or need")
        if "step" in f:
            seen.setdefault(ts, {}).setdefault(step, {}).setdefault(decision, []).append(n)
    for n, _, f in rows:
        if n in superseded:
            continue
        if f.get("step") == "observe":
            if not f.get("work"):
                errs.append(f"progress.log:{n}: observe missing work=; fix: record the S02 turn-1 work item, for example work=PROJ-12; preserve the old line and append a revised= replacement")
            if not labels_ok(f.get("labels", "")):
                errs.append(f"progress.log:{n}: labels={f.get('labels', '')} has invalid format; fix: use labels=shared=a,b;project=c,d, omit empty sides, or labels=none; preserve the old line and append a revised= replacement")
        if f.get("step") == "need-to-piece":
            looked = [g for g in f.get("groups", "").split(",") if g]
            unknown = [g for g in looked if groups is not None and g not in groups]
            if not looked:
                errs.append(f"progress.log:{n}: need-to-piece missing groups=; fix: record every inspected kit group, for example groups=A,J; preserve the old line and append a revised= replacement")
            elif unknown:
                errs.append(f"progress.log:{n}: groups= contains unknown groups {', '.join(unknown)}; fix: use group letters from `kit list`")
    return errs


SITUATION_FIELDS = {
    "matt_config": r"present|partial|absent",
    "work_source": r"git|none|(?:tracker|doc):\S+",
    "code_home": r"\.|[^,\s][^,]*(,\s*[^,\s][^,]*)*",
    "flow_source": r"sample|asked|doc:[^\s]+",
    "prior_harness": r"none|[^,\s][^,]*(,\s*[^,\s][^,]*)*",
    "history": r"yes|none",
    "tree_relation": r"shared|apart",
    "platform": r"[\w.-]+(@[\w.-]+)?",
    "confirmed": r"yes|no",
}


def parse_situation(text):
    """Return (card, errors); every nonblank, nonheading line must be key: value."""
    card, errs = {}, []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not sep or " " in key:
            errs.append(f"situation.md:{n}: line is not `key: value`; fix: record one factual field per line")
        elif key not in SITUATION_FIELDS:
            errs.append(f"situation.md:{n}: unknown key `{key}`; expected {', '.join(SITUATION_FIELDS)}; fix: remove it or use an existing key")
        elif key in card:
            errs.append(f"situation.md:{n}: duplicate key `{key}`; fix: keep one line")
        else:
            card[key] = value
            if not re.fullmatch(SITUATION_FIELDS[key], value):
                errs.append(f"situation.md:{n}: {key} value `{value}` is not allowed (`{SITUATION_FIELDS[key]}`); fix: correct the value")
    for key in SITUATION_FIELDS:
        if key not in card:
            errs.append(f"situation.md: missing field {key}; fix: add `{key}: <value>`")
    return card, errs


def situation_branches(card):
    """Branches selected from situation-card values; meanings are defined in BOUNDARY.md."""
    source = card["work_source"].split(":")[0]
    return {
        "s02_work": "planned" if card["history"] == "none" else {"git": "git", "tracker": "tracker", "doc": "doc", "none": "ask"}[source],
        "s02_chain": "pain" if card["flow_source"].startswith("doc:") or card["code_home"] != "." else "who",
        "s03_labels": "skip" if card["history"] == "none" and card["prior_harness"] == "none" else "ask",
        "s11": "new" if card["prior_harness"] == "none" else "handoff",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent.parent / "kit"))
    ap.add_argument("--log", help="check a progress.log instead of a kit directory")
    ap.add_argument("--situation", help="check a situation.md instead of a kit directory")
    a = ap.parse_args(argv)
    if a.situation:
        try:
            card, errs = parse_situation(Path(a.situation).read_text(encoding="utf-8"))
        except OSError as e:
            card, errs = {}, [f"situation.md: cannot read file ({e})"]
        for e in errs:
            print(f"ERROR: {e}")
        if errs:
            print(f"{len(errs)} situation card errors.")
            return 1
        for k, v in situation_branches(card).items():
            print(f"branch {k}={v}")
        print("Situation card clean.")
        return 0
    if a.log:
        try:
            errs = check_progress_log(Path(a.log).read_text(encoding="utf-8"), set(read_groups(Path(a.dir))))
        except csv.Error as e:
            errs = [str(e)]
        except OSError as e:
            errs = [f"progress.log: cannot read file ({e})"]
        for e in errs:
            print(f"ERROR: {e}")
        print(f"{len(errs)} log errors." if errs else "Log clean.")
        return 1 if errs else 0
    errs = check(Path(a.dir)) + check_rules_and_gates(Path(a.dir))
    for e in errs:
        print(f"ERROR: {e}")
    print(f"{len(errs)} data errors." if errs else "Kit data clean.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
