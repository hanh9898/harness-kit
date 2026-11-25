"""Kit data validation through tools/check_kit.py on real data and invalid fixtures."""
import csv

import pytest

from conftest import CHECK_KIT, KIT, COLUMNS, run, row, write_kit, write_piece_aliases


def test_real_kit_is_valid():
    r = run(CHECK_KIT, "--dir", KIT)
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize("alias_pairs, location, error", [
    ([("A01", "P2")], "piece-aliases.csv:2", "invalid or reserved piece slug"),
    ([("A01", "axis1")], "piece-aliases.csv:2", "invalid or reserved piece slug"),
    ([("A01", "a01")], "piece-aliases.csv:2", "invalid or reserved piece slug"),
    ([("A1", "valid-piece")], "piece-aliases.csv:2", "invalid or reserved legacy_id"),
    ([("P10", "valid-piece")], "piece-aliases.csv:2", "invalid or reserved legacy_id"),
    ([("P06", "valid-piece")], "piece-aliases.csv:2", "invalid or reserved legacy_id"),
    ([("A01", "valid-piece"), ("A01", "other-piece")], "piece-aliases.csv:3", "duplicate legacy_id"),
    ([("A01", "valid-piece"), ("A02", "valid-piece")], "piece-aliases.csv:3", "duplicate alias target"),
])
def test_piece_alias_validation(tmp_path, alias_pairs, location, error):
    root = write_kit(tmp_path, [row("valid-piece")])
    write_piece_aliases(root, *alias_pairs)
    result = run(CHECK_KIT, "--dir", root)
    assert result.returncode == 1 and f"{location}: {error}" in result.stdout


def test_good_sample_passes(tmp_path):
    root = write_kit(tmp_path, [row("A01"), row("A02", rung="skill"), row("A03", rung="mcp")])
    assert run(CHECK_KIT, "--dir", root).returncode == 0


def test_named_extra_column_passes(tmp_path):
    root = write_kit(tmp_path, [row("A01", notes="quoted, comma")], header=[*COLUMNS, "notes"])
    assert run(CHECK_KIT, "--dir", root).returncode == 0


def test_quoted_multiline_detail_passes(tmp_path):
    root = write_kit(tmp_path, [row("A01", detail='First line, with "quotes"\nSecond line'), row("A02")])
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize(("gap", "line"), [("", 5), ("\n", 6)], ids=["adjacent", "blank-line"])
def test_lego_diagnostics_use_physical_lines_after_multiline_cell(tmp_path, gap, line):
    root = write_kit(
        tmp_path, [row("A01", detail="First line\nSecond line"), row("A02")], groups={"A": "Intake"}
    )
    invalid = row("A02", group="B", summary="", rung="plugin")
    with (root / "legos.csv").open("a", encoding="utf-8", newline="") as f:
        f.write(gap)
        csv.writer(f).writerow([*(invalid[c] for c in COLUMNS), "extra"])

    r = run(CHECK_KIT, "--dir", root)

    assert r.returncode == 1
    assert not r.stderr, r.stderr
    prefix = f"ERROR: legos.csv:{line}: "
    assert r.stdout.splitlines() == [
        prefix + "A02 has extra cells beyond the header; fix: match the row to the header",
        prefix + "A02 has an empty `summary` cell; fix: supply a value",
        prefix + "A02 rung `plugin` is not in instruction-file | skill | script-cli | mcp; fix: choose one of these four values",
        prefix + "duplicate id A02 from line 4; fix: choose another ID",
        prefix + "group `B` has no name in groups.csv; fix: add `B,<group name>`",
        "5 data errors.",
    ]


@pytest.mark.parametrize(("filename", "data"), [
    ("legos.csv", ",".join(COLUMNS) + '\nA01,A,Alpha,s,w,skill,stated,src,"detail\nA02,A,Beta,s,w,skill,stated,src,detail\n'),
    ("groups.csv", 'id,name\nA,"Group A\nB,Group B\n'),
    ("rules.csv", 'id,topic,rule,source,certainty,check,verified_on\nR01,t,r,s,stated,c,"\nR02,t,r,s,stated,c,\n'),
    ("gates.csv", 'id,gate,verify_method,verified_quote,note\nR01,no,unreadable,,"note\nR02,no,unreadable,,note\n'),
], ids=["legos", "groups", "rules", "gates"])
def test_unclosed_csv_quote_rejected(tmp_path, filename, data):
    root = write_kit(tmp_path, [row("A01")])
    if filename == "gates.csv":
        (root / "rules.csv").write_text(
            "id,topic,rule,source,certainty,check,verified_on\nR01,t,r,s,stated,c,\nR02,t,r,s,stated,c,\n",
            encoding="utf-8",
        )
    (root / filename).write_text(data, encoding="utf-8")

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert f"ERROR: {filename}:3: malformed CSV" in r.stdout
    assert not r.stderr, r.stderr


def test_progress_log_reports_malformed_groups_csv(tmp_path):
    (tmp_path / "groups.csv").write_text('id,name\nA,"Group A\n', encoding="utf-8")
    log = tmp_path / "progress.log"
    log.touch()

    r = run(CHECK_KIT, "--dir", tmp_path, "--log", log)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "ERROR: groups.csv:2: malformed CSV" in r.stdout
    assert not r.stderr, r.stderr


def test_missing_column_reported(tmp_path):
    header = [c for c in COLUMNS if c != "certainty"]
    root = write_kit(tmp_path, [row("A01")], header=header)
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode != 0 and "certainty" in r.stdout + r.stderr


def test_bad_rung_reported_with_line_and_allowed_values(tmp_path):
    root = write_kit(tmp_path, [row("A01"), row("A02", rung="plugin")])
    r = run(CHECK_KIT, "--dir", root)
    out = r.stdout + r.stderr
    assert r.returncode != 0
    assert "A02" in out and "plugin" in out
    for ok in ("instruction-file", "skill", "script-cli", "mcp"):
        assert ok in out


def test_vietnamese_rung_label_rejected(tmp_path):
    root = write_kit(tmp_path, [row("A01", rung="invalid-rung")])
    assert run(CHECK_KIT, "--dir", root).returncode != 0


def test_duplicate_id_reported(tmp_path):
    root = write_kit(tmp_path, [row("A01"), row("A02"), row("A01", name="Other")])
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode != 0 and "A01" in r.stdout + r.stderr and "duplicate" in r.stdout + r.stderr


def test_empty_required_cell_reported(tmp_path):
    root = write_kit(tmp_path, [row("A01", summary="")])
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode != 0 and "summary" in r.stdout + r.stderr


def test_truncated_row_reports_all_missing_cells(tmp_path):
    root = write_kit(tmp_path, [row("A01")])
    with (root / "legos.csv").open("a", encoding="utf-8") as f:
        f.write("Z99\n")

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1
    assert not r.stderr, r.stderr
    expected = [
        f"ERROR: legos.csv:3: Z99 has an empty `{column}` cell; fix: supply a value"
        for column in COLUMNS[1:]
    ]
    assert r.stdout.splitlines() == [*expected, "8 data errors."]


@pytest.mark.parametrize("extra", ["stray value", ""], ids=["nonempty", "empty"])
def test_surplus_lego_cells_rejected(tmp_path, extra):
    root = write_kit(tmp_path, [row("A01")])
    overflow = row("A02")
    with (root / "legos.csv").open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([*(overflow[c] for c in COLUMNS), extra])

    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "legos.csv:3: A02 has extra cells beyond the header;" in r.stdout


def test_missing_legos_file_reported(tmp_path):
    r = run(CHECK_KIT, "--dir", tmp_path)
    assert r.returncode != 0 and "legos.csv" in r.stdout + r.stderr


def test_group_without_name_reported(tmp_path):
    root = write_kit(tmp_path, [row("A01"), row("B01", group="B")], groups={"A": "Intake"})
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1 and "`B`" in r.stdout and "groups.csv" in r.stdout and "`A`" not in r.stdout


def test_missing_groups_file_reported(tmp_path):
    root = write_kit(tmp_path, [row("A01")])
    (root / "groups.csv").unlink()
    r = run(CHECK_KIT, "--dir", root)
    assert r.returncode == 1 and "groups.csv" in r.stdout
