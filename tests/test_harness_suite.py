"""The installable suite and its scoped runbooks ship together."""
import json
import re
import shutil

import pytest

from conftest import KIT, ROOT, run

SKILL_ROOT = ROOT / "skills/harness"
ENTRIES = {"harness-setup", "harness-evolve", "harness-implement", "harness-library"}


def test_manifests_expose_the_same_four_installed_entries():
    pi = json.loads((ROOT / "package.json").read_text())["pi"]["skills"]
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["skills"]
    expected = {f"./skills/harness/{name}" for name in ENTRIES}
    assert len(pi) == len(claude) == len(expected)
    assert set(pi) == set(claude) == expected
    for name in ENTRIES:
        skill = SKILL_ROOT / name / "SKILL.md"
        assert f"\nname: {name}\n" in skill.read_text()
        assert "allow_implicit_invocation: true" in (skill.parent / "agents/openai.yaml").read_text()


@pytest.mark.parametrize("name", sorted(ENTRIES))
def test_entry_runbooks_have_package_local_links(name):
    for path in (SKILL_ROOT / name).glob("*.md"):
        assert_package_local_links(path)


@pytest.mark.parametrize("name", ["M2-CONFIG.md", "PERSISTENCE.md", "STAGE-CONTRACTS.md"])
def test_kit_contracts_have_package_local_links(name):
    assert_package_local_links(KIT / name)


@pytest.mark.parametrize("entry", [
    "harness-setup/RESUME.md",
    "harness-evolve/DESIGN-WRITEBACK.md",
    "harness-implement/SKILL.md",
    "harness-library/SKILL.md",
])
def test_continuation_uses_one_shared_handoff_contract(entry):
    text = (SKILL_ROOT / entry).read_text(encoding="utf-8")
    assert text.count("](../../../kit/PERSISTENCE.md#continuation-handoff)") == 1


def test_handoff_distinguishes_effect_verification_and_blockers():
    persistence = (KIT / "PERSISTENCE.md").read_text(encoding="utf-8")
    _, _, handoff = persistence.partition("## Continuation handoff\n")
    assert re.findall(r"^\| `(\w+)` \|", handoff, re.MULTILINE) == [
        "Applied", "Verified", "Blocked", "Unknown",
    ]
    assert "recipient's scope" in handoff
    assert "Do not claim `handoff` was invoked." in handoff


def assert_package_local_links(path):
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#") or "<" in target:
            continue
        assert (path.parent / target.split("#")[0]).is_file(), (path.name, target)


def test_library_helpers_resolve_from_a_linked_skill_in_a_foreign_checkout(tmp_path):
    plugin = tmp_path / "checkout with spaces"
    for directory in ("skills", "kit"):
        shutil.copytree(ROOT / directory, plugin / directory)
    registered = tmp_path / "harness-library"
    registered.symlink_to(plugin / "skills/harness/harness-library", target_is_directory=True)
    instructions = (registered / "READ.md").read_text()
    helper_path, = re.findall(r"`<skill-dir>/([^`]+/)`", instructions)
    helpers = registered.resolve() / helper_path
    assert run(helpers / "kit", "show", "reread-source-before-write").returncode == 0
    result = run(helpers / "library", "--store", tmp_path / "selected.sqlite3",
                 "selection", "reread-source-before-write", "--source", "supplied")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["effective"] is True


def test_evolve_reuses_the_shared_m2_configuration_contract():
    adoption = SKILL_ROOT / "harness-evolve" / "ADOPTION.md"
    assert "](../../../kit/M2-CONFIG.md)" in adoption.read_text()
