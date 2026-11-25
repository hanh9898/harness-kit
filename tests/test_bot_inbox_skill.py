"""Inbox package and documented guardrails; live qualification is in HOST.md."""
import json
import re

import pytest

from conftest import ROOT, run

SKILL = ROOT / "skills/bot/bot-inbox"
BUDGET = ROOT / "tools/skill_budget.py"


def test_explicitly_linked_inbox_has_exact_id_and_fits_budget(tmp_path):
    registry = tmp_path / ".agents/skills"
    registry.mkdir(parents=True)
    (registry / "bot-inbox").symlink_to(SKILL, target_is_directory=True)
    result = run(BUDGET, "--root", tmp_path, "--dir", ".agents/skills", "--strict", "--max-total", "150", "--json")
    assert result.returncode == 0, result.stdout
    [profile] = json.loads(result.stdout)["dirs"]
    [entry] = profile["rows"]
    assert entry["name"] == "bot-inbox"
    assert 0 < entry["chars"] <= 150


@pytest.mark.parametrize(
    ("manifest", "section"),
    [("package.json", "pi"), (".claude-plugin/plugin.json", None)],
)
def test_inbox_is_not_in_default_registration(manifest, section):
    config = json.loads((ROOT / manifest).read_text(encoding="utf-8"))
    entries = (config[section] if section else config)["skills"]
    assert not any(SKILL.is_relative_to((ROOT / entry).resolve()) for entry in entries)


def test_skill_links_to_packaged_host_routes_and_qualification():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    host = (SKILL / "HOST.md").read_text(encoding="utf-8")
    headings = {title.lower().replace(" ", "-") for title in re.findall(r"^## (.+)$", host, re.M)}
    anchors = set(re.findall(r"\]\(HOST\.md#([^)]+)\)", body))
    assert {"resolve-the-route", "qualify-in-an-isolated-bot"} <= anchors <= headings
    assert set(re.findall(r"^\| `([^`]+)` \|", host, re.M)) == {
        "native", "external", "manual", "unsupported",
    }


@pytest.mark.parametrize(
    ("filename", "section", "guardrails"),
    [
        ("SKILL.md", "Keep one active card per action", (
            "authorized respondent, canonical subject and requested action",
            "store-enforced uniqueness or a verified single writer",
            "cannot set priority or defer cards",
        )),
        ("SKILL.md", "Deliver and handle replies separately", (
            "separate send authority",
            "stable delivery key",
            "on unknown outcome, reconcile before retrying",
            "wrong person or thread",
            "independent grant gate",
        )),
        ("HOST.md", "Resolve the route", (
            "explicit opt-in",
            "stop the dependent operation on unresolved id/source conflicts",
        )),
        ("HOST.md", "Qualify in an isolated Bot", (
            "one active card for the action and one initial delivery",
            "zero additional deliveries on replay",
            "zero effect grants",
            "zero results delivered across routes",
            "manual reconciliation is evidence only for the manual route",
        )),
    ],
)
def test_documented_guardrails_stay_in_their_operation_section(filename, section, guardrails):
    body = (SKILL / filename).read_text(encoding="utf-8")
    guidance = body.split(f"\n## {section}\n", 1)[1].split("\n## ", 1)[0]
    normalized = " ".join(guidance.lower().split())
    for guardrail in guardrails:
        assert guardrail in normalized


def test_pr_reconciliation_uses_live_state_and_leaves_unknowns_untouched():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    guidance = body.split("\n## Reconcile PR review cards\n", 1)[1]
    assert "live state from the authoritative target" in guidance
    rows = dict(re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", guidance, re.M))
    assert rows["Open"].startswith("Leave the review card open")
    assert rows["Merged or closed"].startswith("Close the matching review card idempotently")
    assert rows["Unavailable, stale or wrong target"].startswith("Leave the card unchanged")
