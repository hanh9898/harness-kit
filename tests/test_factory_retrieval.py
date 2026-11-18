"""Catalog discovery and packaged links supplement actual host observations."""
import re
import shutil
from conftest import KIT_CLI, ROOT, run


def test_selected_factory_arrangement_is_retrievable():
    result = run(KIT_CLI, 'show', 'J13')
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'certainty: inferred' in result.stdout
    assert 'FACTORY.md' in result.stdout
    assert 'issues/30' in result.stdout


def test_factory_references_survive_relocation(tmp_path):
    plugin = tmp_path / 'relocated plugin'
    for folder in ('kit', 'skills'):
        shutil.copytree(ROOT / folder, plugin / folder)
    source = plugin / 'kit/FACTORY.md'
    assert source.is_file()
    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', source.read_text()):
        if '://' not in target:
            assert (source.parent / target).is_file(), target
