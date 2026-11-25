"""Check packaged handoff guidance and real CLI readbacks, not host execution."""
import json
import re
from dataclasses import dataclass, replace
from hashlib import sha256
from pathlib import Path
from shutil import copyfile

import pytest

from conftest import KIT, ROOT, run
from test_library_cli import draft, save
from test_library_selection import REREAD, decision, invoke, upgrade_catalog
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
    assert "`needed_route_refs` can identify the ticket drafting route but do not authorize invocation" in intake
    assert "Apply [H5](#spec-approval-h5) before resolving or invoking it" in intake
    assert "Both inputs use the same operation checks" in intake


def test_prepare_routes_cover_only_missing_artifacts():
    prepare = section(IMPLEMENT / "ROUTES.md", "Prepare only missing artifacts")
    rows = dict(re.findall(r"^\| ((?:Spec|Ticket|Neither)[^|]*?) \| (.*?) \|$", prepare, re.M))
    assert rows == {
        "Spec and ticket": "None",
        "Spec only": "`harness-project-to-tickets` after H5",
        "Ticket only": "`harness-project-to-spec`",
        "Neither": "`harness-project-to-spec`, then `harness-project-to-tickets` after H5",
    }


def test_route_readiness_is_not_granted_by_registration_or_preparation():
    readiness = section(IMPLEMENT / "ROUTES.md", "Route readiness")
    assert "all three distinct, unshadowed project bindings" in readiness
    assert "The pair alone is not execution-ready" in readiness
    assert "readback alone does not qualify native routes" in readiness
    assert "[dispatch gates](WORK.md#dispatch-and-integrate)" in readiness
    assert "](ROUTES.md#route-readiness)" in (IMPLEMENT / "EXECUTION.md").read_text(encoding="utf-8")


def test_legacy_drafting_is_not_an_override_fallback():
    prepare = section(IMPLEMENT / "ROUTES.md", "Prepare only missing artifacts")
    assert "If the project has not adopted the overrides" in prepare
    assert "verified as agent-callable for the current caller and project" in prepare
    assert "not a fallback for a missing or blocked override in an opted-in project" in prepare


@dataclass(frozen=True)
class FixtureBinding:
    source: Path
    caller: str = "harness-implement"
    policy: str = "agent-callable"


def fixture_readback(candidates, opened):
    if len(candidates) != 1:
        return None
    binding, = candidates
    source = binding.source.resolve(strict=True)
    body = source.read_bytes()
    opened.append(source)
    skill_id, = re.findall(r"^name: (\S+)$", body.decode().split("---")[1], re.M)
    return skill_id, source, binding.caller, binding.policy, sha256(body).hexdigest()


@pytest.fixture
def override_project(tmp_path):
    guide = section(IMPLEMENT / "ROUTES.md", "Project override routes")
    pairs = re.findall(r"^\| `([\w-]+)` \| `([\w-]+)` \|", guide, re.M)
    assert pairs == [
        ("to-spec", "harness-project-to-spec"),
        ("to-tickets", "harness-project-to-tickets"),
        ("implement", "harness-project-implement"),
    ]
    routes = dict(pairs)
    project, neighbor = tmp_path / "project", tmp_path / "neighbor"
    neighbor.mkdir()
    (neighbor / "protected").write_bytes(b"keep")
    for original_id in routes:
        original = project / ".devin/skills" / original_id / "SKILL.md"
        original.parent.mkdir(parents=True)
        original.write_text(f"---\nname: {original_id}\ndisable-model-invocation: true\n---\n",
                            encoding="utf-8")

    def snapshot():
        return {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}

    def register(granted):
        before = snapshot()
        bindings, pins, additions = {}, {}, {}
        for skill_id in granted:
            template = ROOT / "skills/overrides" / skill_id / "SKILL.md"
            source = project / ".devin/skills" / skill_id / "SKILL.md"
            source.parent.mkdir()
            content = template.read_bytes()
            additions[source.relative_to(tmp_path)] = content
            copyfile(template, source)
            bindings[skill_id] = [FixtureBinding(source)]
            pins[skill_id] = (skill_id, source, "harness-implement", "agent-callable",
                              sha256(content).hexdigest())
        assert snapshot() == before | additions
        return bindings, pins

    return routes, register, snapshot, neighbor


@pytest.mark.parametrize("blocker", [None, "missing", "wrong-source", "wrong-caller",
                                    "user-only", "duplicate", "changed-digest"])
def test_fixture_project_override_readbacks(override_project, blocker):
    routes, register, snapshot, neighbor = override_project
    execution_id = routes["implement"]
    granted = [skill_id for role, skill_id in routes.items() if role != "implement" or blocker != "missing"]
    bindings, expected = register(granted)
    if blocker in {"wrong-source", "duplicate"}:
        original, = bindings[execution_id]
        shadow = neighbor / "SKILL.md"
        shadow.write_bytes(original.source.read_bytes())
        assert sha256(shadow.read_bytes()).hexdigest() == expected[execution_id][-1]
        bindings[execution_id] = ([original] if blocker == "duplicate" else []) + [FixtureBinding(shadow)]
    if blocker == "wrong-caller":
        bindings[execution_id] = [replace(bindings[execution_id][0], caller="setup")]
    if blocker == "user-only":
        bindings[execution_id] = [replace(bindings[execution_id][0], policy="user-only")]
    if blocker == "changed-digest":
        with bindings[execution_id][0].source.open("ab") as skill:
            skill.write(b"\nUnapproved change.\n")

    before = snapshot()
    verified = []
    for skill_id in routes.values():
        readback = fixture_readback(bindings.get(skill_id, []), [])
        if readback is not None and readback == expected.get(skill_id):
            verified.append(skill_id)
            print(f"fixture {skill_id}: Source={readback[1]} caller={readback[2]} policy={readback[3]}")
    outcome = "draft pair only" if blocker else "complete fixture registration"
    print(f"fixture {blocker or 'all-three'}: {outcome}; no execution qualification")
    assert verified == ([routes["to-spec"], routes["to-tickets"]] if blocker else list(routes.values()))
    assert snapshot() == before


@pytest.mark.parametrize(("case", "approval", "roles"), [
    ("Spec and ticket", "r2", []),
    ("Spec only", "r2", ["to-tickets"]),
    ("Ticket only", None, ["to-spec"]),
    ("Neither", "r2", ["to-spec", "to-tickets"]),
    ("Neither", None, ["to-spec"]),
    ("Neither", "r1", ["to-spec"]),
    ("Spec only", "r1", []),
])
def test_fixture_preparation_load_trace(override_project, case, approval, roles):
    routes, register, _, _ = override_project
    bindings, expected = register(routes.values())
    guide = section(IMPLEMENT / "ROUTES.md", "Prepare only missing artifacts")
    row, = re.findall(rf"^\| {case} \| (.*?) \|$", guide, re.M)
    opened = []
    spec_revision = "r2"
    for skill_id in re.findall(r"`([\w-]+)`", row):
        if skill_id == routes["to-tickets"]:
            if approval != spec_revision:
                print(f"ticket draft held: spec={spec_revision} approval={approval or '(none)'}")
                break
            print(f"ticket draft allowed: approval matches spec={spec_revision}")
        assert fixture_readback(bindings[skill_id], opened) == expected[skill_id]
    loaded = [p.parent.name for p in opened]
    print(f"prepare {case}: {', '.join(loaded) or '(none)'}")
    assert loaded == [routes[role] for role in roles]


@pytest.mark.parametrize("entry", ["direct or legacy preparation", "v1 `prepare` handoffs"])
@pytest.mark.parametrize("status", ["missing", "stale", "revoked"])
def test_prepare_holds_unapproved_spec_before_to_tickets(entry, status):
    prepare = section(IMPLEMENT / "WORK.md", "Prepare")
    _, heading, approval = prepare.partition("\n### Spec approval (H5)\n")
    assert heading, f"{entry} has no spec approval gate"
    assert entry in approval
    denied = re.search(r"^\| (Missing.*?) \| (.*?) \|$", approval, re.M)
    assert denied, f"{entry} has no blocked approval outcome"
    assert status in denied[1].lower().split(", ")
    assert "`AwaitSpecApproval`" in denied[2]
    assert "Do not resolve or invoke a ticket drafting route" in denied[2]
    assert "return the spec reference, revision, basis, scope, and blocker to the caller." in approval
    assert "requests H5 from the authorized spec owner only if a new approval is needed" in approval
    assert "Resume only on a new `prepare` request." in approval
    assert "Recheck approval on resume." in approval


def test_prepare_reuses_only_current_spec_approval():
    prepare = section(IMPLEMENT / "WORK.md", "Prepare")
    _, heading, approval = prepare.partition("\n### Spec approval (H5)\n")
    assert heading
    for required in (
        "authoritative spec or decision source",
        "authorized spec owner",
        "exact spec reference and revision",
        "decision reference and basis",
        "scope",
        "acceptance criteria and dependencies still match",
    ):
        assert required in approval
    assert "| Current and matching | Use the [verified drafting route](ROUTES.md#prepare-only-missing-artifacts) without asking again. |" in approval


def test_implement_keeps_destination_authority_and_reconciliation_separate():
    work = IMPLEMENT / "WORK.md"
    publish = section(work, "Publish or update")
    execute = section(work, "Dispatch and integrate")
    write = section(work, "Write boundary and reconciliation")
    assert "namespace blocks the write" in publish
    assert "including legacy records without a `work_id`" in publish
    assert "An ID hit must match all three" in publish
    assert "only create when both checks rule out an existing ticket" in publish
    assert "only after reading back" in publish
    assert "A stale claim, wrong route or revoked grant blocks the write" in execute
    assert "stale, disabled, unavailable or unreconciled selection" in execute
    assert "enforced by the destination when it accepts the write" in write
    assert "Do not run in the background" in write
    assert "Inspect destination receipts, history and state before resuming" in write
    assert "Do not replay, reassign, close or roll back pending reconciliation" in write


def test_publish_entries_use_the_same_gate():
    publish = section(IMPLEMENT / "WORK.md", "Publish or update")
    handoff = section(KIT / "STAGE-CONTRACTS.md", "Setup or Evolve → Implement: `publish`")
    assert "Direct publish, v1 handoffs and legacy records use the same gate" in publish
    assert "WORK.md#publish-or-update" in handoff
    assert "The checker validates shape only" in handoff


def test_publish_preflight_keeps_deduplication_at_the_selected_destination():
    publish = " ".join(section(IMPLEMENT / "WORK.md", "Publish or update").split())
    assert "Preflight is read-only" in publish
    assert "use the local record's own instance, namespace and role" in publish
    assert "Never switch to Product or fall back to local after a tracker error" in publish
    assert "look up the stable `work_id` once and search by node, question and intended outcome" in publish


@pytest.mark.parametrize(("case", "outcome"), [
    ("Draft revision changed", "Keep the draft; do not publish."),
    ("Material split with missing, mismatched or revoked owner approval", "Keep the draft; do not publish."),
    ("Product role or mismatched Harness locator", "Keep the draft; do not write to any destination."),
    ("Missing, stale, revoked or mismatched publish grant", "Keep the draft; do not publish."),
    ("Timeout after send", "Record `Unknown`; reconcile at the same destination without resending."),
])
def test_publish_failure_contract(case, outcome):
    publish = section(IMPLEMENT / "WORK.md", "Publish or update")
    assert f"| {case} | {outcome} |" in publish


def test_publish_split_approval_binds_the_draft_and_material_diff():
    publish = " ".join(section(IMPLEMENT / "WORK.md", "Publish or update").split())
    assert "ownership, acceptance, dependencies, scope or impact" in publish
    assert "exact draft reference and revision, material diff, decision basis and scope" in publish
    assert "authorized decision owner" in publish
    assert "H6 does not replace H5 or H7" in publish
    assert "An unchanged split may reuse the current decision" in publish


@pytest.mark.parametrize("role", ["harness", "product"])
def test_publish_checker_only_validates_shape(tmp_path, role):
    envelope = {
        "version": 1,
        "operation": "publish",
        "draft_ref": "draft:HARNESS-FIX-01@2",
        "target": {"instance": "local-records:fixture", "namespace": "harness:fixture", "role": role},
        "work_id": "harness:fixture:verification-rule",
        "grant_ref": "authority:fixture-publish@2",
    }
    original = json.dumps(envelope).encode()
    handoff = tmp_path / "publish.json"
    handoff.write_bytes(original)

    checked = run(CHECKER, "--expect-operation", "publish", handoff)

    assert checked.returncode == 0, checked.stderr
    assert handoff.read_bytes() == original
    assert list(tmp_path.iterdir()) == [handoff]


@pytest.mark.parametrize("source", ["supplied", "saved"])
def test_live_selection_readback_has_source_specific_v1_evidence(tmp_path, source):
    identity = REREAD if source == "supplied" else draft()["id"]
    args = ("selection", identity, "--source", source)
    if source == "supplied":
        upgrade_catalog(tmp_path)
        bundled = read(tmp_path, *args)
        state = read(tmp_path, *args, "--kit-dir", tmp_path / "kit")
        assert state["current_snapshot"]["sha256"] != bundled["current_snapshot"]["sha256"]
    else:
        saved = save(tmp_path, draft())
        assert saved.returncode == 0, saved.stderr
        state = read(tmp_path, *args)

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
        assert "`--kit-dir <pinned-catalog>`" in read_guide
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
