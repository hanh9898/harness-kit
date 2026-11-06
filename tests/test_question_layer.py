"""Question layer: asking document, skill pointers and 41 complete sheets; behavior is covered by CHECKLIST.md."""
import re

from conftest import ROOT

SETUP = ROOT / "skills" / "harness" / "harness-setup"
EVOLVE = ROOT / "skills" / "harness" / "harness-evolve"

FIELDS = ("Stage", "Helps", "If skipped", "Why", "Ask", "Terms", "Enough", "Unsure", "Suggest")
HEAD = re.compile(r"^###\s+\[([SV]\d\d)\]", re.M)


def _sheets():
    """Return {ID: sheet body} for every Sxx or Vxx question in both skills."""
    out = {}
    for skill in (SETUP, EVOLVE):
        for f in skill.glob("*.md"):
            text = f.read_text(encoding="utf-8")
            marks = list(HEAD.finditer(text))
            for i, m in enumerate(marks):
                end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
                nxt = re.search(r"^#{1,2}\s", text[m.end():end], re.M)
                if nxt:
                    end = m.end() + nxt.start()
                assert m.group(1) not in out, f"duplicate question sheet {m.group(1)}"
                out[m.group(1)] = (f, text[m.start():end])
    return out


def test_asking_exists_with_required_sections():
    text = (SETUP / "ASKING.md").read_text(encoding="utf-8")
    for needle in ("## Overview message", "## Full form", "## Compact form", "## Rules", "## Confirming a chain",
                   "## Incomplete answers"):
        assert needle in text, needle


def test_both_skills_point_to_asking_and_stay_short():
    setup = (SETUP / "SKILL.md").read_text(encoding="utf-8")
    evolve = (EVOLVE / "SKILL.md").read_text(encoding="utf-8")
    assert "](ASKING.md)" in setup
    assert "](../harness-setup/ASKING.md)" in evolve
    assert not (EVOLVE / "ASKING.md").exists()
    assert len(setup.splitlines()) <= 110
    assert len(evolve.splitlines()) <= 80


def test_all_41_questions_have_a_complete_sheet():
    sheets = _sheets()
    want = {f"S{n:02d}" for n in range(1, 32)} | {f"V{n:02d}" for n in range(1, 11)}
    assert set(sheets) == want, (want - set(sheets), set(sheets) - want)
    for sid, (f, body) in sheets.items():
        for field in FIELDS:
            assert re.search(rf"^- {field}\b", body, re.M), (sid, f.name, field)
        stage = re.search(r"^- Stage: (\d)/(\d)", body, re.M)
        assert stage, (sid, "Stage k/N")
        n = 6 if sid.startswith("S") else 4
        assert int(stage.group(2)) == n and 1 <= int(stage.group(1)) <= n, sid


def test_each_step_file_points_back_to_asking():
    for f in ("BOUNDARY.md", "GATE.md", "PROPOSALS.md", "DELEGATION.md", "ROLES.md", "STANDARDS-STEP.md",
              "ISOLATION.md", "WIRING.md"):
        assert "](ASKING.md)" in (SETUP / f).read_text(encoding="utf-8"), f
    for f in ("DRIFT.md", "CHECK-STEP.md", "UPDATE.md"):
        assert "](../harness-setup/ASKING.md)" in (EVOLVE / f).read_text(encoding="utf-8"), f


def test_questions_avoid_harness_words_in_why_and_ask():
    banned = re.compile(r"\b(rung|kit|gate|lego|legos|tracer|check_scope)\b", re.I)
    for sid, (f, body) in _sheets().items():
        for line in body.splitlines():
            if re.match(r"^- (Why|Ask)\b", line):
                assert not banned.search(line), (sid, line)


def test_no_absolute_paths_in_asking():
    assert "/Users/" not in (SETUP / "ASKING.md").read_text(encoding="utf-8")


# --- Ticket 22: revisions from two unscripted readers. ---

def _asking():
    return (SETUP / "ASKING.md").read_text(encoding="utf-8")


def test_level_scale_describes_all_seven_levels():
    f, body = _sheets()["S18"]
    for n in range(1, 8):
        assert re.search(rf"^\s*{n}\s*=", body, re.M), f"S18 lacks a description for level {n}"
    assert "who decides" in body.lower() or "you decide" in body.lower()


def test_asking_has_the_ticket_22_rules():
    text = _asking()
    for needle in ("## Words the user sees", "## Contradiction between git and the account",
                   "## Echo the user's own choice"):
        assert needle in text, needle


def test_stage_four_is_announced_and_grouped():
    deleg = (SETUP / "DELEGATION.md").read_text(encoding="utf-8")
    assert "announce" in deleg.lower()
    roles = (SETUP / "ROLES.md").read_text(encoding="utf-8")
    assert "all four cells in one turn" in roles


def test_overview_has_a_word_limit():
    assert re.search(r"at most \d+ words", _asking())


def test_kit_readme_counts_match_csv():
    import csv
    readme = (ROOT / "kit" / "README.md").read_text(encoding="utf-8")
    for name in ("legos.csv", "rules.csv"):
        with open(ROOT / "kit" / name, newline="", encoding="utf-8") as fh:
            n = len(list(csv.reader(fh))) - 1
        m = re.search(rf"\| `{re.escape(name)}` \|[^|]*\| (\d+) \|", readme)
        assert m and int(m.group(1)) == n, (name, n, m and m.group(1))
