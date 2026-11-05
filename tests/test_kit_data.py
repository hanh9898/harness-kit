"""Kit data validation through tools/check_kit.py on real data and invalid fixtures."""
from conftest import CHECK_KIT, KIT, COLUMNS, run, row, write_kit


def test_real_kit_is_valid():
    r = run(CHECK_KIT, "--dir", KIT)
    assert r.returncode == 0, r.stdout + r.stderr


def test_good_sample_passes(tmp_path):
    root = write_kit(tmp_path, [row("A01"), row("A02", rung="skill"), row("A03", rung="mcp")])
    assert run(CHECK_KIT, "--dir", root).returncode == 0


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


def test_missing_legos_file_reported(tmp_path):
    r = run(CHECK_KIT, "--dir", tmp_path)
    assert r.returncode != 0 and "legos.csv" in r.stdout + r.stderr
