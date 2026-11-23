"""Durable resource selection through the confirmed public operation seam."""
import csv
import json
import re
import shutil

import pytest

from conftest import ROOT, run

CLI = ROOT / 'kit/scripts/library'


def invoke(root, *args):
    return run(CLI, '--store', root / 'library.sqlite3', *args)


def decision(root, **changes):
    value = dict(owner='Report author', scope='personal',
                 decision=dict(authority='User requested this scoped library change',
                               rationale='Keep selection intentional', methods=[], standards=['kit:6.09']),
                 evidence=['Consumer bytes inspected'], continuation='Inspect selection before further changes.')
    value.update(changes)
    path = root / 'decision.json'
    path.write_text(json.dumps(value))
    return path


def change(root, command, expected, source='supplied', id='H14', **changes):
    return invoke(root, command, id, '--source', source, '--kit-dir', root / 'kit',
                  '--input', decision(root, **changes), '--expect-selection-revision', expected)


def selection(root, source='supplied', id='H14', history=False):
    r = invoke(root, 'selection-history' if history else 'selection', id,
               '--source', source, '--kit-dir', root / 'kit')
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def supplied(root):
    shutil.copytree(ROOT / 'kit', root / 'kit')


def update_supplied(root):
    path = root / 'kit/legos.csv'
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row['id'] == 'H14':
            row['name'] = 'Updated hook policy'
            row['detail'] = 'New distribution content, not consumer adoption.'
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)


def test_exclusion_survives_supplied_update_and_explicit_restore_preserves_provenance(tmp_path):
    supplied(tmp_path)
    consumer = tmp_path / 'consumer.md'
    consumer.write_text('Applied original hook policy\n')
    assert selection(tmp_path)['enabled'] is True
    assert not (tmp_path / 'library.sqlite3').exists()
    disabled = change(tmp_path, 'disable', 0)
    assert disabled.returncode == 0, disabled.stderr
    before = selection(tmp_path)
    assert before['enabled'] is False and before['revision'] == 1
    update_supplied(tmp_path)
    result = invoke(tmp_path, 'search', 'H14', '--kit-dir', tmp_path / 'kit')
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['matches'] == []
    assert selection(tmp_path)['record'] == before['record']
    restored = change(tmp_path, 'restore', 1)
    assert restored.returncode == 0, restored.stderr
    result = json.loads(invoke(tmp_path, 'search', 'H14', '--kit-dir', tmp_path / 'kit').stdout)
    assert result['matches'][0]['name'] == 'Updated hook policy'
    history = selection(tmp_path, history=True)
    assert [r['enabled'] for r in history] == [False, True]
    assert history[0] == before['record']
    assert history[0]['snapshot'] != history[1]['snapshot']
    assert history[1]['owner'] == 'Report author'
    assert history[1]['continuation'] == 'Inspect selection before further changes.'
    assert consumer.read_text() == 'Applied original hook policy\n'


def test_supplied_patterns_and_delegation_use_the_same_explicit_selection_boundary(tmp_path):
    supplied(tmp_path)
    for identity in ('P6', 'axis1', 'step2', 'combine', '6.09'):
        r = change(tmp_path, 'disable', 0, id=identity)
        assert r.returncode == 0, (identity, r.stderr)
        state = selection(tmp_path, id=identity)
        assert state['available'] and not state['effective']
        assert state['record']['snapshot']
        assert change(tmp_path, 'restore', 1, id=identity).returncode == 0
        assert selection(tmp_path, id=identity)['effective']


@pytest.mark.parametrize('identity, filename, entry', [
    ('P6', 'patterns.md', r'^\| 6 \|.*\n'),
    ('axis1', 'delegation.md', r'^\| 1 \| Reversibility.*\n'),
    ('step2', 'delegation.md', r'^\| 2 \| Sell.*\n'),
    ('combine', 'delegation.md', r'^## How the axes combine.*\n(?s:.*?)(?=^## |\Z)'),
])
def test_exclusion_survives_removed_markdown_entry(tmp_path, identity, filename, entry):
    supplied(tmp_path)
    disabled = change(tmp_path, 'disable', 0, id=identity)
    assert disabled.returncode == 0, disabled.stderr
    before = json.loads(disabled.stdout)
    path = tmp_path / 'kit' / filename
    original = path.read_text(encoding='utf-8')
    without_entry, removed = re.subn(entry, '', original, flags=re.MULTILINE)
    assert removed == 1
    path.write_text(without_entry, encoding='utf-8')

    state = selection(tmp_path, id=identity)
    assert state == {**before, 'available': False, 'effective': False, 'current_snapshot': None}
    failed = change(tmp_path, 'restore', 1, id=identity)
    assert failed.returncode == 2 and 'Resource unavailable' in failed.stderr and not failed.stdout
    assert selection(tmp_path, id=identity, history=True) == [before['record']]

    path.write_text(original, encoding='utf-8')
    assert selection(tmp_path, id=identity) == before
    restored = change(tmp_path, 'restore', 1, id=identity)
    assert restored.returncode == 0, restored.stderr
    after = json.loads(restored.stdout)
    assert after['revision'] == 2 and after['effective']
    assert selection(tmp_path, id=identity, history=True) == [before['record'], after['record']]


@pytest.mark.parametrize('damage', ['invalid-text', 'directory'])
def test_selection_fails_when_pattern_catalog_cannot_be_read(tmp_path, damage):
    supplied(tmp_path)
    assert change(tmp_path, 'disable', 0, id='P6').returncode == 0
    path = tmp_path / 'kit/patterns.md'
    if damage == 'invalid-text':
        path.write_bytes(b'\xff')
    else:
        path.unlink()
        path.mkdir()

    failed = invoke(tmp_path, 'selection', 'P6', '--source', 'supplied', '--kit-dir', tmp_path / 'kit')
    assert failed.returncode == 2 and not failed.stdout
    assert 'Cannot inspect supplied resource' in failed.stderr
    assert 'patterns.md' in failed.stderr
    assert len(selection(tmp_path, id='P6', history=True)) == 1


def test_content_edits_and_colliding_saved_ids_do_not_clear_supplied_exclusion(tmp_path):
    from test_library_cli import draft, save
    supplied(tmp_path)
    origin = dict(reference='kit:H14', revision='old-origin', snapshot='Original hook policy')
    assert save(tmp_path, draft(id='H14', name='Personal hook', origin=origin)).returncode == 0
    assert change(tmp_path, 'disable', 0).returncode == 0
    found = json.loads(invoke(tmp_path, 'search', 'H14', '--kit-dir', tmp_path / 'kit').stdout)
    assert [r['origin'] for r in found['matches']] == ['saved']
    assert change(tmp_path, 'disable', 0, source='saved').returncode == 0
    assert save(tmp_path, draft(id='H14', name='Personal hook', content='Independent customization edit', origin=origin), 1).returncode == 0
    assert not selection(tmp_path, source='saved')['effective']
    assert change(tmp_path, 'restore', 1, source='saved').returncode == 0
    assert not selection(tmp_path)['effective']
    content = json.loads(invoke(tmp_path, 'show', 'H14').stdout)
    assert content['revision'] == 2 and content['resource']['content'] == 'Independent customization edit'
    assert content['resource']['origin'] == origin
    assert len(json.loads(invoke(tmp_path, 'history', 'H14').stdout)) == 2


def test_exclusion_survives_absence_reappearance_and_store_relocation(tmp_path):
    supplied(tmp_path)
    assert change(tmp_path, 'disable', 0).returncode == 0
    path = tmp_path / 'kit/legos.csv'
    original = path.read_text()
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader()
        writer.writerows(row for row in rows if row['id'] != 'H14')
    state = selection(tmp_path)
    assert not state['available'] and not state['enabled']
    assert change(tmp_path, 'restore', 1).returncode != 0
    assert len(selection(tmp_path, history=True)) == 1
    path.write_text(original)
    moved = tmp_path / 'moved'; moved.mkdir()
    shutil.copytree(tmp_path / 'kit', moved / 'kit')
    shutil.copy2(tmp_path / 'library.sqlite3', moved / 'library.sqlite3')
    assert not selection(moved)['effective']
    result = json.loads(invoke(moved, 'search', 'H14', '--kit-dir', moved / 'kit', '--include-disabled').stdout)
    assert result['matches'][0]['enabled'] is False
    assert result['excluded'] == 1
    assert selection(moved, history=True) == selection(tmp_path, history=True)


def test_stale_and_duplicate_selection_changes_reconcile_without_new_effects(tmp_path):
    supplied(tmp_path)
    assert change(tmp_path, 'disable', 0).returncode == 0
    for command, expected in (('disable', 0), ('disable', 1), ('restore', 0)):
        failed = change(tmp_path, command, expected)
        assert failed.returncode != 0 and not failed.stdout
    assert len(selection(tmp_path, history=True)) == 1
    assert change(tmp_path, 'restore', 1).returncode == 0
    assert change(tmp_path, 'disable', 1).returncode != 0
    assert change(tmp_path, 'restore', 2).returncode != 0
    assert selection(tmp_path)['effective']
    assert len(selection(tmp_path, history=True)) == 2


def test_invalid_selection_facts_unknown_identity_and_failed_storage_keep_state(tmp_path):
    supplied(tmp_path)
    for facts in ({'owner': ''}, {'scope': 'project'}, {'decision': {}}, {'evidence': 'asserted'}, {'continuation': ''}):
        assert change(tmp_path, 'disable', 0, **facts).returncode != 0
        assert not (tmp_path / 'library.sqlite3').exists()
    assert change(tmp_path, 'disable', 0, id='missing').returncode != 0
    assert not (tmp_path / 'library.sqlite3').exists()
    assert change(tmp_path, 'disable', 0).returncode == 0
    for facts in ({'owner': 'Other author'}, {'scope': 'project:/elsewhere'}):
        assert change(tmp_path, 'restore', 1, **facts).returncode != 0
    assert len(selection(tmp_path, history=True)) == 1
    (tmp_path / 'library.sqlite3').write_bytes(b'corrupt store')
    failed = change(tmp_path, 'restore', 1)
    assert failed.returncode != 0 and not failed.stdout
    assert (tmp_path / 'library.sqlite3').read_bytes() == b'corrupt store'
    assert invoke(tmp_path, 'search', 'H14', '--kit-dir', tmp_path / 'kit').returncode != 0


def test_competing_selection_writers_preserve_one_decision(tmp_path):
    import subprocess
    import sys
    supplied(tmp_path)
    payload = decision(tmp_path)
    command = [sys.executable, '-I', str(CLI), '--store', str(tmp_path / 'library.sqlite3'),
               'disable', 'H14', '--source', 'supplied', '--kit-dir', str(tmp_path / 'kit'),
               '--input', str(payload), '--expect-selection-revision', '0']
    writers = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
    results = [(p.communicate(), p.returncode) for p in writers]
    assert sorted(code for _, code in results) == [0, 2]
    assert len(selection(tmp_path, history=True)) == 1
    assert not selection(tmp_path)['effective']


def test_content_and_selection_writers_both_commit_without_lost_updates(tmp_path):
    import subprocess
    import sys
    from test_library_cli import draft, save
    supplied(tmp_path)
    assert save(tmp_path, draft(id='H14')).returncode == 0
    edit = tmp_path / 'edit.json'; edit.write_text(json.dumps(draft(id='H14', content='Independent updated content')))
    base = [sys.executable, '-I', str(CLI), '--store', str(tmp_path / 'library.sqlite3')]
    commands = [base + ['save', '--input', str(edit), '--expect-revision', '1'],
                base + ['disable', 'H14', '--source', 'saved', '--kit-dir', str(tmp_path / 'kit'),
                        '--input', str(decision(tmp_path)), '--expect-selection-revision', '0']]
    writers = [subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for c in commands]
    results = [(p.communicate(), p.returncode) for p in writers]
    assert all(code == 0 for _, code in results), results
    assert not selection(tmp_path, source='saved')['effective']
    current = json.loads(invoke(tmp_path, 'show', 'H14').stdout)
    assert current['revision'] == 2 and current['resource']['content'] == 'Independent updated content'


def test_direct_saved_retrieval_exposes_exclusion_without_hiding_provenance(tmp_path):
    from test_library_cli import draft, save
    supplied(tmp_path)
    assert save(tmp_path, draft(id='H14')).returncode == 0
    assert change(tmp_path, 'disable', 0, source='saved').returncode == 0
    current = json.loads(invoke(tmp_path, 'show', 'H14').stdout)
    assert current['selection']['enabled'] is False
    assert current['resource']['content'] == draft()['content']
    assert current['revision'] == 1
