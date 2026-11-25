"""harness-setup structural and boundary checks; runtime behavior is covered by CHECKLIST.md."""
import json
import re

from conftest import CHECK_BOUNDARY, KIT, ROOT, TOKENS, run

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
    assert "](FOUNDATION.md#target-profile-and-caller-mode)" in body
    assert "](RECORD-FORMAT.md#current-stage-handoffs)" in body


def test_setup_guidance_keeps_bot_work_opt_in_and_repo_inputs_optional_for_bot_only():
    foundation = (SKILL / "FOUNDATION.md").read_text(encoding="utf-8")
    repo_only, = re.findall(r"^\| `repo-only` \| (.*?) \|$", foundation, re.M)
    bot_only, = re.findall(r"^\| `bot-only` \| (.*?) \|$", foundation, re.M)
    assert "existing two-pass questions" in repo_only
    assert "Do not open Bot discovery" in repo_only
    assert "load Inbox/Memory" in repo_only
    assert "emit `bot-setup`" in repo_only
    assert "Skip repo and Product tracker inputs" in bot_only


def test_documented_setup_payloads_pass_the_stage_checker(tmp_path):
    records = (SKILL / "RECORD-FORMAT.md").read_text(encoding="utf-8")
    examples = {}
    for source in re.findall(r"^```json\n(.*?)^```$", records, re.M | re.S):
        payload = json.loads(source)
        operation = payload["operation"]
        assert operation not in examples
        examples[operation] = payload
        handoff = tmp_path / f"{operation}.json"
        handoff.write_text(source, encoding="utf-8")
        result = run(KIT / "scripts/check-stage-handoff", "--expect-operation", operation, handoff)
        assert result.returncode == 0, result.stderr
    assert set(examples) == {"prepare", "publish", "bot-setup"}
    target = examples["publish"]["target"]
    assert target["instance"].startswith("local:")
    assert target["role"] == "harness"
    assert examples["bot-setup"]["disabled_capabilities"] == ["wake"]


def test_canonical_publish_contract_allows_the_selected_local_harness_target():
    contract = (KIT / "STAGE-CONTRACTS.md").read_text(encoding="utf-8")
    publish = contract.split("→ Implement: `publish`\n", 1)[1].split("\n## ", 1)[0]
    assert "selected local Harness record" in publish
    assert "not a fallback" in publish


def test_setup_selects_mode_before_any_prerequisite_route():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    entry, design = body.split("## Phase A:", 1)
    design, implementation = design.split("## Phase B:", 1)
    assert "Choose Inspect, Advice or Apply" in entry
    assert "Default to Inspect" in entry
    assert "Apply must be explicit" in entry
    assert "Inspect and Advice never install or activate anything" in entry
    assert "even with a prior install grant" in entry
    verify = "](ACTIVATION.md#verify-upstream-prerequisites)"
    assert verify in design[:design.index("](DISCOVERY.md)")]
    assert "Apply only" in implementation[:implementation.index(verify)]
    assert verify in implementation[:implementation.index("](ACTIVATION.md)")]


def test_missing_methods_block_dependent_discovery_and_only_apply_reaches_install():
    activation = (SKILL / "ACTIVATION.md").read_text(encoding="utf-8")
    verify, install = activation.split("\n## Install required upstream skills\n", 1)
    install = install.split("\n## ", 1)[0]
    assert "confirmed missing" in verify and "only in Apply" in verify
    assert "hold dependent work" in verify
    assert "H3" in install.split("```sh", 1)[0]
    assert 'npx "skills@$INSTALLER_VERSION" add "$MATT_REPO_AT_PIN"' in install
    discovery = (SKILL / "DISCOVERY.md").read_text(encoding="utf-8")
    assert "](ACTIVATION.md#install-required-upstream-skills)" not in discovery
    assert "hold dependent discovery" in discovery


def test_wrong_caller_and_ambiguity_are_not_missing_and_probes_are_scoped():
    activation = (SKILL / "ACTIVATION.md").read_text(encoding="utf-8")
    verify = activation.split("\n## Install required upstream skills\n", 1)[0]
    assert "wrong caller" in verify and "ambiguous" in verify
    assert "blocked, not missing" in verify
    assert "exact ID, source, revision, caller and invocation policy" in verify
    assert "Probe each required route once per" in verify


def test_project_overrides_are_templates_not_default_entries():
    overrides = ROOT / "skills/overrides"
    templates = {path.parent.name: path for path in overrides.glob("*/SKILL.md")}
    assert set(templates) == {
        "harness-project-to-spec", "harness-project-to-tickets", "harness-project-implement",
    }
    for skill_id, path in templates.items():
        head = path.read_text(encoding="utf-8").split("---")[1]
        assert f"name: {skill_id}" in head.splitlines()
        assert not re.search(r"^disable-model-invocation:\s*true$", head, re.M)
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    pi = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["pi"]
    for manifest in (claude, pi):
        roots = [(ROOT / entry).resolve() for entry in manifest["skills"]]
        assert not any(path.resolve().is_relative_to(root)
                       for root in roots for path in templates.values())


def test_h4_is_a_separate_registration_gate_and_pair_is_draft_only():
    activation = (SKILL / "ACTIVATION.md").read_text(encoding="utf-8")
    registration = activation.split("## Register the v1 implementation overrides on Devin", 1)[1]
    registration = registration.split("\n## ", 1)[0]
    assert "project administrator grant (H4)" in registration
    assert "H3 does not authorize registration" in registration
    assert "H4 does not authorize execution" in registration
    assert "draft-only" in registration
    assert "route-readiness" in registration
    assert registration.index("First read back") < registration.index("permitted no-write probe")
    assert "Do not require prior output evidence for the first probe" in registration


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
