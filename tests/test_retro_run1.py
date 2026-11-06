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
    assert check_kit.check_progress_log(forward)
    other = "2026-01-01T00:00:00Z step=observe work=w labels=none\n2026-01-01T00:05:00Z step=gate revised=2026-01-01T00:00:00Z\n"
    assert check_kit.check_progress_log(other)


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


def test_record_format_states_revision_convention():
    t = read("RECORD-FORMAT.md")
    assert "revised=" in t and "last line" in t.lower()
    assert "never edited" in t and "check_kit.py --log" in t


def test_point1_existing_harness_is_handed_over_not_moved():
    p, r, e = read("PROPOSALS.md"), read("RECORD-FORMAT.md"), (SETUP.parent / "harness-evolve" / "SKILL.md").read_text(encoding="utf-8")
    assert "kind: folder" in p and "adopted" in p and "needs-change" in p and "harness-evolve" in p
    assert "adopted" in r and "needs-change" in r
    assert "needs-change" in e


def test_point3_step0_agent_skills_block():
    s = read("SKILL.md")
    assert "Issue tracker" in s and "Triage labels" in s and "Domain docs" in s
    assert "draft" in s and "does not relax" in s
    assert len(s.splitlines()) <= 100


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


def test_revised_line_is_itself_checked():
    log = OLD_FORMAT_LOG + "2026-01-01T01:00:00Z step=observe platform=x flow=a labels=none revised=2026-01-01T00:00:00Z\n"
    errs = check_kit.check_progress_log(log)
    assert any("progress.log:3: observe missing work=" in e for e in errs)
