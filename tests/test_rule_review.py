"""Resource review: portable requirements retain provenance without host guarantees."""
import csv

from conftest import KIT


def rules():
    with (KIT / "rules.csv").open(encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def test_host_cap_example_is_not_a_universal_rule():
    r = rules()
    assert "4.26" not in r
    assert "4.25" in r


def test_role_stop_condition_keeps_its_provenance_and_inference_label():
    r = rules()
    assert "alignment-assessment-cybersecurity-incidents" in r["3.14"]["source"]
    assert "investigating-unintended-model-actions" in r["3.14"]["source"]
    assert r["3.14"]["certainty"] == "inferred"


def test_adopted_rules_have_source_links_or_explicit_practice_provenance():
    lacking = sorted(i for i, x in rules().items() if "http" not in x["source"] and not x["source"].startswith("practice:"))
    assert lacking == []
