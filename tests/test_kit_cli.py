"""The kit CLI: external subprocess behavior on small fixture kits."""
from conftest import KIT, KIT_CLI, run, row, write_kit


def kit(tmp_path, *args):
    root = write_kit(tmp_path / "k", [
        row("A01", "A", "Alpha hook"), row("A02", "A", "Alpha file"),
        row("B01", "B", "Beta script", rung="script-cli"),
    ])
    return run(KIT_CLI, "--dir", root, *args)


def test_list_without_group_shows_groups_with_counts_not_pieces(tmp_path):
    r = kit(tmp_path, "list")
    assert r.returncode == 0
    assert "A" in r.stdout and "2" in r.stdout and "B" in r.stdout
    assert "Alpha hook" not in r.stdout and "Detail A01" not in r.stdout


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


def test_pattern_unknown_fails_with_next_step():
    r = run(KIT_CLI, "show", "P99")
    assert r.returncode != 0 and "kit list P" in r.stderr and r.stdout == ""
