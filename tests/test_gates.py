"""Gate data: verified rules require dates, verbatim source quotes and verification methods."""
import csv
import re

from conftest import CHECK_KIT, KIT, run, row, write_kit

RULE_COLS = ["id", "topic", "rule", "source", "certainty", "check", "verified_on"]
GATE_COLS = ["id", "gate", "verify_method", "verified_quote", "note"]


def rule(id, certainty="stated", verified_on="2026-11-05"):
    return dict(id=id, topic="configuration", rule=f"Rule {id}", source="K01 https://example.com",
                certainty=certainty, check="machine", verified_on=verified_on)


def gate(id, gate="yes", method="raw-grep", quote="Exact sentence from the page.", note=""):
    return dict(id=id, gate=gate, verify_method=method, verified_quote=quote, note=note)


def write(root, rules, gates):
    write_kit(root, [row("A01")])
    for name, cols, data in (("rules.csv", RULE_COLS, rules), ("gates.csv", GATE_COLS, gates)):
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


def test_gate_without_verified_on_rejected(tmp_path):
    fails(tmp_path, [rule("9.01", verified_on="")], [gate("9.01")], "verified_on")


def test_gate_with_malformed_date_rejected(tmp_path):
    fails(tmp_path, [rule("9.01", verified_on="yesterday")], [gate("9.01")], "verified_on")


def test_gate_without_quote_rejected(tmp_path):
    fails(tmp_path, [rule("9.01")], [gate("9.01", quote="")], "verified_quote")


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


def test_demoted_rule_with_gate_no_needs_reason(tmp_path):
    fails(tmp_path, [rule("9.01", certainty="open", verified_on="")], [gate("9.01", gate="no", quote="", note="")], "note")


def test_real_kit_gates_are_verified():
    rules = {r["id"]: r for r in csv.DictReader((KIT / "rules.csv").open(encoding="utf-8", newline=""))}
    gates = list(csv.DictReader((KIT / "gates.csv").open(encoding="utf-8", newline="")))
    yes = [g for g in gates if g["gate"] == "yes"]
    assert len({g["id"] for g in gates}) == len(gates)
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
