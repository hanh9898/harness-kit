"""harness-setup structural and boundary checks; runtime behavior is covered by CHECKLIST.md."""
from conftest import CHECK_BOUNDARY, ROOT, TOKENS, run

SKILL = ROOT / "skills" / "harness" / "harness-setup"


def assert_setup_eligibility(body, registration):
    """Packaging eligibility only; supported loading still requires host evidence."""
    head = body.split("---")[1]
    keys = {l.split(":")[0] for l in head.strip().splitlines()}
    assert {"name", "description"} <= keys
    assert "disable-model-invocation: true" not in head
    assert "allow_implicit_invocation: true" in registration


def test_setup_is_eligible_for_explicit_and_model_selected_use():
    assert_setup_eligibility((SKILL / "SKILL.md").read_text(encoding="utf-8"),
                             (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))


def test_runtime_reference_branches_are_packaged():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for sib in ("ENVIRONMENT.md", "FOUNDATION.md", "DISCOVERY.md", "ACTIVATION.md", "RESUME.md"):
        assert (SKILL / sib).is_file() and f"]({sib})" in body


def test_upstream_install_is_reached_before_discovery_and_override_authoring():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    design, implementation = body.split("## Phase B:", 1)
    install = "](ACTIVATION.md#install-required-upstream-skills)"
    assert install in design[:design.index("](DISCOVERY.md)")]
    assert install in implementation[:implementation.index("](ACTIVATION.md)")]
    activation = (SKILL / "ACTIVATION.md").read_text(encoding="utf-8")
    assert "## Install required upstream skills\n" in activation


def test_checklist_file_exists():
    assert (SKILL / "CHECKLIST.md").is_file()


def test_skills_have_no_forbidden_tokens():
    r = run(CHECK_BOUNDARY, "--root", ROOT / "skills", "--tokens", TOKENS, "--strict")
    assert r.returncode == 0, r.stdout


def test_skill_has_no_machine_absolute_paths():
    for f in SKILL.rglob("*"):
        if f.is_file():
            assert "/Users/" not in f.read_text(encoding="utf-8"), f


def test_kit_commands_resolve_from_skill_dir_and_run_from_a_foreign_copy(tmp_path):
    import re
    import shutil
    # Every kit command in the skill resolves through <skill-dir>.
    cmds = []
    for f in SKILL.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if "kit/scripts/kit" in line and re.match(r"\S+/kit/scripts/kit ", line):
                assert line.startswith("<skill-dir>/../../../kit/scripts/kit "), (f.name, line)
                cmds.append(line.split("#")[0].split()[1:])
    assert cmds
    # Copy the plugin to an unrelated directory; <skill-dir> belongs to that copy.
    plugin = tmp_path / "somewhere else" / "plug"
    shutil.copytree(ROOT, plugin, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    skill_dir = plugin / "skills" / "harness" / "harness-setup"
    kit = skill_dir / ".." / ".." / ".." / "kit" / "scripts" / "kit"
    out = run(kit, "list")
    assert out.returncode == 0 and out.stdout.strip()
    first = run(kit, "list", out.stdout.split()[0])
    assert first.returncode == 0
    show = run(kit, "show", first.stdout.split()[0])
    assert show.returncode == 0 and show.stdout.strip()
    assert run(kit, "list", "P").returncode == 0 and run(kit, "show", "P1").returncode == 0
    assert run(kit, "list", "delegation").returncode == 0 and run(kit, "show", "axis1").returncode == 0
