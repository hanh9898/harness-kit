"""Public retrieval seam; this does not qualify experimental outcomes."""
import re
import shutil

from conftest import ROOT, run


def test_measured_improvement_exposes_bounded_learning_after_relocation(tmp_path):
    plugin = tmp_path / "relocated plugin"
    for folder in ("skills", "kit"):
        shutil.copytree(ROOT / folder, plugin / folder)
    result = run(plugin / "kit/scripts/kit", "show", "measured-improvement")
    assert result.returncode == 0, result.stdout + result.stderr
    paths = re.findall(r"(?:skills|kit)/[\w/.-]+\.md", result.stdout)
    assert paths, "Measured-improvement retrieval has no bounded-learning route"
    for path in paths:
        assert (plugin / path).is_file(), path
    assert "note:R23" in result.stdout
