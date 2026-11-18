"""Focused public catalog checks; these establish discovery, not host behavior."""
from conftest import KIT_CLI, run


def test_team_arrangement_can_be_found_without_a_factory():
    listed = run(KIT_CLI, 'list', 'G')
    assert listed.returncode == 0
    assert 'Team responsibilities and review' in listed.stdout
    result = run(KIT_CLI, 'show', 'G13')
    assert result.returncode == 0
    assert 'certainty: inferred' in result.stdout
    assert 'team-workflow/TEAM.md' in result.stdout


def test_task_contract_and_flow_are_retrievable_without_team_setup():
    result = run(KIT_CLI, 'show', 'G14')
    assert result.returncode == 0
    assert 'certainty: inferred' in result.stdout
    assert 'team-workflow/TASKS.md' in result.stdout
    assert 'manual' in result.stdout.lower()
