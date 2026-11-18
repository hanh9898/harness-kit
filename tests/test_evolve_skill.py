"""harness-evolve structural and boundary checks; runtime behavior is covered by CHECKLIST.md."""
import re
import shutil

from conftest import CHECK_BOUNDARY, ROOT, TOKENS, run

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


def test_kit_commands_resolve_from_a_foreign_copy(tmp_path):
    cmds = []
    for f in SKILL.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if "kit/scripts/kit" in line and re.match(r"\S+/kit/scripts/kit ", line):
                assert line.startswith("<skill-dir>/../../../kit/scripts/kit "), (f.name, line)
                cmds.append(line)
    assert cmds
    plugin = tmp_path / "somewhere else" / "plug"
    shutil.copytree(ROOT, plugin, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    skill_dir = plugin / "skills" / "harness" / "harness-evolve"
    kit = skill_dir / ".." / ".." / ".." / "kit" / "scripts" / "kit"
    out = run(kit, "list")
    assert out.returncode == 0 and out.stdout.strip()
    assert run(kit, "show", run(kit, "list", out.stdout.split()[0]).stdout.split()[0]).returncode == 0
    assert (skill_dir / "UPDATE.md").is_file()
