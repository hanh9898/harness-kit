#!/usr/bin/env python3
"""generate_kit: one-time conversion of research reports into kit data (legos.csv, groups.csv, rules.csv, patterns.md, delegation.md).

  generate_kit.py --reports DIR --dest DIR

--reports points to synthesis.md and research/ (reports 25, 26, 27, 28). The conversion is partly automated:
  - Structured fields parsed from reports: IDs, groups, certainty, source URLs, rule order and pattern organization counts.
  - Free text (names, summaries, rules, patterns and delegation guidance) has been translated into English seed data;
    The script checks every seed ID and count against the reports and stops on mismatches.
Refuses to overwrite existing output files: writes nothing and exits 1. After the first generation, CSV is authoritative.
Uses only the standard library.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = HERE / "seed"
PARTIAL_REPORTS = {"17", "27", "28"}
RUNGS = ("instruction-file", "skill", "script-cli", "mcp")
TOPICS = {1: "skill-writing", 2: "agent-docs", 3: "prompts-and-roles", 4: "configuration",
          5: "workflow", 6: "tools-and-cli", 7: "testing-and-review"}
OUTPUTS = ("legos.csv", "groups.csv", "rules.csv", "patterns.md", "delegation.md")
LEGO_COLUMNS = ["id", "group", "name", "summary", "needed_when", "rung", "certainty", "sources", "detail"]
RULE_COLUMNS = ["id", "topic", "rule", "source", "certainty", "check", "verified_on"]
PREFIX = {"C": "https://code.claude.com/docs/en/", "X": "https://learn.chatgpt.com/docs/"}


class GenError(Exception):
    pass


def certainty_for(reliability_text, source_ids):
    """Row certainty; references to reports 17, 27 or 28 always yield partial (R6)."""
    # Escaped input-schema labels preserve compatibility with archived source reports.
    if any(s in {f"R{n}" for n in PARTIAL_REPORTS} or s in PARTIAL_REPORTS for s in source_ids):
        return "partial"
    t = reliability_text.strip().removeprefix("NGU\u1ed2N ")
    if t.startswith("N\xd3I R\xd5"):
        return "stated"
    if t.startswith("\u0053\u0055\u0059\u0020\u0052\u0041"):
        return "inferred"
    if "M\u1ede" in t:
        return "open"
    return "inferred"


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        raise GenError(f"Cannot read {path} ({e}); fix: point --reports to a directory containing synthesis.md and research/")


# ---------- legos (report 25) ----------
def source_urls(text):
    """Report 25 section 2 source table: code -> URL for platform docs and research articles."""
    urls = {}
    text = text.split("## 2. B\u1ea3ng ngu\u1ed3n")[1].split("\n## 3.")[0]
    for m in re.finditer(r"^\| ([CX]\d\d) \| ([^|]+?) \|", text, re.M):
        code, cell = m.groups()
        slug = cell.split()[0]
        if code[0] == "C" and slug.endswith("llms.txt"):
            urls[code] = "https://code.claude.com/docs/llms.txt"
        else:
            urls[code] = PREFIX[code[0]] + slug
    for m in re.finditer(r"^\| (A\d\d) \| [^|]*`(https?://[^`\s]+)`", text, re.M):
        urls[m.group(1)] = m.group(2)
    return urls


def parse_legos(text):
    body = text.split("## 3. Kho c\xe1c mi\u1ebfng lego")[1].split("\n## 4.")[0]
    urls = source_urls(text)
    out = []
    for block in re.split(r"(?m)^(?=### [A-N]\d+\. )", body)[1:]:
        m = re.match(r"### ([A-N])(\d+)\. ", block)
        letter, n = m.groups()
        field = lambda key: next((l[len(key):] for l in block.splitlines() if l.startswith(key)), "")
        mech, sure, need = field("- C\u01a1 ch\u1ebf: "), field("- \u0110\u1ed9 ch\u1eafc: "), field("- C\u1ea7n khi: ")
        cited = " ".join([mech, sure, need])
        codes = [c for grp in re.findall(r"\[([A-Z]\d\d(?:[, ]+[A-Z]\d\d)*)\]", cited) for c in re.findall(r"[A-Z]\d\d", grp)]
        reports = re.findall(r"\bR(\d\d)\b", cited)
        links = [urls[c] for c in dict.fromkeys(codes) if c in urls]
        notes = [f"note:R{r}" for r in dict.fromkeys(reports)]
        src_ids = [f"R{r}" for r in reports]
        out.append({"id": f"{letter}{int(n):02d}", "group": letter, "certainty": certainty_for(sure, src_ids),
                    "sources": " | ".join(links + notes) or "practice:observed in working harnesses"})
    return out


def build_legos(reports):
    parsed = parse_legos(read(reports / "research" / "25-lego-catalog.md"))
    seed = {}
    for ln, line in enumerate(read(SEED / "legos-en.txt").splitlines(), 1):
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(" || ")]
        if len(parts) != 6:
            raise GenError(f"seed/legos-en.txt:{ln}: expected 6 fields, got {len(parts)}; fix: use `ID || name || summary || needed_when || rung || detail`")
        if parts[4] not in RUNGS:
            raise GenError(f"seed/legos-en.txt:{ln}: rung `{parts[4]}` is not in {' | '.join(RUNGS)}")
        seed[parts[0]] = parts
    ids = [p["id"] for p in parsed]
    if set(ids) != set(seed) or len(ids) != len(seed):
        raise GenError(f"seed/legos-en.txt has {len(seed)} pieces; report 25 has {len(ids)}; missing {sorted(set(ids) - set(seed))[:5]}, extra {sorted(set(seed) - set(ids))[:5]}; fix: align every seed ID")
    rows = []
    for p in parsed:
        _, name, summary, needed, rung, detail = seed[p["id"]]
        rows.append({**p, "name": name, "summary": summary, "needed_when": needed, "rung": rung, "detail": detail})
    return rows


def build_groups(reports):
    """English group names from seed/groups-en.txt, matched to report 25 group headings."""
    letters = re.findall(r"^### Nh\xf3m ([A-N])\. ", read(reports / "research" / "25-lego-catalog.md"), re.M)
    seed = dict(line.split(" || ", 1) for line in read(SEED / "groups-en.txt").splitlines() if line.strip())
    if sorted(seed) != sorted(letters):
        raise GenError(f"seed/groups-en.txt groups {sorted(seed)} differ from report 25 groups {sorted(letters)}; fix: align the seed")
    return [{"id": g, "name": seed[g].strip()} for g in letters]


# ---------- rules (synthesis.md) ----------
def parse_rules(text):
    rows = [l for l in text.splitlines() if re.match(r"^\| [1-7]\.\d\d \|", l)]
    parsed = []
    for l in rows:
        cells = [c.strip() for c in l.strip().strip("|").split(" | ")]
        parsed.append(cells)
    # Source code -> URL, derived from cells containing one code and a link.
    idmap = {}
    for cells in parsed:
        for part in cells[2].split(";"):
            ids = re.findall(r"\b([A-Z]\d{1,2}[a-z]?)[‡†◆⚠]", part)
            link = re.findall(r"\]\((https?://[^)]+)\)", part)
            if len(ids) == 1 and link:
                idmap.setdefault(ids[0], link[0])
    guide = re.search(r"Ngu\u1ed3n S1:[^`]*`(https?://[^`]+)`", text)
    if guide:
        idmap.setdefault("S1", guide.group(1))
    out = []
    for cells in parsed:
        rid, _, src, level, check = cells[:5]
        pieces, report_refs = [], []
        for part in src.split(";"):
            part = part.strip()
            ids = re.findall(r"\b([A-Z]\d{1,2}[a-z]?)[‡†◆⚠]+(?:\s*(tr\.\d+|\d+\.\d+))?", part)
            link = re.findall(r"\]\((https?://[^)]+)\)", part)
            for i, loc in ids:
                url = link[0] if len(ids) == 1 and link else idmap.get(i, "")
                pieces.append(" ".join(x for x in (i, loc.replace("tr.", "p.") if loc else "", url) if x))
            if not ids and link:
                pieces.append(link[0])
            m = re.match(r"(\d\d)\b", part)
            if m:
                pieces.append(f"note:R{m.group(1)}")
                report_refs.append(m.group(1))
            report_refs += re.findall(r"b\xe1o c\xe1o (\d\d)\b", part)
        topic = TOPICS[int(rid.split(".")[0])]
        c = "machine+review" if ("m\xe1y" in check and "review" in check) else ("machine" if "m\xe1y" in check else "review")
        out.append({"id": rid, "topic": topic, "source": " | ".join(dict.fromkeys(pieces)) or "unspecified",
                    "certainty": certainty_for(level, [f"R{r}" for r in report_refs]), "check": c, "verified_on": ""})
    return out


def build_rules(reports):
    parsed = parse_rules(read(reports / "synthesis.md"))
    seed = {}
    with (SEED / "rules-en.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            seed[r["id"]] = r["rule"]
    ids = [p["id"] for p in parsed]
    if set(ids) != set(seed) or len(ids) != len(seed):
        raise GenError(f"seed/rules-en.csv has {len(seed)} rules; synthesis.md has {len(ids)}; missing {sorted(set(ids) - set(seed))[:5]}, extra {sorted(set(seed) - set(ids))[:5]}; fix: align every seed ID")
    return [{**p, "rule": seed[p["id"]]} for p in parsed]


# ---------- architecture patterns (report 26) ----------
def build_patterns(reports):
    t = read(reports / "research" / "26-architecture-frameworks.md")
    block = t.split("## 3. Ma tr\u1eadn h\u1ed9i t\u1ee5")[1].split("\n## ")[0]
    lines = [l for l in block.splitlines() if l.startswith("|")][2:]
    parties = []
    for l in lines:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        m = re.match(r"(\d+)", cells[-2])
        parties.append(int(m.group(1)) if m else 0)
    seed = [[p.strip() for p in l.split(" || ")] for l in read(SEED / "patterns-en.txt").splitlines() if l.strip()]
    if len(seed) != len(parties) or any(len(s) != 6 for s in seed):
        raise GenError(f"seed/patterns-en.txt has {len(seed)} patterns; report 26 section 3 has {len(parties)} rows; fix: align the seed")
    out = ["# Team architecture patterns", "",
           f"{len(seed)} patterns for agent teams, taken from the rows of the convergence matrix in the source research. "
           "\"Defined by\" counts independent organizations that define an equivalent pattern. "
           "Start from the simplest pattern and add another only when evidence supports it.", "",
           "| # | Pattern | Also called | What it is | Use when | Avoid when | Defined by | Certainty |",
           "|---|---|---|---|---|---|---|---|"]
    for i, (s, n) in enumerate(zip(seed, parties), 1):
        name, aka, what, use, avoid, cert = s
        out.append(f"| {i} | {name} | {aka} | {what} | {use} | {avoid} | {n} | {cert} |")
    out += ["", "## Notes", "",
            "- Vendors use one loose term for two different ideas (all-to-all talk versus peer handoff); this table keeps them as two separate patterns.",
            "- No source defines \"one small team per ticket\" or \"periodic background run\" as an architecture pattern; the second is a trigger, not a team shape.",
            "- Two sources could not be read (one vendor guide and one framework page), so their pattern names are unchecked.",
            "- Agent teams are an experimental feature in the platform that defines them; state that condition when you adopt the pattern.", ""]
    return "\n".join(out)


def build_delegation(reports):
    # Require reports 27 and 28 and verify that all seven original levels exist.
    t27 = read(reports / "research" / "27-delegated-decision-frameworks.md")
    read(reports / "research" / "28-delegated-decision-frameworks-gap.md")
    levels = re.findall(r'\b\d "(?:Tell|Sell|Consult|Agree|Advise|Inquire|Delegate):', t27)
    text = read(SEED / "delegation-en.md")
    shown = re.findall(r"^\| [1-7] \| (?:Tell|Sell|Consult|Agree|Advise|Inquire|Delegate) \|", text, re.M)
    if len(levels) != 7 or len(shown) != 7:
        raise GenError(f"Level scale: report 27 has {len(levels)}, seed has {len(shown)}; fix: update seed/delegation-en.md")
    return text


# ---------- write ----------
def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reports", required=True, help="directory containing synthesis.md and research/")
    ap.add_argument("--dest", required=True, help="target kit directory; output files must not already exist")
    a = ap.parse_args(argv)
    dest, reports = Path(a.dest), Path(a.reports)
    clash = [n for n in OUTPUTS if (dest / n).exists()]
    if clash:
        print(f"ERROR: {dest} already contains {', '.join(clash)}; CSV is authoritative and will not be overwritten.\n"
              "fix: edit those files manually or rerun with --dest pointing to another directory.", file=sys.stderr)
        return 1
    try:
        legos, groups, rules = build_legos(reports), build_groups(reports), build_rules(reports)
        patterns, delegation = build_patterns(reports), build_delegation(reports)
    except GenError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    dest.mkdir(parents=True, exist_ok=True)
    write_csv(dest / "legos.csv", LEGO_COLUMNS, legos)
    write_csv(dest / "groups.csv", ["id", "name"], groups)
    write_csv(dest / "rules.csv", RULE_COLUMNS, rules)
    (dest / "patterns.md").write_text(patterns, encoding="utf-8")
    (dest / "delegation.md").write_text(delegation, encoding="utf-8")
    n_patterns = len(re.findall(r"^\| \d+ \|", patterns, re.M))
    print(f"Generated in {dest}: {len(legos)} pieces, {len(rules)} rules, {n_patterns} architecture patterns, and delegation guidance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
