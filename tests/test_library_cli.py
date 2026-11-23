"""Library operations through the public subprocess seam, with disposable stores."""
import json
import os
import subprocess

from conftest import ROOT, row, run, write_kit

CLI = ROOT / "kit/scripts/library"


def draft(**changes):
    value = dict(id="report-rule", name="Report rule", kind="rule", owner="report author",
                 scope="personal", content="Name unresolved facts before publishing.",
                 sources=[], conditions=[], gaps=["Accuracy review not yet exercised"],
                 origin=None, evidence=[], continuation="Read a representative report next.",
                 decision={"authority": "User requested this personal save", "rationale": "Reuse across reports",
                           "methods": ["writing-for-agents"], "standards": ["source attribution"]})
    value.update(changes)
    return value


def save(tmp_path, value, expected=0, store=None):
    payload = tmp_path / "input.json"
    payload.write_text(json.dumps(value), encoding="utf-8")
    return run(CLI, "--store", store or tmp_path / "library.sqlite3", "save", "--input", payload,
               "--expect-revision", expected)


def retrieve(match):
    env = dict(os.environ, PATH=os.pathsep.join((str(CLI.parent), os.environ["PATH"])))
    command = match["retrieve"]
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    assert result.returncode == 0, f"{command}\n{result.stderr}"
    return result.stdout


def test_unfinished_personal_rule_is_saved_with_attribution_and_continuation(tmp_path):
    r = save(tmp_path, draft())
    assert r.returncode == 0, r.stderr
    saved = json.loads(r.stdout)
    assert saved["revision"] == 1 and saved["warnings"]
    r = run(CLI, "--store", tmp_path / "library.sqlite3", "show", "report-rule")
    assert r.returncode == 0, r.stderr
    actual = json.loads(r.stdout)
    assert actual["resource"]["owner"] == "report author"
    assert actual["resource"]["gaps"] == ["Accuracy review not yet exercised"]
    assert actual["resource"]["continuation"] == "Read a representative report next."
    assert actual["resource"]["sources"] == [] and actual["resource"]["origin"] is None
    assert actual["consumption"] == "Requires checking conditions and gaps; saving is not adoption."


def test_edit_preserves_origin_history_and_rejects_stale_retries(tmp_path):
    origin = {"reference": "kit:B01", "revision": "source-1", "snapshot": "Original instruction"}
    assert save(tmp_path, draft(origin=origin)).returncode == 0
    edited = draft(content="Check unresolved facts and name their owner.", origin=origin)
    r = save(tmp_path, edited, expected=1)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["revision"] == 2
    stale = save(tmp_path, draft(content="Stale overwrite", origin=origin), expected=1)
    assert stale.returncode != 0
    current = json.loads(run(CLI, "--store", tmp_path / "library.sqlite3", "show", "report-rule").stdout)
    assert current["resource"]["content"] == edited["content"]
    history = run(CLI, "--store", tmp_path / "library.sqlite3", "history", "report-rule")
    assert history.returncode == 0, history.stderr
    records = json.loads(history.stdout)
    assert [r["revision"] for r in records] == [1, 2]
    assert records[0]["resource"]["content"] == draft()["content"]
    assert records[1]["resource"]["origin"] == origin


def test_invalid_operation_cannot_replace_valid_resource_or_create_a_store(tmp_path):
    for key, value in (("owner", ""), ("scope", "project"), ("decision", {}), ("id", "../elsewhere"),
                       ("kind", "unknown"), ("sources", [{"reference": "source", "certainty": "proven"}])):
        target = tmp_path / (key + ".sqlite3")
        r = save(tmp_path, draft(**{key: value}), store=target)
        assert r.returncode != 0, (key, r.stdout)
        assert not target.exists()
    assert save(tmp_path, draft()).returncode == 0
    for change in ({"scope": "project:/work/project-a"}, {"owner": "someone else"},
                   {"origin": {"reference": "made-up", "revision": "2", "snapshot": "different"}}):
        r = save(tmp_path, draft(**change), expected=1)
        assert r.returncode != 0, r.stdout
    result = json.loads(run(CLI, "--store", tmp_path / "library.sqlite3", "show", "report-rule").stdout)
    assert result["revision"] == 1 and result["resource"]["scope"] == "personal"


def test_focused_search_returns_supplied_and_personal_material_without_creating_store(tmp_path):
    target = tmp_path / "library.sqlite3"
    r = run(CLI, "--store", target, "search", "hook")
    assert r.returncode == 0, r.stderr
    hits = json.loads(r.stdout)["matches"]
    assert hits and all(h["origin"] == "supplied" for h in hits)
    assert not target.exists()
    assert save(tmp_path, draft(name="Quarterly accuracy", content="Track evidence before release.")).returncode == 0
    r = run(CLI, "--store", target, "search", "quarterly")
    hits = json.loads(r.stdout)["matches"]
    assert len(hits) == 1 and hits[0]["id"] == "report-rule" and hits[0]["origin"] == "saved"
    assert hits[0]["owner"] == "report author" and hits[0]["scope"] == "personal"
    r = run(CLI, "--store", target, "search", "")
    assert r.returncode != 0


def test_search_retrieve_uses_saved_store_with_spaces(tmp_path):
    target = tmp_path / "my library.db"
    resource = draft()
    saved = save(tmp_path, resource, store=target)
    assert saved.returncode == 0, saved.stderr

    result = run(CLI, "--store", target, "search", resource["id"])
    assert result.returncode == 0, result.stderr
    match, = json.loads(result.stdout)["matches"]
    assert match["origin"] == "saved"
    retrieved = json.loads(retrieve(match))
    assert retrieved["resource"] == resource
    assert retrieved["revision"] == match["revision"]


def test_search_retrieve_uses_selected_catalog(tmp_path):
    piece = row("H99", "H", "Custom catalog hook", detail="Only in the selected catalog.")
    kit = write_kit(tmp_path / "custom kit's catalog", [piece])
    (kit / "rules.csv").write_text("id,rule,source,certainty\n", encoding="utf-8")

    result = run(CLI, "--store", tmp_path / "absent.db", "search", piece["id"], "--kit-dir", kit)
    assert result.returncode == 0, result.stderr
    match, = json.loads(result.stdout)["matches"]
    assert match["origin"] == "supplied" and match["id"] == piece["id"]
    output = retrieve(match).splitlines()
    assert f"id: {piece['id']}" in output
    assert f"name: {piece['name']}" in output
    assert f"detail: {piece['detail']}" in output


def test_concurrent_edits_have_one_winner_and_no_lost_history(tmp_path):
    import sys
    assert save(tmp_path, draft()).returncode == 0
    writers = []
    for label in ("Editor A", "Editor B"):
        payload = tmp_path / (label + ".json")
        payload.write_text(json.dumps(draft(content=label)), encoding="utf-8")
        writers.append(subprocess.Popen([sys.executable, "-I", str(CLI), "--store", str(tmp_path / "library.sqlite3"),
                                         "save", "--input", str(payload), "--expect-revision", "1"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    results = [(p.communicate(), p.returncode) for p in writers]
    assert sorted(code for _, code in results) == [0, 2]
    winner = json.loads(next(out for (out, err), code in results if code == 0))
    history = json.loads(run(CLI, "--store", tmp_path / "library.sqlite3", "history", "report-rule").stdout)
    assert [r["revision"] for r in history] == [1, 2]
    assert history[-1]["resource"]["content"] == winner["resource"]["content"]


def test_project_workflow_roundtrip_preserves_other_consumers_and_serialized_text(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    (b / "consumer.md").write_text("Unchanged consumer guidance\n")
    content = 'Check "quoted" input; preserve Tiếng Việt.\nDo not evaluate $(touch surprise) or `commands`.\n'
    value = draft(kind="workflow", scope=f"project:{a}", content=content,
                  sources=[{"reference": "user request", "certainty": "stated"}])
    r = save(tmp_path, value, store=a / "resources.sqlite3")
    assert r.returncode == 0, r.stderr
    r = run(CLI, "--store", a / "resources.sqlite3", "show", "report-rule")
    assert json.loads(r.stdout)["resource"]["content"] == content
    assert (b / "consumer.md").read_text() == "Unchanged consumer guidance\n"
    assert sorted(p.name for p in a.iterdir()) == ["resources.sqlite3"]


def test_persistence_failure_and_unknown_store_do_not_claim_save(tmp_path):
    target = tmp_path / "corrupt.sqlite3"
    target.write_bytes(b"not a database")
    r = save(tmp_path, draft(), store=target)
    assert r.returncode != 0 and not r.stdout
    assert target.read_bytes() == b"not a database"
    assert run(CLI, "--store", target, "search", "hook").returncode != 0
    missing = tmp_path / "missing" / "library.sqlite3"
    r = save(tmp_path, draft(), store=missing)
    assert r.returncode != 0 and not r.stdout and not missing.exists()
    r = run(CLI, "--store", tmp_path / "absent.sqlite3", "show", "report-rule")
    assert r.returncode != 0 and not (tmp_path / "absent.sqlite3").exists()


def test_ambiguous_duplicate_json_fields_are_rejected_before_effects(tmp_path):
    payload = tmp_path / "ambiguous.json"
    payload.write_text(json.dumps(draft()).replace('"scope": "personal"',
                                                  '"scope": "personal", "scope": "project:/other"'))
    target = tmp_path / "library.sqlite3"
    r = run(CLI, "--store", target, "save", "--input", payload, "--expect-revision", "0")
    assert r.returncode != 0 and not target.exists(), r.stdout


def test_edit_of_missing_store_does_not_create_an_empty_store(tmp_path):
    target = tmp_path / "missing.sqlite3"
    r = save(tmp_path, draft(), expected=1, store=target)
    assert r.returncode != 0 and not target.exists(), r.stderr


def test_save_fails_when_store_symlink_target_goes_missing(tmp_path):
    target = tmp_path / "library.sqlite3"
    created = save(tmp_path, draft(), store=target)
    assert created.returncode == 0, created.stderr
    link = tmp_path / "store-link"
    link.symlink_to(target.name)
    target.rename(tmp_path / "offline.sqlite3")

    failed = save(tmp_path, draft(id="another-rule"), store=link)
    assert failed.returncode == 2, failed.stdout
    assert not failed.stdout
    assert f"Store symlink target is missing: {link}" in failed.stderr
    assert link.is_symlink() and not target.exists()
