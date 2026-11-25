"""Public discovery and relocated references; not host qualification."""
import re
import shutil
from conftest import ROOT, KIT_CLI, run


def test_authority_retrieval_reaches_governed_replacement_after_relocation(tmp_path):
    result = run(KIT_CLI, 'show', 'authority-design-and-calibration')
    assert result.returncode == 0 and 'authority/DESIGN.md' in result.stdout
    plugin = tmp_path / 'relocated package'
    for folder in ('kit', 'skills'):
        shutil.copytree(ROOT / folder, plugin / folder)
    destination = plugin / 'kit/authority/REPLACE.md'
    for relative in ('kit/authority/DESIGN.md',
                     'skills/harness/harness-evolve/ADOPTION.md'):
        source = plugin / relative
        links = [(source.parent / target).resolve() for target in
                 re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', source.read_text()) if '://' not in target]
        assert destination in links
    assert destination.is_file()
    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', destination.read_text()):
        if '://' not in target:
            assert (destination.parent / target).is_file(), target
