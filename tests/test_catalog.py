"""Taxonomy integrity and progressive discovery across resource kinds."""
import csv
import importlib.util
import json

import pytest

from conftest import CHECK_KIT, KIT, KIT_CLI, row, run, write_kit

SPEC = importlib.util.spec_from_file_location("catalog", KIT / "catalog.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


def write_csv(root, filename, fields, rows):
    with (root / filename).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fixture_kit(tmp_path):
    root = write_kit(tmp_path / "kit", [row("A01", summary="Brief " * 80)])
    write_csv(root, "categories.csv", ["id", "parent", "name"], [
        dict(id="01", parent="", name="Foundations"),
        dict(id="1.1", parent="01", name="Instructions"),
        dict(id="1.2", parent="01", name="Standards"),
    ])
    write_csv(root, "rules.csv", ["id", "topic", "rule", "source", "certainty"], [
        dict(id="1.1", topic="Instructions", rule="A category ID is also a rule ID.",
             source="https://example.com/rules", certainty="stated")])
    (root / "patterns.md").write_text(
        "| # | Pattern | Also called | What it is | Avoid when |\n"
        "| 1 | Single agent | Solo | One agent works | Full pattern detail |\n", encoding="utf-8")
    (root / "delegation.md").write_text(
        "## Axes\n| # | Axis | Question to ask | Sources |\n"
        "| 1 | Reversibility | Can it be undone? | Source account |\n"
        "## Levels\n| Step | Name | Meaning |\n| 1 | Tell | Person decides |\n"
        "## How the axes combine\nFull combination instructions.\n", encoding="utf-8")
    rich = dict(id="write-instructions", kind="guide", name="Writing guide", summary="Write clear instructions.",
                when_to_use="When preparing instructions.", prerequisites=[], instructions=["Full guide instructions."],
                applicable_standards=["rule:1.1"], verification=["Read the result."], sources=["https://example.com/guide"],
                certainty="inferred", limitations="Requires human judgment.", checked_on="2026-11-10", host_scope="Any host")
    (root / "resources.json").write_text(json.dumps([rich]), encoding="utf-8")
    keys = [("lego", "A01"), ("rule", "1.1"), ("pattern", "P1"), ("delegation", "axis1"),
            ("delegation", "step1"), ("delegation", "combine"), ("guide", "write-instructions")]
    write_csv(root, "catalog.csv", ["kind", "id", "category", "rationale"], [
        dict(kind=kind, id=rid, category="1.1", rationale="Supports instruction authoring.") for kind, rid in keys])
    return root


def test_complete_fixture_validates_with_all_kinds(tmp_path):
    root = fixture_kit(tmp_path)
    assert catalog.validate_catalog(root) == []
    assert len(catalog.load_resources(root)) == 7


def test_browse_progressively_discloses_counts_and_bounded_summaries(tmp_path):
    root = fixture_kit(tmp_path)
    top = run(KIT_CLI, "--dir", root, "browse")
    assert top.returncode == 0 and top.stdout == "01\tFoundations\t7 resources\n"
    parent = run(KIT_CLI, "--dir", root, "browse", "01")
    assert parent.returncode == 0
    assert parent.stdout == "1.1\tInstructions\t7 resources\n1.2\tStandards\t0 resources\n"
    leaf = run(KIT_CLI, "--dir", root, "browse", "1.1")
    assert leaf.returncode == 0
    lines = leaf.stdout.splitlines()
    assert len(lines) == 7
    assert {line.split(":")[0] for line in lines} == {"lego", "rule", "pattern", "delegation", "guide"}
    assert all(len(line.split("\t")[2]) <= catalog.SUMMARY_LIMIT for line in lines)
    assert "Full guide instructions" not in leaf.stdout
    assert "Full combination instructions" not in leaf.stdout
    assert "Full pattern detail" not in leaf.stdout
    assert "Detail A01" not in leaf.stdout


@pytest.mark.parametrize("key,detail", [
    ("lego:A01", "Detail A01"), ("rule:1.1", "https://example.com/rules"),
    ("pattern:P1", "Full pattern detail"), ("delegation:axis1", "Source account"),
    ("delegation:step1", "Person decides"), ("delegation:combine", "Full combination instructions"),
    ("guide:write-instructions", "Full guide instructions"),
])
def test_inspect_resolves_stable_keys_and_includes_category_and_source(tmp_path, key, detail):
    result = run(KIT_CLI, "--dir", fixture_kit(tmp_path), "inspect", key)
    assert result.returncode == 0, result.stderr
    assert f"resource: {key}" in result.stdout
    assert "category: 1.1 Instructions" in result.stdout
    assert "source_file:" in result.stdout and detail in result.stdout


def test_rule_and_category_ids_do_not_collide(tmp_path):
    root = fixture_kit(tmp_path)
    result = run(KIT_CLI, "--dir", root, "inspect", "rule:1.1")
    assert result.returncode == 0 and "A category ID is also a rule ID" in result.stdout
    for query in ("1.1", "rule:*", "RULE:1.1", "lego:", "rule:1.1:extra"):
        result = run(KIT_CLI, "--dir", root, "inspect", query)
        assert result.returncode != 0 and not result.stdout and "kit browse" in result.stderr
    result = run(KIT_CLI, "--dir", root, "browse", "rule:1.1")
    assert result.returncode != 0 and not result.stdout


def test_assignment_diagnostics_report_dangling_duplicate_missing_and_nonleaf(tmp_path):
    root = fixture_kit(tmp_path)
    assignments = catalog.load_catalog(root)
    assignments = [entry for entry in assignments if entry["kind"] != "guide"]
    assignments += [assignments[0], dict(kind="lego", id="missing", category="01", rationale="")]
    write_csv(root, "catalog.csv", ["kind", "id", "category", "rationale"], assignments)
    errors = "\n".join(catalog.validate_catalog(root))
    for expected in ("unknown resource lego:missing", "duplicate assignment for lego:A01",
                     "missing assignment for guide:write-instructions", "must name a leaf", "nonempty rationale"):
        assert expected in errors


def test_core_checker_reports_catalog_errors(tmp_path):
    root = fixture_kit(tmp_path)
    assignments = catalog.load_catalog(root)
    assignments[0]["category"] = "9.9"
    write_csv(root, "catalog.csv", ["kind", "id", "category", "rationale"], assignments)
    result = run(CHECK_KIT, "--dir", root)
    assert result.returncode == 1
    assert "lego:A01 category 9.9 must name a leaf" in result.stdout


def test_category_hierarchy_and_duplicate_source_diagnostics(tmp_path):
    root = fixture_kit(tmp_path)
    categories = catalog.load_categories(root)
    categories += [categories[0], dict(id="1.3", parent="02", name="Wrong parent")]
    write_csv(root, "categories.csv", ["id", "parent", "name"], categories)
    with (root / "patterns.md").open("a", encoding="utf-8") as stream:
        stream.write("| 1 | Duplicate | Solo | Repeated | Detail |\n")
    assert "duplicate source resource pattern:P1" in "\n".join(catalog.validate_catalog(root))
    (root / "patterns.md").unlink()
    errors = "\n".join(catalog.validate_catalog(root))
    assert "duplicate category 01" in errors
    assert "invalid leaf 1.3 for parent 02" in errors
    assert "unknown or non-root parent 02" in errors


@pytest.mark.parametrize("field,value,diagnostic", [
    ("sources", ["note:R1"], "HTTP(S) URLs"), ("sources", [], "sources must not be empty"),
    ("certainty", "certain", "certainty must be one of"), ("checked_on", "2026-02-30", "ISO date"),
    ("instructions", "Do this", "instructions must be an array"),
    ("verification", [], "verification must not be empty"),
    ("category", "1.1", "category belongs only in catalog.csv"),
    ("id", "Not a slug", "lowercase slug"), ("host_scope", "", "host_scope must be a nonempty string"),
])
def test_rich_resource_structure_is_validated(tmp_path, field, value, diagnostic):
    root = fixture_kit(tmp_path)
    rich = catalog.load_rich_resources(root)
    rich[0][field] = value
    (root / "resources.json").write_text(json.dumps(rich), encoding="utf-8")
    assert diagnostic in "\n".join(catalog.validate_catalog(root))


def test_absent_rich_resources_are_optional(tmp_path):
    root = fixture_kit(tmp_path)
    (root / "resources.json").unlink()
    rows = [entry for entry in catalog.load_catalog(root) if entry["kind"] != "guide"]
    write_csv(root, "catalog.csv", ["kind", "id", "category", "rationale"], rows)
    assert catalog.validate_catalog(root) == []


def test_real_catalog_covers_every_resource_once_and_browses_five_parents():
    assert catalog.validate_catalog(KIT) == []
    categories = catalog.load_categories(KIT)
    assert len([row for row in categories if not row["parent"]]) == 5
    assert len([row for row in categories if row["parent"]]) == 29
    resources = catalog.load_resources(KIT)
    assert {r["category"] for r in catalog.load_catalog(KIT)} == {r["id"] for r in categories if r["parent"]}
    result = run(KIT_CLI, "browse")
    assert result.returncode == 0 and len(result.stdout.splitlines()) == 5
    assert sum(int(line.split("\t")[-1].split()[0]) for line in result.stdout.splitlines()) == len(resources)


def test_duplicate_source_ids_do_not_silently_overwrite(tmp_path):
    root = fixture_kit(tmp_path)
    rich = catalog.load_rich_resources(root)
    (root / "resources.json").write_text(json.dumps(rich + rich), encoding="utf-8")
    assert "duplicate source resource guide:write-instructions" in "\n".join(catalog.validate_catalog(root))
    result = run(KIT_CLI, "--dir", root, "inspect", "guide:write-instructions")
    assert result.returncode != 0 and not result.stdout


@pytest.mark.parametrize("filename,text", [
    ("categories.csv", "id,name\n01,Foundations\n"),
    ("catalog.csv", "kind,id,category\nlego,A01,1.1\n"),
    ("categories.csv", "id,parent,name\n01,,Foundations,extra\n"),
])
def test_malformed_taxonomy_tables_are_diagnostics(tmp_path, filename, text):
    root = fixture_kit(tmp_path)
    (root / filename).write_text(text, encoding="utf-8")
    assert filename in "\n".join(catalog.validate_catalog(root))


def test_delegation_inspection_preserves_source_uncertainty():
    resource = catalog.load_resources(KIT)["delegation", "combine"]
    assert "certainty" not in resource["fields"]
    assert "`partial`" in " ".join(resource["fields"]["source_context"])
