"""The unreleased kit supports one current format, without obsolete sections or compatibility scaffolding."""
import re

import pytest

from conftest import ROOT

SETUP = ROOT / "skills" / "harness" / "harness-setup"
FILES = list((ROOT / "skills").rglob("*.md")) + list((ROOT / "skills").rglob("*.py")) + list((ROOT / "tools").glob("*.py")) \
    + list((ROOT / "kit").glob("*.csv")) + list((ROOT / "skills").rglob("*.txt"))
COMPAT = re.compile(r"legacy|predate|old format|old entry|older entr|written before|before the gate existed|gate: not run|is readable"
                    r"|MOVE-PLAN|Repo with no history", re.I)


@pytest.mark.parametrize("path", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_no_backward_compat_or_removed_branch_text(path):
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        assert not COMPAT.search(line), f"{path.relative_to(ROOT)}:{n}: {line[:80]}"


def test_setup_skill_md_is_short_with_no_long_line():
    lines = (SETUP / "SKILL.md").read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 100
    assert max(len(l) for l in lines) <= 690


def test_setup_total_lines_did_not_grow():
    total = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in SETUP.glob("*.md") if p.name != "CHECKLIST.md")
    assert total <= 1044, total
