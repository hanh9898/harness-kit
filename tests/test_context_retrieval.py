"""Existing catalog seam: task-context access remains reachable after relocation.

These checks cover retrieval/packaging only. Real source use is observed through
Codex in test_context_host.py and the retained ticket-22 evidence.
"""
import re
import shutil

from conftest import ROOT, run


def test_source_map_resource_reaches_task_context_contract(tmp_path):
    plugin = tmp_path / "relocated plugin"
    for folder in ("skills", "kit"):
        shutil.copytree(ROOT / folder, plugin / folder)
    result = run(plugin / "kit/scripts/kit", "show", "B08")
    assert result.returncode == 0, result.stdout + result.stderr
    # The public retrieval response must carry a usable package-relative route,
    # not only a generic suggestion to keep a source map.
    paths = re.findall(r"(?:skills|kit)/[\w/.-]+\.md", result.stdout)
    assert paths, "Retrieved source-map material has no task-context access reference"
    for path in paths:
        assert (plugin / path).is_file(), path
    assert "https://code.claude.com/docs/en/cli-reference" in result.stdout
    assert "issues/15" in result.stdout
