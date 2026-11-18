"""Packaging/reachability only; no wording assertion stands for safe continuation."""
import re
import shutil
from conftest import ROOT


def test_shared_failure_branch_is_reachable_from_each_flow_after_relocation(tmp_path):
    plugin = tmp_path / 'relocated kit'
    for folder in ('skills', 'kit'):
        shutil.copytree(ROOT / folder, plugin / folder)
    for relative in ('skills/harness/harness-setup/RESUME.md',
                     'skills/harness/harness-evolve/UPDATE.md', 'kit/LIBRARY.md'):
        source = plugin / relative
        links = [(source.parent / target).resolve() for target in
                 re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', source.read_text()) if '://' not in target]
        assert plugin / 'kit/PERSISTENCE.md' in links
    source = plugin / 'kit/PERSISTENCE.md'
    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', source.read_text()):
        if '://' not in target:
            assert (source.parent / target).is_file(), target
