"""Check the RFC-001 v1 contract without interpreting prompts at runtime."""

import json
import re
import sqlite3
from contextlib import closing
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest

from conftest import ROOT, run
from test_harness_suite import DISCOVERY_ROUTES
from test_library_read_no_write import CLI, READS, library, read_args


SKILLS = Path("skills")
HARNESS = SKILLS / "harness"
SETUP = HARNESS / "harness-setup"
EVOLVE = HARNESS / "harness-evolve"
IMPLEMENT = HARNESS / "harness-implement"
LIBRARY_SKILL = HARNESS / "harness-library"
DISCOVERY = SETUP / "DISCOVERY.md"
ROUTES = IMPLEMENT / "ROUTES.md"
ACTIVATION = SETUP / "ACTIVATION.md"
WORK = IMPLEMENT / "WORK.md"
ADOPTION = EVOLVE / "ADOPTION.md"
INBOX = SKILLS / "bot/bot-inbox/SKILL.md"
MEMORY = SKILLS / "bot/bot-memory/SKILL.md"
PERSISTENCE = Path("kit/PERSISTENCE.md")
LIBRARY = Path("kit/LIBRARY.md")
PROPOSAL = Path("kit/PROPOSAL-ENTRY.md")
DEFAULT = (SETUP, EVOLVE, IMPLEMENT, LIBRARY_SKILL)
ENTRIES = (*(path / "SKILL.md" for path in DEFAULT), INBOX, MEMORY)
OVERRIDES = {name: f"harness-project-{name}" for name in ("to-spec", "to-tickets", "implement")}

REQUIRED = {
    ACTIVATION: {
        "setup.install": "entry.explicit-apply authority.install",
        "setup.discovery": "method.grilling method.domain-modeling",
        "setup.author-overrides": "method.writing-for-agents original.to-spec original.to-tickets original.implement",
        "setup.execution-ready": "override.to-spec override.to-tickets override.implement",
        "bot.configure-disabled": "bot.exact-target bot.disabled-config authority.bot-config",
        "bot.rebind": "bot.exact-target bot.old-disabled-readback bot.drain-fence bot.reconciled authority.rebind",
        "bot.pilot.initial": "bot.configure-disabled bot.disabled-readback authority.pilot",
        "bot.pilot.rebound": "bot.rebind bot.disabled-readback authority.pilot",
        "trigger.enable.initial": "bot.pilot.initial bot.exact-target trigger.exact-id pilot.manual-fresh-worker authority.trigger",
        "trigger.enable.rebound": "bot.pilot.rebound bot.exact-target trigger.exact-id pilot.manual-fresh-worker authority.trigger",
    },
    WORK: {
        "prepare.spec-approved": "spec.exact-revision authority.spec-decision",
        "prepare.tickets": "prepare.spec-approved",
        "publish.apply": "publish.split-current publish.exact-grant publish.harness-target",
        "work.claim": "work.canonical-task authority.work-claim",
    },
    PERSISTENCE: {
        "continuation.handoff": "method.handoff evidence.access",
        "wake.claim": "wake.automation-only wake.exact-target wake.current-binding wake.trigger-active-readback",
        "wake.ack": "wake.claim wake.durable-dedupe",
    },
    INBOX: {"inbox.grant-request": "inbox.match-revision inbox.authenticated-yes"},
    LIBRARY: {
        "library.read": "library.no-sidecar library.bound-store",
        "library.commit": "library.exact-grant library.cas",
    },
    MEMORY: {
        "memory.read.empty": "memory.confirmed-unconfigured",
        "memory.read.ready-empty": "memory.bound-ready memory.no-row",
        "memory.write": "memory.bound-ready memory.acl memory.cas",
    },
    PROPOSAL: {
        "entry.research": "entry.no-explicit-request access.read-only",
        "entry.offer": "entry.research",
        "entry.selected-request": "entry.offer user.selection",
        "entry.effect.direct": "entry.explicit-request authority.live-effect",
        "entry.effect.selected": "entry.selected-request authority.live-effect",
    },
}

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def split_markdown(text):
    prose, declarations = [], []
    fence = None
    block = None
    for line in text.splitlines():
        marker = FENCE.fullmatch(line)
        if fence is None:
            if marker is None:
                prose.append(line)
            else:
                chars, info = marker.groups()
                fence = chars
                block = [] if info.strip() == "v1-gates" else None
        elif marker and marker[1].startswith(fence) and not marker[2].strip():
            if block is not None:
                declarations.append("\n".join(block))
            fence, block = None, None
        elif block is not None:
            block.append(line)
    assert block is None, "Unclosed v1-gates fence"
    return "\n".join(prose), declarations


def unique_object(pairs):
    result = dict(pairs)
    assert len(result) == len(pairs), f"Duplicate object key: {pairs}"
    return result


def declared_gates(block, owner):
    try:
        rows = json.loads(block, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{owner}: invalid v1-gates JSON: {exc}")
    assert isinstance(rows, list), f"{owner}: v1-gates must be a JSON list"
    for row in rows:
        assert isinstance(row, dict) and row.keys() == {"id", "requires"}, f"{owner}: expected id and requires (closed object): {row}"
        gate, required = row["id"], row["requires"]
        assert isinstance(gate, str) and re.fullmatch(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+", gate), (owner, gate)
        assert isinstance(required, list) and all(isinstance(item, str) for item in required), (owner, gate)
        assert len(set(required)) == len(required), (owner, gate, "duplicate predecessor")
        yield gate, frozenset(required)


def test_v1_gate_owners_and_predecessors():
    gates, owners = {}, {}
    shipped_docs = {path.relative_to(ROOT) for area in ("kit", "skills", "examples")
                    for path in (ROOT / area).rglob("*.md")}
    for path in sorted(shipped_docs | REQUIRED.keys()):
        assert (ROOT / path).is_file(), f"Missing gate owner: {path}"
        _, blocks = split_markdown(read(path))
        assert len(blocks) == int(path in REQUIRED), f"{path}: expected {'one' if path in REQUIRED else 'no'} v1-gates block"
        for block in blocks:
            for gate, predecessors in declared_gates(block, path):
                assert gate not in owners, f"{gate}: duplicate owners {owners.get(gate)} and {path}"
                gates[gate], owners[gate] = predecessors, path

    expected = {gate: (owner, frozenset(predecessors.split()))
                for owner, leaves in REQUIRED.items() for gate, predecessors in leaves.items()}
    for owner, leaves in REQUIRED.items():
        for predecessors in leaves.values():
            for predecessor in predecessors.split():
                expected.setdefault(predecessor, (owner, frozenset()))
    expected.update({
        "entry.explicit-apply": (PROPOSAL, frozenset()),
        "method.handoff": (ACTIVATION, frozenset()),
    })

    for gate, (owner, predecessors) in expected.items():
        assert owners.get(gate) == owner, f"{gate}: expected owner {owner}, got {owners.get(gate)}"
        assert predecessors <= gates[gate], f"{owner}: {gate} missing predecessor(s) {sorted(predecessors - gates[gate])}"
    assert not (gates.keys() - expected.keys()), f"Unrecognized gate(s): {sorted(gates.keys() - expected.keys())}"
    for gate, predecessors in gates.items():
        assert predecessors <= gates.keys(), f"{gate}: undeclared predecessor(s) {sorted(predecessors - gates.keys())}"
    try:
        tuple(TopologicalSorter(gates).static_order())
    except CycleError as exc:
        pytest.fail(f"Gate dependency cycle: {exc.args[1]}")
    for gate, (owner, predecessors) in expected.items():
        assert gates[gate] == predecessors, f"{owner}: {gate} unexpected predecessor(s) {sorted(gates[gate] - predecessors)}"


def local_links(path, prose):
    for raw in INLINE_LINK.findall(prose):
        url = urlsplit(raw)
        if not (url.scheme or url.netloc):
            destination = path.parent / unquote(url.path) if url.path else path
            yield (ROOT / destination).resolve(), unquote(url.fragment)


def heading_anchors(path):
    seen = set()
    prose, _ = split_markdown(read(path))
    for heading in re.findall(r"^ {0,3}#{1,6} +(.+)$", prose, re.M):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        anchor, suffix = slug, 0
        while anchor in seen:
            suffix += 1
            anchor = f"{slug}-{suffix}"
        seen.add(anchor)
    return seen | set(re.findall(r'<a\s+(?:id|name)="([^"]+)"\s*>', prose))


def require_link(source, destination, anchor="", *, lead_only=False):
    prose, _ = split_markdown(read(source))
    if lead_only:
        prose = prose.split("\n## ", 1)[0]
    links = set(local_links(source, prose))
    assert ((ROOT / destination).resolve(), anchor) in links, f"{source}: missing link to {destination}#{anchor}"
    assert (ROOT / destination).is_file(), f"{source}: broken link to {destination}"
    if anchor:
        assert anchor in heading_anchors(destination), f"{source}: stale anchor {destination}#{anchor}"


@pytest.mark.parametrize("entry", (*ENTRIES, DISCOVERY), ids=str)
def test_entry_links_proposal_gate_before_its_procedure(entry):
    require_link(entry, PROPOSAL, lead_only=True)


@pytest.mark.parametrize(("source", "destination", "anchor"), [
    (SETUP / "SKILL.md", ACTIVATION, "verify-upstream-prerequisites"),
    (SETUP / "SKILL.md", ACTIVATION, ""),
    (DISCOVERY, ACTIVATION, "verify-upstream-prerequisites"),
    (ACTIVATION, PROPOSAL, "selection-h1"),
    (ACTIVATION, ROUTES, "project-override-routes"),
    (ACTIVATION, ROUTES, "route-readiness"),
    (ACTIVATION, PERSISTENCE, "automation-wake"),
    (ADOPTION, ACTIVATION, "configure-and-qualify-a-bot"),
    (IMPLEMENT / "SKILL.md", WORK, "publish-or-update"),
    (ROUTES, WORK, "spec-approval-h5"),
    (ROUTES, WORK, "dispatch-and-integrate"),
    (INBOX, WORK, "tasks-board-and-inbox"),
    (INBOX, PERSISTENCE, "automation-wake"),
    (PROPOSAL, PERSISTENCE, "automation-wake"),
    (LIBRARY_SKILL / "READ.md", LIBRARY, "configured-store-reads"),
    (LIBRARY_SKILL / "WRITE.md", LIBRARY, "guarded-writes"),
    *((source, PERSISTENCE, "continuation-handoff") for source in (
        SETUP / "SKILL.md", SETUP / "RESUME.md", EVOLVE / "DESIGN-WRITEBACK.md",
        IMPLEMENT / "SKILL.md", LIBRARY_SKILL / "SKILL.md",
    )),
])
def test_callers_link_canonical_gate(source, destination, anchor):
    require_link(source, destination, anchor)


def assert_skill_name(path):
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", read(path), re.S)
    assert frontmatter, f"{path}: missing skill frontmatter"
    assert re.findall(r"^name:\s*(.+)$", frontmatter[1], re.M) == [path.parent.name], path


def test_discovery_inventory_and_parent_order():
    expected = {SKILLS / f"discovery/{name}/SKILL.md" for _, name, _ in DISCOVERY_ROUTES}
    actual = {path.relative_to(ROOT) for path in ROOT.glob("**/*-discovery/SKILL.md")
              if not any(part.startswith(".") for part in path.relative_to(ROOT).parts)}
    assert actual == expected, f"Discovery inventory drift: missing {sorted(expected - actual)}, extra {sorted(actual - expected)}"
    prose, _ = split_markdown(read(DISCOVERY))
    rows = re.findall(
        r"^\|\s*(\d+\.\d+)\s*\|\s*(\[`([\w-]+)`\]\([^)]+\))\s*\|\s*`?([\w—-]+)`?\s*\|",
        prose, re.M,
    )
    assert [(order, name, parent) for order, _, name, parent in rows] == list(DISCOVERY_ROUTES), (
        "Discovery: route, pass order or parent changed"
    )
    for _, link, name, _ in rows:
        topic = SKILLS / f"discovery/{name}/SKILL.md"
        assert list(local_links(DISCOVERY, link)) == [((ROOT / topic).resolve(), "")], (
            f"{DISCOVERY}: wrong link for {name}"
        )
        assert_skill_name(topic)
        require_link(topic, PROPOSAL, lead_only=True)
        require_link(topic, DISCOVERY, "topic-route-and-result", lead_only=True)


def test_default_opt_in_and_override_inventory():
    expected = {f"./{path.as_posix()}" for path in DEFAULT}
    for manifest, config in [
        (".claude-plugin/plugin.json", json.loads(read(".claude-plugin/plugin.json"))),
        ("package.json", json.loads(read("package.json"))["pi"]),
    ]:
        entries = config["skills"]
        assert len(entries) == len(expected) and set(entries) == expected, f"{manifest}: default entries changed"
    for area in (HARNESS, SKILLS / "bot"):
        actual = {path.relative_to(ROOT) for path in (ROOT / area).rglob("SKILL.md")}
        assert actual == {path for path in ENTRIES if area in path.parents}, f"{area}: entry inventory changed"
    for entry in ENTRIES:
        assert_skill_name(entry)
    override_paths = {SKILLS / f"overrides/{name}/SKILL.md" for name in OVERRIDES.values()}
    assert {path.relative_to(ROOT) for path in (ROOT / SKILLS / "overrides").rglob("SKILL.md")} == override_paths
    routes, _ = split_markdown(read(ROUTES))
    for original, name in OVERRIDES.items():
        path = SKILLS / f"overrides/{name}/SKILL.md"
        assert_skill_name(path)
        row = re.findall(rf"^\|\s*`{original}`\s*\|\s*`{name}`\s*\|(.+)$", routes, re.M)
        assert len(row) == 1 and ((ROOT / path).resolve(), "") in set(local_links(ROUTES, row[0])), (ROUTES, name)

    originals = {"grilling", "domain-modeling", "writing-for-agents", "handoff", "implement-spec", *OVERRIDES}
    for path in ROOT.glob("**/SKILL.md"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        name = re.match(r"\A---\n(?:.*\n)*?name:\s*([\w-]+)\s*\n", read(path.relative_to(ROOT)))
        assert path.parent.name not in originals and (name is None or name[1] not in originals), f"Vendored original: {path}"


@pytest.mark.parametrize(("source", "heading", "policy"), [
    (ACTIVATION, "Install required upstream skills", "Confirm Setup is in Apply before entering this route."),
    (WORK, "Spec approval (H5)", "Match the exact spec reference and revision"),
    (INBOX, "Validate and record replies", "must match both the card and the live subject"),
    (PERSISTENCE, "Automation wake", "Chat, @mentions, Bot messages, direct requests and Inbox replies never wake a Bot."),
    (WORK, "Tasks board and Inbox", "Inbox cards and replies do not authorize a Tasks claim"),
])
def test_prose_states_the_boundary_at_the_gate(source, heading, policy):
    prose, _ = split_markdown(read(source))
    section = re.search(rf"^##+ {re.escape(heading)}\n(.*?)(?=\n##+ |\Z)", prose, re.M | re.S)
    assert section and policy in " ".join(section[1].split()), f"{source}#{heading}: missing policy: {policy}"


@pytest.mark.parametrize(("command", "strict"), READS)
@pytest.mark.parametrize("journal", ["wal", "delete"])
def test_library_preflight_precedes_sqlite_open(library, command, strict, journal):
    store, candidate = library
    with closing(sqlite3.connect(store)) as db:
        assert db.execute(f"PRAGMA journal_mode={journal}").fetchone() == (journal,)
    probe = """
import ctypes, runpy, sqlite3, sys
from types import SimpleNamespace
ctypes.CDLL = lambda *_: SimpleNamespace(syscall=lambda *_: -1)
def reject_open(*args, **kwargs):
    raise AssertionError("Library reached SQLite before no-write preflight")
sqlite3.connect = reject_open
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""
    result = run("-c", probe, CLI, *read_args(store, candidate, command, strict))
    assert (result.returncode, result.stdout) == (2, ""), result.stderr
    if journal == "wal":
        assert "Store is unreadable:" in result.stderr and "cannot enforce" not in result.stderr, result.stderr
    else:
        assert "cannot enforce a no-write SQLite open on this host" in result.stderr, result.stderr
