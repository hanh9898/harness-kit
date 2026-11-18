"""One-time generator: independent report counts, partial certainty, and generated kit validation;
rerunning preserves hand-edited kit data."""
import csv
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import CHECK_BOUNDARY, CHECK_KIT, KIT, KIT_CLI, ROOT, TOKENS, run

GEN = ROOT / "skills" / "harness" / "harness-evolve" / "scripts" / "generate_kit.py"
SEED = GEN.parent / "seed"
NOTES = ROOT / "docs" / "generation-notes.md"
REPORTS = Path(os.environ.get("HARNESS_REPORTS", "/Users/hanhnt2/Desktop/hbu-1976-control/.scratch/harness-standards-suite"))
# Rows added AFTER initial generation: H18, G13/G14, N07/N08, D24 and J13. CSV is authoritative.
# the generator and seeds do NOT add these rows, so source report counts remain 162/211.
ADDED_AFTER_GENERATION = {"legos": 7, "rules": sum(r["source"].startswith("practice:") for r in csv.DictReader((ROOT / "kit" / "rules.csv").open(encoding="utf-8", newline="")))}
NOMINAL = {"legos": 162, "rules": 211, "patterns": 13}
needs_reports = pytest.mark.skipif(not (REPORTS / "synthesis.md").is_file(), reason="source reports are unavailable on this machine")
CERTAINTY = {"stated", "inferred", "open", "partial"}
RUNGS = {"instruction-file", "skill", "script-cli", "mcp"}
PARTIAL_REPORTS = ("17", "27", "28")
VIET = re.compile(r"[\xe0\xe1\u1ea1\u1ea3\xe3\xe2\u1ea7\u1ea5\u1ead\u1ea9\u1eab\u0103\u1eb1\u1eaf\u1eb7\u1eb3\u1eb5\xe8\xe9\u1eb9\u1ebb\u1ebd\xea\u1ec1\u1ebf\u1ec7\u1ec3\u1ec5\xec\xed\u1ecb\u1ec9\u0129\xf2\xf3\u1ecd\u1ecf\xf5\xf4\u1ed3\u1ed1\u1ed9\u1ed5\u1ed7\u01a1\u1edd\u1edb\u1ee3\u1edf\u1ee1\xf9\xfa\u1ee5\u1ee7\u0169\u01b0\u1eeb\u1ee9\u1ef1\u1eed\u1eef\u1ef3\xfd\u1ef5\u1ef7\u1ef9\u0111]", re.I)


def gen(dest, *extra):
    return subprocess.run([sys.executable, "-I", str(GEN), "--reports", str(REPORTS), "--dest", str(dest), *extra],
                          capture_output=True, text=True)


def rows(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_gen():
    spec = importlib.util.spec_from_file_location("generate_kit", GEN)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---- Independent report counts; separate regexes, no generator calls. ----
def count_legos():
    t = (REPORTS / "research" / "25-lego-catalog.md").read_text(encoding="utf-8")
    return len(re.findall(r"^### [A-N]\d+\. ", t, re.M))


def count_groups():
    t = (REPORTS / "research" / "25-lego-catalog.md").read_text(encoding="utf-8")
    return len(re.findall(r"^### Nh\xf3m [A-N]\. ", t, re.M))


def count_rules():
    t = (REPORTS / "synthesis.md").read_text(encoding="utf-8")
    return len(re.findall(r"^\| [1-7]\.\d\d \|", t, re.M))


def count_patterns():
    t = (REPORTS / "research" / "26-architecture-frameworks.md").read_text(encoding="utf-8")
    block = t.split("## 3. Ma tr\u1eadn h\u1ed9i t\u1ee5")[1].split("\n## ")[0]
    lines = [l for l in block.splitlines() if l.startswith("|")]
    return len(lines) - 2  # Exclude the header and separator.


def count_levels():
    t = (REPORTS / "research" / "27-delegated-decision-frameworks.md").read_text(encoding="utf-8")
    return len(re.findall(r'\b\d "(?:Tell|Sell|Consult|Agree|Advise|Inquire|Delegate):', t))


@needs_reports
def test_independent_counts_match_generated_or_difference_is_explained(tmp_path):
    r = gen(tmp_path / "out")
    assert r.returncode == 0, r.stdout + r.stderr
    out = tmp_path / "out"
    got = {"legos": len(rows(out / "legos.csv")), "rules": len(rows(out / "rules.csv")),
           "patterns": len(re.findall(r"^\| \d+ \|", (out / "patterns.md").read_text(encoding="utf-8"), re.M))}
    counted = {"legos": count_legos(), "rules": count_rules(), "patterns": count_patterns()}
    assert got == counted, f"CSV/md counts {got} differ from report counts {counted}"
    assert count_groups() == 14 == len({r["group"] for r in rows(out / "legos.csv")})
    notes = NOTES.read_text(encoding="utf-8") if NOTES.is_file() else ""
    for key, nominal in NOMINAL.items():
        if counted[key] != nominal:
            assert re.search(rf"^## {key}\b.*{nominal}.*{counted[key]}", notes, re.M | re.S), \
                f"{key}: counted {counted[key]} instead of {nominal}, without an explanation in docs/generation-notes.md"
    levels = len(re.findall(r"^\| [1-7] \| (?:Tell|Sell|Consult|Agree|Advise|Inquire|Delegate) \|",
                            (out / "delegation.md").read_text(encoding="utf-8"), re.M))
    assert levels == count_levels() == 7


@needs_reports
def test_committed_kit_matches_counts():
    assert len(rows(KIT / "legos.csv")) == count_legos() + ADDED_AFTER_GENERATION["legos"]
    assert len(rows(KIT / "rules.csv")) == count_rules() + ADDED_AFTER_GENERATION["rules"]


# ---- Partial certainty (R6). ----
def violations(rows_, source_key="sources"):
    bad = []
    for r in rows_:
        refs = set(re.findall(r"\bR(\d+)\b", r[source_key]))
        if refs & set(PARTIAL_REPORTS) and r["certainty"] != "partial":
            bad.append(r["id"])
    return bad


def test_checker_catches_partial_source_with_high_certainty():
    assert violations([{"id": "X1", "sources": "note:R27", "certainty": "stated"}]) == ["X1"]
    assert violations([{"id": "X2", "sources": "note:R27 | note:R03", "certainty": "partial"}]) == []
    assert violations([{"id": "X3", "sources": "note:R24", "certainty": "stated"}]) == []


@pytest.mark.parametrize("name,key", [("legos.csv", "sources"), ("rules.csv", "source")])
def test_no_partial_source_row_has_high_certainty(name, key):
    assert violations(rows(KIT / name), key) == []


def test_certainty_pure_function_marks_partial():
    g = load_gen()
    assert g.certainty_for("N\xd3I R\xd5 (C08)", ["C08", "R27"]) == "partial"
    assert g.certainty_for("N\xd3I R\xd5 (C08)", ["C08"]) == "stated"
    assert g.certainty_for("SUY RA (ba n\u1ec1n)", ["C08"]) == "inferred"


def test_delegation_rows_are_all_partial():
    text = (KIT / "delegation.md").read_text(encoding="utf-8")
    table_rows = [l for l in text.splitlines() if re.match(r"^\| (\d) \|", l)]
    assert len(table_rows) == 4 + 7
    for l in table_rows:
        assert "| partial |" in l, l


# ---- Generated kit passes every checker. ----
def test_committed_kit_files_and_values():
    for r in rows(KIT / "legos.csv"):
        assert r["rung"] in RUNGS and r["certainty"] in CERTAINTY, r["id"]
        assert not VIET.search(" ".join(r.values())), f"{r['id']} contains accented text"
    rr = rows(KIT / "rules.csv")
    assert list(rr[0].keys()) == ["id", "topic", "rule", "source", "certainty", "check", "verified_on"]
    ids = [r["id"] for r in rr]
    assert len(ids) == len(set(ids))
    for r in rr:
        assert r["certainty"] in CERTAINTY and r["rule"].strip() and r["source"].strip(), r["id"]
        assert not VIET.search(" ".join(r.values())), f"{r['id']} contains accented text"


@needs_reports
def test_generated_kit_passes_all_checkers(tmp_path):
    out = tmp_path / "out"
    assert gen(out).returncode == 0
    assert run(CHECK_KIT, "--dir", out).returncode == 0
    b = run(CHECK_BOUNDARY, "--root", out, "--tokens", TOKENS, "--strict")
    assert b.returncode == 0, b.stdout
    cli = subprocess.run([sys.executable, "-I", str(KIT_CLI), "--dir", str(out), "list"], capture_output=True, text=True)
    assert cli.returncode == 0 and re.search(r"^A\tIntake\t7 ", cli.stdout, re.M)


def test_seed_folder_has_no_forbidden_tokens():
    r = run(CHECK_BOUNDARY, "--root", SEED, "--tokens", TOKENS, "--strict")
    assert r.returncode == 0, r.stdout


# ---- Rerunning preserves hand-edited kit data. ----
@needs_reports
def test_rerun_refuses_to_overwrite_hand_edited_kit(tmp_path):
    out = tmp_path / "out"
    assert gen(out).returncode == 0
    f = out / "legos.csv"
    f.write_text(f.read_text(encoding="utf-8").replace("stated", "open", 1), encoding="utf-8")
    edited = {p.name: p.read_bytes() for p in out.iterdir()}
    r = gen(out)
    assert r.returncode != 0 and "legos.csv" in r.stdout + r.stderr
    assert {p.name: p.read_bytes() for p in out.iterdir()} == edited
    other = tmp_path / "other"
    assert gen(other).returncode == 0 and (other / "rules.csv").is_file()


@needs_reports
def test_refuses_when_any_single_target_exists_and_writes_nothing(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "patterns.md").write_text("mine", encoding="utf-8")
    r = gen(out)
    assert r.returncode != 0
    assert sorted(p.name for p in out.iterdir()) == ["patterns.md"]
    assert (out / "patterns.md").read_text(encoding="utf-8") == "mine"
