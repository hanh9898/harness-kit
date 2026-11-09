"""Translation-review regressions (ticket 16): corrected rules do not revert."""
import csv

from conftest import KIT


def rules():
    with (KIT / "rules.csv").open(encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def test_cap_rule_keeps_the_only_source_example():
    assert "max_turns=30" in rules()["4.26"]["rule"]


def test_rules_fixed_in_review_keep_their_urls():
    r = rules()
    assert "alignment-assessment-cybersecurity-incidents" in r["3.14"]["source"]
    assert "investigating-unintended-model-actions" in r["3.14"]["source"]
    assert "/model-config" in r["4.29"]["source"] and "/sub-agents" in r["4.29"]["source"]


def test_only_known_rules_lack_a_url():
    lacking = sorted(i for i, x in rules().items() if "http" not in x["source"])
    assert lacking == ["1.33", "2.02", "2.24", "2.25", "2.26", "3.23", "4.42", "5.35", "7.26", "7.32", "7.33", "7.34"]
