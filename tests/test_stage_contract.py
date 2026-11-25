"""Exercise the v1 handoff contract through the local checker."""
import json

import pytest

from conftest import KIT, ROOT, run

CHECKER = KIT / "scripts" / "check-stage-handoff"
FIXTURES = ROOT / "tests" / "fixtures" / "stage-handoffs"


def fixture(operation):
    return json.loads((FIXTURES / f"{operation}.json").read_text(encoding="utf-8"))


def check(tmp_path, handoff, *args):
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps(handoff), encoding="utf-8")
    return run(CHECKER, path, *args)


def assert_invalid(result, message):
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("invalid handoff: ")
    assert message in result.stderr


@pytest.mark.parametrize("operation", ["prepare", "publish", "execute", "selection", "result", "bot-setup"])
def test_accepts_each_v1_handoff(operation):
    result = run(CHECKER, FIXTURES / f"{operation}.json", "--expect-operation", operation)
    assert result.returncode == 0, result.stderr
    assert result.stdout == f"OK: v1 {operation} handoff shape is valid\n"
    assert result.stderr == ""


def test_rejects_unknown_version_fixture():
    assert_invalid(run(CHECKER, FIXTURES / "invalid-version.json"), "version must be the integer 1")


@pytest.mark.parametrize("version", [True, 1.0, "1", None])
def test_requires_integer_version(tmp_path, version):
    assert_invalid(check(tmp_path, dict(fixture("execute"), version=version)), "version must be the integer 1")


def test_rejects_valid_payload_for_another_operation():
    result = run(CHECKER, FIXTURES / "publish.json", "--expect-operation", "execute")
    assert_invalid(result, "expected operation 'execute', got 'publish'")


def test_rejects_mislabeled_shape_without_an_expected_operation(tmp_path):
    assert_invalid(check(tmp_path, dict(fixture("execute"), operation="publish")), "publish missing required fields")


@pytest.mark.parametrize("operation", ["dispatch", ["execute"], None])
def test_rejects_unknown_operation(tmp_path, operation):
    assert_invalid(check(tmp_path, dict(fixture("execute"), operation=operation)), "operation must be one of")


@pytest.mark.parametrize("operation, field", [
    ("prepare", "acceptance"), ("publish", "grant_ref"), ("execute", "assignment_ref"),
    ("selection", "selection_revision"), ("result", "outcome"), ("bot-setup", "contract_ref"),
])
def test_requires_operation_specific_fields(tmp_path, operation, field):
    handoff = fixture(operation)
    del handoff[field]
    assert_invalid(check(tmp_path, handoff), f"{operation} missing required fields: {field}")


@pytest.mark.parametrize("updates, message", [
    ({"assignment_ref": " "}, "execute.assignment_ref must be a reference"),
    ({"route_ref": {"id": "route-check-19"}}, "execute.route_ref must be a reference"),
    ({"expected_target_revision": True}, "execute.expected_target_revision must be a revision"),
    ({"ticket_ref": {"id": "work-17"}}, "execute.ticket_ref missing required fields"),
    ({"grant_ref": "publish-approval-41"}, "execute has unexpected fields: 'grant_ref'"),
])
def test_rejects_malformed_or_cross_operation_fields(tmp_path, updates, message):
    assert_invalid(check(tmp_path, dict(fixture("execute"), **updates)), message)


def test_execute_accepts_unresolved_selection_reference(tmp_path):
    result = check(tmp_path, dict(fixture("execute"), selection_ref="unresolved-selection@3"))
    assert result.returncode == 0, result.stderr


def test_prepare_accepts_original_request_or_immutable_ref_but_not_both(tmp_path):
    handoff = dict(fixture("prepare"), request="Original request\nwith details.")
    assert_invalid(check(tmp_path, handoff), "prepare requires exactly one of request or request_ref")
    del handoff["request_ref"]
    result = check(tmp_path, handoff)
    assert result.returncode == 0, result.stderr
    del handoff["request"]
    assert_invalid(check(tmp_path, handoff), "prepare requires exactly one of request or request_ref")


def test_selection_checks_revision_kind_and_internal_status(tmp_path):
    handoff = dict(fixture("selection"), source="saved", content_revision=3)
    assert_invalid(check(tmp_path, handoff), "distribution_revision does not match selection.source")
    del handoff["distribution_revision"]
    result = check(tmp_path, handoff)
    assert result.returncode == 0, result.stderr
    handoff.update(available=False)
    assert_invalid(check(tmp_path, handoff), "effective must equal enabled and available")
    handoff.update(effective=False)
    del handoff["content_revision"], handoff["digest"]
    result = check(tmp_path, handoff)
    assert result.returncode == 0, result.stderr


def test_saved_selection_accepts_content_revision_without_digest(tmp_path):
    handoff = dict(fixture("selection"), source="saved", id="saved-checklist", content_revision=3)
    del handoff["digest"], handoff["distribution_revision"]
    result = check(tmp_path, handoff)
    assert result.returncode == 0, result.stderr


def test_available_supplied_selection_requires_snapshot_digest(tmp_path):
    handoff = fixture("selection")
    del handoff["digest"]
    assert_invalid(check(tmp_path, handoff), "selection.digest is required")


def test_result_needs_effect_identity_and_reconciliation_reference(tmp_path):
    handoff = fixture("result")
    del handoff["effect_id"]
    assert_invalid(check(tmp_path, handoff), "result requires effect_id or request_id")
    handoff["request_id"] = "dispatch-55"
    del handoff["history_ref"]
    assert_invalid(check(tmp_path, handoff), "result requires receipt_ref or history_ref")
    handoff.update(outcome="Applied", receipt_ref="receipt-5")
    result = check(tmp_path, handoff)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("content, message", [
    (b"{", "Expecting property name"),
    (b"[]", "handoff must be an object"),
    (b'{"version": 1, "version": 2}', "duplicate JSON field: 'version'"),
    (b'{"version": NaN}', "invalid JSON constant: NaN"),
    (b"\xff", "invalid start byte"),
])
def test_rejects_invalid_input_without_a_traceback(tmp_path, content, message):
    path = tmp_path / "invalid.json"
    path.write_bytes(content)
    assert_invalid(run(CHECKER, path), message)


def test_rejects_missing_input_file(tmp_path):
    assert_invalid(run(CHECKER, tmp_path / "absent.json"), "No such file or directory")
