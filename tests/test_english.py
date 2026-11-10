"""Exercise language checks through Git repositories and public CLI entry points."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CHECK = Path(__file__).resolve().parents[1] / "tools/check_english.py"
SAMPLE = "\u0111\u1ed5i"


def git(root, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "Test User", "GIT_AUTHOR_EMAIL": "test@example.com",
           "GIT_COMMITTER_NAME": "Test User", "GIT_COMMITTER_EMAIL": "test@example.com"}
    return subprocess.run(["git", "-C", str(root), *args], env=env, check=True,
                          capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init")
    (tmp_path / "README.md").write_text("English documentation.\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "-c", "core.hooksPath=/dev/null", "commit", "-m", "chore: initialize")
    return tmp_path


def run(repo, *args):
    return subprocess.run([sys.executable, "-I", str(CHECK), "--root", str(repo), *map(str, args)],
                          capture_output=True, text=True)


def test_accepts_english_and_ignores_untracked_local_notes(repo):
    (repo / "local.md").write_text(SAMPLE)
    assert run(repo, "--commits", "--history").returncode == 0


def test_reports_content_and_filename_violations(repo):
    path = repo / (SAMPLE + ".md")
    path.write_text("English\n" + SAMPLE)
    git(repo, "add", ".")
    result = run(repo)
    assert result.returncode == 1
    assert "tracked path:1" in result.stderr and ".md:2" in result.stderr


def test_normalizes_decomposed_unicode(repo):
    (repo / "README.md").write_text("a\u0301")
    assert run(repo).returncode == 1


def test_staged_check_uses_index_instead_of_working_tree(repo):
    path = repo / "README.md"
    path.write_text(SAMPLE)
    assert run(repo, "--staged").returncode == 0
    git(repo, "add", ".")
    path.write_text("English again")
    assert run(repo, "--staged").returncode == 1


def test_detects_a_bad_message_after_the_current_tree_is_clean(repo):
    git(repo, "-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-m", SAMPLE)
    assert run(repo).returncode == 0
    assert run(repo, "--commits").returncode == 1


def test_detects_historical_content_after_it_has_been_removed(repo):
    path = repo / "README.md"
    path.write_text(SAMPLE)
    git(repo, "add", ".")
    git(repo, "-c", "core.hooksPath=/dev/null", "commit", "-m", "test: temporary content")
    path.write_text("English again")
    git(repo, "add", ".")
    git(repo, "-c", "core.hooksPath=/dev/null", "commit", "-m", "test: replace content")
    assert run(repo).returncode == 0
    assert run(repo, "--history").returncode == 1


@pytest.mark.parametrize("field", ["title", "body"])
def test_checks_pull_request_metadata(repo, field):
    event = repo / "event.json"
    event.write_text(json.dumps({"pull_request": {field: SAMPLE}}))
    result = run(repo, "--event-file", event)
    assert result.returncode == 1 and f"pull_request.{field}" in result.stderr


def test_commit_message_hook_input(repo):
    message = repo / "message.txt"
    message.write_text("feat: " + SAMPLE)
    assert run(repo, "--message-file", message).returncode == 1
    message.write_text("feat: use English")
    assert run(repo, "--message-file", message).returncode == 0


def test_installed_hooks_block_invalid_source_and_messages(repo):
    source = CHECK.parents[1]
    shutil.copytree(source / ".githooks", repo / ".githooks")
    (repo / "tools").mkdir()
    shutil.copyfile(CHECK, repo / "tools/check_english.py")
    git(repo, "config", "core.hooksPath", ".githooks")
    git(repo, "add", ".")
    with pytest.raises(subprocess.CalledProcessError) as rejected:
        git(repo, "commit", "-m", SAMPLE)
    assert "commit message:1" in rejected.value.stderr
    git(repo, "commit", "-m", "chore: install checks")
    (repo / "README.md").write_text(SAMPLE)
    git(repo, "add", ".")
    with pytest.raises(subprocess.CalledProcessError) as rejected:
        git(repo, "commit", "-m", "test: rejected source")
    assert "README.md:1" in rejected.value.stderr
