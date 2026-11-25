"""Target-side write grants for both revision histories."""
import json
import runpy
import sqlite3
import sys

import pytest

from test_library_cli import draft, save
from test_library_selection import CLI, REREAD, decision, invoke, rename_supplied, selection, supplied, upgrade_catalog
from test_library_updates import OLD, plan


def grant_write(root, operation, source, identity, payload, expected, *catalog):
    return invoke(root, "grant-write", operation, identity, "--source", source,
                  "--input", payload, "--expect-revision", expected, "--ttl-seconds", 60, *catalog)


def issue(root, *args):
    result = grant_write(root, *args)
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


def prepare_grant(root, operation):
    if operation in ("save", "update"):
        assert save(root, draft(origin=OLD)).returncode == 0
        value = plan(root) if operation == "update" else draft(origin=OLD, content="Revised guidance.")
        args = ("saved", "report-rule")
        history = ("history", "report-rule")
    else:
        decision_file = decision(root)
        value = json.loads(decision_file.read_text(encoding="utf-8"))
        args = ("supplied", REREAD)
        history = ("selection-history", REREAD, "--source", "supplied")
        if operation == "restore":
            prior = invoke(root, *request("disable", *args, decision_file, 0))
        else:
            # An unrelated resource gives disable a legacy store with no guard.
            prior = save(root, draft())
        assert prior.returncode == 0, prior.stderr
    payload = root / "approved.json"
    payload.write_text(json.dumps(value), encoding="utf-8")
    return (operation, *args, payload, 0 if operation == "disable" else 1), history


@pytest.mark.parametrize("operation", ["save", "restore"], ids=["content", "selection"])
def test_stale_grant_does_not_replace_current_grant(tmp_path, operation):
    grant, history = prepare_grant(tmp_path, operation)
    stale = (*grant[:-1], 0)
    database = tmp_path / "library.sqlite3"
    before = read(tmp_path, *history)

    def reject_stale(root, args, expected_found):
        result = grant_write(root, *args)
        assert result.returncode == 2, "stale grant was issued"
        assert result.stdout == ""
        assert expected_found in result.stderr
        assert ("show/history" if operation == "save" else "selection-history") in result.stderr

    legacy = database.read_bytes()
    reject_stale(tmp_path, stale, "expected 0, found 1")
    assert database.read_bytes() == legacy
    token = issue(tmp_path, *grant)
    guarded = database.read_bytes()
    reject_stale(tmp_path, stale, "expected 0, found 1")
    assert database.read_bytes() == guarded
    assert read(tmp_path, *history) == before

    missing = tmp_path / "missing"
    missing.mkdir()
    reject_stale(missing, grant, "expected 1, found 0")
    assert not (missing / database.name).exists()

    args = (*request(*grant), "--write-grant", token)
    result = invoke(tmp_path, *args)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["revision"] == 2
    assert invoke(tmp_path, *args).returncode == 2
    assert len(read(tmp_path, *history)) == len(before) + 1


@pytest.mark.parametrize("operation", ["save", "update", "disable", "restore"])
@pytest.mark.parametrize("invalid", ["malformed", "shape", "duplicate", "constant", "binding"])
def test_invalid_request_does_not_enable_guard_or_replace_token(tmp_path, operation, invalid):
    grant, history = prepare_grant(tmp_path, operation)
    database = tmp_path / "library.sqlite3"
    invalid_payload = tmp_path / "invalid.json"
    approved = grant[-2].read_bytes()
    invalid_payload.write_bytes({
        "malformed": b"{",
        "shape": b"{}",
        "duplicate": approved[:-1] + b', "metadata":{"key":0,"key":1}}',
        "constant": approved[:-1] + b', "metadata":[NaN]}',
        "binding": approved,
    }[invalid])
    bad_grant = (*grant[:-2], invalid_payload, grant[-1])
    if invalid == "binding":
        if operation == "save":
            # Change the request ID, not the target key that must retain its token.
            invalid_payload.write_text(json.dumps(draft(id="other", origin=OLD)), encoding="utf-8")
        elif operation == "update":
            invalid_payload.write_text(json.dumps(plan(tmp_path, comparison_token="stale")), encoding="utf-8")
        elif operation == "disable":
            invalid_payload.write_text(decision(tmp_path, confirm_rename_from="unrelated").read_text(encoding="utf-8"),
                                       encoding="utf-8")
        else:
            bad_grant = (operation, "saved", *bad_grant[2:])
    before = read(tmp_path, *history)

    def reject(root):
        result = grant_write(root, *bad_grant)
        assert result.returncode == 2, "invalid grant was issued"
        assert result.stdout == ""

    legacy = database.read_bytes()
    reject(tmp_path)
    assert database.read_bytes() == legacy
    assert read(tmp_path, *history) == before

    legacy_root = tmp_path / "legacy"
    legacy_root.mkdir()
    (legacy_root / database.name).write_bytes(legacy)
    assert invoke(legacy_root, *request(*grant)).returncode == 0

    token = issue(tmp_path, *grant)
    guarded = database.read_bytes()
    reject(tmp_path)
    assert database.read_bytes() == guarded
    assert read(tmp_path, *history) == before

    missing = tmp_path / "missing"
    missing.mkdir()
    reject(missing)
    assert not (missing / database.name).exists()

    assert invoke(tmp_path, *request(*grant), "--write-grant", token).returncode == 0
    assert len(read(tmp_path, *history)) == len(before) + 1


def test_slug_upgrade_requires_canonical_grant_without_resetting_revision(tmp_path):
    upgrade_catalog(tmp_path, keep_legacy_id=True)
    target = ("--kit-dir", tmp_path / "kit")
    payload = decision(tmp_path)
    grant = issue(tmp_path, "disable", "supplied", "H14", payload, 0, *target)
    result = invoke(tmp_path, *request("disable", "supplied", "H14", payload, 0),
                    *target, "--write-grant", grant)
    assert result.returncode == 0, result.stderr
    legacy_grant = issue(tmp_path, "restore", "supplied", "H14", payload, 1, *target)

    upgrade_catalog(tmp_path)
    rejected = invoke(tmp_path, "grant-write", "restore", "H14", "--source", "supplied",
                      "--input", payload, "--expect-revision", 1, "--ttl-seconds", 60, *target)
    assert rejected.returncode == 2 and REREAD in rejected.stderr
    mutation = (*request("restore", "supplied", REREAD, payload, 1), *target)
    assert_denied(invoke(tmp_path, *mutation, "--write-grant", legacy_grant))
    assert selection(tmp_path, id=REREAD)["effective"] is False

    grant = issue(tmp_path, "restore", "supplied", REREAD, payload, 1, *target)
    stale = invoke(tmp_path, *request("restore", "supplied", REREAD, payload, 0),
                   *target, "--write-grant", grant)
    assert stale.returncode == 2 and "Selection revision conflict" in stale.stderr
    result = invoke(tmp_path, *mutation, "--write-grant", grant)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["revision"] == 2
    assert revoke(tmp_path, grant).returncode == 2


def test_guarded_rename_preserves_exclusion_without_replaying_a_revoked_write(tmp_path):
    supplied(tmp_path)
    payload = decision(tmp_path)
    disable = request("disable", "supplied", REREAD, payload, 0)
    grant = issue(tmp_path, "disable", "supplied", REREAD, payload, 0)
    first = invoke(tmp_path, *disable, "--write-grant", grant)
    assert first.returncode == 0, first.stderr
    old_history = selection(tmp_path, id=REREAD, history=True)
    rename_supplied(tmp_path, REREAD, "replacement-hook")
    assert selection(tmp_path, id="replacement-hook")["possible_previous_ids"] == [REREAD]

    payload = decision(tmp_path, confirm_rename_from=REREAD)
    grant_args = ("disable", "supplied", "replacement-hook", payload, 0)
    target = ("--kit-dir", tmp_path / "kit")
    inherit = (*request(*grant_args), *target)
    grant = issue(tmp_path, *grant_args, *target)
    assert revoke(tmp_path, grant).returncode == 0
    assert_denied(invoke(tmp_path, *inherit, "--write-grant", grant))
    assert selection(tmp_path, id="replacement-hook", history=True) == []
    assert not selection(tmp_path, id="replacement-hook")["effective"]

    fresh = issue(tmp_path, *grant_args, *target)
    applied = invoke(tmp_path, *inherit, "--write-grant", fresh)
    assert applied.returncode == 0, applied.stderr
    state = selection(tmp_path, id="replacement-hook")
    assert not state["effective"]
    assert state["record"]["renamed_from"] == {"id": REREAD, "revision": 1}
    assert len(selection(tmp_path, id="replacement-hook", history=True)) == 1
    assert selection(tmp_path, id=REREAD, history=True) == old_history
    assert selection(tmp_path, id="evidence-labels")["effective"]


def test_guarded_store_never_falls_back_to_legacy_writes(tmp_path):
    # An empty grant table is the durable marker even after the last grant is gone.
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        db.execute("CREATE TABLE write_grants (grant_id TEXT)")
    args = request("disable", "supplied", REREAD, decision(tmp_path), 0)
    assert_denied(invoke(tmp_path, *args))
    assert read(tmp_path, "selection-history", REREAD, "--source", "supplied") == []


@pytest.mark.parametrize("operation", ["save", "update", "disable", "restore"])
def test_revoked_grant_leaves_history_unchanged_at_still_current_revision(tmp_path, operation):
    grant, history = prepare_grant(tmp_path, operation)
    args = request(*grant)
    token = issue(tmp_path, *grant)
    before = read(tmp_path, *history)
    assert revoke(tmp_path, token).returncode == 0
    assert_denied(invoke(tmp_path, *args, "--write-grant", token))
    assert_denied(invoke(tmp_path, *args))
    assert read(tmp_path, *history) == before

    token = issue(tmp_path, *grant)
    result = invoke(tmp_path, *args, "--write-grant", token)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["revision"] == grant[-1] + 1
    assert read(tmp_path, *history)[:-1] == before
    assert revoke(tmp_path, token).returncode == 2  # Committed grant is spent.


def test_grant_is_exact_and_reissuing_prevents_use_or_revocation_by_old_token(tmp_path):
    payload = decision(tmp_path)
    grant = ("disable", "supplied", REREAD, payload, 0)
    args = request(*grant)
    assert save(tmp_path, draft(id=REREAD)).returncode == 0
    old = issue(tmp_path, *grant)
    token = issue(tmp_path, *grant)
    assert revoke(tmp_path, old).returncode == 2
    assert_denied(invoke(tmp_path, *args, "--write-grant", old))
    saved = request("disable", "saved", REREAD, payload, 0)
    other_id = request("disable", "supplied", "evidence-labels", payload, 0)
    for wrong_request in (saved, other_id):
        assert_denied(invoke(tmp_path, *wrong_request, "--write-grant", token))
    for operation, expected, error in [
        ("restore", 0, "already has the requested state"),
        ("disable", 1, "expected 1, found 0"),
    ]:
        rejected = grant_write(tmp_path, operation, "supplied", REREAD, payload, expected)
        assert (rejected.returncode, rejected.stdout) == (2, "")
        assert error in rejected.stderr
    other_store = tmp_path / "other"
    other_store.mkdir()
    issue(other_store, *grant)
    assert_denied(invoke(other_store, *args, "--write-grant", token))
    approved_bytes = payload.read_bytes()
    payload.write_bytes(approved_bytes + b"\n")
    assert_denied(invoke(tmp_path, *args, "--write-grant", token))
    payload.write_bytes(approved_bytes)
    assert invoke(tmp_path, *args, "--write-grant", token).returncode == 0


def test_content_grant_cannot_be_used_for_a_different_operation(tmp_path):
    assert save(tmp_path, draft(origin=OLD)).returncode == 0
    # The exact bytes also describe a valid save; only the operation differs.
    payload = tmp_path / "request.json"
    payload.write_text(json.dumps(draft(origin=OLD) | plan(tmp_path)), encoding="utf-8")
    token = issue(tmp_path, "update", "saved", "report-rule", payload, 1)
    args = ("saved", "report-rule", payload, 1)
    assert_denied(invoke(tmp_path, *request("save", *args), "--write-grant", token))
    assert invoke(tmp_path, *request("update", *args), "--write-grant", token).returncode == 0


@pytest.mark.parametrize("operation", ["save", "disable"])
def test_valid_grant_can_bootstrap_at_zero_without_writing_history(tmp_path, operation):
    if operation == "save":
        payload = tmp_path / "request.json"
        payload.write_text(json.dumps(draft()), encoding="utf-8")
        grant = (operation, "saved", "report-rule", payload, 0)
        history = ("history", "report-rule")
    else:
        grant = (operation, "supplied", REREAD, decision(tmp_path), 0)
        history = ("selection-history", REREAD, "--source", "supplied")

    token = issue(tmp_path, *grant)
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        assert db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() == [("write_grants",)]
    args = request(*grant)
    assert_denied(invoke(tmp_path, *args))
    result = invoke(tmp_path, *args, "--write-grant", token)
    assert result.returncode == 0, result.stderr
    assert [event["revision"] for event in read(tmp_path, *history)] == [1]


@pytest.mark.parametrize(("operation", "source", "predecessor", "error"), [
    ("update", "saved", None, "requires a saved resource"),
    ("restore", "supplied", None, "already has the requested state"),
    ("disable", "saved", None, "Resource unavailable"),
    ("disable", "supplied", "unrelated", "possible predecessor"),
])
def test_grant_cannot_bootstrap_an_operation_that_requires_existing_state(tmp_path, operation, source, predecessor,
                                                                        error):
    if operation == "update":
        root = tmp_path / "existing"
        root.mkdir()
        grant, _ = prepare_grant(root, operation)
        identity, payload = grant[2:4]
    else:
        identity = REREAD
        payload = decision(tmp_path, **({"confirm_rename_from": predecessor} if predecessor else {}))
    result = grant_write(tmp_path, operation, source, identity, payload, 0)
    assert (result.returncode, result.stdout) == (2, "")
    assert error in result.stderr
    assert not (tmp_path / "library.sqlite3").exists()


def test_expired_grant_cannot_disable_or_fall_back_to_legacy(tmp_path):
    grant = ("disable", "supplied", REREAD, decision(tmp_path), 0)
    token = issue(tmp_path, *grant)
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        db.execute("UPDATE write_grants SET expires_at = 0")
    assert_denied(invoke(tmp_path, *request(*grant), "--write-grant", token))
    assert_denied(invoke(tmp_path, *request(*grant)))
    assert read(tmp_path, "selection-history", REREAD, "--source", "supplied") == []


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
    args = request("disable", "supplied", REREAD, decision(tmp_path), 0)
    assert invoke(tmp_path, *args, "--write-grant", "unknown").returncode == 2
    assert not (tmp_path / "library.sqlite3").exists()


def run_with_write_before_lock(tmp_path, monkeypatch, capsys, args, write):
    real_connect = sqlite3.connect
    competing_writes = []

    def connect(*args, **kwargs):
        db = real_connect(*args, **kwargs)

        def before_statement(statement):
            if statement == "BEGIN IMMEDIATE":
                competing_writes.append(write())

        db.set_trace_callback(before_statement)
        return db

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        patch.setattr(sys, "argv", [str(CLI), "--store", str(tmp_path / "library.sqlite3"), *map(str, args)])
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(CLI), run_name="__main__")
    assert [r.returncode for r in competing_writes] == [0]
    assert result.value.code == 2
    output = capsys.readouterr()
    assert not output.out
    return output.err


def test_revocation_just_before_begin_immediate_is_observed(tmp_path, monkeypatch, capsys):
    grant = ("disable", "supplied", REREAD, decision(tmp_path), 0)
    token = issue(tmp_path, *grant)
    args = (*request(*grant), "--write-grant", token)
    error = run_with_write_before_lock(tmp_path, monkeypatch, capsys, args, lambda: revoke(tmp_path, token))
    assert "No current write grant matches this mutation" in error
    assert read(tmp_path, "selection-history", REREAD, "--source", "supplied") == []


def test_grant_rechecks_after_concurrent_bootstrap_writer(tmp_path, monkeypatch, capsys):
    payload = tmp_path / "request.json"
    payload.write_text(json.dumps(draft(content="Losing request")), encoding="utf-8")
    args = ("grant-write", "save", "report-rule", "--source", "saved",
            "--input", payload, "--expect-revision", 0, "--ttl-seconds", 60)
    winner = draft(content="Winning request")
    error = run_with_write_before_lock(tmp_path, monkeypatch, capsys, args, lambda: save(tmp_path, winner))
    assert "expected 0, found 1" in error
    assert [event["resource"] for event in read(tmp_path, "history", "report-rule")] == [winner]
    with sqlite3.connect(tmp_path / "library.sqlite3") as db:
        assert db.execute("SELECT 1 FROM sqlite_master WHERE name='write_grants'").fetchone() is None
