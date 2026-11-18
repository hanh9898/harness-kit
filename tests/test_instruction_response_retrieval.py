"""Public catalog and relocated-reference checks; not runtime acceptance."""
import re
import shutil

from conftest import KIT_CLI, ROOT, run


def test_instruction_design_is_retrievable_with_its_source_scope():
    result = run(KIT_CLI, "show", "N07")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "certainty: inferred" in result.stdout
    assert "instruction-response/DESIGN.md" in result.stdout
    assert "issues/15" in result.stdout


def test_instruction_references_survive_plugin_relocation(tmp_path):
    plugin = tmp_path / "relocated plugin"
    for folder in ("skills", "kit"):
        shutil.copytree(ROOT / folder, plugin / folder)
    reference = plugin / "kit/instruction-response"
    assert reference.is_dir()
    for source in reference.glob("*.md"):
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", source.read_text()):
            if "://" not in target:
                assert (source.parent / target).is_file(), (source.name, target)
