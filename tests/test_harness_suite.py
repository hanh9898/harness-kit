"""The installable suite and its scoped runbooks ship together."""
import json
import re
import shutil

import pytest

from conftest import ROOT, run

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
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
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
