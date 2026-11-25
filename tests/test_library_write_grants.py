"""Target-side write grants for both revision histories."""
import json
import runpy
import sqlite3
import sys

import pytest

from test_library_cli import draft, save
from test_library_selection import CLI, decision, invoke
from test_library_updates import OLD, plan


def issue(root, operation, source, identity, payload, expected):
    result = invoke(root, "grant-write", operation, identity, "--source", source,
                    "--input", payload, "--expect-revision", expected, "--ttl-seconds", 60)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["write_grant"]


def revoke(root, token):
    return invoke(root, "revoke-write", token)


def read(root, *args):
    result = invoke(root, *args)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def request(operation, source, identity, payload, expected):
    args = (operation,)
    if operation != "save":
        args += (identity,)
    if operation in ("disable", "restore"):
        args += ("--source", source, "--expect-selection-revision", expected)
    else:
        args += ("--expect-revision", expected)
    return (*args, "--input", payload)


def assert_denied(result):
    assert (result.returncode, result.stdout) == (2, "")
    assert "No current write grant matches this mutation" in result.stderr


def test_guarded_store_never_falls_back_to_legacy_writes(tmp_path):
    # An empty grant table is the durable marker even after the last grant is gone.
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        db.execute("CREATE TABLE write_grants (grant_id TEXT)")
    args = request("disable", "supplied", "H14", decision(tmp_path), 0)
    assert_denied(invoke(tmp_path, *args))
    assert read(tmp_path, "selection-history", "H14", "--source", "supplied") == []


@pytest.mark.parametrize("operation", ["save", "update", "disable", "restore"])
def test_revoked_grant_leaves_history_unchanged_at_still_current_revision(tmp_path, operation):
    source, identity = ("saved", "report-rule") if operation in ("save", "update") else ("supplied", "H14")
    selection = source == "supplied"
    expected = 0
    if selection:
        payload = decision(tmp_path)
        if operation == "restore":
            prior = invoke(tmp_path, *request("disable", source, identity, payload, 0))
            assert prior.returncode == 0, prior.stderr
            expected = 1
        history = ("selection-history", identity, "--source", source)
    else:
        assert save(tmp_path, draft(origin=OLD)).returncode == 0
        expected = 1
        payload = tmp_path / "request.json"
        payload.write_text(json.dumps(plan(tmp_path) if operation == "update"
                                      else draft(origin=OLD, content="New draft content")), encoding="utf-8")
        history = ("history", identity)

    args = request(operation, source, identity, payload, expected)
    token = issue(tmp_path, operation, source, identity, payload, expected)
    before = read(tmp_path, *history)
    assert revoke(tmp_path, token).returncode == 0
    assert_denied(invoke(tmp_path, *args, "--write-grant", token))
    assert_denied(invoke(tmp_path, *args))
    assert read(tmp_path, *history) == before

    token = issue(tmp_path, operation, source, identity, payload, expected)
    result = invoke(tmp_path, *args, "--write-grant", token)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["revision"] == expected + 1
    assert read(tmp_path, *history)[:-1] == before
    assert revoke(tmp_path, token).returncode == 2  # Committed grant is spent.


def test_grant_is_exact_and_reissuing_prevents_use_or_revocation_by_old_token(tmp_path):
    payload = decision(tmp_path)
    grant = ("disable", "supplied", "H14", payload, 0)
    args = request(*grant)
    assert save(tmp_path, draft(id="H14")).returncode == 0
    old = issue(tmp_path, *grant)
    token = issue(tmp_path, *grant)
    assert revoke(tmp_path, old).returncode == 2
    assert_denied(invoke(tmp_path, *args, "--write-grant", old))
    saved = request("disable", "saved", "H14", payload, 0)
    other_id = request("disable", "supplied", "H15", payload, 0)
    for wrong_request in (saved, other_id):
        assert_denied(invoke(tmp_path, *wrong_request, "--write-grant", token))
    wrong_op = issue(tmp_path, "restore", "supplied", "H14", payload, 0)
    assert_denied(invoke(tmp_path, *args, "--write-grant", wrong_op))
    future = issue(tmp_path, "disable", "supplied", "H14", payload, 1)
    assert_denied(invoke(tmp_path, *args, "--write-grant", future))
    token = issue(tmp_path, *grant)
    other_store = tmp_path / "other"
    other_store.mkdir()
    issue(other_store, *grant)
    assert_denied(invoke(other_store, *args, "--write-grant", token))
    approved_bytes = payload.read_bytes()
    payload.write_bytes(approved_bytes + b"\n")
    assert_denied(invoke(tmp_path, *args, "--write-grant", token))
    payload.write_bytes(approved_bytes)
    assert invoke(tmp_path, *args, "--write-grant", token).returncode == 0


def test_expired_grant_cannot_disable_or_fall_back_to_legacy(tmp_path):
    grant = ("disable", "supplied", "H14", decision(tmp_path), 0)
    token = issue(tmp_path, *grant)
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        db.execute("UPDATE write_grants SET expires_at = 0")
    assert_denied(invoke(tmp_path, *request(*grant), "--write-grant", token))
    assert_denied(invoke(tmp_path, *request(*grant)))
    assert read(tmp_path, "selection-history", "H14", "--source", "supplied") == []


def test_grant_consumption_rolls_back_if_resource_insert_fails(tmp_path):
    assert save(tmp_path, draft()).returncode == 0
    payload = tmp_path / "draft.json"
    payload.write_text(json.dumps(draft(content="A new draft")), encoding="utf-8")
    grant = ("save", "saved", "report-rule", payload, 1)
    token = issue(tmp_path, *grant)
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        db.execute("""CREATE TRIGGER abort_insert BEFORE INSERT ON revisions
            BEGIN SELECT RAISE(ABORT, 'test insert failure'); END""")
    args = (*request(*grant), "--write-grant", token)
    result = invoke(tmp_path, *args)
    assert result.returncode == 2 and "test insert failure" in result.stderr
    assert len(read(tmp_path, "history", "report-rule")) == 1
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        db.execute("DROP TRIGGER abort_insert")
    assert invoke(tmp_path, *args).returncode == 0
    assert len(read(tmp_path, "history", "report-rule")) == 2


def test_unknown_grant_cannot_create_a_store(tmp_path):
    args = request("disable", "supplied", "H14", decision(tmp_path), 0)
    assert invoke(tmp_path, *args, "--write-grant", "unknown").returncode == 2
    assert not (tmp_path / "library.sqlite3").exists()


def test_revocation_just_before_begin_immediate_is_observed(tmp_path, monkeypatch, capsys):
    payload = decision(tmp_path)
    grant = ("disable", "supplied", "H14", payload, 0)
    token = issue(tmp_path, *grant)
    store = tmp_path / "library.sqlite3"
    real_connect = sqlite3.connect
    revocations = []

    def connect(*args, **kwargs):
        db = real_connect(*args, **kwargs)

        def before_statement(statement):
            if statement == "BEGIN IMMEDIATE":
                revocations.append(revoke(tmp_path, token))

        db.set_trace_callback(before_statement)
        return db

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        patch.setattr(sys, "argv", [str(CLI), "--store", str(store),
                                  *map(str, request(*grant)), "--write-grant", token])
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(CLI), run_name="__main__")
    assert [r.returncode for r in revocations] == [0]
    assert result.value.code == 2
    output = capsys.readouterr()
    assert not output.out and "No current write grant matches this mutation" in output.err
    assert read(tmp_path, "selection-history", "H14", "--source", "supplied") == []
