"""First-run follow-up: inspected kit groups, quoted log values, and hosted platform names."""
from conftest import CHECK_KIT, ROOT, run

FIX = ROOT / "tests" / "fixtures" / "situation"
TS = "2026-01-01T00:0{}:00Z"


def log(tmp_path, *lines):
    f = tmp_path / "progress.log"
    f.write_text("".join(f"{TS.format(i)} {l}\n" for i, l in enumerate(lines)), encoding="utf-8")
    return run(CHECK_KIT, "--log", f)


def test_need_to_piece_with_groups_looked_at_passes(tmp_path):
    r = log(tmp_path, 'step=observe platform=x flow="ticket, then code, then review" labels=none',
            "step=need-to-piece need=pull-tickets piece=J03 groups=A,E,J")
    assert r.returncode == 0, r.stdout


def test_need_to_piece_without_groups_fails_and_says_how(tmp_path):
    for line in ("step=need-to-piece need=x piece=A01", "step=need-to-piece need=x piece=A01 groups="):
        r = log(tmp_path, line)
        assert r.returncode == 1 and "groups=" in r.stdout and "kit" in r.stdout, line


def test_need_to_piece_with_a_group_the_kit_lacks_fails(tmp_path):
    r = log(tmp_path, "step=need-to-piece need=x piece=A01 groups=A,Z")
    assert r.returncode == 1 and "Z" in r.stdout


def test_unclosed_quote_fails(tmp_path):
    r = log(tmp_path, 'step=observe platform=x flow="ticket then code labels=none')
    assert r.returncode == 1 and "double quotes" in r.stdout


def test_quoted_value_is_one_field():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import check_kit
    eff = check_kit.effective_lines(f'{TS.format(0)} step=observe platform=x flow="a then b" labels=none\n')
    assert eff[("observe", "")]["flow"] == "a then b" and eff[("observe", "")]["labels"] == "none"


def card(tmp_path, platform):
    f = tmp_path / "situation.md"
    f.write_text((FIX / "code-repo.md").read_text(encoding="utf-8").replace("platform: claude-code", f"platform: {platform}"),
                 encoding="utf-8")
    return run(CHECK_KIT, "--situation", f)


def test_platform_may_name_the_host_it_runs_through(tmp_path):
    for ok in ("claude-code", "claude-code@runner", "codex@ci.example"):
        assert card(tmp_path, ok).returncode == 0, ok
    for bad in ("claude-code@", "@runner", "claude-code@a@b", "claude code"):
        r = card(tmp_path, bad)
        assert r.returncode == 1 and "platform" in r.stdout, bad
