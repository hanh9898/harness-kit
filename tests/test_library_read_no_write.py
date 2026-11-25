"""No-write regression cases run against the public Library CLI."""

import ctypes
import json
import os
import select
import sqlite3
import subprocess
import sys

import pytest

from conftest import run
from test_library_cli import CLI, draft, save
from test_library_selection import REREAD, decision


EXPLICIT = ("show", "history", "compare")
OPTIONAL = ("search", "selection", "selection-history")
READS = [(name, False) for name in EXPLICIT + OPTIONAL] + [(name, True) for name in OPTIONAL]
NO_WRITE_UNAVAILABLE = "cannot enforce a no-write SQLite open on this host"


@pytest.fixture(scope="module")
def no_write_host():
    if (sys.platform != "linux" or os.uname().machine not in ("x86_64", "aarch64")
            or ctypes.sizeof(ctypes.c_void_p) != 8):
        return False
    return ctypes.CDLL(None).syscall(444, None, ctypes.c_size_t(0), 1) >= 3


def read_args(store, candidate, command, strict):
    args = ["--store", str(store)]
    if strict:
        args.append("--require-existing-store")
    args += [command, "report-rule"]
    if command in ("selection", "selection-history"):
        args += ["--source", "saved"]
    if command == "compare":
        args += ["--candidate", str(candidate)]
    return args


def files(root):
    return {p.relative_to(root).as_posix(): None if p.is_dir() else p.read_bytes()
            for p in root.rglob("*")}


@pytest.fixture
def library(tmp_path):
    store = tmp_path / "library.sqlite3"
    result = save(tmp_path, draft(), store=store)
    assert result.returncode == 0, result.stderr
    candidate = tmp_path / "candidate.json"
    candidate.write_text(json.dumps(dict(reference="kit:report-rule", revision="new", snapshot="New text.")),
                         encoding="utf-8")
    return store, candidate


@pytest.mark.parametrize(("command", "strict"), READS)
@pytest.mark.parametrize("state", ["wal-idle", "wal-active", "rollback", "malformed", "missing"])
def test_public_reads_do_not_change_store_files(library, command, strict, state, no_write_host):
    store, candidate = library
    sidecars = {store.name + "-wal", store.name + "-shm"}
    writer = None
    if state.startswith("wal-"):
        writer = sqlite3.connect(store)
        assert writer.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
        if state == "wal-active":
            writer.execute("CREATE TABLE active_writer (id INTEGER)")
            writer.commit()
        else:
            writer.close()
            writer = None
    elif state == "malformed":
        store.write_bytes(b"not a SQLite database")
    elif state == "missing":
        store.unlink()
        store = store.parent / "absent" / store.name

    try:
        before = files(candidate.parent)
        assert sidecars.intersection(before) == (sidecars if state == "wal-active" else set())
        result = run(CLI, *read_args(store, candidate, command, strict))
        after = files(candidate.parent)
        assert after == before, (
            f"{command} exit={result.returncode}, added={sorted(after.keys() - before.keys())}, "
            f"removed={sorted(before.keys() - after.keys())}, "
            f"changed={sorted(p for p in before.keys() & after.keys() if before[p] != after[p])}"
        )
        if state == "rollback" and not no_write_host:
            assert (result.returncode, result.stdout) == (2, "")
            assert NO_WRITE_UNAVAILABLE in result.stderr
            return
        optional_missing = state == "missing" and command in OPTIONAL and not strict
        if state != "rollback" and not optional_missing:
            assert (result.returncode, result.stdout) == (2, "")
            error = "missing" if state == "missing" else "unreadable"
            assert f"Store is {error}: {store}" in result.stderr
            return

        assert (result.returncode, result.stderr) == (0, "")
        payload = json.loads(result.stdout)
        if command == "search":
            saved = [hit["id"] for hit in payload["matches"] if hit["origin"] == "saved"]
            assert saved == ([] if optional_missing else ["report-rule"])
        elif command in ("selection", "selection-history"):
            if command == "selection":
                assert (payload["revision"], payload["record"], payload["effective"]) == (
                    0, None, not optional_missing)
            else:
                assert payload == []
        elif command == "history":
            assert [(item["id"], item["revision"]) for item in payload] == [("report-rule", 1)]
        else:
            assert (payload["id"], payload["revision"]) == ("report-rule", 1)
            if command == "compare":
                assert payload["candidate"]["snapshot"] == "New text."
    finally:
        if writer is not None:
            writer.close()


@pytest.mark.parametrize("invalid", ["{", "{}"])
def test_malformed_compare_candidate_is_rejected_without_writes(library, invalid, no_write_host):
    if not no_write_host:
        pytest.skip("Candidate parsing needs a qualified no-write store")
    store, candidate = library
    candidate.write_text(invalid, encoding="utf-8")
    before = files(store.parent)
    result = run(CLI, *read_args(store, candidate, "compare", False))
    assert (result.returncode, result.stdout) == (2, "")
    assert ("Expecting property name" if invalid == "{" else "Candidate needs") in result.stderr
    assert files(store.parent) == before


def test_existing_store_is_not_opened_when_no_write_cannot_be_enforced(library):
    store, candidate = library
    before = files(store.parent)
    code = """
import ctypes, runpy, sqlite3, sys
from types import SimpleNamespace
ctypes.CDLL = lambda *_: SimpleNamespace(syscall=lambda *_: -1)
def reject_open(*args, **kwargs):
    raise AssertionError('SQLite open was not blocked')
sqlite3.connect = reject_open
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
"""
    result = subprocess.run([sys.executable, "-I", "-c", code, str(CLI),
                             *read_args(store, candidate, "show", False)],
                            capture_output=True, text=True, timeout=10)
    assert (result.returncode, result.stdout) == (2, "")
    assert NO_WRITE_UNAVAILABLE in result.stderr
    assert files(store.parent) == before


@pytest.mark.parametrize("command", EXPLICIT)
def test_selection_only_store_reports_missing_resource(tmp_path, command, no_write_host):
    if not no_write_host:
        pytest.skip("Resource lookup needs a qualified no-write store")
    store, candidate = tmp_path / "library.sqlite3", tmp_path / "candidate.json"
    disabled = run(CLI, "--store", store, "disable", REREAD, "--source", "supplied",
                   "--input", decision(tmp_path), "--expect-selection-revision", 0)
    assert disabled.returncode == 0, disabled.stderr
    before = files(store.parent)
    result = run(CLI, *read_args(store, candidate, command, False))
    assert (result.returncode, result.stdout) == (2, "")
    assert "Resource not found" in result.stderr
    assert files(store.parent) == before


PAUSE_BEFORE_SQLITE_OPEN = """
import runpy, sqlite3, sys
connect = sqlite3.connect
def paused_connect(*args, **kwargs):
    print('ready', file=sys.stderr, flush=True)
    if not sys.stdin.readline():
        raise RuntimeError('Missing race trigger')
    return connect(*args, **kwargs)
sqlite3.connect = paused_connect
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
"""


@pytest.mark.parametrize(("command", "strict"), [("search", True), ("show", False)])
@pytest.mark.parametrize("transition", ["wal", "wal-active", "replace-empty"])
def test_database_changed_between_preflight_and_open_is_rejected(library, command, strict, transition, no_write_host):
    if not no_write_host:
        pytest.skip("The race seam needs a qualified no-write store")
    store, candidate = library
    args = read_args(store, candidate, command, strict)
    with subprocess.Popen([sys.executable, "-I", "-c", PAUSE_BEFORE_SQLITE_OPEN, str(CLI), *args],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True) as reader:
        writer = None
        try:
            assert select.select([reader.stderr], [], [], 10)[0], "CLI never reached SQLite open"
            assert reader.stderr.readline() == "ready\n"
            if transition.startswith("wal"):
                writer = sqlite3.connect(store)
                assert writer.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
                if transition == "wal-active":
                    writer.execute("CREATE TABLE active_writer (id INTEGER)")
                    writer.commit()
                else:
                    writer.close()
                    writer = None
            else:
                replacement = store.with_suffix(".replacement")
                replacement.touch()
                replacement.replace(store)
                store.with_name(store.name + "-wal").write_bytes(b"existing sidecar")
            before = files(store.parent)
            stdout, stderr = reader.communicate("\n", timeout=10)
            assert files(store.parent) == before
            assert (reader.returncode, stdout) == (2, "")
            assert f"Store is unreadable: {store}" in stderr
        finally:
            if reader.poll() is None:
                reader.kill()
            if writer is not None:
                writer.close()
