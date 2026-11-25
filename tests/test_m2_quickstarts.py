import os
import re
import shutil
import subprocess

import pytest

from conftest import KIT, ROOT


HARNESS_IDS = ("harness-setup", "harness-evolve", "harness-implement", "harness-library")
LIBRARY_ID = "harness-library"


@pytest.fixture
def devin_project(tmp_path):
    checkout = tmp_path / "kit checkout"
    project = tmp_path / "consumer project"
    project.mkdir()
    shutil.copytree(ROOT / "skills" / "harness", checkout / "skills" / "harness")
    shutil.copytree(KIT, checkout / "kit", ignore=shutil.ignore_patterns("__pycache__"))

    def git(*args):
        return subprocess.run(
            ["git", "-C", checkout, *args], check=True, capture_output=True, text=True
        ).stdout.strip()

    git("init", "--quiet")
    git("add", ".")
    git(
        "-c", "user.name=Fixture", "-c", "user.email=fixture@example.com",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
        "commit", "--quiet", "-m", "Pin a complete skill layout",
    )
    return checkout, project, git("rev-parse", "HEAD")


def bootstrap_devin(checkout, project, revision, **env):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    section = readme.split("### Devin — project scope (v1 pilot)\n", 1)[1].split("\n### ", 1)[0]
    (command,) = re.findall(r"```sh\n(.*?)\n```", section, re.DOTALL)
    return subprocess.run(
        ["sh", "-c", command],
        env={**os.environ, "KIT": str(checkout), "PROJECT": str(project), "KIT_COMMIT": revision, **env},
        capture_output=True,
        text=True,
    )


def test_devin_links_preserve_tool_and_never_overwrite(devin_project):
    checkout, project, revision = devin_project
    entries = project / ".devin" / "skills"
    sources = checkout / "skills" / "harness"
    for skill_id in HARNESS_IDS:
        shutil.copytree(sources / skill_id, entries / skill_id)

    library_path = (entries / LIBRARY_ID).resolve() / "../../../kit/scripts/library"
    copied = subprocess.run(
        ["sh", "-c", '"$1" --help', "sh", library_path], capture_output=True, text=True
    )
    assert copied.returncode == 127
    assert copied.stdout == ""
    rejected_copy = bootstrap_devin(checkout, project, revision)
    assert rejected_copy.returncode == 2
    assert "existing entry does not resolve" in rejected_copy.stderr
    assert all((entries / name / "SKILL.md").is_file() for name in HARNESS_IDS)
    assert all(not path.is_symlink() for path in entries.iterdir())

    shutil.rmtree(entries)
    first = bootstrap_devin(checkout, project, revision)
    assert first.returncode == 0, first.stderr
    assert first.stdout.startswith("usage: library")
    assert {path.name for path in entries.iterdir()} == set(HARNESS_IDS)
    for path in entries.iterdir():
        assert path.is_symlink()
        assert path.resolve() == sources / path.name
    initial = {path.name: (path.readlink(), path.lstat()) for path in entries.iterdir()}

    second = bootstrap_devin(checkout, project, revision)
    assert second.returncode == 0, second.stderr
    assert second.stdout == first.stdout
    for path in entries.iterdir():
        target, stat_before = initial[path.name]
        assert path.readlink() == target
        assert path.lstat().st_ino == stat_before.st_ino
        assert path.lstat().st_ctime_ns == stat_before.st_ctime_ns


@pytest.mark.parametrize("dangling", [False, True], ids=["wrong-source", "dangling"])
def test_devin_link_conflict_leaves_all_entries_unchanged(devin_project, tmp_path, dangling):
    checkout, project, revision = devin_project
    link = project / ".devin" / "skills" / LIBRARY_ID
    link.parent.mkdir(parents=True)
    other = tmp_path / "other checkout" / LIBRARY_ID
    if not dangling:
        shutil.copytree(checkout / "skills" / "harness" / LIBRARY_ID, other)
    link.symlink_to(other, target_is_directory=True)

    result = bootstrap_devin(checkout, project, revision)

    assert result.returncode == 2
    assert result.stdout == ""
    assert str(link) in result.stderr
    assert link.readlink() == other
    assert list(link.parent.iterdir()) == [link]


def test_devin_registration_checks_the_pin_and_clean_checkout_before_writing(devin_project):
    checkout, project, revision = devin_project

    wrong_pin = bootstrap_devin(checkout, project, revision[:-1])
    assert wrong_pin.returncode == 2
    assert "approved commit" in wrong_pin.stderr
    assert not (project / ".devin").exists()

    (checkout / "untracked").touch()
    dirty = bootstrap_devin(checkout, project, revision)
    assert dirty.returncode == 2
    assert "checkout is not clean" in dirty.stderr
    assert not (project / ".devin").exists()


def test_devin_registration_rejects_redirected_skills_directory(devin_project, tmp_path):
    checkout, project, revision = devin_project
    outside = tmp_path / "out-of-scope"
    outside.mkdir()
    devin_dir = project / ".devin"
    devin_dir.mkdir()
    (devin_dir / "skills").symlink_to(outside, target_is_directory=True)

    result = bootstrap_devin(checkout, project, revision)

    assert result.returncode == 2
    assert "not a project-local directory" in result.stderr
    assert not list(outside.iterdir())


@pytest.mark.parametrize(
    ("missing", "expected_error"),
    [("python3", "python3"), ("realpath", "realpath"), (None, "cannot run the pinned Library helper")],
    ids=["missing-python3", "missing-realpath", "failing-helper"],
)
def test_devin_registration_checks_runtime_before_writing(devin_project, tmp_path, missing, expected_error):
    checkout, project, revision = devin_project
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for command in {"sh", "git", "realpath", "mkdir", "ln", "python3"} - {missing}:
        executable = bin_dir / command
        if missing is None and command == "python3":
            executable.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
            executable.chmod(0o755)
        else:
            executable.symlink_to(shutil.which(command))

    result = bootstrap_devin(checkout, project, revision, PATH=str(bin_dir))

    assert result.returncode == 2
    assert expected_error in result.stderr
    assert not (project / ".devin").exists()


@pytest.mark.parametrize("subdir", [False, True], ids=["same-checkout", "nested-project"])
def test_devin_registration_does_not_dirty_the_pinned_checkout(devin_project, subdir):
    checkout, _, revision = devin_project
    project = checkout
    if subdir:
        project /= "nested"
        project.mkdir()

    result = bootstrap_devin(checkout, project, revision)

    assert result.returncode == 2
    assert "outside the pinned kit checkout" in result.stderr
    assert not (project / ".devin").exists()


def test_host_adapters_cover_each_capability_and_its_fallback():
    document = (KIT / "HOST-ADAPTERS.md").read_text(encoding="utf-8")
    table = document.split("## Capability map\n", 1)[1].split("\n## ", 1)[0]
    heading, _, *rows = [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in table.splitlines()
        if line.startswith("|")
    ]
    assert heading == [
        "Capability", "Devin", "Pi", "Claude Code", "Codex",
        "Fallback when the required primitive is absent",
    ]
    assert len(rows) == 6
    assert {row[0].strip("`") for row in rows} == {
        "work-workers", "inbox", "memory", "domain-targets", "wake", "evidence-write-gate",
    }
    assert all(len(row) == len(heading) and all(row) for row in rows)
