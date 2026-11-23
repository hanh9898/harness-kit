"""tools/skill_budget.py: description budget behavior through CLI subprocesses."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parent.parent / "tools" / "skill_budget.py"


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True)


def skill(root, rel, folder, body):
    d = root / rel / folder
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")


def make(root):
    skill(root, ".agents/skills", "a", '---\nname: a\ndescription: "An \\"egg\\" ok"\n---\nbody\n')
    skill(root, ".agents/skills", "src-b", "---\nname: b\ndescription: >\n  one two\n  go\n---\n")
    skill(root, ".claude/skills", "c", "---\nname: c\ndescription: 'it''s'\n---\n")
    return root


def test_totals_per_skill_and_mismatch(tmp_path):
    make(tmp_path)
    r = run("--root", tmp_path)
    assert r.returncode == 0
    assert "== .agents/skills: 2 skills, 21 characters" in r.stdout  # 11 + 10
    assert "name/folder mismatches: 1" in r.stdout
    assert "[name=b]" in r.stdout
    assert "TOTAL: 25 characters" in r.stdout
    assert "WARNING" in r.stdout and "Next step" in r.stdout


def test_json_output(tmp_path):
    make(tmp_path)
    d = json.loads(run("--root", tmp_path, "--json").stdout)
    assert d["total_chars"] == 25
    assert {x["dir"]: x["name_mismatch"] for x in d["dirs"]} == {".claude/skills": 0, ".agents/skills": 1}


def test_strict_exits_1_on_warning_default_0(tmp_path):
    make(tmp_path)
    assert run("--root", tmp_path).returncode == 0
    assert run("--root", tmp_path, "--strict").returncode == 1


def test_strict_clean_and_max_total(tmp_path):
    skill(tmp_path, ".agents/skills", "a", "---\nname: a\ndescription: xyz\n---\n")
    assert run("--root", tmp_path, "--dir", ".agents/skills", "--strict").returncode == 0
    r = run("--root", tmp_path, "--dir", ".agents/skills", "--max-total", "2", "--strict")
    assert r.returncode == 1 and "exceeds limit" in r.stdout


def test_comment_only_description_warns(tmp_path):
    skill(tmp_path, "skills", "example", "---\nname: example\ndescription: # TODO\n---\n")
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 1, r.stdout
    assert "TOTAL: 0 characters" in r.stdout
    assert "WARNING: skills/example: missing description" in r.stdout
    assert run("--root", tmp_path, "--dir", "skills").returncode == 0


@pytest.mark.parametrize("quote", ["'", '"'])
def test_quoted_comment_description_counts_as_text(tmp_path, quote):
    skill(tmp_path, "skills", "example", f"---\nname: example\ndescription: {quote}# TODO{quote}\n---\n")
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 0, r.stdout
    assert "TOTAL: 6 characters" in r.stdout


@pytest.mark.parametrize(
    ("quote", "description", "expected"),
    [
        ('"', r'Say \"hi\" #tag', 'Say "hi" #tag'),
        ("'", "It''s a #tag", "It's a #tag"),
    ],
    ids=["double-quoted", "single-quoted"],
)
def test_trailing_comments_after_quoted_fields(tmp_path, quote, description, expected):
    skill(
        tmp_path, "skills", "example",
        f"---\nname: {quote}example{quote} # display name\n"
        f"description: {quote}{description}{quote} # ignored {quote}notes{quote}\n---\n",
    )
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 0, r.stdout
    assert f"TOTAL: {len(expected)} characters" in r.stdout


@pytest.mark.parametrize(
    ("folder", "name", "description", "expected"),
    [
        ("demo", "demo # display name", "Useful. # public description", "Useful."),
        (
            "demo#v2",
            "demo#v2\t# display name",
            "C# and https://example.com/#docs\t# ignored",
            "C# and https://example.com/#docs",
        ),
        ("demo", "demo", "Useful\n  documentation. # ignored", "Useful documentation."),
    ],
    ids=["space-before-comment", "tab-with-literal-hashes", "multiline"],
)
def test_trailing_comments_after_plain_fields(tmp_path, folder, name, description, expected):
    skill(tmp_path, "skills", folder, f"---\nname: {name}\ndescription: {description}\n---\n")
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 0, r.stdout
    assert f"TOTAL: {len(expected)} characters" in r.stdout


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("  # introduction\n  Useful. # ignored", "Useful."),
        ('  "C# # docs" # ignored', "C# # docs"),
        ("  |-\n    C# # docs", "C# # docs"),
    ],
    ids=["plain-after-comment", "quoted", "block"],
)
def test_description_can_start_below_key(tmp_path, description, expected):
    skill(tmp_path, "skills", "demo", f"---\nname: demo\ndescription:\n{description}\n---\n")
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 0, r.stdout
    assert f"TOTAL: {len(expected)} characters" in r.stdout


def test_strict_discovers_flat_and_grouped_skills(tmp_path):
    skill(tmp_path, "skills", "a", "---\nname: a\ndescription: one\n---\n")
    skill(tmp_path, "skills/group", "b", "---\nname: b\ndescription: two\n---\n")
    skill(tmp_path, "skills/group/b/references", "example", "---\nname: example\ndescription: skip me\n---\n")
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 0, r.stdout
    assert "== skills: 2 skills, 6 characters" in r.stdout


def test_nested_skill_warning_reports_full_path(tmp_path):
    skill(tmp_path, "skills/group/team", "a", "---\nname: a\n---\n")
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 1
    assert "skills/group/team/a: missing description" in r.stdout


def test_flat_skill_without_skill_md_still_warns(tmp_path):
    (tmp_path / "skills" / "a" / "references").mkdir(parents=True)
    r = run("--root", tmp_path, "--dir", "skills", "--strict")
    assert r.returncode == 1
    assert "skills/a: cannot read SKILL.md (FileNotFoundError)" in r.stdout


def test_missing_description_and_bad_root(tmp_path):
    skill(tmp_path, ".agents/skills", "a", "---\nname: a\n---\n")
    r = run("--root", tmp_path, "--dir", ".agents/skills")
    assert r.returncode == 0 and "missing description" in r.stdout
    r = run("--root", tmp_path / "nope")
    assert r.returncode == 2 and "Next step" in r.stderr
