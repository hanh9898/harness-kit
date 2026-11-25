"""Check packaged handoff guidance and real CLI readbacks, not host execution."""
import json
import re

import pytest

from conftest import KIT, ROOT, run
from test_library_cli import draft, save
from test_library_selection import REREAD, decision, invoke
from test_library_write_grants import assert_denied, issue, read, request, revoke

SKILLS = ROOT / "skills/harness"
IMPLEMENT = SKILLS / "harness-implement"
LIBRARY = SKILLS / "harness-library"
CHECKER = KIT / "scripts/check-stage-handoff"


def section(path, heading):
    _, found, body = path.read_text(encoding="utf-8").partition(f"\n## {heading}\n")
    assert found, f"{path.name}: missing section {heading!r}"
    return body.split("\n## ", 1)[0]


def test_implement_routes_v1_and_legacy_to_the_same_operation_gates():
    entry = (IMPLEMENT / "SKILL.md").read_text(encoding="utf-8")
    intake = section(IMPLEMENT / "WORK.md", "Handoff intake")
    for operation, anchor in {
        "prepare": "prepare",
        "publish": "publish-or-update",
        "execute": "dispatch-and-integrate",
    }.items():
        assert f"[`{operation}`](WORK.md#{anchor})" in entry
    assert "](../../../kit/STAGE-CONTRACTS.md)" in intake
    assert "--expect-operation <operation> <file>" in intake
    assert "do not reinterpret a rejected handoff as legacy input" in intake
    assert "Both inputs use the same operation checks" in intake


def test_prepare_routes_cover_only_missing_artifacts():
    prepare = section(IMPLEMENT / "ROUTES.md", "Prepare only missing artifacts")
    rows = dict(re.findall(r"^\| ((?:Spec|Ticket|Neither)[^|]*?) \| (.*?) \|$", prepare, re.M))
    assert rows == {
        "Spec and ticket": "None",
        "Spec only": "`to-tickets`",
        "Ticket only": "`to-spec`",
        "Neither": "`to-spec`, then `to-tickets`",
    }


def test_implement_keeps_destination_authority_and_reconciliation_separate():
    work = IMPLEMENT / "WORK.md"
    publish = section(work, "Publish or update")
    execute = section(work, "Dispatch and integrate")
    write = section(work, "Write boundary and reconciliation")
    assert "namespace blocks the write" in publish
    assert "node, question and intended outcome for older records without a `work_id`" in publish
    assert "A missing ID match does not prove the work is new" in publish
    assert "only after reading back" in publish
    assert "A stale claim, wrong route or revoked grant blocks the write" in execute
    assert "stale, disabled, unavailable or unreconciled selection" in execute
    assert "enforced by the destination when it accepts the write" in write
    assert "Do not run in the background" in write
    assert "Inspect destination receipts, history and state before resuming" in write
    assert "Do not replay, reassign, close or roll back pending reconciliation" in write


@pytest.mark.parametrize("source", ["supplied", "saved"])
def test_live_selection_readback_has_source_specific_v1_evidence(tmp_path, source):
    identity = REREAD if source == "supplied" else draft()["id"]
    if source == "saved":
        saved = save(tmp_path, draft())
        assert saved.returncode == 0, saved.stderr

    state = read(tmp_path, "selection", identity, "--source", source)
    read_guide = (LIBRARY / "READ.md").read_text(encoding="utf-8")
    assert "`revision` as `selection_revision`" in read_guide
    handoff = {
        "version": 1,
        "operation": "selection",
        "store_ref": "disposable-library",
        "scope_ref": "test-project",
        "selection_revision": state["revision"],
        "evidence_refs": ["test-readback"],
        **{field: state[field] for field in ("source", "id", "enabled", "available", "effective")},
    }
    assert state["available"] and state["effective"]
    if source == "supplied":
        assert "`current_snapshot.sha256` as `digest`" in read_guide
        handoff.update(distribution_revision="test-distribution", digest=state["current_snapshot"]["sha256"])
    else:
        assert "`current_snapshot.revision` as `content_revision`" in read_guide
        handoff["content_revision"] = state["current_snapshot"]["revision"]
        assert handoff["selection_revision"] != handoff["content_revision"]

    path = tmp_path / "selection.json"
    path.write_text(json.dumps(handoff), encoding="utf-8")
    result = run(CHECKER, "--expect-operation", "selection", path)
    assert result.returncode == 0, result.stderr


def test_revoked_library_write_and_single_send_reconcile_against_history(tmp_path):
    args = ("selection-history", REREAD, "--source", "supplied")
    payload = decision(tmp_path)
    mutation = request("disable", "supplied", REREAD, payload, 0)
    assert read(tmp_path, *args) == []
    assert not (tmp_path / "library.sqlite3").exists()

    grant = issue(tmp_path, "disable", "supplied", REREAD, payload, 0)
    assert revoke(tmp_path, grant).returncode == 0
    assert_denied(invoke(tmp_path, *mutation, "--write-grant", grant))
    assert read(tmp_path, *args) == []

    fresh_grant = issue(tmp_path, "disable", "supplied", REREAD, payload, 0)
    sent = invoke(tmp_path, *mutation, "--write-grant", fresh_grant)
    assert sent.returncode == 0, sent.stderr
    # Do not use the write response as evidence. Reopen the destination, without replay.
    history = read(tmp_path, *args)
    assert [(row["action"], row["revision"]) for row in history] == [("disable", 1)]
    state = read(tmp_path, "selection", REREAD, "--source", "supplied")
    assert not state["effective"] and state["revision"] == 1
