"""The kit CLI: external subprocess behavior on small fixture kits."""
import os
import re
import subprocess

from conftest import KIT, KIT_CLI, run, row, write_kit


def kit(tmp_path, *args):
    root = write_kit(tmp_path / "k", [
        row("A01", "A", "Alpha hook"), row("A02", "A", "Alpha file"),
        row("B01", "B", "Beta script", rung="script-cli"),
    ])
    return run(KIT_CLI, "--dir", root, *args)


def test_list_without_group_shows_group_names_with_counts_not_pieces(tmp_path):
    r = kit(tmp_path, "list")
    assert r.returncode == 0
    lines = r.stdout.splitlines()
    assert lines[0].split("\t")[:2] == ["A", "Group A"] and "2" in lines[0]
    assert lines[1].split("\t")[:2] == ["B", "Group B"]
    assert "Alpha hook" not in r.stdout and "Detail A01" not in r.stdout


def test_real_kit_list_names_every_group():
    r = run(KIT_CLI, "list")
    first = r.stdout.splitlines()[0].split("\t")
    assert first[:2] == ["A", "Intake"]
    assert all(l.split("\t")[1] for l in r.stdout.splitlines() if "\t" in l)


def test_list_group_shows_only_that_group_one_line_each(tmp_path):
    r = kit(tmp_path, "list", "A")
    assert r.returncode == 0
    assert "A01" in r.stdout and "Alpha hook" in r.stdout and "A02" in r.stdout
    assert "B01" not in r.stdout
    assert "Detail A01" not in r.stdout  # Listing omits details.


def test_list_unknown_group_errors_with_next_step(tmp_path):
    r = kit(tmp_path, "list", "Z")
    assert r.returncode != 0
    assert "kit list" in r.stderr


def test_show_by_id(tmp_path):
    r = kit(tmp_path, "show", "B01")
    assert r.returncode == 0
    assert "Beta script" in r.stdout and "Detail B01" in r.stdout and "script-cli" in r.stdout
    assert "A01" not in r.stdout


def test_show_by_name_case_insensitive(tmp_path):
    r = kit(tmp_path, "show", "alpha FILE")
    assert r.returncode == 0 and "Detail A02" in r.stdout


def test_show_unknown_id_fails_and_names_next_step(tmp_path):
    r = kit(tmp_path, "show", "Q99")
    assert r.returncode != 0
    assert "Q99" in r.stderr and "kit list" in r.stderr
    assert r.stdout == ""


def test_no_path_dumps_whole_store(tmp_path):
    for args in (["show"], ["show", "--all"], ["list", "--all"], ["dump"], []):
        r = kit(tmp_path, *args)
        assert r.returncode != 0, args
        assert "Detail A01" not in r.stdout and "Detail B01" not in r.stdout, args


def test_show_refuses_pattern_matching_many(tmp_path):
    for q in ("*", "", "A", "Alpha"):
        r = kit(tmp_path, "show", q)
        assert r.returncode != 0, q
        assert "Detail" not in r.stdout, q


def test_real_kit_runs_from_default_dir():
    r = run(KIT_CLI, "list")
    assert r.returncode == 0 and r.stdout.strip()


def test_patterns_list_and_show_one_row_only():
    r = run(KIT_CLI, "list", "P")
    assert r.returncode == 0 and "P6" in r.stdout and "Orchestrator" in r.stdout
    assert "Avoid when" not in r.stdout
    r = run(KIT_CLI, "show", "P6")
    assert r.returncode == 0 and "Orchestrator with workers" in r.stdout and "Avoid when" in r.stdout
    assert "Peer handoff" not in r.stdout


def test_patterns_list_and_show_unpadded_table(tmp_path):
    root = write_kit(tmp_path / "k", [row("A01")])
    (root / "patterns.md").write_text(
        "|#|Pattern|Also called|What it is|\n"
        "|---|---|---|---|\n"
        "|1|Single agent||One agent does the work.|\n"
        r"|2|Router|Dispatcher|Picks A \| B|" "\n",
        encoding="utf-8",
    )

    r = run(KIT_CLI, "--dir", root, "list", "P")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == [
        "P1\tSingle agent\tOne agent does the work.",
        "P2\tRouter\t" r"Picks A \| B",
    ]

    r = run(KIT_CLI, "--dir", root, "show", "P2")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == [
        "#: 2", "Pattern: Router", "Also called: Dispatcher", r"What it is: Picks A \| B",
    ]


def test_patterns_list_missing_file(tmp_path):
    r = kit(tmp_path, "list", "P")
    assert r.returncode == 2
    assert r.stdout == ""
    assert r.stderr == "ERROR: patterns.md is missing from the kit directory.\n"


def test_pattern_unknown_fails_with_next_step():
    r = run(KIT_CLI, "show", "P99")
    assert r.returncode != 0 and "kit list P" in r.stderr and r.stdout == ""


def test_delegation_list_and_show_one_row_only():
    r = run(KIT_CLI, "list", "delegation")
    assert r.returncode == 0 and "axis4" in r.stdout and "step7" in r.stdout
    assert "What the sources say" not in r.stdout
    r = run(KIT_CLI, "show", "axis1")
    assert r.returncode == 0 and "Reversibility" in r.stdout and "Information level" not in r.stdout
    r = run(KIT_CLI, "show", "step3")
    assert r.returncode == 0 and "Consult" in r.stdout and "Typical use" in r.stdout and "Delegate" not in r.stdout
    r = run(KIT_CLI, "show", "combine")
    assert r.returncode == 0 and "Turning delegation off" in r.stdout and "Reversibility" not in r.stdout


def test_delegation_unknown_fails_with_next_step():
    r = run(KIT_CLI, "show", "step9")
    assert r.returncode != 0 and "kit list delegation" in r.stderr and r.stdout == ""


def test_rules_list_gate_rules_first_and_show_one_rule(tmp_path):
    root = write_kit(tmp_path / "k", [row("A01")])
    (root / "rules.csv").write_text(
        "id,topic,rule,source,certainty,check,verified_on\n"
        "1.01,t1,Rule gate one,s,stated,machine,2026-01-01\n"
        "1.02,t1,Rule plain two,s,stated,review,\n", encoding="utf-8")
    (root / "gates.csv").write_text(
        "id,gate,verify_method,verified_quote,note\n1.01,yes,raw-grep,Quoted one,n\n", encoding="utf-8")
    r = run(KIT_CLI, "--dir", root, "list", "rules")
    assert r.returncode == 0 and "1.01" in r.stdout and "1.02" not in r.stdout
    r = run(KIT_CLI, "--dir", root, "list", "rules", "t1")
    assert "1.01*" in r.stdout and "1.02" in r.stdout and "1.02*" not in r.stdout
    r = run(KIT_CLI, "--dir", root, "show", "1.01")
    assert r.returncode == 0 and "Quoted one" in r.stdout and "Rule plain two" not in r.stdout
    r = run(KIT_CLI, "--dir", root, "show", "9.99")
    assert r.returncode != 0 and "kit list rules" in r.stderr


def test_unknown_rule_topic_hint_lists_the_selected_catalog(tmp_path, monkeypatch):
    root = write_kit(tmp_path / "alternate's catalog", [row("A01")])
    (root / "rules.csv").write_text(
        "id,topic,rule,source,certainty,check,verified_on\n"
        "1.01,alternate-only,Alternate rule,s,stated,review,\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    r = run(KIT_CLI, "--dir", root.name, "list", "rules", "missing-topic")
    assert r.returncode == 2 and "Topic `missing-topic` does not exist." in r.stderr
    hint = re.search(r"Next step: run `(.+)` to see topics\.", r.stderr)
    assert hint, r.stderr

    monkeypatch.setenv("PATH", str(KIT_CLI.parent), prepend=os.pathsep)
    topics = subprocess.run(hint[1], shell=True, capture_output=True, text=True, cwd=KIT)
    assert topics.returncode == 0, topics.stderr
    assert topics.stdout == "alternate-only\t1 rules\n"


def test_unknown_rule_topic_hint_without_override_is_unchanged():
    r = run(KIT_CLI, "list", "rules", "missing-topic")
    assert r.returncode == 2
    assert r.stderr == (
        "ERROR: Topic `missing-topic` does not exist.\n"
        "Next step: run `kit list rules all` to see topics.\n"
    )
