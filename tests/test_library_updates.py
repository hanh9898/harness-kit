"""Origin updates at the owner-confirmed public library operation seam."""
import json

from conftest import run
from test_library_cli import CLI, draft, save


OLD = {"reference": "source:reports", "revision": "v1", "snapshot": "Review facts.\nPublish weekly.\n"}
NEW = {"reference": "source:reports", "revision": "v2", "snapshot": "Review facts.\nPublish monthly.\n"}
CUSTOM = "Review facts with Linh.\nPublish weekly.\n"


def operation(tmp_path, command, value, *args):
    path = tmp_path / (command + ".json")
    path.write_text(json.dumps(value))
    flag = "--candidate" if command == "compare" else "--input"
    return run(CLI, "--store", tmp_path / "library.sqlite3", command, "report-rule", flag, path, *args)


def read(tmp_path, command="show"):
    r = run(CLI, "--store", tmp_path / "library.sqlite3", command, "report-rule")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_comparison_exposes_actual_three_versions_and_missing_basis_without_writes(tmp_path):
    assert save(tmp_path, draft(origin=OLD, content=CUSTOM)).returncode == 0
    r = operation(tmp_path, "compare", NEW)
    assert r.returncode == 0, r.stderr
    comparison = json.loads(r.stdout)
    assert comparison["old_origin"] == OLD
    assert comparison["customization"] == CUSTOM
    assert comparison["candidate"] == NEW
    assert "+Review facts with Linh." in comparison["diffs"]["customization"]
    assert "+Publish monthly." in comparison["diffs"]["origin"]
    assert comparison["semantic_compatibility"] == "unchecked"
    assert len(read(tmp_path, "history")) == 1
    other = tmp_path / "unknown"
    other.mkdir()
    assert save(other, draft(origin=None, content=CUSTOM)).returncode == 0
    missing = json.loads(operation(other, "compare", NEW).stdout)
    assert missing["basis"] == "missing" and missing["old_origin"] is None
    assert missing["diffs"]["origin"] is None
    assert missing["unknowns"] and read(other)["revision"] == 1


def plan(tmp_path, **changes):
    comparison = json.loads(operation(tmp_path, "compare", NEW).stdout)
    value = dict(candidate=NEW, comparison_token=comparison["token"], mode="update",
                 outcome="complete", content="Review facts with Linh.\nPublish monthly.\n",
                 review={"summary": "Cadence and reviewer are independent under the report contract.",
                         "checks": ["Checked monthly reporting still requires Linh's fact review."],
                         "compatible_changes": ["Monthly cadence"], "conflicts": [], "unknowns": [],
                         "prior_selection_valid": True},
                 decision=draft()["decision"], continuation="Check a monthly report before consumer adoption.")
    value.update(changes)
    return value


def test_checked_compatible_update_retains_customization_and_rejects_stale_or_unchecked_plan(tmp_path):
    assert save(tmp_path, draft(origin=OLD, content=CUSTOM, known_uses=["consumer-a"])).returncode == 0
    request = plan(tmp_path)
    unchecked = dict(request, review={})
    assert operation(tmp_path, "update", unchecked, "--expect-revision", 1).returncode != 0
    assert read(tmp_path)["revision"] == 1
    r = operation(tmp_path, "update", request, "--expect-revision", 1)
    assert r.returncode == 0, r.stderr
    saved = read(tmp_path)
    assert saved["resource"]["content"] == "Review facts with Linh.\nPublish monthly.\n"
    assert saved["resource"]["origin"] == NEW
    assert saved["resource"]["known_uses"] == ["consumer-a"]
    assert saved["resource"]["origin_update"]["comparison"]["old_origin"] == OLD
    assert saved["resource"]["origin_update"]["review"] == request["review"]
    assert read(tmp_path, "history")[0]["resource"]["content"] == CUSTOM
    assert operation(tmp_path, "update", request, "--expect-revision", 2).returncode != 0
    assert read(tmp_path)["revision"] == 2


def test_semantic_conflict_allows_independent_change_but_preserves_basis_and_valid_prior(tmp_path):
    # Distinct lines still conflict: retention duration cannot be shorter than the reporting interval.
    old = dict(OLD, snapshot="Keep evidence 30 days.\nPublish weekly.\nTitle: report.\n")
    candidate = dict(NEW, snapshot="Keep evidence 3 days.\nPublish weekly.\nTitle: facts.\n")
    custom = "Keep evidence 30 days.\nPublish monthly.\nTitle: report.\n"
    assert save(tmp_path, draft(origin=old, content=custom)).returncode == 0
    comparison = json.loads(operation(tmp_path, "compare", candidate).stdout)
    request = plan(tmp_path, candidate=candidate, comparison_token=comparison["token"], outcome="partial",
                   content="Keep evidence 30 days.\nPublish monthly.\nTitle: facts.\n")
    request["review"].update(compatible_changes=["Title is independent of retention"],
                             conflicts=["3-day retention loses evidence before monthly publication"],
                             checks=["30-day retention remains valid for the monthly report"])
    r = operation(tmp_path, "update", request, "--expect-revision", 1)
    assert r.returncode == 0, r.stderr
    current = read(tmp_path)
    assert current["resource"]["content"] == request["content"]
    assert current["resource"]["origin"] == old
    assert current["resource"]["origin_update"]["comparison"]["candidate"] == candidate
    assert current["warnings"] and current["resource"]["origin_update"]["outcome"] == "partial"


def test_missing_basis_cannot_claim_complete_merge_and_can_record_blocker_without_losing_content(tmp_path):
    assert save(tmp_path, draft(origin=None, content=CUSTOM)).returncode == 0
    request = plan(tmp_path)
    assert operation(tmp_path, "update", request, "--expect-revision", 1).returncode != 0
    assert read(tmp_path)["revision"] == 1
    request.update(outcome="blocked", content=CUSTOM)
    request["review"].update(compatible_changes=[], unknowns=["Obtain old origin from owner"],
                             prior_selection_valid=False)
    r = operation(tmp_path, "update", request, "--expect-revision", 1)
    assert r.returncode == 0, r.stderr
    saved = read(tmp_path)
    assert saved["resource"]["origin"] is None and saved["resource"]["content"] == CUSTOM
    assert saved["consumption"].startswith("Blocked")
    assert saved["resource"]["origin_update"]["comparison"]["basis"] == "missing"


def test_parent_replacement_selects_exact_new_children_and_carry_forward_checks_target_and_history(tmp_path):
    old = dict(OLD, snapshot="Assembly: weekly reports\nChild review: check facts.\nChild delivery: email.\n")
    custom = "Assembly: weekly reports\nChild review: Linh checks facts.\nChild delivery: email.\n"
    new = dict(NEW, snapshot="Assembly: monthly reports\nChild accuracy: check facts.\nChild delivery: archive.\n")
    assert save(tmp_path, draft(origin=old, content=custom)).returncode == 0
    comparison = json.loads(operation(tmp_path, "compare", new).stdout)
    request = plan(tmp_path, candidate=new, comparison_token=comparison["token"], mode="replace-parent", content=custom)
    assert operation(tmp_path, "update", request, "--expect-revision", 1).returncode != 0
    request["content"] = new["snapshot"]
    r = operation(tmp_path, "update", request, "--expect-revision", 1)
    assert r.returncode == 0, r.stderr
    assert read(tmp_path)["resource"]["content"] == new["snapshot"]
    assert "Linh" in read(tmp_path, "history")[0]["resource"]["content"]
    comparison = json.loads(operation(tmp_path, "compare", new).stdout)
    request.update(mode="carry-forward", comparison_token=comparison["token"],
                   content=new["snapshot"].replace("check facts", "Linh checks facts"),
                   carry_forward={"from_revision": 1, "customization": "Linh checks facts.",
                                  "target": "Child review", "contract_check": "Linh is still the authorized fact reviewer."})
    assert operation(tmp_path, "update", request, "--expect-revision", 2).returncode != 0
    request["carry_forward"]["target"] = "Child accuracy"
    request["carry_forward"]["from_revision"] = 999
    assert operation(tmp_path, "update", request, "--expect-revision", 2).returncode != 0
    request["carry_forward"]["from_revision"] = 1
    r = operation(tmp_path, "update", request, "--expect-revision", 2)
    assert r.returncode == 0, r.stderr
    result = read(tmp_path)["resource"]
    assert "Linh checks facts." in result["content"] and "archive" in result["content"]
    assert "email" not in result["content"]
    assert result["origin"] == new
    assert result["origin_update"]["carry_forward"]["from_revision"] == 1
    assert len(read(tmp_path, "history")) == 3


def test_candidate_change_or_missing_authority_cannot_use_a_checked_plan(tmp_path):
    assert save(tmp_path, draft(origin=OLD, content=CUSTOM)).returncode == 0
    request = plan(tmp_path)
    altered = dict(request, candidate=dict(NEW, snapshot="Publish without review."))
    assert operation(tmp_path, "update", altered, "--expect-revision", 1).returncode != 0
    request["decision"] = dict(request["decision"], authority="")
    assert operation(tmp_path, "update", request, "--expect-revision", 1).returncode != 0
    assert read(tmp_path)["revision"] == 1
    assert read(tmp_path)["resource"]["content"] == CUSTOM


def test_two_checked_updates_serialize_and_preserve_the_losing_work_for_reconciliation(tmp_path):
    import subprocess
    import sys
    assert save(tmp_path, draft(origin=OLD, content=CUSTOM)).returncode == 0
    request = plan(tmp_path)
    processes = []
    for name in ("a", "b"):
        path = tmp_path / (name + ".json")
        path.write_text(json.dumps(dict(request, continuation=f"Resume editor {name}")))
        processes.append(subprocess.Popen([sys.executable, "-I", str(CLI), "--store", str(tmp_path / "library.sqlite3"),
                                          "update", "report-rule", "--input", str(path), "--expect-revision", "1"],
                                         text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    outputs = [(p.communicate(), p.returncode) for p in processes]
    assert sorted(code for _, code in outputs) == [0, 2]
    history = read(tmp_path, "history")
    assert len(history) == 2 and history[0]["resource"]["content"] == CUSTOM
    assert history[1]["resource"]["origin_update"]["comparison"]["customization"] == CUSTOM
    assert "reconcile" in next(stderr for (_, stderr), code in outputs if code == 2)


def test_update_failure_does_not_create_or_damage_store(tmp_path):
    missing = tmp_path / "missing"
    missing.mkdir()
    assert operation(missing, "update", {}, "--expect-revision", 1).returncode != 0
    assert not (missing / "library.sqlite3").exists()
    corrupt = tmp_path / "library.sqlite3"
    corrupt.write_bytes(b"unreadable store")
    r = operation(tmp_path, "update", {}, "--expect-revision", 1)
    assert r.returncode != 0 and not r.stdout
    assert corrupt.read_bytes() == b"unreadable store"


def test_legacy_extension_metadata_does_not_break_readback_or_lose_history(tmp_path):
    r = save(tmp_path, draft(origin=OLD, content=CUSTOM, origin_update="legacy opaque note"))
    assert r.returncode == 0, r.stderr
    assert read(tmp_path)["resource"]["origin_update"] == "legacy opaque note"
    r = operation(tmp_path, "update", plan(tmp_path), "--expect-revision", 1)
    assert r.returncode == 0, r.stderr
    assert read(tmp_path, "history")[0]["resource"]["origin_update"] == "legacy opaque note"


def excluded_saved_resource(tmp_path, content=CUSTOM, origin=OLD):
    from test_library_selection import change, selection
    assert save(tmp_path, draft(origin=origin, content=content, known_uses=["consumer-a", "consumer-b"])).returncode == 0
    for name in ("consumer-a", "consumer-b"):
        (tmp_path / name).write_text("Applied prior policy; adoption is separate.\n")
    assert change(tmp_path, "disable", 0, source="saved", id="report-rule").returncode == 0
    return selection(tmp_path, source="saved", id="report-rule")["record"]


def assert_excluded_update(tmp_path, original_exclusion, revision, content):
    from test_library_selection import selection
    current = read(tmp_path)
    assert current["revision"] == revision and current["resource"]["content"] == content
    assert current["resource"]["known_uses"] == ["consumer-a", "consumer-b"]
    state = selection(tmp_path, source="saved", id="report-rule")
    assert not state["enabled"] and not state["effective"] and state["revision"] == 1
    assert state["record"] == original_exclusion
    assert current["selection"] == state
    assert state["current_snapshot"]["revision"] == revision
    assert selection(tmp_path, source="saved", id="report-rule", history=True) == [original_exclusion]
    matches = run(CLI, "--store", tmp_path / "library.sqlite3", "search", "report-rule")
    assert matches.returncode == 0, matches.stderr
    assert json.loads(matches.stdout)["matches"] == []
    inspected = run(CLI, "--store", tmp_path / "library.sqlite3", "search", "report-rule", "--include-disabled")
    assert json.loads(inspected.stdout)["matches"][0]["enabled"] is False
    for name in ("consumer-a", "consumer-b"):
        assert (tmp_path / name).read_text() == "Applied prior policy; adoption is separate.\n"


def restore_updated_resource(tmp_path, original_exclusion, revision):
    from test_library_selection import change, selection
    before = read(tmp_path, "history")
    restored = change(tmp_path, "restore", 1, source="saved", id="report-rule")
    assert restored.returncode == 0, restored.stderr
    records = selection(tmp_path, source="saved", id="report-rule", history=True)
    assert records[0] == original_exclusion
    assert [r["enabled"] for r in records] == [False, True]
    assert records[1]["snapshot"]["revision"] == revision
    assert read(tmp_path, "history") == before  # Restoration creates no content revision.
    assert read(tmp_path)["selection"]["effective"] is True
    matches = run(CLI, "--store", tmp_path / "library.sqlite3", "search", "report-rule")
    assert json.loads(matches.stdout)["matches"][0]["revision"] == revision
    assert change(tmp_path, "restore", 2, source="saved", id="report-rule").returncode != 0
    assert selection(tmp_path, source="saved", id="report-rule", history=True) == records
    for name in ("consumer-a", "consumer-b"):
        assert (tmp_path / name).read_text() == "Applied prior policy; adoption is separate.\n"


def test_disabled_saved_resource_stays_excluded_through_compatible_and_partial_origin_updates(tmp_path):
    exclusion = excluded_saved_resource(tmp_path)
    request = plan(tmp_path)
    result = operation(tmp_path, "update", request, "--expect-revision", 1)
    assert result.returncode == 0, result.stderr
    assert_excluded_update(tmp_path, exclusion, 2, request["content"])
    assert read(tmp_path)["resource"]["origin"] == NEW
    candidate = dict(NEW, revision="v3", snapshot="Skip fact review.\nPublish monthly.\nTitle: facts.\n")
    comparison = json.loads(operation(tmp_path, "compare", candidate).stdout)
    request.update(candidate=candidate, comparison_token=comparison["token"], outcome="partial",
                   content="Review facts with Linh.\nPublish monthly.\nTitle: facts.\n")
    request["review"].update(compatible_changes=["Title is independent of required fact review"],
                             conflicts=["Skipping review contradicts fact review requirement"],
                             checks=["Linh still reviews facts; title does not change that duty"])
    result = operation(tmp_path, "update", request, "--expect-revision", 2)
    assert result.returncode == 0, result.stderr
    assert_excluded_update(tmp_path, exclusion, 3, request["content"])
    current = read(tmp_path)["resource"]
    assert current["origin"] == NEW and current["origin_update"]["outcome"] == "partial"
    assert current["origin_update"]["comparison"]["candidate"] == candidate
    assert read(tmp_path, "history")[0]["resource"] == exclusion["snapshot"]["resource"]
    restore_updated_resource(tmp_path, exclusion, 3)


def test_disabled_parent_replacement_and_requested_carry_forward_preserve_exclusion(tmp_path):
    exclusion = excluded_saved_resource(tmp_path)
    candidate = dict(NEW, snapshot="Child verification: Review facts.\nChild delivery: Archive report.\n")
    comparison = json.loads(operation(tmp_path, "compare", candidate).stdout)
    request = plan(tmp_path, candidate=candidate, comparison_token=comparison["token"],
                   mode="replace-parent", content=candidate["snapshot"])
    result = operation(tmp_path, "update", request, "--expect-revision", 1)
    assert result.returncode == 0, result.stderr
    assert_excluded_update(tmp_path, exclusion, 2, candidate["snapshot"])
    assert "Linh" not in read(tmp_path)["resource"]["content"]
    assert read(tmp_path, "history")[0]["resource"]["content"] == CUSTOM
    comparison = json.loads(operation(tmp_path, "compare", candidate).stdout)
    request.update(mode="carry-forward", comparison_token=comparison["token"],
                   content="Child verification: Review facts with Linh.\nChild delivery: Archive report.\n",
                   carry_forward=dict(from_revision=1, customization="Review facts with Linh.",
                                      target="Child verification", contract_check="Linh is authorized to verify facts."))
    result = operation(tmp_path, "update", request, "--expect-revision", 2)
    assert result.returncode == 0, result.stderr
    assert_excluded_update(tmp_path, exclusion, 3, request["content"])
    assert read(tmp_path)["resource"]["origin"] == candidate
    assert read(tmp_path)["resource"]["origin_update"]["carry_forward"] == request["carry_forward"]
    restore_updated_resource(tmp_path, exclusion, 3)
