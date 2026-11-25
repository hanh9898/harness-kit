"""Check the portable package and its policy, not a live Bot or memory store."""
import json
import re

from conftest import ROOT, run

SKILL = ROOT / "skills/bot/bot-memory"


def section(path, heading):
    body = (SKILL / path).read_text(encoding="utf-8")
    return body.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]


def test_default_manifests_do_not_register_bot_memory():
    pi = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["pi"]["skills"]
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["skills"]
    for entry in pi + claude:
        assert not SKILL.is_relative_to((ROOT / entry).resolve())


def test_opt_in_budget_and_package_local_runbook():
    result = run(ROOT / "tools/skill_budget.py", "--root", ROOT, "--dir", "skills/bot",
                 "--strict", "--json")
    assert result.returncode == 0, result.stdout + result.stderr
    row, = (row for row in json.loads(result.stdout)["dirs"][0]["rows"]
            if row["folder"] == SKILL.name)
    assert row["name"] == SKILL.name
    assert 0 < row["chars"] <= 150

    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    targets = re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", entry)
    assert "HOST.md" in targets
    for target in targets:
        if "://" not in target:
            assert (SKILL / target).is_file(), target


def test_storage_scopes_are_separate():
    scopes = section("SKILL.md", "Keep storage scopes separate")
    rows = dict(re.findall(r"^\| ([^|]+?) \| (.+) \|$", scopes, re.M))
    assert set(rows) == {
        "Layer", "---", "Durable Bot rules", "Personal memory", "Job files", "Operational state",
    }
    assert "`MEMORY.md`" in rows["Durable Bot rules"]
    assert "explicit consent" in rows["Personal memory"]
    assert "`files/<job>/`" in rows["Job files"]
    assert "Checkpoints" in rows["Operational state"]


def test_only_scoped_uncontested_high_rules_apply():
    policy = " ".join(section("SKILL.md", "Read and apply").split())
    assert "Only auto-apply an in-scope, uncontested `high` rule." in policy
    assert "A `low` rule is a candidate to verify, not an instruction." in policy
    assert "never create a store, file, directory or write-side sync" in policy
    host = " ".join(section("HOST.md", "Store requirements").split())
    assert "Enforce caller, instance and topic access before any read." in host
    assert "read-only refresh" in host
    assert "do not use a sync operation that could publish" in host


def test_rule_writes_are_scoped_deduplicated_and_conflict_safe():
    policy = " ".join(section("SKILL.md", "Record and reconcile").split())
    assert "Verify write authority for the owner, caller, instance and topic." in policy
    assert "forwarded message must not record it again" in policy
    assert "[source: <event>; added: YYYY-MM-DD; confidence: high]" in policy
    assert "Sync one batch immediately per accepted change" in policy
    assert "fresh authorized worker" in policy
    assert "preserve the published revision and the local draft" in policy
    assert "Do not auto-apply or overwrite the disputed rule before reconciliation." in policy

    host = " ".join(section("HOST.md", "Store requirements").split())
    assert "only if its expected revision is still current" in host
    assert "check the authoritative receipt or history before sending another batch" in host


def test_host_qualification_names_negative_cases_and_evidence():
    host = (SKILL / "HOST.md").read_text(encoding="utf-8")
    assert set(re.findall(r"^\| `([^\n`]+)` \|", host, re.M)) == {
        "native", "external", "manual", "unsupported",
    }
    qualification = " ".join(section("HOST.md", "Qualify on an isolated Bot").split())
    for case in (
        "pinned source", "absent store", "audit zero store creation",
        "Resume the old worker", "drop the response after a test write commits",
        "at most one sync batch", "not auto-applied", "stale conflicting write",
        "out-of-scope read", "denied before disclosure", "synthetic private data",
    ):
        assert case in qualification
