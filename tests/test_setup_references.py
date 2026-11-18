"""Package-local runtime and historical reference links remain usable after migration."""
import re

from conftest import ROOT

SETUP = ROOT / "skills/harness/harness-setup"


def test_local_markdown_references_resolve():
    for path in SETUP.glob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#") or "<" in target:
                continue
            assert (path.parent / target.split("#")[0]).exists(), (path.name, target)
