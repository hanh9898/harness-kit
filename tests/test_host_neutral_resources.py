"""Keep host implementation details out of the active library's normative guidance."""
import importlib.util
import re

from conftest import KIT

SPEC = importlib.util.spec_from_file_location("resource_catalog", KIT / "catalog.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)

HOST_DETAILS = re.compile(
    r"claude|codex|anthropic|openai|\bpi\b|"
    r"PreToolUse|PostToolUse|SubagentStop|TeammateIdle|TaskCompleted|"
    r"InstructionsLoaded|permissionDecision|bypassPermissions|onFailure|"
    r"skillOverrides|skillListingBudgetFraction|stop_hook_active|"
    r"allowedTools|disallowedTools|max_turns|tool_use_id|custom_id|claude_args|"
    r"--dangerously-skip-permissions|/doctor",
    re.I,
)
PROVENANCE_FIELDS = {"source", "sources", "source_context", "limitations", "checked_on"}


def test_active_guidance_has_no_host_names_or_proprietary_controls():
    # A lexical regression check supplements the editorial review; it cannot prove portability.
    for key, resource in catalog.load_resources(KIT).items():
        for field, value in resource["fields"].items():
            if field.casefold() in PROVENANCE_FIELDS:
                continue
            text = "\n".join(value) if isinstance(value, list) else str(value)
            assert not HOST_DETAILS.search(text), (key, field, text)
    for category in catalog.load_categories(KIT):
        assert not HOST_DETAILS.search(category["name"]), category


def test_provenance_is_retained_without_becoming_a_host_requirement():
    resources = catalog.load_resources(KIT)
    source_values = [str(value) for resource in resources.values()
                     for field, value in resource["fields"].items()
                     if field.casefold() in {"source", "sources"}]
    assert any("https://" in value for value in source_values)
    assert any(HOST_DETAILS.search(value) for value in source_values)
