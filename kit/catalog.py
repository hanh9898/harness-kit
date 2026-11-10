"""Taxonomy, resource indexing, and bounded discovery using the standard library."""
import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

SUMMARY_LIMIT = 240
NAME_LIMIT = 100
RICH_KINDS = {"guide", "workflow", "rule", "piece"}
CERTAINTIES = {"stated", "inferred", "partial"}


def read_csv(kit_dir, name, required=False, columns=None):
    path = Path(kit_dir) / name
    if not path.exists() and not required:
        return []
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if columns is not None and reader.fieldnames != columns:
            raise ValueError(f"{name}: expected columns {','.join(columns)}")
        rows = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError(f"{name}: row width does not match its header")
        return rows


def load_categories(kit_dir):
    return read_csv(kit_dir, "categories.csv", required=True, columns=["id", "parent", "name"])


def load_catalog(kit_dir):
    return read_csv(kit_dir, "catalog.csv", required=True, columns=["kind", "id", "category", "rationale"])


def load_patterns(kit_dir):
    """Return numbered pattern rows and their column headings."""
    path = Path(kit_dir) / "patterns.md"
    head, out = [], {}
    if not path.is_file():
        return out, head
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split(" | ")]
        if line.startswith("| #"):
            head = cells
        elif line.startswith("| ") and cells[0].isdigit():
            number = int(cells[0])
            if number in out:
                raise ValueError(f"patterns.md: duplicate source resource pattern:P{number}")
            out[number] = cells
    return out, head


def load_delegation(kit_dir):
    """Return axis rows, step rows, combination prose, and table headings."""
    path = Path(kit_dir) / "delegation.md"
    axes, steps, combine, heads = {}, {}, [], {}
    if not path.is_file():
        return axes, steps, combine, heads
    in_combine = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_combine = line.startswith("## How the axes combine")
            continue
        if in_combine and line.strip():
            combine.append(line)
        cells = [cell.strip() for cell in line.strip().strip("|").split(" | ")]
        if line.startswith("| #"):
            heads["axis"] = cells
        elif line.startswith("| Step"):
            heads["step"] = cells
        elif line.startswith("| ") and cells[0].isdigit():
            kind = "axis" if "axis" in heads and "step" not in heads else "step"
            table = axes if kind == "axis" else steps
            number = int(cells[0])
            if number in table:
                raise ValueError(f"delegation.md: duplicate source resource delegation:{kind}{number}")
            table[number] = cells
    return axes, steps, combine, heads


def load_rich_resources(kit_dir):
    path = Path(kit_dir) / "resources.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("resources.json: expected an array of resource objects")
    return data


def _resource_rows(kit_dir):
    """Normalize references to source records without copying a content store."""
    rows = []
    for kind, filename in (("lego", "legos.csv"), ("rule", "rules.csv")):
        for row in read_csv(kit_dir, filename):
            rows.append(dict(kind=kind, id=row.get("id", ""),
                             name=row.get("name", row.get("topic", "")),
                             summary=row.get("summary", row.get("rule", "")),
                             source_file=filename, fields=row))
    patterns, head = load_patterns(kit_dir)
    for number, cells in patterns.items():
        fields = dict(zip(head, cells))
        rows.append(dict(kind="pattern", id=f"P{number}", name=fields.get("Pattern", ""),
                         summary=fields.get("What it is", ""), source_file="patterns.md", fields=fields))
    axes, steps, combine, heads = load_delegation(kit_dir)
    delegation_path = Path(kit_dir) / "delegation.md"
    source_context = [line for line in delegation_path.read_text(encoding="utf-8").splitlines()
                      if line.startswith("**Certainty.**")] if delegation_path.exists() else []
    for kind, table in (("axis", axes), ("step", steps)):
        for number, cells in table.items():
            fields = dict(zip(heads[kind], cells))
            if source_context:
                fields["source_context"] = source_context
            rows.append(dict(kind="delegation", id=f"{kind}{number}", name=cells[1],
                             summary=cells[2], source_file="delegation.md", fields=fields))
    if combine:
        rows.append(dict(kind="delegation", id="combine", name="How the axes combine",
                         summary="Apply the delegation axes together to choose a bounded level of authority.",
                         source_file="delegation.md", fields={"instructions": combine, "source_context": source_context}))
    for row in load_rich_resources(kit_dir):
        if not isinstance(row, dict):
            raise ValueError("resources.json: every resource must be an object")
        rows.append(dict(kind=row.get("kind", ""), id=row.get("id", ""),
                         name=row.get("name", ""), summary=row.get("summary", ""),
                         source_file="resources.json", fields=row))
    return rows


def load_resources(kit_dir):
    resources = {}
    for resource in _resource_rows(kit_dir):
        key = resource["kind"], resource["id"]
        if key in resources:
            raise ValueError(f"duplicate source resource {key[0]}:{key[1]}")
        resources[key] = resource
    return resources


def _rich_errors(rows):
    errors = []
    text_fields = ("id", "kind", "name", "summary", "when_to_use", "certainty", "limitations", "checked_on", "host_scope")
    list_fields = ("prerequisites", "instructions", "applicable_standards", "verification", "sources")
    for index, row in enumerate(rows, 1):
        label = f"resources.json entry {index}"
        if not isinstance(row, dict):
            errors.append(f"{label}: expected a resource object")
            continue
        for field in text_fields:
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{label}: {field} must be a nonempty string")
        for field in list_fields:
            value = row.get(field)
            if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{label}: {field} must be an array of nonempty strings")
            elif field in {"instructions", "verification", "sources"} and not value:
                errors.append(f"{label}: {field} must not be empty")
        if not isinstance(row.get("kind"), str) or row["kind"] not in RICH_KINDS:
            errors.append(f"{label}: kind must be one of {', '.join(sorted(RICH_KINDS))}")
        if not isinstance(row.get("id"), str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row["id"]):
            errors.append(f"{label}: id must be a lowercase slug")
        if not isinstance(row.get("certainty"), str) or row["certainty"] not in CERTAINTIES:
            errors.append(f"{label}: certainty must be one of {', '.join(sorted(CERTAINTIES))}")
        try:
            checked = row.get("checked_on", "")
            if not isinstance(checked, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", checked):
                raise ValueError
            date.fromisoformat(checked)
        except (TypeError, ValueError):
            errors.append(f"{label}: checked_on must be an ISO date (YYYY-MM-DD)")
        for source in row.get("sources", []) if isinstance(row.get("sources"), list) else []:
            try:
                url = urlsplit(source) if isinstance(source, str) else None
                if url is None or url.scheme not in {"http", "https"} or not url.netloc or any(c.isspace() for c in source):
                    raise ValueError
            except ValueError:
                errors.append(f"{label}: sources must contain HTTP(S) URLs")
        if "category" in row:
            errors.append(f"{label}: category belongs only in catalog.csv")
    return errors


def validate_catalog(kit_dir):
    """Return actionable diagnostics for the maintained taxonomy and all source assignments."""
    errors = []
    try:
        categories, assignments = load_categories(kit_dir), load_catalog(kit_dir)
        errors.extend(_rich_errors(load_rich_resources(kit_dir)))
        resources = _resource_rows(kit_dir)
    except (OSError, ValueError, csv.Error, IndexError, KeyError) as exc:
        return errors + [str(exc)]
    by_id = {}
    for row in categories:
        cid, parent, name = (row.get(field) or "" for field in ("id", "parent", "name"))
        if cid in by_id:
            errors.append(f"categories.csv: duplicate category {cid}")
        by_id[cid] = row
        if not name.strip():
            errors.append(f"categories.csv: category {cid} needs a name")
        if not parent and not re.fullmatch(r"0[1-5]", cid):
            errors.append(f"categories.csv: invalid parent category {cid}; expected 01 through 05")
        if parent and (not re.fullmatch(r"[1-5]\.[1-9]\d*", cid) or cid.split(".")[0] != parent.lstrip("0")):
            errors.append(f"categories.csv: invalid leaf {cid} for parent {parent}")
    for cid, row in by_id.items():
        parent = row.get("parent")
        if parent and (parent not in by_id or by_id[parent].get("parent")):
            errors.append(f"categories.csv: category {cid} has unknown or non-root parent {parent}")
        if not parent and not any(child.get("parent") == cid for child in categories):
            errors.append(f"categories.csv: parent {cid} has no leaves")
    source_counts = Counter()
    for resource in resources:
        kind, rid = resource["kind"], resource["id"]
        if not isinstance(kind, str) or not isinstance(rid, str) or not kind or not rid:
            errors.append("source resource needs nonempty string kind and id")
            continue
        source_counts[kind, rid] += 1
    for (kind, rid), count in source_counts.items():
        if count > 1:
            errors.append(f"duplicate source resource {kind}:{rid}")
    assigned = Counter()
    for row in assignments:
        kind, rid, cid = (row.get(field) or "" for field in ("kind", "id", "category"))
        key = kind, rid
        assigned[key] += 1
        if key not in source_counts:
            errors.append(f"catalog.csv: unknown resource {kind}:{rid}")
        if cid not in by_id or not by_id[cid].get("parent"):
            errors.append(f"catalog.csv: {kind}:{rid} category {cid} must name a leaf")
        if not (row.get("rationale") or "").strip():
            errors.append(f"catalog.csv: {kind}:{rid} needs a nonempty rationale")
    for (kind, rid), count in assigned.items():
        if count > 1:
            errors.append(f"catalog.csv: duplicate assignment for {kind}:{rid}")
    for kind, rid in sorted(source_counts.keys() - assigned.keys()):
        errors.append(f"catalog.csv: missing assignment for {kind}:{rid}")
    return errors


def _bounded(value, limit):
    value = " ".join(value.split())
    return value if len(value) <= limit else value[:limit - 1] + "…"


def browse_lines(kit_dir, category=None):
    """Show roots, a parent's leaves, or one leaf's bounded resource summaries."""
    categories, assignments = load_categories(kit_dir), load_catalog(kit_dir)
    counts = Counter(row["category"] for row in assignments)
    if category is None:
        return [f"{row['id']}\t{row['name']}\t{sum(counts[leaf['id']] for leaf in categories if leaf['parent'] == row['id'])} resources"
                for row in categories if not row["parent"]]
    matches = [row for row in categories if row["id"] == category]
    if len(matches) != 1:
        raise ValueError(f"Category `{category}` does not exist uniquely. Next step: run `kit browse`.")
    if not matches[0]["parent"]:
        return [f"{row['id']}\t{row['name']}\t{counts[row['id']]} resources"
                for row in categories if row["parent"] == category]
    resources = load_resources(kit_dir)
    lines = []
    for row in assignments:
        if row["category"] == category:
            key = row["kind"], row["id"]
            if key not in resources:
                raise ValueError(f"catalog.csv: unknown resource {key[0]}:{key[1]}")
            resource = resources[key]
            lines.append(f"{key[0]}:{key[1]}\t{_bounded(resource['name'], NAME_LIMIT)}\t{_bounded(resource['summary'], SUMMARY_LIMIT)}")
    return lines


def inspect_lines(kit_dir, query):
    """Resolve one exact kind:id and include its category, source record, and full fields."""
    if query.count(":") != 1 or not all(query.split(":")):
        raise ValueError("Expected one exact kind:id. Next step: run `kit browse`.")
    key = tuple(query.split(":"))
    resources = load_resources(kit_dir)
    if key not in resources:
        raise ValueError(f"Resource `{query}` does not exist. Next step: run `kit browse`.")
    assignments = [row for row in load_catalog(kit_dir) if (row["kind"], row["id"]) == key]
    if len(assignments) != 1:
        raise ValueError(f"Resource `{query}` needs exactly one catalog assignment.")
    assignment = assignments[0]
    categories = {row["id"]: row for row in load_categories(kit_dir)}
    category = categories.get(assignment["category"])
    if not category or not category["parent"]:
        raise ValueError(f"Resource `{query}` needs a valid leaf category.")
    resource = resources[key]
    lines = [f"resource: {query}", f"category: {category['id']} {category['name']}",
             f"rationale: {assignment['rationale']}", f"source_file: {resource['source_file']}"]
    for field, value in resource["fields"].items():
        if isinstance(value, list):
            lines.append(f"{field}:")
            lines.extend(f"- {item}" for item in value)
        else:
            lines.append(f"{field}: {value}")
    if key[0] == "rule":
        for gate in read_csv(kit_dir, "gates.csv"):
            if gate.get("id") == key[1] and gate.get("gate") == "yes":
                lines.extend(f"{field}: {value}" for field, value in gate.items() if field != "id")
    return lines
