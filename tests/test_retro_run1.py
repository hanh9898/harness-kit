"""First real-user retrospective: machine-checked revised= log entries and key skill guidance."""
import sys

from conftest import CHECK_KIT, ROOT, run

sys.path.insert(0, str(ROOT / "tools"))
import check_kit  # noqa: E402

SETUP = ROOT / "skills" / "harness" / "harness-setup"


def read(name):
    return (SETUP / name).read_text(encoding="utf-8")


GOOD_LOG = """\
2026-01-01T00:00:00Z step=observe platform=x work=w flow=a labels=none
2026-01-01T00:05:00Z step=proposal part=folders outcome=layout-a
2026-01-01T00:09:00Z step=proposal part=tools outcome=t
2026-01-01T00:20:00Z step=proposal part=folders outcome=layout-b revised=2026-01-01T00:05:00Z
"""


def test_valid_log_with_revision_passes():
    assert check_kit.check_progress_log(GOOD_LOG) == []


def test_revised_pointing_nowhere_is_caught():
    bad = GOOD_LOG.replace("revised=2026-01-01T00:05:00Z", "revised=2026-01-01T00:06:00Z")
    errs = check_kit.check_progress_log(bad)
    assert len(errs) == 1 and "revised" in errs[0]


def test_revised_pointing_forward_or_to_other_step_is_caught():
    forward = "2026-01-01T00:00:00Z step=observe work=w labels=none revised=2026-01-01T00:05:00Z\n2026-01-01T00:05:00Z step=gate items=a\n"
    assert any("progress.log:1:" in e and "earlier timestamp" in e for e in check_kit.check_progress_log(forward))
    other = "2026-01-01T00:00:00Z step=observe labels=none\n2026-01-01T00:05:00Z step=gate revised=2026-01-01T00:00:00Z\n"
    errs = check_kit.check_progress_log(other)
    assert any("progress.log:2:" in e and "points to step=observe" in e for e in errs)
    assert any("progress.log:1: observe missing work=" in e for e in errs)


def test_last_line_per_step_and_part_wins():
    eff = check_kit.effective_lines(GOOD_LOG)
    assert eff[("proposal", "folders")]["outcome"] == "layout-b"
    assert eff[("proposal", "tools")]["outcome"] == "t"
    assert eff[("observe", "")]["platform"] == "x"
    assert len(eff) == 3


def test_cli_checks_a_log_file(tmp_path):
    f = tmp_path / "progress.log"
    f.write_text(GOOD_LOG, encoding="utf-8")
    assert run(CHECK_KIT, "--log", f).returncode == 0
    f.write_text(GOOD_LOG.replace("revised=2026-01-01T00:05:00Z", "revised=nope"), encoding="utf-8")
    assert run(CHECK_KIT, "--log", f).returncode == 1


def test_cli_rejects_self_revision(tmp_path):
    f = tmp_path / "progress.log"
    f.write_text(
        "2026-01-01T00:00:00Z step=observe work=w labels=none revised=2026-01-01T00:00:00Z\n",
        encoding="utf-8",
    )
    result = run(CHECK_KIT, "--log", f)
    assert result.returncode == 1, result.stdout
    assert "progress.log:1: revised=2026-01-01T00:00:00Z does not reference an earlier timestamp" in result.stdout


def test_record_format_states_revision_convention():
    t = read("RECORD-FORMAT.md")
    assert "revised=" in t and "last line" in t.lower()
    assert "never edited" in t and "check_kit.py --log" in t


def test_point1_existing_harness_is_handed_over_not_moved():
    p, r, e = read("PROPOSALS.md"), read("RECORD-FORMAT.md"), (SETUP.parent / "harness-evolve" / "SKILL.md").read_text(encoding="utf-8")
    assert "kind: folder" in p and "adopted" in p and "needs-change" in p and "harness-evolve" in p
    assert "adopted" in r and "needs-change" in r
    assert "needs-change" in e




def test_point5_overrun_rule():
    a = read("ASKING.md")
    assert "longer than expected" in a and "questions left" in a


OLD_FORMAT_LOG = """\
2026-01-01T00:00:00Z step=observe platform=x flow=a labels=everything
2026-01-01T00:01:00Z step=need-to-piece need=n piece=B08
"""


def test_line_in_old_format_fails_until_revised():
    errs = check_kit.check_progress_log(OLD_FORMAT_LOG)
    assert any("missing work=" in e for e in errs)
    assert any("missing groups=" in e for e in errs)


def test_revised_line_supersedes_old_format_line():
    log = OLD_FORMAT_LOG + (
        "2026-01-01T01:00:00Z step=observe platform=x work=w flow=a labels=none revised=2026-01-01T00:00:00Z\n"
        "2026-01-01T01:01:00Z step=need-to-piece need=n piece=B08 groups=A,J revised=2026-01-01T00:01:00Z\n"
    )
    assert check_kit.check_progress_log(log) == []


def test_valid_revision_chain_supersedes_old_fields():
    log = (
        "2026-01-01T00:00:00Z step=observe labels=everything\n"
        "2026-01-01T00:01:00Z step=observe labels=none revised=2026-01-01T00:00:00Z\n"
        "2026-01-01T00:02:00Z step=observe work=w labels=none revised=2026-01-01T00:01:00Z\n"
    )
    assert check_kit.check_progress_log(log) == []


def test_superseded_line_still_needs_a_valid_revision_link():
    log = (
        "2026-01-01T00:00:00Z step=observe labels=everything revised=2026-01-01T00:00:00Z\n"
        "2026-01-01T00:01:00Z step=observe work=w labels=none revised=2026-01-01T00:00:00Z\n"
    )
    errs = check_kit.check_progress_log(log)
    assert len(errs) == 1
    assert "progress.log:1: revised=2026-01-01T00:00:00Z does not reference an earlier timestamp" in errs[0]


def test_revision_only_supersedes_the_target_row():
    log = (
        "2026-01-01T00:00:00Z step=observe labels=everything\n"
        "2026-01-01T00:00:00Z step=observe labels=none revised=2026-01-01T00:00:00Z\n"
    )
    errs = check_kit.check_progress_log(log)
    assert len(errs) == 1
    assert "progress.log:2: observe missing work=" in errs[0]


def test_revisions_distinguish_needs_logged_in_the_same_second():
    log = (
        "2026-01-01T00:00:00Z step=need-to-piece need=a piece=B08\n"
        "2026-01-01T00:00:00Z step=need-to-piece need=b piece=J03\n"
        "2026-01-01T00:01:00Z step=need-to-piece need=b piece=J03 groups=J revised=2026-01-01T00:00:00Z\n"
    )
    errs = check_kit.check_progress_log(log)
    assert len(errs) == 1
    assert "progress.log:1: need-to-piece missing groups=" in errs[0]

    log += "2026-01-01T00:02:00Z step=need-to-piece need=a piece=B08 groups=B revised=2026-01-01T00:00:00Z\n"
    assert check_kit.check_progress_log(log) == []


def test_same_second_revision_cannot_target_a_different_need():
    log = (
        "2026-01-01T00:00:00Z step=need-to-piece need=a piece=B08 groups=B\n"
        "2026-01-01T00:00:00Z step=need-to-piece need=b piece=J03 groups=J revised=2026-01-01T00:00:00Z\n"
    )
    errs = check_kit.check_progress_log(log)
    assert len(errs) == 1
    assert "progress.log:2:" in errs[0] and "does not identify an earlier row for this decision" in errs[0]


def test_shared_timestamp_cannot_hide_an_unrelated_need():
    log = (
        "2026-01-01T00:00:00Z step=gate items=a\n"
        "2026-01-01T00:00:00Z step=need-to-piece need=a piece=B08\n"
        "2026-01-01T00:01:00Z step=need-to-piece need=b piece=J03 groups=J revised=2026-01-01T00:00:00Z\n"
    )
    errs = check_kit.check_progress_log(log)
    assert any("progress.log:2: need-to-piece missing groups=" in e for e in errs)
    assert any("progress.log:3:" in e and "does not identify an earlier row for this decision" in e for e in errs)


def test_revision_supersedes_repeated_rows_for_the_same_need():
    log = (
        "2026-01-01T00:00:00Z step=need-to-piece need=a piece=B08\n"
        "2026-01-01T00:00:00Z step=need-to-piece need=a piece=B08\n"
        "2026-01-01T00:01:00Z step=need-to-piece need=a piece=B08 groups=B revised=2026-01-01T00:00:00Z\n"
    )
    assert check_kit.check_progress_log(log) == []


def test_revised_line_is_itself_checked():
    log = OLD_FORMAT_LOG + "2026-01-01T01:00:00Z step=observe platform=x flow=a labels=none revised=2026-01-01T00:00:00Z\n"
    errs = check_kit.check_progress_log(log)
    assert any("progress.log:3: observe missing work=" in e for e in errs)
