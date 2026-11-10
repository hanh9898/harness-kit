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


def test_practice_rules_come_after_all_generated_rules_and_stay_unverified():
    r = list(rows("rules.csv").values())
    flags = [x["source"].startswith("practice:") for x in r]
    assert any(flags) and flags == sorted(flags), "practice rules must be appended after the generated ones"
    for x in r:
        if x["source"].startswith("practice:"):
            assert x["certainty"] == "inferred" and x["verified_on"] == "" and x["topic"], x["id"]
    by_id = rows("rules.csv")
    assert by_id["2.24"]["topic"] == "agent-docs" and by_id["7.32"]["topic"] == "testing-and-review"


def test_h18_is_the_last_lego():
    assert list(rows("legos.csv"))[-1] == "H18"


def test_l08_detail_gives_checkable_completion_condition():
    d = rows("legos.csv")["L08"]["detail"]
    assert "120000" in d and "git diff --summary" in d


def test_i04_detail_lists_the_five_classes():
    d = rows("legos.csv")["I04"]["detail"]
    for letter in "ABCDE":
        assert f"{letter}." in d, letter


def test_completion_check_requires_explicit_policy_and_a_fallback():
    d = rows("legos.csv")["D04"]["detail"].lower()
    assert "warning or blocking" in d and "cap retries" in d
    assert "cannot intercept" in d and "launcher or ci" in d
