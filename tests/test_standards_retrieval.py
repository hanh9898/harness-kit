"""Public retrieval regression; behavioral qualification remains at the host seam."""
from conftest import KIT_CLI, run


def test_document_standards_are_retrievable_with_applicability_and_source():
    result = run(KIT_CLI, "show", "standards-selection-and-document-checks")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "certainty: inferred" in result.stdout
    assert "standards/SELECT.md" in result.stdout
    assert "issues/15" in result.stdout


def test_standards_references_survive_plugin_relocation(tmp_path):
    import re
    import shutil
    from conftest import ROOT

    plugin = tmp_path / "relocated plugin"
    for folder in ("skills", "kit"):
        shutil.copytree(ROOT / folder, plugin / folder)
    for source in (plugin / "kit/standards").glob("*.md"):
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", source.read_text()):
            if "://" not in target:
                assert (source.parent / target).is_file(), (source.name, target)
