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
    skill(root, ".agents/skills", "src-b", "---\nname: b\ndescription: >-\n  one two\n  go\n---\n")
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


def test_json_top_limits_rows_per_directory_without_changing_totals_or_warnings(tmp_path):
    make(tmp_path)
    skill(tmp_path, ".claude/skills", "z", "---\nname: z\ndescription: biggest\n---\n")
    skill(tmp_path, ".agents/skills", "empty", "---\nname: empty\n---\n")
    args = ("--root", tmp_path, "--json", "--strict", "--max-total", "31")
    full = run(*args)
    limited = run(*args, "--top", "1")
    assert limited.returncode == full.returncode == 1
    full_report = json.loads(full.stdout)
    limited_report = json.loads(limited.stdout)
    assert {d["dir"]: [row["folder"] for row in d["rows"]] for d in limited_report["dirs"]} == {
        ".claude/skills": ["z"],
        ".agents/skills": ["a"],
    }
    for report in (full_report, limited_report):
        for directory in report["dirs"]:
            del directory["rows"]
    assert limited_report == full_report


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


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("|-\n  Intro.\n    detail\n  end\n", "Intro.\n  detail\nend"),
        ("|-2 # indent is relative to the key\n    detail\n  end\n", "  detail\nend"),
        ("|\n  one\n  two\n\n", "one\ntwo\n"),
        ("|2+\n  one  \n \n    \n\n", "one  \n\n  \n\n"),
        (
            ">-\n  First\n  sentence.\n\n    detail\n\n  Next\n\n  paragraph.\n",
            "First sentence.\n\n  detail\n\nNext\nparagraph.",
        ),
    ],
    ids=["literal-indent", "explicit-indent", "clip", "keep-whitespace", "folded-indent"],
)
def test_block_description_budget(tmp_path, description, expected):
    skill(tmp_path, "skills", "demo", f"---\nname: demo\ndescription: {description}---\n")
    args = ("--root", tmp_path, "--dir", "skills", "--json", "--strict", "--max-total")
    chars = len(expected)
    at_limit = run(*args, chars)
    report = json.loads(at_limit.stdout)
    assert at_limit.returncode == 0, report
    assert report["total_chars"] == report["dirs"][0]["rows"][0]["chars"] == chars
    assert report["warnings"] == []

    over_limit = run(*args, chars - 1)
    assert over_limit.returncode == 1, over_limit.stdout
    assert f"Total {chars} characters exceeds limit {chars - 1}." in json.loads(over_limit.stdout)["warnings"][0]


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
