"""Executable contract for user-visible Harness Setup scope selection."""
import json
import subprocess

from conftest import KIT, run

SCOPE = KIT / "scripts/check-setup-scope"
OPTIONS = [
    {"id": "repo-only", "label": "Only this repository"},
    {"id": "bot-only", "label": "Only a Bot"},
    {"id": "repo-and-bot", "label": "Both the repository and a Bot"},
]


def scenario(**overrides):
    value = {
        "version": 1,
        "request": "",
        "intent": "unclear",
        "basis": [],
        "user_view": {
            "text": "Choose the setup scope.",
            "shown_profile": "undecided",
            "options": OPTIONS,
            "bot_question_asked": False,
        },
        "recorded_profile": "undecided",
        "bot_identity": "not-applicable",
        "effects": [],
    }
    value.update(overrides)
    return value


def check(tmp_path, value):
    path = tmp_path / "scope.json"
    original = json.dumps(value, indent=2)
    path.write_text(original, encoding="utf-8")
    result = run(SCOPE, path)
    assert path.read_text(encoding="utf-8") == original
    return result


def test_empty_request_in_git_repo_stays_undecided_and_shows_three_plain_choices(tmp_path):
    scratch = tmp_path / "scratch-project"
    scratch.mkdir()
    init = subprocess.run(["git", "init", "-q", str(scratch)], capture_output=True, text=True)
    assert init.returncode == 0, init.stderr
    before = sorted(path.relative_to(scratch).as_posix() for path in scratch.rglob("*"))
    result = check(tmp_path, scenario(basis=["git-directory"]))
    assert result.returncode == 0, result.stderr
    after = sorted(path.relative_to(scratch).as_posix() for path in scratch.rglob("*"))
    assert after == before


def test_clear_repo_request_names_repo_only_without_opening_bot_questions(tmp_path):
    result = check(tmp_path, scenario(
        request="Set up Harness guidance for this repository.",
        intent="repo-only",
        basis=["user-request"],
        user_view={
            "text": "Scope: only this repository. No Bot setup is included.",
            "shown_profile": "repo-only",
            "options": [],
            "bot_question_asked": False,
        },
        recorded_profile="repo-only",
    ))
    assert result.returncode == 0, result.stderr


def test_bot_intent_can_be_selected_before_a_real_bot_identity(tmp_path):
    result = check(tmp_path, scenario(
        request="Set up a Bot, no repository.",
        intent="bot-only",
        basis=["user-request"],
        user_view={
            "text": "Scope: only a Bot. The exact Bot is still unverified.",
            "shown_profile": "bot-only",
            "options": [],
            "bot_question_asked": False,
        },
        recorded_profile="bot-only",
        bot_identity="missing",
    ))
    assert result.returncode == 0, result.stderr


def test_repo_and_bot_request_records_both_without_effects(tmp_path):
    result = check(tmp_path, scenario(
        request="Set up the repository Harness and its Bot.",
        intent="repo-and-bot",
        basis=["user-request"],
        user_view={
            "text": "Scope: both the repository and a Bot.",
            "shown_profile": "repo-and-bot",
            "options": [],
            "bot_question_asked": False,
        },
        recorded_profile="repo-and-bot",
        bot_identity="missing",
    ))
    assert result.returncode == 0, result.stderr


def test_unclear_request_cannot_be_decided_from_git_or_agent_host(tmp_path):
    value = scenario(
        basis=["git-directory", "agent-host"],
        user_view={"text": "Scope: only this repository.", "shown_profile": "repo-only", "options": [], "bot_question_asked": False},
        recorded_profile="repo-only",
    )
    result = check(tmp_path, value)
    assert result.returncode == 1
    assert "git-directory" in result.stderr and "agent-host" in result.stderr


def test_undecided_scope_requires_all_three_user_visible_options(tmp_path):
    value = scenario()
    value["user_view"]["options"] = OPTIONS[:2]
    result = check(tmp_path, value)
    assert result.returncode == 1
    assert "three" in result.stderr


def test_scope_selection_never_authorizes_effects_or_missing_bot_configuration(tmp_path):
    value = scenario(
        intent="bot-only",
        basis=["user-request"],
        user_view={"text": "Scope: only a Bot.", "shown_profile": "bot-only", "options": [], "bot_question_asked": False},
        recorded_profile="bot-only",
        bot_identity="missing",
        effects=["configure-bot"],
    )
    result = check(tmp_path, value)
    assert result.returncode == 1
    assert "configure-bot" in result.stderr


def test_bare_request_cannot_use_empty_user_request_as_decision_evidence(tmp_path):
    value = scenario(
        request="",
        intent="repo-only",
        basis=["user-request"],
        user_view={"text": "Scope: repo.", "shown_profile": "repo-only", "options": [], "bot_question_asked": False},
        recorded_profile="repo-only",
    )
    result = check(tmp_path, value)
    assert result.returncode == 1
    assert "user-selection" in result.stderr
