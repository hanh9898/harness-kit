"""harness-setup structural and boundary checks; runtime behavior is covered by CHECKLIST.md."""
from conftest import CHECK_BOUNDARY, ROOT, TOKENS, run

SKILL = ROOT / "skills" / "harness" / "harness-setup"


def test_skill_is_hand_typed_only():
    head = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    keys = {l.split(":")[0] for l in head.strip().splitlines()}
    assert keys == {"name", "description", "disable-model-invocation"}
    assert "disable-model-invocation: true" in head
    assert "allow_implicit_invocation: false" in (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")


def test_body_short_and_every_sibling_pointed_to():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert len(body.splitlines()) <= 170
    for sib in ("BOUNDARY.md", "RECORD-FORMAT.md", "GATE.md", "PROPOSALS.md", "DELEGATION.md", "ROLES.md"):
        assert (SKILL / sib).is_file() and f"]({sib})" in body


def test_checklist_file_exists():
    assert (SKILL / "CHECKLIST.md").is_file()


def test_skills_have_no_forbidden_tokens():
    r = run(CHECK_BOUNDARY, "--root", ROOT / "skills", "--tokens", TOKENS, "--strict")
    assert r.returncode == 0, r.stdout
