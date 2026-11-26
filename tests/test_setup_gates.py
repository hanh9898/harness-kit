"""Executable Setup preflight and transition gate contracts."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from conftest import KIT, run

PREFLIGHT = KIT / "scripts/check-setup-preflight"
TRANSITION = KIT / "scripts/check-setup-transition"

MAIN_BRANCHES = [
    "Environment & authority",
    "Guidance & knowledge",
    "Capabilities",
    "Agent configuration & roles",
    "Coordination",
    "Verification & feedback",
    "State & continuation",
]


def run_json(script, *args, env=None):
    result = subprocess.run(
        [sys.executable, "-I", str(script), *map(str, args), "--json"],
        capture_output=True,
        text=True,
        env=env,
    )
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise AssertionError(f"expected JSON stdout, got {result.stdout!r}; stderr={result.stderr!r}")
    return result, report


def fake_path(tmp_path, *, crontab=""):
    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    git = shutil.which("git")
    if git:
        (fakebin / "git").symlink_to(git)
    cron = fakebin / "crontab"
    cron.write_text(f"#!/bin/sh\nif [ \"$1\" = -l ]; then printf '%s' '{crontab}'; exit 0; fi\nexit 1\n", encoding="utf-8")
    cron.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = str(fakebin)
    env["HOME"] = str(tmp_path / "home")
    return env


def snapshot(root):
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_missing_node_and_npx_block_an_apply_install_without_writing(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    env = fake_path(tmp_path)
    before = snapshot(tmp_path)

    result, report = run_json(
        PREFLIGHT,
        "--target", target,
        "--mode", "apply",
        "--effect", "install-upstream=grant:install@1",
        "--requires-tool", "node",
        "--requires-tool", "npx",
        env=env,
    )

    assert result.returncode == 1
    missing = {row["tool"] for row in report["blockers"] if row["id"] == "missing-tool"}
    assert missing == {"node", "npx"}
    assert all("install-upstream" in row["needed_for"] for row in report["blockers"] if row["id"] == "missing-tool")
    assert snapshot(tmp_path) == before


def test_apply_without_the_effect_grant_stops_before_the_operation(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    env = fake_path(tmp_path)

    result, report = run_json(
        PREFLIGHT,
        "--target", target,
        "--mode", "apply",
        "--effect", "install-upstream",
        env=env,
    )

    assert result.returncode == 1
    assert "missing-effect-grant" in {row["id"] for row in report["blockers"]}
    assert not list(target.iterdir())


def test_deploy_overwrite_task_blocks_apply_until_writer_evidence_exists(tmp_path):
    target = tmp_path / "deploy-copy"
    target.mkdir()
    cron_line = f"0 * * * * cd {target} && git reset --hard origin/main\\n"
    env = fake_path(tmp_path, crontab=cron_line)
    before = snapshot(tmp_path)

    result, report = run_json(
        PREFLIGHT,
        "--target", target,
        "--mode", "apply",
        "--effect", "write-record=grant:write@1",
        env=env,
    )

    assert result.returncode == 1
    assert "external-writer-unverified" in {row["id"] for row in report["blockers"]}
    assert "external-writer-candidate" in {row["id"] for row in report["signals"]}
    assert snapshot(tmp_path) == before

    result, report = run_json(
        PREFLIGHT,
        "--target", target,
        "--mode", "apply",
        "--effect", "write-record=grant:write@1",
        "--writer-evidence", "evidence:no-overwrite-writer@1",
        env=env,
    )
    assert result.returncode == 0, report
    assert report["ready"] is True
    assert snapshot(tmp_path) == before


def make_detached_checkout(root):
    root.mkdir()
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
    (root / "file").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "file"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "one"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "--detach", "HEAD"], cwd=root, check=True, capture_output=True)


def test_detached_head_is_a_review_signal_not_a_deploy_verdict(tmp_path):
    target = tmp_path / "checkout"
    make_detached_checkout(target)
    env = fake_path(tmp_path)

    inspect_result, inspect_report = run_json(
        PREFLIGHT, "--target", target, "--mode", "inspect", env=env,
    )
    assert inspect_result.returncode == 0
    signal_ids = {row["id"] for row in inspect_report["signals"]}
    assert "detached-head" in signal_ids
    assert all(row["id"] != "deployed-checkout" for row in inspect_report["signals"])

    apply_result, apply_report = run_json(
        PREFLIGHT,
        "--target", target,
        "--mode", "apply",
        "--effect", "write-record=grant:write@1",
        env=env,
    )
    assert apply_result.returncode == 1
    assert "target-role-unverified" in {row["id"] for row in apply_report["blockers"]}

    evidenced_result, evidenced_report = run_json(
        PREFLIGHT,
        "--target", target,
        "--mode", "apply",
        "--effect", "write-record=grant:write@1",
        "--target-role-evidence", "evidence:real-work-checkout@1",
        env=env,
    )
    assert evidenced_result.returncode == 0, evidenced_report


def outcome(path, confirmation="confirm:batch@1"):
    return {
        "path": path,
        "status": "settled",
        "decision_ref": f"decision:{path}@1",
        "confirmation_ref": confirmation,
        "checkpoint_ref": f"checkpoint:{path}@1",
    }


def base_record():
    return {
        "version": 1,
        "transition": "design-ready",
        "scope_ref": "scope:docs",
        "decision_ref": "decision:docs-guidance@2",
        "branch_outcomes": [outcome(path) for path in MAIN_BRANCHES],
        "confirmations": [
            {"ref": "confirm:batch@1", "covered_paths": list(MAIN_BRANCHES)},
        ],
    }


def prepare_handoff():
    return {
        "version": 1,
        "operation": "prepare",
        "request": "Set up guidance for the docs repository.",
        "scope_ref": "scope:docs",
        "decision_ref": "decision:docs-guidance@2",
        "acceptance": ["The selected reader can locate the documentation guidance."],
        "dependency_refs": [],
        "needed_route_refs": ["route:to-spec@1", "route:to-tickets@1"],
    }


def write_record(tmp_path, record):
    path = tmp_path / "transition.json"
    original = json.dumps(record, indent=2)
    path.write_text(original, encoding="utf-8")
    return path, original


def test_design_ready_accepts_branch_specific_confirmations(tmp_path):
    path, original = write_record(tmp_path, base_record())
    result = run(TRANSITION, path)
    assert result.returncode == 0, result.stderr
    assert path.read_text(encoding="utf-8") == original


def test_design_ready_rejects_a_missing_branch_decision(tmp_path):
    record = base_record()
    missing = record["branch_outcomes"].pop(2)["path"]
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert missing in result.stderr
    assert "missing branch outcome" in result.stderr


def test_blanket_confirmation_does_not_close_an_unlisted_branch(tmp_path):
    record = base_record()
    record["confirmations"][0]["covered_paths"].remove("Capabilities")
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert "Capabilities" in result.stderr
    assert "confirmation" in result.stderr


def test_prepare_requires_the_prepare_handoff(tmp_path):
    record = base_record()
    record["transition"] = "prepare"
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert "handoffs.prepare" in result.stderr

    record["handoffs"] = {"prepare": prepare_handoff()}
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 0, result.stderr


def verified_record():
    record = base_record()
    ticket = {"instance": "local:docs-work-records", "namespace": "harness:docs", "id": "ticket:docs-guidance", "revision": 1}
    record.update({
        "transition": "verified",
        "handoffs": {
            "prepare": prepare_handoff(),
            "publish": {
                "version": 1,
                "operation": "publish",
                "draft_ref": "draft:docs-guidance@3",
                "target": {"instance": "local:docs-work-records", "namespace": "harness:docs", "role": "harness"},
                "work_id": "work:docs-guidance",
                "grant_ref": "grant:docs-guidance-publish@1",
            },
            "execute": {
                "version": 1,
                "operation": "execute",
                "request_ref": "request:docs-guidance@1",
                "scope_ref": "scope:docs",
                "decision_ref": "decision:docs-guidance@2",
                "ticket_ref": ticket,
                "assignment_ref": "assignment:docs-guidance@1",
                "route_ref": "route:harness-project-implement@1",
                "effect_ref": "effect:write-docs-guidance@1",
                "expected_target_revision": 4,
            },
            "result": {
                "version": 1,
                "operation": "result",
                "assignment_ref": "assignment:docs-guidance@1",
                "target_ref": "target:docs-guidance",
                "target_revision": 5,
                "effect_id": "effect:write-docs-guidance@1",
                "outcome": "Applied",
                "receipt_ref": "receipt:docs-guidance@1",
                "verification_refs": ["evidence:docs-guidance-check@1"],
                "evidence_refs": ["evidence:docs-guidance-diff@1"],
                "next_step": "Close under close authority.",
            },
        },
        "acceptance_evidence": [
            {"acceptance_ref": "acceptance:reader-can-locate@1", "evidence_ref": "evidence:docs-guidance-check@1"},
        ],
        "close_authority_ref": "grant:close-docs-guidance@1",
    })
    return record


def test_verified_requires_applied_result_evidence_and_close_authority(tmp_path):
    record = verified_record()
    path, original = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 0, result.stderr
    assert path.read_text(encoding="utf-8") == original

    for mutate, expected in [
        (lambda r: r["handoffs"]["result"].update(outcome="Unknown"), "outcome"),
        (lambda r: r.pop("close_authority_ref"), "close_authority_ref"),
        (lambda r: r.update(acceptance_evidence=[]), "acceptance_evidence"),
        (lambda r: r["handoffs"].pop("execute"), "handoffs.execute"),
    ]:
        bad = verified_record()
        mutate(bad)
        path, _ = write_record(tmp_path, bad)
        result = run(TRANSITION, path)
        assert result.returncode == 1
        assert expected in result.stderr


def test_transition_checker_rejects_mismatched_scope_or_assignment(tmp_path):
    record = verified_record()
    record["handoffs"]["execute"]["assignment_ref"] = "assignment:other@1"
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert "assignment_ref" in result.stderr

    record = verified_record()
    record["handoffs"]["prepare"]["scope_ref"] = "scope:other"
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert "scope_ref" in result.stderr


def test_confirmed_child_branch_requires_its_own_outcome(tmp_path):
    record = base_record()
    record["confirmations"][0]["covered_paths"].append("Capabilities / Skills")
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert "confirmed child branch" in result.stderr


def test_transition_checker_does_not_write_bytecode(tmp_path):
    cache = TRANSITION.parent / "__pycache__"
    if cache.exists():
        import shutil
        shutil.rmtree(cache)
    path, _ = write_record(tmp_path, base_record())
    result = run(TRANSITION, path)
    assert result.returncode == 0, result.stderr
    assert not cache.exists()


def test_writer_scan_checks_both_supplied_symlink_and_resolved_target(tmp_path):
    real = tmp_path / "real-target"
    real.mkdir()
    link = tmp_path / "linked-target"
    link.symlink_to(real, target_is_directory=True)
    cron_line = f"0 * * * * cd {link} && git reset --hard origin/main\\n"
    env = fake_path(tmp_path, crontab=cron_line)
    result, report = run_json(
        PREFLIGHT,
        "--target", link,
        "--mode", "apply",
        "--effect", "write-record=grant:write@1",
        env=env,
    )
    assert result.returncode == 1
    assert "external-writer-unverified" in {row["id"] for row in report["blockers"]}


def test_verified_rejects_execution_ticket_from_another_harness_namespace(tmp_path):
    record = verified_record()
    record["handoffs"]["execute"]["ticket_ref"]["namespace"] = "harness:other"
    path, _ = write_record(tmp_path, record)
    result = run(TRANSITION, path)
    assert result.returncode == 1
    assert "ticket_ref.namespace" in result.stderr


def test_relative_dot_target_does_not_match_unrelated_dotted_filenames(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    cron_line = "0 * * * * cd /opt/other && python3 cache.db-cleanup.py\n"
    env = fake_path(tmp_path, crontab=cron_line)
    result, report = run_json(
        PREFLIGHT,
        "--target", project,
        "--mode", "apply",
        "--effect", "write-record=grant:write@1",
        env=env,
    )
    assert result.returncode == 0, report
    assert "external-writer-candidate" not in {row["id"] for row in report["signals"]}
