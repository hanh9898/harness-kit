"""The installable suite and its scoped runbooks ship together."""
import json
import re
import shutil

import pytest

from conftest import KIT, ROOT, run

SKILL_ROOT = ROOT / "skills/harness"
ENTRIES = {"harness-setup", "harness-evolve", "harness-implement", "harness-library"}
OPT_IN_ENTRIES = {"bot-inbox", "bot-memory"}
DISCOVERY = ROOT / "skills/discovery"
DISCOVERY_ROUTES = (
    ("1.1", "environment-discovery", "—"),
    ("1.2", "guidance-discovery", "—"),
    ("1.3", "capabilities-discovery", "—"),
    ("1.4", "agent-role-discovery", "—"),
    ("1.5", "coordination-discovery", "—"),
    ("1.6", "verification-discovery", "—"),
    ("1.7", "state-continuation-discovery", "—"),
    ("2.1", "skill-discovery", "capabilities-discovery"),
    ("2.2", "workflow-discovery", "coordination-discovery"),
    ("2.3", "hooks-discovery", "coordination-discovery"),
    ("2.4", "automation-discovery", "coordination-discovery"),
)


def test_manifests_expose_the_same_four_installed_entries():
    pi = json.loads((ROOT / "package.json").read_text())["pi"]["skills"]
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["skills"]
    expected = {f"./skills/harness/{name}" for name in ENTRIES}
    assert len(pi) == len(claude) == len(expected)
    assert set(pi) == set(claude) == expected
    for name in ENTRIES:
        skill = SKILL_ROOT / name / "SKILL.md"
        assert f"\nname: {name}\n" in skill.read_text()
        assert "allow_implicit_invocation: true" in (skill.parent / "agents/openai.yaml").read_text()


@pytest.mark.parametrize("name", sorted(ENTRIES))
def test_entry_runbooks_have_package_local_links(name):
    for path in (SKILL_ROOT / name).glob("*.md"):
        assert_package_local_links(path)


@pytest.mark.parametrize("name", ["M2-CONFIG.md", "PERSISTENCE.md", "STAGE-CONTRACTS.md"])
def test_kit_contracts_have_package_local_links(name):
    assert_package_local_links(KIT / name)


@pytest.mark.parametrize("entry", [
    "harness-setup/RESUME.md",
    "harness-evolve/DESIGN-WRITEBACK.md",
    "harness-implement/SKILL.md",
    "harness-library/SKILL.md",
])
def test_continuation_uses_one_shared_handoff_contract(entry):
    text = (SKILL_ROOT / entry).read_text(encoding="utf-8")
    assert text.count("](../../../kit/PERSISTENCE.md#continuation-handoff)") == 1


def test_handoff_distinguishes_effect_verification_and_blockers():
    persistence = (KIT / "PERSISTENCE.md").read_text(encoding="utf-8")
    _, _, handoff = persistence.partition("## Continuation handoff\n")
    assert re.findall(r"^\| `(\w+)` \|", handoff, re.MULTILINE) == [
        "Applied", "Verified", "Blocked", "Unknown",
    ]
    assert "recipient's scope" in handoff
    assert "Do not claim `handoff` was invoked." in handoff


def assert_package_local_links(path):
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#") or "<" in target:
            continue
        assert (path.parent / target.split("#")[0]).is_file(), (path.name, target)


def test_library_helpers_resolve_from_a_linked_skill_in_a_foreign_checkout(tmp_path):
    plugin = tmp_path / "checkout with spaces"
    for directory in ("skills", "kit"):
        shutil.copytree(ROOT / directory, plugin / directory)
    registered = tmp_path / "harness-library"
    registered.symlink_to(plugin / "skills/harness/harness-library", target_is_directory=True)
    instructions = (registered / "READ.md").read_text()
    helper_path, = re.findall(r"`<skill-dir>/([^`]+/)`", instructions)
    helpers = registered.resolve() / helper_path
    assert run(helpers / "kit", "show", "reread-source-before-write").returncode == 0
    result = run(helpers / "library", "--store", tmp_path / "selected.sqlite3",
                 "selection", "reread-source-before-write", "--source", "supplied")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["effective"] is True


def test_evolve_reuses_the_shared_m2_configuration_contract():
    adoption = SKILL_ROOT / "harness-evolve" / "ADOPTION.md"
    assert "](../../../kit/M2-CONFIG.md)" in adoption.read_text()


@pytest.mark.parametrize("skill", sorted(
    [f"harness/{entry}" for entry in ENTRIES]
    + [f"bot/{entry}" for entry in OPT_IN_ENTRIES]
    + [f"discovery/{name}" for _, name, _ in DISCOVERY_ROUTES]
))
def test_skill_links_proposal_entry_before_its_procedure(skill):
    path = ROOT / "skills" / skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    lead = text.split("\n## ", 1)[0]
    assert "](../../../kit/PROPOSAL-ENTRY.md)" in lead
    assert_package_local_links(path)


def test_proposal_entry_covers_both_routes_and_does_not_grant_effects():
    path = KIT / "PROPOSAL-ENTRY.md"
    text = path.read_text(encoding="utf-8")
    direct, research, offer, selection = re.split(r"\n## ", text)[1:]
    assert "Direct" in direct and "0 proposal steps" in direct
    assert "material" in direct and "clarification" in direct
    assert "read-only" in research and "ACL" in research
    assert "no acknowledgement or progress narration" in research and "WAL/SHM" in research
    assert "0 writes" in research and "opt-in" in research
    assert "1–2" in offer and "8 short lines" in offer and "60 words" in offer
    assert "verified evidence in parentheses" in offer and "NoProposal" in offer
    assert "literal titles" in selection and "`Something else`" in selection
    assert "multi-select" in selection and "inline" in selection and "Inbox card" in selection
    assert "Decline, silence" in selection and "exact grant" in selection and "H1" in selection
    assert_package_local_links(path)


def test_discovery_routes_match_pass_order_and_parents():
    path = SKILL_ROOT / "harness-setup" / "DISCOVERY.md"
    text = path.read_text(encoding="utf-8")
    routes = re.findall(
        r"^\| (\d\.\d) \| \[\x60([\w-]+)\x60\]\(../../discovery/([\w-]+)/SKILL\.md\)"
        r" \| `?([\w—-]+)`? \|", text, re.M,
    )
    assert all(name == folder for _, name, folder, _ in routes)
    assert [(order, name, parent) for order, name, _, parent in routes] == list(DISCOVERY_ROUTES)
    assert {path.parent.name for path in DISCOVERY.glob("*/SKILL.md")} == {
        name for _, name, _ in DISCOVERY_ROUTES
    }
    for _, name, _ in DISCOVERY_ROUTES:
        skill = DISCOVERY / name / "SKILL.md"
        assert re.match(rf"---\nname: {name}\ndescription: .+\n---\n", skill.read_text())
    assert "](../../../kit/PROPOSAL-ENTRY.md)" in text
    assert "deferred parent" in text and "independent" in text
    assert "wrong caller" in text and "harness-setup" in text and "pinned source" in text
    assert "not default entries" in text


def test_discovery_retains_branch_choices_without_extra_topic_routes():
    path = SKILL_ROOT / "harness-setup" / "DISCOVERY.md"
    text = path.read_text(encoding="utf-8")
    assert "Environment & authority | Context isolation; Runtime environment; Execution authority |" in text
    assert "Agent configuration & roles | Model profiles; Roles and subagents |" in text
    assert "open question at its own tree path for H2" in text
    assert "use their branch's route, not a separate skill ID" in text


def test_bot_discovery_returns_intent_without_enabling_a_wake():
    role = (DISCOVERY / "agent-role-discovery/SKILL.md").read_text()
    automation = (DISCOVERY / "automation-discovery/SKILL.md").read_text()
    assert "each `bot_id`" in role and "role and contract intent" in role
    assert "Do not infer" in role and "wake mapping" in role
    assert "exactly one `target_bot_id`" in automation
    assert "durable" in automation and "atomic" in automation and "before ACK" in automation
    assert "stop path" in automation and "no default Bot" in automation
    assert "Chat, @mentions, and Inbox replies are never wake triggers" in automation
    assert "Do not configure, enable, claim, ACK or dispatch" in automation


def test_first_time_setup_uses_the_structured_continuation_handoff():
    text = (SKILL_ROOT / "harness-setup/SKILL.md").read_text()
    assert "](../../../kit/PERSISTENCE.md#continuation-handoff)" in text
    assert "`/handoff`" not in text
