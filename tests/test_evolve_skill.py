"""harness-evolve structural and boundary checks; runtime behavior is covered by CHECKLIST.md."""
import json
import re

import pytest

from conftest import CHECK_BOUNDARY, KIT, ROOT, TOKENS, run

SKILL = ROOT / "skills" / "harness" / "harness-evolve"


def test_entry_is_eligible_for_explicit_and_model_selection():
    """Packaging eligibility only; real loading/result evidence lives in CHECKLIST.md."""
    head = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    assert "name: harness-evolve" in head
    assert "description:" in head
    assert "disable-model-invocation: true" not in head
    assert "allow_implicit_invocation: true" in (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")


def test_entry_references_its_runtime_guidance():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for sib in ("DRIFT.md", "CHANGE-FLOW.md", "CHECK-STEP.md", "UPDATE.md", "ADOPTION.md"):
        assert (SKILL / sib).is_file() and f"]({sib})" in body


def test_checklist_file_exists():
    assert (SKILL / "CHECKLIST.md").is_file()


@pytest.mark.parametrize(("runbook", "operation"), [
    ("DESIGN-WRITEBACK.md", "prepare"),
    ("DESIGN-WRITEBACK.md", "publish"),
    ("ADOPTION.md", "bot-setup"),
])
def test_v1_handoff_examples_pass_the_shipped_checker(tmp_path, runbook, operation):
    examples = re.findall(r"```json\n(.*?)\n```", (SKILL / runbook).read_text(encoding="utf-8"), re.S)
    example, = [value for value in examples if json.loads(value)["operation"] == operation]
    path = tmp_path / f"{operation}.json"
    path.write_text(example, encoding="utf-8")
    result = run(KIT / "scripts" / "check-stage-handoff", "--expect-operation", operation, path)
    assert result.returncode == 0, result.stderr
    assert result.stdout == f"OK: v1 {operation} handoff shape is valid\n"
    if operation == "prepare":
        prepare = json.loads(example)
        assert prepare["spec_ref"]
        assert prepare["needed_route_refs"] == ["route:ticket-draft@1"]
        assert "ticket_ref" not in prepare


def test_preparation_reuses_compatible_artifacts():
    guidance = " ".join((SKILL / "DESIGN-WRITEBACK.md").read_text().split())
    assert "If both are compatible, skip preparation" in guidance
    assert "reuse the canonical ticket rather than publishing again" in guidance


@pytest.mark.parametrize(("runbook", "guard"), [
    ("ADOPTION.md", "Missing, unreadable or wrong-identity stores block dependent work"),
    ("ADOPTION.md", "do not reinstall"),
    ("DESIGN-WRITEBACK.md", "namespace blocks publication"),
    ("SKILL.md", "missing, stale or conflicting claim blocks dispatch"),
    ("UPDATE.md", "While `Unknown`, do not retry, re-publish"),
])
def test_runbooks_keep_fail_closed_guards(runbook, guard):
    guidance = " ".join((SKILL / runbook).read_text().split())
    assert guard in guidance


def test_relative_guidance_links_resolve():
    # A concrete packaging contract, not wording or runtime acceptance.
    for source in SKILL.glob("*.md"):
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", source.read_text()):
            if "://" not in target:
                assert (source.parent / target).is_file(), (source.name, target)


def test_skill_has_no_machine_absolute_paths():
    for f in SKILL.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".yaml"}:
            assert "/Users/" not in f.read_text(encoding="utf-8"), f


def test_skills_have_no_forbidden_tokens():
    r = run(CHECK_BOUNDARY, "--root", ROOT / "skills", "--tokens", TOKENS, "--strict")
    assert r.returncode == 0, r.stdout
