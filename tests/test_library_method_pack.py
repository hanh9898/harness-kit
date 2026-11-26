"""Exercise optional method discovery and selection through the public CLI."""

import csv
import hashlib
import json
import shutil
import sqlite3
from contextlib import closing

import pytest

from conftest import ROOT, run
from test_library_read_no_write import NO_WRITE_UNAVAILABLE, files, no_write_host
from test_library_selection import CLI, decision, initialize_empty_store


PACK = ROOT / "packs/verification-methods"
CORE = ROOT / "kit"
CHECK = ROOT / "tools/check_method_pack.py"
NODE = "Verification & feedback"
BLIND = "opt-blind-comparison"
PREMISE = "opt-shared-premise-probe"
RESYNC = "opt-formal-model-resync"
EVAL = ("compare-variants", "subjective-grading")
FAILED = ("repeated-same-gate", "shared-assumption")
MODEL = ("formal-model-exists", "covered-code-changed")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


@pytest.fixture
def bound(tmp_path):
    store, pack, core, binding = (tmp_path / name for name in ("library.db", "pack", "core", "binding.json"))
    initialize_empty_store(store)
    shutil.copytree(PACK, pack)
    shutil.copytree(CORE, core, ignore=shutil.ignore_patterns("__pycache__"))
    stat = store.stat()
    write_json(binding, dict(
        schema=1, owner="Report author", scope="personal",
        store=dict(path=str(store), device=stat.st_dev, inode=stat.st_ino),
        catalog=dict(path=str(core), files={name: sha(core / name) for name in (
            "legos.csv", "rules.csv", "piece-aliases.csv")}),
        pack=dict(path=str(pack), index_sha256=sha(pack / "index.json")),
    ))
    return store, pack, core, binding


@pytest.fixture
def ready(bound, no_write_host):
    if not no_write_host:
        pytest.skip("Ready reads need a qualified no-write SQLite host")
    return bound


def call(bound, *args, with_binding=True):
    store, _, _, binding = bound
    flags = ("--pack-binding", binding) if with_binding else ()
    return run(CLI, "--store", store, *flags, *args)


def result(response):
    assert (response.returncode, response.stderr) == (0, ""), response.stderr
    return json.loads(response.stdout)


def blocked(response, reason):
    assert (response.returncode, response.stdout) == (2, ""), response.stderr
    assert reason in response.stderr


def discover(bound, facts=(), node=NODE, binding=True):
    return call(bound, "pack-discover", "--node", node,
                *(part for fact in facts for part in ("--fact", fact)), with_binding=binding)


def update_binding(bound, change):
    path = bound[3]
    value = json.loads(path.read_bytes())
    change(value)
    write_json(path, value)


def update_index(bound, change):
    path = bound[1] / "index.json"
    value = json.loads(path.read_bytes())
    change(value)
    write_json(path, value)
    update_binding(bound, lambda binding: binding["pack"].update(index_sha256=sha(path)))


def test_repo_only_without_opt_in_does_not_touch_any_sources(bound):
    store, pack, core, binding = bound
    store.unlink()
    shutil.rmtree(pack)
    shutil.rmtree(core)
    binding.unlink()
    before = files(store.parent)
    assert result(discover(bound, binding=False)) == dict(total=0, matches=[], groups=[])
    assert result(discover(bound, EVAL, binding=False))["total"] == 0
    assert files(store.parent) == before


@pytest.mark.parametrize(("node", "facts", "expected"), [
    (NODE, (), set()),
    (NODE, EVAL + FAILED, {BLIND, PREMISE}),
    (NODE, EVAL + ("fully-objective",), set()),
    (NODE, EVAL, {BLIND}),
    (NODE, ("repeated-same-gate",), set()),
    (NODE, MODEL, {RESYNC}),
    ("Automation", MODEL, set()),
    (NODE, ("formal-model-exists",), set()),
], ids=["R2-opted-in-repo-only", "E1-eval", "E2-objective", "E3-confirmed-facts",
        "E4-no-premise", "B1-model-drift", "B2-wrong-node", "B3-no-code-change"])
def test_prototype_cases(ready, node, facts, expected):
    payload = result(discover(ready, facts, node))
    assert payload["total"] == len(expected)
    assert {item["id"] for item in payload["matches"]} == expected
    assert payload["groups"] == []


def test_browse_views_share_ids_and_open_only_selected_body(ready):
    _, pack, _, _ = ready
    (pack / "guidance" / f"{RESYNC}.md").write_text("Changed but not opened.")
    individual = result(call(ready, "pack-browse"))
    grouped = result(call(ready, "pack-browse", "--view", "scenarios"))
    assert individual["matches"] == grouped["matches"]
    assert individual["groups"] == []
    assert {group["id"]: group["ids"] for group in grouped["groups"]} == {
        "eval-comparison": [BLIND, PREMISE], "formal-model-checking": [RESYNC]}
    subset = result(call(ready, "pack-browse", "--view", "scenarios", "--scenario", "eval-comparison"))
    assert [hit["id"] for hit in subset["matches"]] == [BLIND, PREMISE]
    filtered = result(call(ready, "pack-discover", "--node", NODE, "--fact", EVAL[0], "--fact", EVAL[1],
                           "--view", "scenarios"))
    assert filtered["groups"] == [dict(id="eval-comparison", name="Eval comparison", ids=[BLIND])]
    assert all(set(hit) == {"id", "name", "summary", "needed_when", "kind"} for hit in grouped["matches"])
    opened = result(call(ready, "pack-show", BLIND))
    body = pack / "guidance" / f"{BLIND}.md"
    assert opened["content"] == body.read_text()
    assert opened["body_sha256"] == sha(body)
    assert opened["provenance"] == json.loads((pack / "index.json").read_bytes())["items"][BLIND]["provenance"]
    blocked(call(ready, "pack-show", RESYNC), "Pinned method body digest")
    blocked(call(ready, "pack-show", "../index.json"), "Unknown method ID")
    blocked(call(ready, "pack-browse", "--scenario", "unknown"), "Unknown method scenario")
    assert result(call(ready, "search", BLIND, with_binding=False))["total"] == 0


def test_pack_reads_preserve_sqlite_and_sidecar_bytes(bound, no_write_host):
    store = bound[0]
    commands = [("pack-discover", "--node", NODE), ("pack-browse",), ("pack-show", BLIND),
                ("selection", BLIND, "--source", "supplied"),
                ("selection-history", BLIND, "--source", "supplied")]
    before = files(store.parent)
    for cmd in commands:
        response = call(bound, *cmd)
        if no_write_host:
            result(response)
        else:
            blocked(response, NO_WRITE_UNAVAILABLE)
        assert files(store.parent) == before

    with closing(sqlite3.connect(store)) as db:
        assert db.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
        db.execute("CREATE TABLE active_writer (id INTEGER)")
        db.commit()
        before = files(store.parent)
        assert {store.name + "-wal", store.name + "-shm"} <= before.keys()
        for cmd in commands:
            blocked(call(bound, *cmd), "Store is unreadable")
            assert files(store.parent) == before

    store.unlink()
    before = files(store.parent)
    for cmd in commands:
        blocked(call(bound, *cmd), "Store is missing")
        assert files(store.parent) == before


def test_exact_scoped_grants_disable_and_restore_both_views(ready):
    store = ready[0]
    request = decision(store.parent)
    source = ("--source", "supplied")
    selection = ("selection", BLIND, *source)
    assert result(call(ready, *selection))["revision"] == 0
    disable = ("disable", BLIND, *source, "--input", request, "--expect-selection-revision", "0")
    blocked(call(ready, *disable), "require a matching write grant")
    grant_args = ("grant-write", "disable", BLIND, *source, "--input", request, "--expect-revision", "0",
                  "--ttl-seconds", "60")
    grant = result(call(ready, *grant_args))["write_grant"]
    update_index(ready, lambda index: index["items"][BLIND].update(summary="Use a shared masked rubric."))
    blocked(call(ready, *disable, "--write-grant", grant), "No current write grant")
    grant = result(call(ready, *grant_args))["write_grant"]
    state = result(call(ready, *disable, "--write-grant", grant))
    assert (state["available"], state["effective"], state["revision"]) == (True, False, 1)
    assert result(discover(ready, EVAL + FAILED))["total"] == 1
    assert result(call(ready, "pack-browse", "--view", "scenarios"))["groups"][0]["ids"] == [PREMISE]
    blocked(call(ready, "pack-show", BLIND), "excluded")
    update_index(ready, lambda index: index["items"][BLIND].update(summary="Compare masked results using one rubric."))
    assert not result(call(ready, *selection))["effective"]

    before = ready[3].read_bytes()
    update_binding(ready, lambda binding: binding.update(owner="Different owner"))
    blocked(call(ready, *selection), "owner or scope")
    blocked(discover(ready, EVAL), "owner or scope")
    ready[3].write_bytes(before)
    grant = result(call(ready, "grant-write", "restore", BLIND, *source, "--input", request,
                        "--expect-revision", "1", "--ttl-seconds", "60"))["write_grant"]
    state = result(call(ready, "restore", BLIND, *source, "--input", request,
                        "--expect-selection-revision", "1", "--write-grant", grant))
    assert (state["effective"], state["revision"]) == (True, 2)
    history = result(call(ready, "selection-history", BLIND, *source))
    assert [entry["action"] for entry in history] == ["disable", "restore"]


def test_retired_method_history_remains_readable_without_reopening_method(ready):
    store = ready[0]
    source = ("--source", "supplied")
    request = decision(store.parent)
    grant = result(call(ready, "grant-write", "disable", BLIND, *source, "--input", request,
                        "--expect-revision", "0", "--ttl-seconds", "60"))["write_grant"]
    result(call(ready, "disable", BLIND, *source, "--input", request,
                "--expect-selection-revision", "0", "--write-grant", grant))
    cmd = ("selection-history", BLIND, *source)
    history = result(call(ready, *cmd))

    def retire(index):
        del index["items"][BLIND]
        index["scenarios"]["eval-comparison"]["ids"].remove(BLIND)

    update_index(ready, retire)
    before = files(store.parent)
    assert result(call(ready, *cmd)) == history
    assert files(store.parent) == before
    blocked(call(ready, "pack-show", BLIND), "Unknown method ID")
    blocked(call(ready, "grant-write", "restore", BLIND, *source, "--input", request,
                 "--expect-revision", "1", "--ttl-seconds", "60"), "Unknown method ID")
    blocked(call(ready, "selection-history", "opt-unknown", *source), "Unknown method ID")
    update_binding(ready, lambda binding: binding.update(owner="Different owner"))
    blocked(call(ready, *cmd), "owner or scope")


def test_moved_method_preserves_the_supplied_selection_history(ready):
    store, _, core, _ = ready
    source = ("--source", "supplied")
    request = decision(store.parent)
    path = core / "legos.csv"
    original = path.read_bytes()
    with path.open(encoding="utf-8", newline="") as stream:
        rows = csv.DictReader(stream)
        piece = next(rows)
        fields = rows.fieldnames
    with path.open("a", encoding="utf-8", newline="") as stream:
        csv.DictWriter(stream, fields).writerow(dict(piece, id=BLIND))
    legacy = result(call(ready, "disable", BLIND, *source, "--kit-dir", core, "--input", request,
                         "--expect-selection-revision", "0", with_binding=False))["record"]
    path.write_bytes(original)

    cmd = ("selection-history", BLIND, *source)
    assert result(call(ready, *cmd)) == [legacy]
    grant = result(call(ready, "grant-write", "restore", BLIND, *source, "--input", request,
                        "--expect-revision", "1", "--ttl-seconds", "60"))["write_grant"]
    current = result(call(ready, "restore", BLIND, *source, "--input", request,
                          "--expect-selection-revision", "1", "--write-grant", grant))["record"]
    assert [record["snapshot"]["kind"] for record in (legacy, current)] == ["piece", "method"]
    assert result(call(ready, *cmd)) == [legacy, current]


@pytest.mark.parametrize(("variant", "diagnostic"), [
    ("index", "Pinned method pack index digest"),
    ("core", "Pinned core catalog digest"),
    ("collision", "collide with core catalog"),
    ("alias-collision", "collide with core catalog"),
    ("identity", "wrong-identity"),
    ("binding-duplicate", "duplicate JSON field"),
    ("binding-extra", "must have exactly these fields"),
    ("fact", "distinct supported values"),
    ("scenario", "distinct supported values"),
    ("source", "Invalid pinned provenance"),
    ("symlink", "symbolic links"),
])
def test_invalid_binding_never_falls_back_or_writes(bound, variant, diagnostic):
    store, pack, core, binding = bound
    if variant == "index":
        (pack / "index.json").write_bytes(b"{}")
    elif variant == "core":
        (core / "legos.csv").write_bytes(b"changed")
    elif variant in ("collision", "alias-collision"):
        path = core / ("legos.csv" if variant == "collision" else "piece-aliases.csv")
        with path.open("a", encoding="utf-8") as stream:
            stream.write(f"{BLIND},H,name,summary,trigger,instruction-file,stated,source,detail\n"
                         if variant == "collision" else f"Z99,{BLIND}\n")
        update_binding(bound, lambda b: b["catalog"]["files"].update({path.name: sha(path)}))
    elif variant == "identity":
        store.rename(store.with_suffix(".prior"))
        initialize_empty_store(store)
    elif variant == "binding-duplicate":
        binding.write_bytes(b'{"schema": 1, "schema": 1}')
    elif variant == "binding-extra":
        update_binding(bound, lambda b: b.update(unknown=True))
    elif variant == "fact":
        update_index(bound, lambda index: index["items"][BLIND]["all"].append("unknown-fact"))
    elif variant == "scenario":
        update_index(bound, lambda index: index["scenarios"]["eval-comparison"]["ids"].append("unknown-id"))
    elif variant == "source":
        update_index(bound, lambda index: index["items"][BLIND]["provenance"].update(url="http://example.com"))
    elif variant == "symlink":
        index = pack / "index.json"
        index.unlink()
        index.symlink_to(PACK / "index.json")
    before = files(store.parent)
    blocked(discover(bound, EVAL), diagnostic)
    assert result(discover(bound, EVAL, binding=False))["total"] == 0
    assert files(store.parent) == before


@pytest.mark.parametrize(("variant", "diagnostic"), [
    ("unexpected", "file whitelist"),
    ("body", "/Users/"),
    ("summary", "/Users/"),
    ("alternate-source", "reviewed provenance allowlist"),
    ("collision", "collide with core catalog"),
])
def test_pack_checker_narrows_boundary_exception(bound, variant, diagnostic):
    _, pack, core, _ = bound
    if variant == "unexpected":
        (pack / "extra.md").touch()
    elif variant == "body":
        body = pack / "guidance" / f"{BLIND}.md"
        body.write_text("/Users/test/example\n")
        update_index(bound, lambda index: index["items"][BLIND].update(body_sha256=sha(body)))
    elif variant == "summary":
        update_index(bound, lambda index: index["items"][BLIND].update(summary="/Users/test/example"))
    elif variant == "alternate-source":
        update_index(bound, lambda index: index["items"][BLIND]["provenance"].update(
            url="https://github.com/example/collection/blob/" + "f" * 40 + "/skills/eval.md"))
    else:
        with (core / "rules.csv").open("a", encoding="utf-8") as stream:
            stream.write(f"{BLIND},topic,rule,source,stated,check,\n")
    checked = run(CHECK, "--pack", pack, "--kit-dir", core)
    assert checked.returncode == 1
    assert diagnostic in checked.stdout + checked.stderr


@pytest.mark.parametrize("layout", ["reordered", "no-final-newline"])
def test_pack_checker_accepts_valid_catalog_layouts(bound, layout):
    _, pack, core, _ = bound
    path = core / "legos.csv"
    if layout == "reordered":
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.reader(stream))
        with path.open("w", encoding="utf-8", newline="") as stream:
            csv.writer(stream).writerows(row[::-1] for row in rows)
    else:
        path.write_bytes(path.read_bytes().rstrip(b"\r\n"))
    checked = run(CHECK, "--pack", pack, "--kit-dir", core)
    assert checked.returncode == 0, checked.stdout + checked.stderr


def test_pack_checker_rejects_duplicate_catalog_headers(bound):
    _, pack, core, _ = bound
    path = core / "legos.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        header, *rows = csv.reader(stream)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", *header])
        writer.writerows(["conflicting-id", *row] for row in rows)
    checked = run(CHECK, "--pack", pack, "--kit-dir", core)
    assert checked.returncode == 1
    assert "legos.csv:1: duplicate columns" in checked.stderr


def test_pack_checker_scans_decoded_index_text(bound):
    _, pack, core, _ = bound
    update_index(bound, lambda index: index["items"][BLIND].update(summary='Use rubric:"shared" for both variants.'))
    checked = run(CHECK, "--pack", pack, "--kit-dir", core)
    assert checked.returncode == 0, checked.stdout + checked.stderr

    update_index(bound, lambda index: index["items"][BLIND].update(summary=r"Read C:\example"))
    checked = run(CHECK, "--pack", pack, "--kit-dir", core)
    assert checked.returncode == 1 and "Windows drive path" in checked.stdout
