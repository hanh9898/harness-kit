"""Gate data: verified rules require dates, verbatim source quotes and verification methods."""
import csv
import re

import pytest

from conftest import CHECK_KIT, KIT, run, row, write_kit

RULE_COLS = ["id", "topic", "rule", "source", "certainty", "check", "verified_on"]
GATE_COLS = ["id", "gate", "verify_method", "verified_quote", "note"]


def rule(id, certainty="stated", verified_on="2026-11-05"):
    return dict(id=id, topic="configuration", rule=f"Rule {id}", source="K01 https://example.com",
                certainty=certainty, check="machine", verified_on=verified_on)


def gate(id, gate="yes", method="raw-grep", quote="Exact sentence from the page.", note=""):
    return dict(id=id, gate=gate, verify_method=method, verified_quote=quote, note=note)


def write(root, rules, gates, *, rule_cols=RULE_COLS):
    write_kit(root, [row("A01")])
    for name, cols, data in (("rules.csv", rule_cols, rules), ("gates.csv", GATE_COLS, gates)):
        with (root / name).open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for r in data:
                w.writerow([r.get(c, "") for c in cols])
    return root


def fails(tmp_path, rules, gates, needle):
    r = run(CHECK_KIT, "--dir", write(tmp_path, rules, gates))
    out = r.stdout + r.stderr
    assert r.returncode != 0 and needle in out, out


def test_good_gate_passes(tmp_path):
    r = run(CHECK_KIT, "--dir", write(tmp_path, [rule("9.01")], [gate("9.01")]))
    assert r.returncode == 0, r.stdout


@pytest.mark.parametrize("with_gates", [True, False], ids=["with-gates", "without-gates"])
@pytest.mark.parametrize("column", RULE_COLS)
def test_missing_rule_column_rejected(tmp_path, column, with_gates):
    header = [c for c in RULE_COLS if c != column]
    root = write(tmp_path, [rule("9.01")], [gate("9.01")], rule_cols=header)
    if not with_gates:
        (root / "gates.csv").unlink()

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert f"rules.csv:1: missing columns {column};" in r.stdout


@pytest.mark.parametrize("with_gates", [True, False], ids=["with-gates", "without-gates"])
def test_truncated_rule_row_rejected(tmp_path, with_gates):
    root = write(tmp_path, [rule("9.01")], [gate("9.01")])
    if not with_gates:
        (root / "gates.csv").unlink()
    incomplete = rule("9.02")
    with (root / "rules.csv").open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([incomplete[c] for c in RULE_COLS[:-1]])

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "rules.csv:3: 9.02 is missing cells for verified_on;" in r.stdout


def test_surplus_rule_cells_rejected(tmp_path):
    root = write(tmp_path, [rule("9.01")], [gate("9.01")])
    overflow = rule("9.02", verified_on="")
    with (root / "rules.csv").open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([*(overflow[c] for c in RULE_COLS), "stray value"])

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "rules.csv:3: 9.02 has extra cells beyond the header;" in r.stdout


@pytest.mark.parametrize("with_gates", [True, False], ids=["with-gates", "without-gates"])
@pytest.mark.parametrize("rule_id", ["", " \t"], ids=["empty", "whitespace"])
def test_blank_rule_id_rejected(tmp_path, with_gates, rule_id):
    root = write(tmp_path, [rule("9.01"), rule(rule_id, verified_on="")], [gate("9.01")])
    if not with_gates:
        (root / "gates.csv").unlink()

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "rules.csv:3: ? has an empty `id` cell;" in r.stdout


@pytest.mark.parametrize("with_gates", [True, False], ids=["with-gates", "without-gates"])
def test_duplicate_rule_id_rejected(tmp_path, with_gates):
    root = write(tmp_path, [rule("9.01", certainty="inferred", verified_on=""), rule("9.01")],
                 [gate("9.01")])
    if not with_gates:
        (root / "gates.csv").unlink()

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "rules.csv:3: duplicate id 9.01 from line 2" in r.stdout


def test_duplicate_gate_id_rejected(tmp_path):
    root = write(tmp_path, [rule("9.01"), rule("9.02")],
                 [gate("9.01"), gate("9.02"), gate("9.01", quote="Another exact sentence.")])
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "gates.csv:4: duplicate id 9.01 from line 2" in r.stdout


def test_gate_without_verified_on_rejected(tmp_path):
    fails(tmp_path, [rule("9.01", verified_on="")], [gate("9.01")], "verified_on")


def test_rule_without_gate_row_cannot_carry_verified_on(tmp_path):
    fails(tmp_path, [rule("9.01"), rule("9.02")], [gate("9.01")],
          "9.02 has no gate row but retains verified_on")


def test_rule_without_gate_row_can_leave_verified_on_empty(tmp_path):
    r = run(CHECK_KIT, "--dir", write(tmp_path, [rule("9.01"), rule("9.02", verified_on="")],
                                    [gate("9.01")]))
    assert r.returncode == 0, r.stdout


def test_gate_with_malformed_date_rejected(tmp_path):
    fails(tmp_path, [rule("9.01", verified_on="yesterday")], [gate("9.01")], "verified_on")


def test_gate_with_impossible_date_rejected(tmp_path):
    fails(tmp_path, [rule("9.01", verified_on="2026-02-29")], [gate("9.01")],
          "rules.csv verified_on `2026-02-29` is not a calendar date")


def test_gate_with_valid_leap_day_passes(tmp_path):
    r = run(CHECK_KIT, "--dir", write(tmp_path, [rule("9.01", verified_on="2024-02-29")], [gate("9.01")]))
    assert r.returncode == 0, r.stdout


def test_gate_without_quote_rejected(tmp_path):
    fails(tmp_path, [rule("9.01")], [gate("9.01", quote="")], "verified_quote")


def test_gate_with_webfetch_rejected(tmp_path):
    fails(tmp_path, [rule("9.01")], [gate("9.01", method="webfetch")],
          "verify_method `webfetch` is insufficient for a gate; fix: use raw-grep")


def test_gate_with_unknown_method_rejected(tmp_path):
    fails(tmp_path, [rule("9.01")], [gate("9.01", method="vibes")], "verify_method")


def test_gate_with_low_certainty_rejected(tmp_path):
    fails(tmp_path, [rule("9.01", certainty="open")], [gate("9.01")], "certainty")


def test_gate_for_unknown_rule_rejected(tmp_path):
    fails(tmp_path, [rule("9.01")], [gate("9.99")], "9.99")


def test_gate_value_must_be_yes_or_no(tmp_path):
    fails(tmp_path, [rule("9.01")], [gate("9.01", gate="maybe")], "gate")


def test_demoted_rule_is_not_a_gate(tmp_path):
    ok = run(CHECK_KIT, "--dir", write(tmp_path, [rule("9.01", certainty="open", verified_on="")],
                                       [gate("9.01", gate="no", method="unreadable", quote="", note="page unreachable")]))
    assert ok.returncode == 0, ok.stdout


def test_non_gate_with_webfetch_passes(tmp_path):
    ok = run(CHECK_KIT, "--dir", write(tmp_path, [rule("9.01", certainty="open", verified_on="")],
                                       [gate("9.01", gate="no", method="webfetch", note="summary only")]))
    assert ok.returncode == 0, ok.stdout


def test_demoted_rule_with_gate_no_needs_reason(tmp_path):
    fails(tmp_path, [rule("9.01", certainty="open", verified_on="")], [gate("9.01", gate="no", quote="", note="")], "note")


def test_real_kit_gates_are_verified():
    rules = {r["id"]: r for r in csv.DictReader((KIT / "rules.csv").open(encoding="utf-8", newline=""))}
    gates = list(csv.DictReader((KIT / "gates.csv").open(encoding="utf-8", newline="")))
    yes = [g for g in gates if g["gate"] == "yes"]
    assert 5 <= len(gates) <= 10
    for g in yes:
        r = rules[g["id"]]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["verified_on"]), g["id"]
        assert g["verified_quote"].strip() and r["certainty"] == "stated", g["id"]
    for g in gates:
        if g["gate"] == "no":
            assert rules[g["id"]]["certainty"] != "stated" and rules[g["id"]]["verified_on"] == "", g["id"]


def test_only_gate_rules_carry_verified_on():
    gates = {g["id"] for g in csv.DictReader((KIT / "gates.csv").open(encoding="utf-8", newline="")) if g["gate"] == "yes"}
    for r in csv.DictReader((KIT / "rules.csv").open(encoding="utf-8", newline="")):
        assert (r["verified_on"] != "") == (r["id"] in gates), r["id"]
