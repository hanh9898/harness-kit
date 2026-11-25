import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path

import pytest

from conftest import KIT, ROOT


HARNESS_IDS = ("harness-setup", "harness-evolve", "harness-implement", "harness-library")
LIBRARY_ID = "harness-library"
PREPARE_EXAMPLE = ROOT / "examples" / "devin-prepare"
PREPARE_IDS = ("harness-m2-to-spec", "harness-m2-to-tickets")


@pytest.fixture
def devin_project(tmp_path):
    checkout = tmp_path / "kit checkout"
    project = tmp_path / "consumer project"
    project.mkdir()
    shutil.copytree(ROOT / "skills" / "harness", checkout / "skills" / "harness")
    for group in ("discovery", "overrides"):
        shutil.copytree(ROOT / "skills" / group, checkout / "skills" / group)
    shutil.copytree(PREPARE_EXAMPLE, checkout / "examples" / PREPARE_EXAMPLE.name)
    shutil.copytree(ROOT / ".claude-plugin", checkout / ".claude-plugin")
    shutil.copy2(ROOT / "package.json", checkout)
    shutil.copytree(KIT, checkout / "kit", ignore=shutil.ignore_patterns("__pycache__"))

    def git(*args):
        return subprocess.run(
            ["git", "-C", checkout, *args], check=True, capture_output=True, text=True
        ).stdout.strip()

    git("init", "--quiet")
    git("add", ".")
    git(
        "-c", "user.name=Fixture", "-c", "user.email=fixture@example.com",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
        "commit", "--quiet", "-m", "Pin a complete skill layout",
    )
    return checkout, project, git("rev-parse", "HEAD")


def bootstrap_devin(checkout, project, revision, phase="apply", **env):
    runbook = (KIT / "HOST-ADAPTERS.md").read_text(encoding="utf-8")
    section = runbook.split("## Devin project links\n", 1)[1].split("\n## ", 1)[0]
    (command,) = re.findall(r"```sh\n(.*?)\n```", section, re.DOTALL)
    return subprocess.run(
        ["sh", "-c", command, "bootstrap", phase],
        env={**os.environ, "KIT": str(checkout), "PROJECT": str(project), "KIT_COMMIT": revision, **env},
        capture_output=True,
        text=True,
    )


def test_devin_inspect_leaves_project_untouched(devin_project):
    checkout, project, revision = devin_project
    result = bootstrap_devin(checkout, project, revision, "inspect")
    assert result.returncode == 0, result.stderr
    assert str(project) in result.stdout
    assert revision in result.stdout
    assert all(skill_id in result.stdout for skill_id in HARNESS_IDS)
    assert not list(project.iterdir())


def test_devin_links_preserve_tool_and_never_overwrite(devin_project):
    checkout, project, revision = devin_project
    entries = project / ".devin" / "skills"
    sources = checkout / "skills" / "harness"
    for skill_id in HARNESS_IDS:
        shutil.copytree(sources / skill_id, entries / skill_id)

    library_path = (entries / LIBRARY_ID).resolve() / "../../../kit/scripts/library"
    copied = subprocess.run(
        ["sh", "-c", '"$1" --help', "sh", library_path], capture_output=True, text=True
    )
    assert copied.returncode == 127
    assert copied.stdout == ""
    rejected_copy = bootstrap_devin(checkout, project, revision)
    assert rejected_copy.returncode == 2
    assert "existing entry does not resolve" in rejected_copy.stderr
    assert all((entries / name / "SKILL.md").is_file() for name in HARNESS_IDS)
    assert all(not path.is_symlink() for path in entries.iterdir())

    shutil.rmtree(entries)
    first = bootstrap_devin(checkout, project, revision)
    assert first.returncode == 0, first.stderr
    assert first.stdout.startswith("usage: library")
    assert {path.name for path in entries.iterdir()} == set(HARNESS_IDS)
    for path in entries.iterdir():
        assert path.is_symlink()
        assert path.resolve() == sources / path.name
    initial = {path.name: (path.readlink(), path.lstat()) for path in entries.iterdir()}
    directory_before = entries.stat()

    second = bootstrap_devin(checkout, project, revision)
    assert second.returncode == 0, second.stderr
    assert second.stdout == first.stdout
    assert entries.stat().st_ctime_ns == directory_before.st_ctime_ns
    for path in entries.iterdir():
        target, stat_before = initial[path.name]
        assert path.readlink() == target
        assert path.lstat().st_ino == stat_before.st_ino
        assert path.lstat().st_ctime_ns == stat_before.st_ctime_ns


@pytest.mark.parametrize("dangling", [False, True], ids=["wrong-source", "dangling"])
def test_devin_link_conflict_leaves_all_entries_unchanged(devin_project, tmp_path, dangling):
    checkout, project, revision = devin_project
    link = project / ".devin" / "skills" / LIBRARY_ID
    link.parent.mkdir(parents=True)
    other = tmp_path / "other checkout" / LIBRARY_ID
    if not dangling:
        shutil.copytree(checkout / "skills" / "harness" / LIBRARY_ID, other)
    link.symlink_to(other, target_is_directory=True)

    result = bootstrap_devin(checkout, project, revision)

    assert result.returncode == 2
    assert result.stdout == ""
    assert str(link) in result.stderr
    assert link.readlink() == other
    assert list(link.parent.iterdir()) == [link]


def test_devin_registration_checks_the_pin_and_clean_checkout_before_writing(devin_project):
    checkout, project, revision = devin_project

    wrong_pin = bootstrap_devin(checkout, project, revision[:-1])
    assert wrong_pin.returncode == 2
    assert "approved commit" in wrong_pin.stderr
    assert not (project / ".devin").exists()

    (checkout / "untracked").touch()
    dirty = bootstrap_devin(checkout, project, revision)
    assert dirty.returncode == 2
    assert "checkout is not clean" in dirty.stderr
    assert not (project / ".devin").exists()


def test_devin_registration_rejects_redirected_skills_directory(devin_project, tmp_path):
    checkout, project, revision = devin_project
    outside = tmp_path / "out-of-scope"
    outside.mkdir()
    devin_dir = project / ".devin"
    devin_dir.mkdir()
    (devin_dir / "skills").symlink_to(outside, target_is_directory=True)

    result = bootstrap_devin(checkout, project, revision)

    assert result.returncode == 2
    assert "not a project-local directory" in result.stderr
    assert not list(outside.iterdir())


@pytest.mark.parametrize(
    ("missing", "expected_error"),
    [("python3", "python3"), ("realpath", "realpath"), (None, "cannot run the pinned Library helper")],
    ids=["missing-python3", "missing-realpath", "failing-helper"],
)
def test_devin_registration_checks_runtime_before_writing(devin_project, tmp_path, missing, expected_error):
    checkout, project, revision = devin_project
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for command in {"sh", "git", "realpath", "mkdir", "ln", "python3"} - {missing}:
        executable = bin_dir / command
        if missing is None and command == "python3":
            executable.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
            executable.chmod(0o755)
        else:
            executable.symlink_to(shutil.which(command))

    result = bootstrap_devin(checkout, project, revision, PATH=str(bin_dir))

    assert result.returncode == 2
    assert expected_error in result.stderr
    assert not (project / ".devin").exists()


@pytest.mark.parametrize("subdir", [False, True], ids=["same-checkout", "nested-project"])
def test_devin_registration_does_not_dirty_the_pinned_checkout(devin_project, subdir):
    checkout, _, revision = devin_project
    project = checkout
    if subdir:
        project /= "nested"
        project.mkdir()

    result = bootstrap_devin(checkout, project, revision)

    assert result.returncode == 2
    assert "outside the pinned kit checkout" in result.stderr
    assert not (project / ".devin").exists()


def test_host_adapters_cover_each_capability_and_its_fallback():
    document = (KIT / "HOST-ADAPTERS.md").read_text(encoding="utf-8")
    table = document.split("## Capability map\n", 1)[1].split("\n## ", 1)[0]
    heading, _, *rows = [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in table.splitlines()
        if line.startswith("|")
    ]
    assert heading == [
        "Capability", "Devin", "Pi", "Claude Code", "Codex",
        "Fallback when the required primitive is absent",
    ]
    assert len(rows) == 6
    assert {row[0].strip("`") for row in rows} == {
        "work-workers", "inbox", "memory", "domain-targets", "wake", "evidence-write-gate",
    }
    assert all(len(row) == len(heading) and all(row) for row in rows)


@dataclass(frozen=True)
class EntryReadback:
    exact_id: str
    source: Path
    project: Path
    caller: str
    commit: str
    digest: str


def check_entry(observed, expected):
    for field in ("exact_id", "project", "source", "caller", "commit", "digest"):
        if getattr(observed, field) != getattr(expected, field):
            raise ValueError(field)


@pytest.mark.parametrize("host", ["devin", "pi", "claude-code", "codex"])
def test_pinned_host_fixture_keeps_internal_routes_out_of_default_inventory(devin_project, host):
    checkout, project, commit = devin_project
    skills = checkout / "skills"
    caller = f"{host}:bound-project-session"
    if host == "devin":
        applied = bootstrap_devin(checkout, project, commit)
        assert applied.returncode == 0, applied.stderr
        inventory_root = project / ".devin" / "skills"
    elif host in {"pi", "claude-code"}:
        manifest = "package.json" if host == "pi" else ".claude-plugin/plugin.json"
    else:
        inventory_root = project / ".agents" / "skills"
        inventory_root.mkdir(parents=True)
        for exact_id in HARNESS_IDS:
            (inventory_root / exact_id).symlink_to(
                skills / "harness" / exact_id, target_is_directory=True,
            )

    def inventory():
        if host in {"devin", "codex"}:
            paths = inventory_root.iterdir()
        else:
            package = json.loads((checkout / manifest).read_text())
            paths = map(checkout.joinpath, (package["pi"] if host == "pi" else package)["skills"])
        return {path.name: path for path in paths}

    def read(exact_id, source, origin=project):
        return EntryReadback(
            exact_id, source, origin, caller, commit,
            hashlib.sha256(source.read_bytes()).hexdigest(),
        )

    def default_prompt():
        return {
            name: root.joinpath("SKILL.md").read_text().split("\n---", 1)[0]
            for name, root in inventory().items()
        }

    def pin(exact_id, relative, expected_source):
        original = subprocess.check_output(["git", "-C", checkout, "show", f"{commit}:{relative}"])
        return EntryReadback(
            exact_id, expected_source, project, caller, commit, hashlib.sha256(original).hexdigest(),
        )

    before = default_prompt()
    assert set(before) == set(HARNESS_IDS)
    for exact_id, root in inventory().items():
        source = root / "SKILL.md"
        assert f"\nname: {exact_id}\n" in before[exact_id]
        relative = f"skills/harness/{exact_id}/SKILL.md"
        assert source.resolve() == checkout / relative
        if host == "devin":
            expected_source = project / ".devin" / "skills" / exact_id / "SKILL.md"
        elif host == "codex":
            expected_source = project / ".agents" / "skills" / exact_id / "SKILL.md"
        else:
            expected_source = checkout / relative
        check_entry(read(exact_id, source), pin(exact_id, relative, expected_source))

    library = inventory()[LIBRARY_ID].resolve() / "../../../kit/scripts/library"
    probe = subprocess.run(
        [library, "--help"], capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert probe.returncode == 0 and probe.stdout.startswith("usage: library"), probe.stderr

    for group, exact_id in [
        ("skills/discovery", "workflow-discovery"),
        ("skills/overrides", "harness-project-implement"),
        *((f"examples/{PREPARE_EXAMPLE.name}", exact_id) for exact_id in PREPARE_IDS),
    ]:
        source = checkout / group / exact_id / "SKILL.md"
        expected = pin(exact_id, source.relative_to(checkout), source)
        assert f"\nname: {exact_id}\n" in source.read_text()
        foreign = project.parent / "foreign project"
        foreign_source = foreign / group / exact_id / "SKILL.md"
        foreign_source.parent.mkdir(parents=True)
        foreign_source.symlink_to(source)
        observed = read(exact_id, foreign_source, foreign)
        assert observed.digest == expected.digest
        assert observed.source.resolve() == expected.source.resolve()
        with pytest.raises(ValueError, match="project"):
            check_entry(observed, expected)
        for field, value in [("caller", f"{host}:other-session"), ("commit", "other-pin"),
                             ("exact_id", "other-id"), ("source", foreign_source)]:
            with pytest.raises(ValueError, match=field):
                check_entry(replace(expected, **{field: value}), expected)
        check_entry(read(exact_id, source), expected)
        assert default_prompt() == before


@pytest.fixture
def devin_prepare_records():
    prepare = json.loads((PREPARE_EXAMPLE / "prepare.json").read_text(encoding="utf-8"))
    records = json.loads((PREPARE_EXAMPLE / "decision.json").read_text(encoding="utf-8"))

    def open_ref(reference):
        filename, pointer = reference.split("#/", 1)
        assert filename == "decision.json"
        record = records
        for key in pointer.split("/"):
            record = record[key]
        return record

    return prepare, records, open_ref


def check_prepare_handoff(handoff):
    checked = subprocess.run(
        [KIT / "scripts" / "check-stage-handoff", "--expect-operation", "prepare", handoff],
        capture_output=True, text=True,
    )
    assert checked.returncode == 0, checked.stderr


def test_devin_prepare_example_opens_pinned_fixture_records(devin_prepare_records):
    check_prepare_handoff(PREPARE_EXAMPLE / "prepare.json")
    prepare, records, open_ref = devin_prepare_records
    assert {"spec_ref", "ticket_ref"}.isdisjoint(prepare)

    decision = open_ref(prepare["decision_ref"])
    assert prepare["decision_ref"].endswith(f'/{decision["id"]}@{decision["revision"]}')
    assert decision["scope_ref"] == prepare["scope_ref"]
    assert decision["acceptance"] == prepare["acceptance"]
    assert decision["dependency_refs"] == prepare["dependency_refs"]
    assert open_ref(decision["basis_ref"])
    assert open_ref(prepare["scope_ref"])["fixture_only"] is True
    assert all(open_ref(reference) for reference in prepare["dependency_refs"])

    routes = [open_ref(reference) for reference in prepare["needed_route_refs"]]
    assert [route["skill_id"] for route in routes] == list(PREPARE_IDS)
    assert records["upstream"] == {
        "repository": "https://github.com/mattpocock/skills",
        "revision": "abeeaf95660ba9e8b7c753eb38f441ca707a8823",
    }
    for route in routes:
        exact_id = route["skill_id"]
        assert route["source"] == f"{exact_id}/SKILL.md"
        assert route["invocation_policy"] == "agent-callable"
        frontmatter = (PREPARE_EXAMPLE / route["source"]).read_text(encoding="utf-8").split("---")[1]
        assert f"\nname: {exact_id}\n" in frontmatter
        assert re.search(r"^description: .+", frontmatter, re.MULTILINE)
        assert "disable-model-invocation: true" not in frontmatter


def test_devin_prepare_fixture_replays_missing_artifacts_and_h5(devin_prepare_records, tmp_path):
    prepare, _, open_ref = devin_prepare_records
    route_refs = prepare["needed_route_refs"]
    spec, tickets = PREPARE_IDS
    approved_spec_ref = "inline:verification-spec@1"
    fixture_h5_receipt = (approved_spec_ref, prepare["decision_ref"], prepare["scope_ref"])
    ticket_ref = {"instance": "fixture", "namespace": "harness", "id": "draft-check", "revision": 1}

    def replay(handoff, h5_receipt=None):
        facts = set()
        spec_ref = handoff.get("spec_ref")
        if spec_ref and h5_receipt == (spec_ref, handoff["decision_ref"], handoff["scope_ref"]):
            facts.add("prepare.spec-approved")

        calls = []
        for reference in handoff["needed_route_refs"]:
            route = open_ref(reference)
            if f'{route["artifact"]}_ref' in handoff:
                continue
            if not facts.issuperset(route["requires"]):
                return calls, "AwaitSpecApproval"
            calls.append(route["skill_id"])
        return calls, "DraftOnly"

    assert replay(prepare) == ([spec], "AwaitSpecApproval")
    with_spec = {**prepare, "spec_ref": approved_spec_ref}
    assert replay(with_spec) == ([], "AwaitSpecApproval")
    assert replay({**with_spec, "spec_ref": "inline:verification-spec@2"}, fixture_h5_receipt) == (
        [], "AwaitSpecApproval",
    )
    assert replay({**prepare, "ticket_ref": ticket_ref}) == ([spec], "DraftOnly")
    assert replay({**with_spec, "ticket_ref": ticket_ref}, fixture_h5_receipt) == ([], "DraftOnly")
    assert replay(with_spec, fixture_h5_receipt) == ([tickets], "DraftOnly")

    resumed = {
        **with_spec,
        "needed_route_refs": [
            reference for reference in route_refs
            if f'{open_ref(reference)["artifact"]}_ref' not in with_spec
        ],
    }
    resumed_path = tmp_path / "resume.json"
    resumed_path.write_text(json.dumps(resumed), encoding="utf-8")
    check_prepare_handoff(resumed_path)
    assert replay(resumed, fixture_h5_receipt) == ([tickets], "DraftOnly")


def unique_object(pairs):
    fields = dict(pairs)
    if len(fields) != len(pairs):
        raise ValueError("duplicate JSON key")
    return fields


def ref(value):
    return type(value) is str and bool(value)


def revision(value):
    return ref(value) or (type(value) is int and value >= 0)


@dataclass(frozen=True)
class Instance:
    instance_id: str
    scope_ref: str
    binding_revision: int | str


@dataclass(frozen=True)
class Caller(Instance):
    caller_ref: str


@dataclass(frozen=True)
class Automation:
    automation_id: str
    target_bot_id: str
    scope_ref: str
    binding_revision: int | str
    kind: str
    trigger_ref: str
    source_id: str


def parse_routes(payload):
    config = json.loads(payload, object_pairs_hook=unique_object)
    if (not isinstance(config, dict) or set(config) != {"version", "library_ref", "bots", "automations"}
            or type(config["version"]) is not int or config["version"] != 1
            or not ref(config.get("library_ref"))
            or not isinstance(config.get("bots"), list)
            or not isinstance(config.get("automations"), list)):
        raise ValueError("expected version 1 bots[] and automations")
    bots = {}
    for bot in config["bots"]:
        bot_id = bot.get("bot_id")
        if not ref(bot_id) or bot_id in bots:
            raise ValueError("bot_id")
        binding = bot["binding"]
        instance = Instance(*(binding[field] for field in Instance.__dataclass_fields__))
        if (not ref(instance.instance_id) or not ref(instance.scope_ref)
                or not revision(instance.binding_revision)
                or any(other.instance_id == instance.instance_id for other in bots.values())):
            raise ValueError("binding")
        bots[bot_id] = instance
    routes, triggers = {}, set()
    for mapping in config["automations"]:
        route = Automation(**mapping)
        if (not ref(route.target_bot_id) or route.target_bot_id not in bots):
            raise ValueError("target_bot_id")
        bound = bots[route.target_bot_id]
        if (not revision(route.binding_revision) or route.binding_revision != bound.binding_revision
                or route.scope_ref != bound.scope_ref):
            raise ValueError("mapping binding")
        if (not all(map(ref, (route.source_id, route.trigger_ref, route.automation_id)))
                or route.kind not in ("schedule", "integration-event")
                or route.trigger_ref in triggers or route.automation_id in routes):
            raise ValueError("automation identity")
        routes[route.automation_id] = route
        triggers.add(route.trigger_ref)
    return bots, routes


@pytest.fixture
def two_bots():
    bots = []
    for name, version in [("a", 1), ("b", 4)]:
        bots.append({
            "bot_id": f"bot-{name}", "role": f"role:{name}", "contract": f"contract:{name}",
            "binding": {
                "instance_id": f"instance-{name}", "scope_ref": f"scope-{name}",
                "binding_revision": version, "owner_ref": "owner:shared",
                "adapter_ref": f"adapter:{name}", "configuration_ref": f"config:{name}",
                "checkpoint_ref": f"checkpoint:{name}",
            },
            "bot-inbox": {"state": "bound", "store_ref": f"inbox:{name}"},
            "bot-memory": {"state": "bound", "store_ref": f"memory:{name}"},
            "revision": version, "grant": [], "receipt": [],
        })
    return {
        "version": 1, "library_ref": "library:pinned",
        "bots": bots,
        "automations": [
            {"automation_id": f"automation-{suffix}", "target_bot_id": f"bot-{bot}",
             "scope_ref": f"scope-{bot}", "binding_revision": version, "kind": "integration-event",
             "trigger_ref": f"trigger-{suffix}", "source_id": "integration"}
            for suffix, bot, version in [("a1", "a", 1), ("a2", "a", 1), ("b1", "b", 4)]
        ],
    }


@pytest.mark.parametrize("fault", [
    "missing-id", "duplicate-id", "legacy-only", "duplicate-key", "missing-target", "array-target",
    "unknown-target", "duplicate-automation", "duplicate-trigger", "scope", "revision", "bool-revision",
])
def test_automation_mapping_rejects_inexact_routes(two_bots, fault):
    bot_a, bot_b = two_bots["bots"]
    a1, _, b1 = two_bots["automations"]
    match fault:
        case "missing-id":
            del bot_a["bot_id"]
        case "duplicate-id":
            bot_b["bot_id"] = bot_a["bot_id"]
        case "legacy-only":
            del two_bots["bots"]
            two_bots["bot_ref"] = "bot-a"
        case "duplicate-key":
            payload = json.dumps(two_bots).replace('"version": 1', '"version": 1, "version": 1')
            with pytest.raises(ValueError, match="duplicate JSON key"):
                parse_routes(payload)
            return
        case "missing-target":
            del a1["target_bot_id"]
        case "array-target":
            a1["target_bot_id"] = ["bot-a"]
        case "unknown-target":
            a1["target_bot_id"] = "bot-c"
        case "duplicate-automation":
            b1["automation_id"] = a1["automation_id"]
        case "duplicate-trigger":
            b1["trigger_ref"] = a1["trigger_ref"]
        case "scope":
            a1["scope_ref"] = "scope-b"
        case "revision":
            a1["binding_revision"] = 4
        case "bool-revision":
            a1["binding_revision"] = True
    with pytest.raises((ValueError, TypeError)):
        parse_routes(json.dumps(two_bots))


def occurrence_rows(db):
    with sqlite3.connect(db) as conn:
        return conn.execute("SELECT key, state FROM occurrences ORDER BY key").fetchall()


@pytest.fixture
def wake_fixture(two_bots, tmp_path):
    bots, routes = parse_routes(json.dumps(two_bots))
    callers = {
        bot_id: Caller(bound.instance_id, bound.scope_ref, bound.binding_revision, f"caller:{bot_id}")
        for bot_id, bound in bots.items()
    }
    ledgers = {}
    for bot_id, caller in callers.items():
        db = tmp_path / f"{bot_id}.db"
        with sqlite3.connect(db) as conn:
            conn.executescript("""
                PRAGMA user_version = 1;
                CREATE TABLE fence (instance TEXT, scope TEXT, revision TEXT, caller TEXT);
                CREATE TABLE occurrences (key TEXT PRIMARY KEY, state TEXT NOT NULL);
            """)
            conn.execute("INSERT INTO fence VALUES (?, ?, ?, ?)", fence_row(caller))
        ledgers[bot_id] = db
    return callers, routes, ledgers


def fence_row(caller):
    return caller.instance_id, caller.scope_ref, json.dumps(caller.binding_revision), caller.caller_ref


def receive(wake_fixture, bot_id, caller, delivery, occurrence_id, *,
            ingress="authenticated-automation", active_trigger="trigger-a1", crash=None):
    callers, routes, ledgers = wake_fixture
    if (ingress != "authenticated-automation" or bot_id != delivery.target_bot_id
            or routes.get(delivery.automation_id) != delivery
            or not revision(delivery.binding_revision) or not ref(occurrence_id)
            or callers.get(bot_id) != caller or active_trigger != delivery.trigger_ref):
        return ()
    db = ledgers[bot_id]
    key = json.dumps([bot_id, delivery.automation_id, delivery.source_id, occurrence_id])
    with sqlite3.connect(db) as conn:
        conn.execute("BEGIN IMMEDIATE")
        if (conn.execute("PRAGMA user_version").fetchone() != (1,)
                or conn.execute("SELECT * FROM fence").fetchone() != fence_row(caller)):
            return ()
        claimed = conn.execute(
            "INSERT INTO occurrences VALUES (?, 'pending') ON CONFLICT(key) DO NOTHING", (key,),
        ).rowcount
        if crash == "before-commit":
            conn.rollback()
            return ()
    if crash == "after-commit":
        return ()
    assert (key, "pending") in occurrence_rows(db)
    return ("ack", "dispatch") if claimed else ("ack",)


@pytest.mark.parametrize("ingress", ["chat", "@mention", "bot-message", "inbox-reply", "manual"])
def test_non_automation_never_claims_or_acknowledges(wake_fixture, ingress):
    bots, routes, ledgers = wake_fixture
    assert receive(wake_fixture, "bot-a", bots["bot-a"], routes["automation-a1"], "event",
                   ingress=ingress) == ()
    assert all(occurrence_rows(db) == [] for db in ledgers.values())


def test_wake_rejects_mismatched_delivery_and_isolates_occurrences(wake_fixture):
    bots, routes, ledgers = wake_fixture
    a, b = bots["bot-a"], bots["bot-b"]
    a1, a2, b1 = (routes[f"automation-{suffix}"] for suffix in ("a1", "a2", "b1"))
    assert receive(wake_fixture, "bot-b", b, a1, "event", active_trigger=a1.trigger_ref) == ()
    assert receive(wake_fixture, "bot-a", b, a1, "event") == ()
    assert receive(wake_fixture, "bot-a", replace(a, caller_ref=b.caller_ref), a1, "event") == ()
    assert receive(wake_fixture, "bot-a", a, a1, "event", active_trigger=None) == ()
    for field, value in [("trigger_ref", a2.trigger_ref), ("source_id", "other-event-source"),
                         ("scope_ref", "scope-b"), ("binding_revision", 0)]:
        assert receive(wake_fixture, "bot-a", a, replace(a1, **{field: value}), "event") == ()
    assert all(occurrence_rows(db) == [] for db in ledgers.values())
    assert receive(wake_fixture, "bot-a", a, a1, "event") == ("ack", "dispatch")
    assert occurrence_rows(ledgers["bot-b"]) == []
    assert receive(wake_fixture, "bot-a", a, a2, "event", active_trigger=a2.trigger_ref) == (
        "ack", "dispatch",
    )
    assert receive(wake_fixture, "bot-b", b, b1, "event", active_trigger=b1.trigger_ref) == (
        "ack", "dispatch",
    )
    assert len(occurrence_rows(ledgers["bot-a"])) == 2
    assert len(occurrence_rows(ledgers["bot-b"])) == 1


def test_claim_is_durable_before_ack_and_retry_does_not_dispatch(wake_fixture):
    bots, routes, ledgers = wake_fixture
    args = wake_fixture, "bot-a", bots["bot-a"], routes["automation-a1"], "event"
    ledger = ledgers["bot-a"]
    assert receive(*args, crash="before-commit") == ()
    assert occurrence_rows(ledger) == []
    assert receive(*args, crash="after-commit") == ()
    pending = occurrence_rows(ledger)
    assert len(pending) == 1 and pending[0][1] == "pending"
    assert receive(*args) == ("ack",)
    assert receive(*args) == ("ack",)
    assert occurrence_rows(ledger) == pending
    with ThreadPoolExecutor(max_workers=2) as pool:
        deliveries = [pool.submit(receive, *args[:-1], "concurrent") for _ in range(2)]
        assert sorted(d.result() for d in deliveries) == [("ack",), ("ack", "dispatch")]
    assert len(occurrence_rows(ledger)) == 2
    assert occurrence_rows(ledgers["bot-b"]) == []


def test_rebind_fences_old_instance_without_resetting_ledgers(wake_fixture):
    bots, routes, ledgers = wake_fixture
    a, b = bots["bot-a"], bots["bot-b"]
    a1, b1 = routes["automation-a1"], routes["automation-b1"]
    assert receive(wake_fixture, "bot-a", a, a1, "event") == ("ack", "dispatch")
    assert receive(wake_fixture, "bot-b", b, b1, "event", active_trigger=b1.trigger_ref) == (
        "ack", "dispatch",
    )
    before = {bot_id: occurrence_rows(db) for bot_id, db in ledgers.items()}
    new = replace(a, instance_id="instance-a-rebound", binding_revision=2)
    with sqlite3.connect(ledgers["bot-a"]) as conn:
        conn.execute("UPDATE fence SET instance = ?", (new.instance_id,))
    assert receive(wake_fixture, "bot-a", a, a1, "late") == ()
    with sqlite3.connect(ledgers["bot-a"]) as conn:
        conn.execute("UPDATE fence SET revision = ?", (json.dumps(new.binding_revision),))
    new_route = replace(a1, binding_revision=new.binding_revision)
    bots["bot-a"], routes[a1.automation_id] = new, new_route
    assert receive(wake_fixture, "bot-a", new, new_route, "event") == ("ack",)
    assert receive(wake_fixture, "bot-b", b, b1, "event", active_trigger=b1.trigger_ref) == ("ack",)
    assert {bot_id: occurrence_rows(db) for bot_id, db in ledgers.items()} == before


def test_legacy_instance_key_does_not_accept_redelivery_as_a_new_occurrence(wake_fixture):
    bots, routes, ledgers = wake_fixture
    bound, route, db = bots["bot-a"], routes["automation-a1"], ledgers["bot-a"]
    old_key = json.dumps([bound.instance_id, route.source_id, "event"])
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA user_version = 0")
        conn.execute("INSERT INTO occurrences VALUES (?, 'pending')", (old_key,))
    assert receive(wake_fixture, "bot-a", bound, route, "event") == ()
    assert occurrence_rows(db) == [(old_key, "pending")]
    assert occurrence_rows(ledgers["bot-b"]) == []
