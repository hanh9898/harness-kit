"""Project-name boundaries: check real kit data and invalid fixtures using configurable tokens."""
from conftest import CHECK_BOUNDARY, KIT, TOKENS, run, row, write_kit


def test_real_kit_has_no_forbidden_tokens():
    r = run(CHECK_BOUNDARY, "--root", KIT, "--tokens", TOKENS, "--strict")
    assert r.returncode == 0, r.stdout


def test_tokens_file_is_outside_the_kit():
    assert KIT not in TOKENS.parents and TOKENS.is_file()


def test_missing_root_exit_2(tmp_path):
    root = tmp_path / "missing"
    r = run(CHECK_BOUNDARY, "--root", root, "--strict")
    assert r.returncode == 2, r.stdout
    assert f"--root is not a directory: {root}" in r.stderr
    assert not r.stdout


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


def test_selected_token_file_is_skipped_by_path(tmp_path):
    config = tmp_path / "config"
    config.mkdir()
    toks = config / "forbidden.txt"
    toks.write_text("InternalWidget\n", encoding="utf-8")

    r = run(CHECK_BOUNDARY, "--root", tmp_path, "--tokens", toks, "--strict")
    assert r.returncode == 0, r.stdout
    assert r.stdout == "Boundary clean.\n"

    (tmp_path / toks.name).write_text("InternalWidget\n", encoding="utf-8")
    r = run(CHECK_BOUNDARY, "--root", tmp_path, "--tokens", toks, "--strict")
    assert r.returncode == 1, r.stdout
    assert "WARNING: forbidden.txt:1: forbidden token `InternalWidget`" in r.stdout
    assert "1 boundary violations." in r.stdout


def test_default_token_filename_is_still_skipped(tmp_path):
    (tmp_path / TOKENS.name).write_text("HBU1976\n", encoding="utf-8")
    (tmp_path / "example.md").write_text("HBU1976\n", encoding="utf-8")

    r = run(CHECK_BOUNDARY, "--root", tmp_path, "--strict")
    assert r.returncode == 1, r.stdout
    assert "WARNING: example.md:1: forbidden token" in r.stdout
    assert "1 boundary violations." in r.stdout


def test_missing_tokens_file_exit_2(tmp_path):
    kitdir = write_kit(tmp_path / "kit", [row("A01")])
    assert run(CHECK_BOUNDARY, "--root", kitdir, "--tokens", tmp_path / "none.txt").returncode == 2


def _tree(root, files, tokens="Foo  # proper name\nre:\\bL\\d{3}\\b  # ledger ID\n"):
    toks = root / "toks.txt"
    toks.write_text(tokens, encoding="utf-8")
    scan = root / "scan"
    for rel, body in files.items():
        p = scan / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return scan, toks


def test_regex_token(tmp_path):
    scan, toks = _tree(tmp_path, {"a.md": "code L123 and LL1234\n"})
    r = run(CHECK_BOUNDARY, "--root", scan, "--tokens", toks, "--strict")
    assert r.returncode == 1 and "a.md:1" in r.stdout


def test_every_hit_is_listed(tmp_path):
    scan, toks = _tree(tmp_path, {"a.md": "Foo\n", "b.md": "x\nFoo\n"})
    r = run(CHECK_BOUNDARY, "--root", scan, "--tokens", toks)
    assert "a.md:1" in r.stdout and "b.md:2" in r.stdout


def test_tests_dir_is_skipped_and_clean_dir_passes_strict(tmp_path):
    scan, toks = _tree(tmp_path, {"tests/t.py": "Foo L123\n", "ok.md": "clean\n"})
    r = run(CHECK_BOUNDARY, "--root", scan, "--tokens", toks, "--strict")
    assert r.returncode == 0, r.stdout
