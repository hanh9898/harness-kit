"""Validate the published M2 examples without adding a kit dependency."""
import json
import re

import pytest

from conftest import KIT


def unique_object(pairs):
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise ValueError("duplicate JSON keys")
    return obj


def reject_constant(value):
    raise ValueError(f"non-standard JSON number: {value}")


def decode(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


DOC = (KIT / "M2-CONFIG.md").read_text(encoding="utf-8")
SCHEMA = decode(re.search(r"^```yaml\n(.*?)^```$", DOC, re.M | re.S)[1])
EXAMPLES = {
    value.get("target_profile", value.get("mode")): value
    for value in map(decode, re.findall(r"^```json\n(.*?)^```$", DOC, re.M | re.S))
}


def matches(value, schema):
    """Exercise only the keywords used in the documented JSON Schema."""
    assert schema.keys() <= {
        "$schema", "$defs", "$ref", "type", "const", "enum", "minLength",
        "properties", "additionalProperties", "required", "oneOf", "anyOf", "not",
    }
    if "$ref" in schema:
        pointer = schema["$ref"].removeprefix("#/$defs/")
        if not matches(value, SCHEMA["$defs"][pointer]):
            return False
    if "type" in schema:
        if type(value) is not {"object": dict, "integer": int, "string": str}[schema["type"]]:
            return False
    if "const" in schema and value != schema["const"]:
        return False
    if "enum" in schema and value not in schema["enum"]:
        return False
    if "minLength" in schema and len(value) < schema["minLength"]:
        return False
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if not set(schema.get("required", ())) <= value.keys():
            return False
        if schema.get("additionalProperties") is False and not value.keys() <= properties.keys():
            return False
        if not all(matches(value[key], properties[key]) for key in value.keys() & properties.keys()):
            return False
    return (
        ("oneOf" not in schema or sum(matches(value, sub) for sub in schema["oneOf"]) == 1)
        and ("anyOf" not in schema or any(matches(value, sub) for sub in schema["anyOf"]))
        and ("not" not in schema or not matches(value, schema["not"]))
    )


def accepts(value):
    if not matches(value, SCHEMA):
        return False
    for key, ref in value.items():
        if key.endswith("_ref") or key == "instance_id":
            if not ref.isprintable() or ref != ref.strip():
                return False
    return value.get("target_profile") != "repo-and-bot" or value["repo_ref"] != value["bot_ref"]


TARGETS = {
    "repo-only": {"repo_ref"},
    "bot-only": {"bot_ref"},
    "repo-and-bot": {"repo_ref", "bot_ref"},
}
MODES = {
    "interactive": set(),
    "persistent-bot": {"instance_id", "adapter_ref", "checkpoint_ref"},
}


def test_docs_cover_exact_profiles_and_modes():
    assert set(EXAMPLES) == TARGETS.keys() | MODES.keys()


@pytest.mark.parametrize("example,required_refs", {**TARGETS, **MODES}.items())
def test_config_examples_accept_only_their_allowed_refs(example, required_refs):
    value = EXAMPLES[example]
    assert accepts(value)
    assert required_refs <= value.keys()
    controlled_refs = set().union(*(TARGETS if example in TARGETS else MODES).values())
    optional_refs = {"adapter_ref"} if example == "interactive" else set()
    assert value.keys() & (controlled_refs - required_refs) <= optional_refs
    required = required_refs | {"version", "scope_ref"}
    if example in TARGETS:
        required |= {"target_profile", "owner_ref"}
    else:
        required.add("mode")
    for field in required:
        assert not accepts({key: val for key, val in value.items() if key != field}), (example, field)
    for field in controlled_refs - required_refs - optional_refs:
        assert not accepts(dict(value, **{field: "forbidden:ref"})), (example, field)


def test_interactive_may_pin_an_adapter_without_a_persistent_instance():
    assert accepts(dict(EXAMPLES["interactive"], adapter_ref="binding:manual"))


def test_rejects_unrecognized_variants_and_extra_fields():
    assert not accepts(dict(EXAMPLES["repo-only"], target_profile="repo"))
    assert not accepts(dict(EXAMPLES["interactive"], mode="active"))
    assert not accepts(dict(EXAMPLES["bot-only"], product_tracker_ref="tracker:product"))
    assert not accepts(dict(EXAMPLES["persistent-bot"], trigger_enabled=True))


def test_rejects_repo_and_bot_refs_that_point_to_the_same_target():
    both = EXAMPLES["repo-and-bot"]
    assert not accepts(dict(both, bot_ref=both["repo_ref"]))


@pytest.mark.parametrize("ref", ["", " ", " leading", "trailing ", "line\nbreak", None, 1])
def test_rejects_invalid_reference_values(ref):
    assert not accepts(dict(EXAMPLES["repo-only"], repo_ref=ref))
    assert not accepts(dict(EXAMPLES["persistent-bot"], instance_id=ref))


@pytest.mark.parametrize("version", [True, 1.0, "1", None, 0, 2])
def test_rejects_non_v1_or_non_integer_version(version):
    assert not accepts(dict(EXAMPLES["repo-only"], version=version))
    assert not accepts(dict(EXAMPLES["interactive"], version=version))


@pytest.mark.parametrize("text", ['{"version": 1, "version": 1}', "NaN", "Infinity", "-Infinity"])
def test_json_interchange_rejects_duplicate_keys_and_nonstandard_numbers(text):
    with pytest.raises(ValueError):
        decode(text)
