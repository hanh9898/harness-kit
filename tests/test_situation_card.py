"""Situation-card schema and value-selected branches for four repository fixtures."""
import re

import pytest

from conftest import CHECK_KIT, ROOT, run

FIX = ROOT / "tests" / "fixtures" / "situation"
SETUP = ROOT / "skills" / "harness" / "harness-setup"
KINDS = ["code-repo", "control-repo", "new-repo", "existing-harness"]

EXPECTED = {
    "code-repo": dict(s02_work="git", s02_chain="who", s03_labels="ask", s11="new"),
    "control-repo": dict(s02_work="tracker", s02_chain="pain", s03_labels="ask", s11="new"),
    "new-repo": dict(s02_work="planned", s02_chain="who", s03_labels="skip", s11="new"),
    "existing-harness": dict(s02_work="git", s02_chain="who", s03_labels="ask", s11="handoff"),
}


def branches(stdout):
    return dict(l.split(" ", 1)[1].split("=") for l in stdout.splitlines() if l.startswith("branch "))


@pytest.mark.parametrize("kind", KINDS)
def test_each_sample_card_is_valid_and_picks_its_branches(kind):
    r = run(CHECK_KIT, "--situation", FIX / f"{kind}.md")
    assert r.returncode == 0, r.stdout
    assert branches(r.stdout) == EXPECTED[kind]


def test_the_four_kinds_differ_only_by_card_values():
    seen = {tuple(sorted(v.items())) for v in EXPECTED.values()}
    assert len(seen) == 4


def edited(tmp_path, kind, old, new):
    text = (FIX / f"{kind}.md").read_text(encoding="utf-8")
    assert old in text
    f = tmp_path / "situation.md"
    f.write_text(text.replace(old, new), encoding="utf-8")
    return f


BAD = [
    ("history: yes\n", "", "history"),                                  # Missing field.
    ("history: yes", "history: sometimes", "history"),                  # Invalid enum value.
    ("matt_config: present", "matt_config: maybe", "matt_config"),
    ("work_source: git", "work_source: github", "work_source"),
    ("work_source: git", "work_source: tracker:", "work_source"),
    ("flow_source: sample", "flow_source: guessed", "flow_source"),
    ("tree_relation: shared", "tree_relation: same", "tree_relation"),
    ("confirmed: yes", "confirmed: maybe", "confirmed"),
    ("code_home: .", "code_home: ", "code_home"),
    ("platform: claude-code", "platform: the app the team uses", "platform"),
    ("history: yes", "history: yes\nhistory: none", "history"),         # Duplicate key.
    ("history: yes", "history: yes\nowner: me", "owner"),               # Unknown key.
    ("history: yes", "history: yes\nThe repo was started last year.", "line"),  # Prose.
]


@pytest.mark.parametrize("old,new,needle", BAD)
def test_bad_card_exits_1_and_names_the_problem(tmp_path, old, new, needle):
    r = run(CHECK_KIT, "--situation", edited(tmp_path, "code-repo", old, new))
    assert r.returncode == 1, r.stdout
    assert needle in r.stdout and "branch" not in r.stdout


def test_missing_file_exits_1(tmp_path):
    assert run(CHECK_KIT, "--situation", tmp_path / "nope.md").returncode == 1


def test_every_branch_value_is_explained_in_boundary_md():
    text = (SETUP / "BOUNDARY.md").read_text(encoding="utf-8")
    for name in {k for v in EXPECTED.values() for k in v}:
        assert f"`{name}`" in text, name
    for value in {x for v in EXPECTED.values() for x in v.values()}:
        assert f"`{value}`" in text, value
