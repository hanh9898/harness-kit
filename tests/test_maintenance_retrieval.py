"""Public retrieval/package checks; actual host effects have separate evidence."""
import re
import shutil

from conftest import ROOT, run


def test_current_history_and_retention_routes_survive_relocation(tmp_path):
    plugin = tmp_path / 'relocated plugin'
    for folder in ('skills', 'kit'):
        shutil.copytree(ROOT / folder, plugin / folder)
    for identity in ('current-state-file', 'decision-log-and-state-machine', 'retention-and-cleanup'):
        result = run(plugin / 'kit/scripts/kit', 'show', identity)
        assert result.returncode == 0
        assert 'kit/MAINTENANCE.md' in result.stdout
    source = plugin / 'kit/MAINTENANCE.md'
    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', source.read_text()):
        if '://' not in target:
            assert (source.parent / target).is_file(), target
