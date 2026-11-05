"""Project-name boundaries: check real kit data and invalid fixtures using configurable tokens."""
from conftest import CHECK_BOUNDARY, KIT, TOKENS, run, row, write_kit


def test_real_kit_has_no_forbidden_tokens():
    r = run(CHECK_BOUNDARY, "--root", KIT, "--tokens", TOKENS, "--strict")
    assert r.returncode == 0, r.stdout


def test_tokens_file_is_outside_the_kit():
    assert KIT not in TOKENS.parents and TOKENS.is_file()


def test_sample_with_leak_is_reported_at_right_file_and_line(tmp_path):
    kitdir = write_kit(tmp_path / "kit", [row("A01"), row("A02", detail="used in HBU1976 once")])
    r = run(CHECK_BOUNDARY, "--root", kitdir, "--tokens", TOKENS, "--strict")
    assert r.returncode == 1
    assert "legos.csv:3" in r.stdout and "fix:" in r.stdout


def test_tokens_come_from_file(tmp_path):
    kitdir = write_kit(tmp_path / "kit", [row("A01", detail="mentions Zorblax")])
    toks = tmp_path / "t.txt"
    toks.write_text("Zorblax  # sample name\n", encoding="utf-8")
    assert run(CHECK_BOUNDARY, "--root", kitdir, "--tokens", toks, "--strict").returncode == 1
    toks.write_text("Other\n", encoding="utf-8")
    assert run(CHECK_BOUNDARY, "--root", kitdir, "--tokens", toks, "--strict").returncode == 0


def test_missing_tokens_file_exit_2(tmp_path):
    kitdir = write_kit(tmp_path / "kit", [row("A01")])
    assert run(CHECK_BOUNDARY, "--root", kitdir, "--tokens", tmp_path / "none.txt").returncode == 2
