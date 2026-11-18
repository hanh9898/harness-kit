"""Public retrieval regression; host evidence establishes useful authority behavior."""
from conftest import KIT_CLI, ROOT, run


def test_authority_route_is_independently_retrievable():
    result = run(KIT_CLI, 'show', 'D24')
    assert result.returncode == 0
    assert 'authority/DESIGN.md' in result.stdout
    assert 'certainty: inferred' in result.stdout
    assert (ROOT / 'kit/authority/DESIGN.md').is_file()


def test_legacy_retrieval_identifies_history_and_replacement_without_losing_rows():
    for args, retained in [(('list', 'delegation'), 'step7'),
                           (('show', 'axis1'), 'Reversibility'),
                           (('show', 'step3'), 'Consult'),
                           (('show', 'combine'), 'Turning delegation off')]:
        result = run(KIT_CLI, *args)
        assert result.returncode == 0
        assert retained in result.stdout
        assert 'historical' in result.stdout.lower()
        assert 'D24' in result.stdout


def test_authority_references_survive_plugin_relocation(tmp_path):
    import re
    import shutil
    plugin = tmp_path / 'relocated plugin'
    for folder in ('kit', 'skills'):
        shutil.copytree(ROOT / folder, plugin / folder)
    for source in (plugin / 'kit/authority').glob('*.md'):
        for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', source.read_text()):
            if '://' not in target:
                assert (source.parent / target).is_file(), (source.name, target)
