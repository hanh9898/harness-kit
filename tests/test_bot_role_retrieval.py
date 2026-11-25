"""Discover and select shipped Bot roles through the same CLI as other pieces."""
import json
import re
import shlex
import shutil

from conftest import KIT, ROOT, run


def output(script, *args):
    result = run(script, *args)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def test_bot_role_search_opens_packaged_sections_after_relocation(tmp_path):
    plugin = tmp_path / "relocated plugin"
    for folder in ("kit", "skills"):
        shutil.copytree(ROOT / folder, plugin / folder)
    kit = plugin / "kit"
    store = tmp_path / "library.sqlite3"
    found = json.loads(output(kit / "scripts/library", "--store", store,
                              "search", "bot role template", "--limit", 30))
    assert not found["truncated"]
    assert not store.exists()

    ids = {item["id"] for item in found["matches"]}
    assert {"software-factory", "chief-of-staff", "product-engineer",
            "qa-engineer", "bot-portable-template"} <= ids
    roles = (kit / "BOT-ROLES.md").read_text(encoding="utf-8")
    anchors = {title.lower().replace(" ", "-")
               for title in re.findall(r"^## (.+)$", roles, re.M)}
    assert ids == anchors | {"bot-portable-template"}

    for item in found["matches"]:
        assert (item["kind"], item["origin"]) == ("piece", "supplied")
        slug = item["id"]
        command, *args = shlex.split(item["retrieve"])
        assert command == "kit"
        shown = output(kit / "scripts/kit", *args)
        assert f"id: {slug}\n" in shown
        assert "group: C\n" in shown
        assert "rung: instruction-file\n" in shown
        ref = ("kit/BOT-TEMPLATE.md" if slug == "bot-portable-template"
               else f"kit/BOT-ROLES.md#{slug}")
        assert ref in shown.split("detail:", 1)[1]

    for body in (roles, (kit / "BOT-TEMPLATE.md").read_text(encoding="utf-8")):
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", body):
            if "://" not in target:
                assert (kit / target).is_file(), target


def test_bot_role_uses_normal_scoped_selection(tmp_path):
    store = tmp_path / "library.sqlite3"
    cli = KIT / "scripts/library"
    role = "software-factory"

    def library(*args):
        return json.loads(output(cli, "--store", store, *args))

    initial = library("selection", role, "--source", "supplied")
    assert (initial["available"], initial["effective"], initial["revision"]) == (True, True, 0)
    assert initial["current_snapshot"]["reference"] == f"legos.csv#{role}"
    assert not store.exists()

    decision = tmp_path / "decision.json"
    decision.write_text(json.dumps({
        "owner": "Test owner",
        "scope": "personal",
        "decision": {"authority": "Fixture owner approved", "rationale": "Role is not in scope",
                     "methods": [], "standards": []},
        "evidence": ["Inspected the supplied role"],
        "continuation": "Leave other roles unchanged.",
    }), encoding="utf-8")
    disabled = library("disable", role, "--source", "supplied", "--input", decision,
                       "--expect-selection-revision", 0)
    assert (disabled["available"], disabled["effective"], disabled["revision"]) == (True, False, 1)
    assert library("selection", role, "--source", "supplied") == disabled
    assert library("selection", "chief-of-staff", "--source", "supplied")["effective"]
    found = library("search", "bot role template", "--limit", 30)
    assert found["excluded"] == 1
    assert role not in {match["id"] for match in found["matches"]}
