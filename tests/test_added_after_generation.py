"""Post-generation additions (ticket 07, step 1): lego H18, two rules and three detail updates.
After initial generation, CSV is authoritative; the generator and seeds do not track these additions."""
import csv
import re

from conftest import KIT, KIT_CLI, run


def rows(name):
    with (KIT / name).open(encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def test_h18_review_checklist_has_six_points():
    h = rows("legos.csv")["H18"]
    assert h["group"] == "H" and h["certainty"] == "inferred"
    points = re.findall(r"(?:^|\. )([1-6])\) ", h["detail"])
    assert points == ["1", "2", "3", "4", "5", "6"], h["detail"]
    assert "independent" in h["summary"].lower() and "clean context" in h["detail"]


def test_h18_is_shown_by_the_cli():
    r = run(KIT_CLI, "--dir", KIT, "show", "H18")
    assert r.returncode == 0 and "checklist" in r.stdout.lower()


def test_new_rules_are_appended_at_the_end():
    ids = list(rows("rules.csv"))
    assert ids[-8:] == ["2.24", "7.32", "1.33", "2.25", "2.26", "3.23", "7.33", "7.34"]
    r = rows("rules.csv")
    assert r["2.24"]["topic"] == "agent-docs" and r["7.32"]["topic"] == "testing-and-review"
    for i in ids[-8:]:
        assert r[i]["certainty"] == "inferred" and r[i]["verified_on"] == "" and r[i]["source"]


def test_h18_is_the_last_lego():
    assert list(rows("legos.csv"))[-1] == "H18"


def test_l08_detail_gives_checkable_completion_condition():
    d = rows("legos.csv")["L08"]["detail"]
    assert "120000" in d and "absolute path" in d


def test_i04_detail_lists_the_five_classes():
    d = rows("legos.csv")["I04"]["detail"]
    for letter in "ABCDE":
        assert f"{letter}." in d, letter


def test_d04_detail_records_the_disagreement_without_picking_a_side():
    d = rows("legos.csv")["D04"]["detail"].lower()
    assert "disagree" in d and "not settled" in d
    assert "warn first" in d and "does not pick a side" in d
