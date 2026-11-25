"""Durable resource selection through the confirmed public operation seam."""
import csv
import json
import os
import re
import shlex
import shutil
import sqlite3
import subprocess
from contextlib import closing

import pytest

from conftest import ROOT, row, run, write_kit, write_piece_aliases

CLI = ROOT / 'kit/scripts/library'
REREAD = 'reread-source-before-write'


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


def change(root, command, expected, source='supplied', id=REREAD, **changes):
    return invoke(root, command, id, '--source', source, '--kit-dir', root / 'kit',
                  '--input', decision(root, **changes), '--expect-selection-revision', expected)


def selection(root, source='supplied', id=REREAD, history=False):
    r = invoke(root, 'selection-history' if history else 'selection', id,
               '--source', source, '--kit-dir', root / 'kit')
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def supplied(root):
    shutil.copytree(ROOT / 'kit', root / 'kit')


def initialize_empty_store(store):
    with closing(sqlite3.connect(store)) as db:
        db.execute('VACUUM')


def upgrade_catalog(root, keep_legacy_id=False):
    catalog = root / 'kit'
    piece = row(REREAD if not keep_legacy_id else 'H14', group='H', name='Read live source',
                detail='Refresh the source before recording a decision.')
    if not keep_legacy_id:
        piece.update(detail='Updated guidance: distinguish unreadable sources from empty results.')
    write_kit(catalog, [piece])
    if keep_legacy_id:
        (catalog / 'piece-aliases.csv').unlink(missing_ok=True)
    else:
        write_piece_aliases(catalog, ('H14', REREAD))
    (catalog / 'rules.csv').write_text('id,rule,source,certainty\n')


def test_slug_upgrade_keeps_legacy_selection_stream_after_content_change(tmp_path):
    from test_library_cli import draft, save

    upgrade_catalog(tmp_path, keep_legacy_id=True)
    assert save(tmp_path, draft(id='H14')).returncode == 0
    disabled = change(tmp_path, 'disable', 0, id='H14')
    assert disabled.returncode == 0, disabled.stderr
    previous = selection(tmp_path, id='H14', history=True)
    store = tmp_path / 'library.sqlite3'
    before = store.read_bytes()

    upgrade_catalog(tmp_path)
    state = selection(tmp_path, id=REREAD)
    assert selection(tmp_path, id='H14') == state
    assert (state['id'], state['revision'], state['effective']) == (REREAD, 1, False)
    assert state['record'] == previous[0]
    assert state['current_snapshot']['reference'] == f'legos.csv#{REREAD}'
    assert state['current_snapshot']['resource']['detail'] != previous[0]['snapshot']['resource']['detail']
    assert selection(tmp_path, id=REREAD, history=True) == previous
    assert store.read_bytes() == before

    search = ('search', 'H14', '--kit-dir', tmp_path / 'kit')
    visible = json.loads(invoke(tmp_path, *search).stdout)
    assert visible['excluded'] == 1
    assert [(hit['id'], hit['origin']) for hit in visible['matches']] == [('H14', 'saved')]
    visible = json.loads(invoke(tmp_path, *search, '--include-disabled').stdout)
    supplied_match, = [hit for hit in visible['matches'] if hit['origin'] == 'supplied']
    assert (supplied_match['id'], supplied_match['enabled']) == (REREAD, False)
    assert shlex.split(supplied_match['retrieve'])[-1] == REREAD

    old_write = change(tmp_path, 'restore', 1, id='H14')
    assert old_write.returncode == 2 and REREAD in old_write.stderr
    restored = change(tmp_path, 'restore', 1, id=REREAD)
    assert restored.returncode == 0, restored.stderr
    assert json.loads(restored.stdout)['effective']
    after = selection(tmp_path, id=REREAD, history=True)
    assert after[:-1] == previous
    assert (after[-1]['id'], after[-1]['revision'], after[-1]['snapshot']['reference']) == (
        REREAD, 2, f'legos.csv#{REREAD}')
    assert selection(tmp_path, id='H14', history=True) == after
    assert selection(tmp_path, source='saved', id='H14')['effective']


def test_slug_upgrade_keeps_previously_restored_state(tmp_path):
    upgrade_catalog(tmp_path, keep_legacy_id=True)
    assert change(tmp_path, 'disable', 0, id='H14').returncode == 0
    assert change(tmp_path, 'restore', 1, id='H14').returncode == 0
    upgrade_catalog(tmp_path)
    state = selection(tmp_path, id=REREAD)
    assert (state['effective'], state['revision'], state['record']['action']) == (True, 2, 'restore')


def test_slug_upgrade_keeps_first_slug_disable_visible_to_old_catalog(tmp_path):
    upgrade_catalog(tmp_path)
    assert change(tmp_path, 'disable', 0, id=REREAD).returncode == 0
    upgrade_catalog(tmp_path, keep_legacy_id=True)
    state = selection(tmp_path, id='H14')
    assert (state['effective'], state['revision']) == (False, 1)
    assert state['record']['id'] == REREAD


def test_slug_upgrade_lists_retired_piece_history(tmp_path):
    upgrade_catalog(tmp_path, keep_legacy_id=True)
    assert change(tmp_path, 'disable', 0, id='H14').returncode == 0
    previous = selection(tmp_path, id='H14', history=True)
    upgrade_catalog(tmp_path)
    write_kit(tmp_path / 'kit', [])
    assert selection(tmp_path, id=REREAD, history=True) == previous
    state = selection(tmp_path, id=REREAD)
    assert (state['available'], state['enabled'], state['revision']) == (False, False, 1)
    (tmp_path / 'kit/legos.csv').unlink()
    assert selection(tmp_path, id=REREAD, history=True) == previous


def test_slug_upgrade_resolves_history_at_selected_catalog_path(tmp_path):
    upgrade_catalog(tmp_path, keep_legacy_id=True)
    assert change(tmp_path, 'disable', 0, id='H14').returncode == 0
    upgrade_catalog(tmp_path)
    moved = tmp_path / 'moved catalog'
    (tmp_path / 'kit').rename(moved)
    args = ('--source', 'supplied', '--kit-dir', moved)
    result = invoke(tmp_path, 'selection', REREAD, *args)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['effective'] is False
    history = invoke(tmp_path, 'selection-history', REREAD, *args)
    assert history.returncode == 0, history.stderr
    assert [record['id'] for record in json.loads(history.stdout)] == ['H14']
    assert selection(tmp_path, id='H14', history=True) == json.loads(history.stdout)


def test_slug_upgrade_does_not_merge_conflicting_streams(tmp_path):
    upgrade_catalog(tmp_path, keep_legacy_id=True)
    assert change(tmp_path, 'disable', 0, id='H14').returncode == 0
    rename_supplied(tmp_path, 'H14', REREAD, name='Independently named resource')
    assert change(tmp_path, 'disable', 0, id=REREAD).returncode == 0
    upgrade_catalog(tmp_path)
    for args in (('selection', 'H14', '--source', 'supplied'), ('search', REREAD)):
        result = invoke(tmp_path, *args, '--kit-dir', tmp_path / 'kit')
        assert result.returncode == 2
        assert 'Conflicting selection histories' in result.stderr
    assert [record['id'] for record in selection(tmp_path, id=REREAD, history=True)] == ['H14', REREAD]


def update_supplied(root):
    path = root / 'kit/legos.csv'
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row['id'] == REREAD:
            row['name'] = 'Updated hook policy'
            row['detail'] = 'New distribution content, not consumer adoption.'
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)


def rename_supplied(root, old, new, filename='legos.csv', keep_old=False, **changes):
    path = root / 'kit' / filename
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        rows, fields = list(reader), reader.fieldnames
    index, = (i for i, row in enumerate(rows) if row['id'] == old)
    replacement = dict(rows[index], id=new, **changes)
    if keep_old:
        rows.append(replacement)
    else:
        rows[index] = replacement
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def confirm_rename(root, old, new, expected=0, source='supplied', **facts):
    return change(root, 'disable', expected, source=source, id=new, confirm_rename_from=old, **facts)


@pytest.mark.parametrize('old,new,filename', [(REREAD, 'replacement-hook', 'legos.csv'),
                                             ('6.09', '99.09', 'rules.csv')])
def test_supplied_rename_holds_exact_match_without_migrating_history(tmp_path, old, new, filename):
    supplied(tmp_path)
    disabled = change(tmp_path, 'disable', 0, id=old)
    assert disabled.returncode == 0, disabled.stderr
    first = json.loads(disabled.stdout)['record']
    rename_supplied(tmp_path, old, new, filename)

    state = selection(tmp_path, id=new)
    assert state['available'] and not state['enabled'] and not state['effective']
    assert state['revision'] == 0 and state['record'] is None
    assert state['possible_previous_ids'] == [old]
    assert not selection(tmp_path, id=old)['available']
    assert selection(tmp_path, id=old, history=True) == [first]
    assert selection(tmp_path, id=new, history=True) == []
    assert selection(tmp_path, id='evidence-labels')['effective']

    row = first['snapshot']['resource']
    args = ('search', row.get('name') or row['rule'], '--kit-dir', tmp_path / 'kit')
    result = json.loads(invoke(tmp_path, *args).stdout)
    assert result['matches'] == [] and result['excluded'] == 1
    visible = json.loads(invoke(tmp_path, *args, '--include-disabled').stdout)['matches']
    assert [(hit['id'], hit['enabled'], hit['possible_previous_ids']) for hit in visible] == [
        (new, False, [old])]
    restore = change(tmp_path, 'restore', 0, id=new)
    assert restore.returncode == 2 and 'confirm_rename_from' in restore.stderr
    assert selection(tmp_path, id=new, history=True) == []


def test_confirmed_rename_preserves_scope_and_exclusion_through_content_edit(tmp_path):
    supplied(tmp_path)
    missing = confirm_rename(tmp_path, REREAD, 'evidence-labels')
    assert missing.returncode == 2 and not (tmp_path / 'library.sqlite3').exists()
    assert change(tmp_path, 'disable', 0).returncode == 0
    rename_supplied(tmp_path, REREAD, 'replacement-hook')

    for old, expected, facts, error in [
        (None, 0, {}, 'must name a predecessor ID'),
        ('evidence-labels', 0, {}, 'possible predecessor'),
        (REREAD, 0, {'owner': 'Another owner'}, 'Changing selection owner'),
        (REREAD, 0, {'scope': f'project:{tmp_path}'}, 'Changing selection scope'),
        (REREAD, 1, {}, 'Selection revision conflict'),
    ]:
        failed = confirm_rename(tmp_path, old, 'replacement-hook', expected, **facts)
        assert failed.returncode == 2 and error in failed.stderr
    assert selection(tmp_path, id='replacement-hook', history=True) == []

    linked = confirm_rename(tmp_path, REREAD, 'replacement-hook')
    assert linked.returncode == 0, linked.stderr
    state = json.loads(linked.stdout)
    assert not state['effective'] and state['revision'] == 1
    assert state['record']['action'] == 'inherit-disable'
    assert state['record']['renamed_from'] == {'id': REREAD, 'revision': 1}
    assert confirm_rename(tmp_path, REREAD, 'replacement-hook').returncode == 2

    rename_supplied(tmp_path, 'replacement-hook', 'replacement-hook', name='Edited hook')
    after_edit = selection(tmp_path, id='replacement-hook')
    assert not after_edit['effective'] and after_edit['record'] == state['record']
    assert after_edit['current_snapshot']['resource']['name'] == 'Edited hook'
    assert change(tmp_path, 'restore', 1, id='replacement-hook').returncode == 0
    assert selection(tmp_path, id='replacement-hook')['effective']
    assert [record['enabled'] for record in selection(tmp_path, id='replacement-hook', history=True)] == [False, True]
    assert [record['enabled'] for record in selection(tmp_path, history=True)] == [False]


def test_confirmed_rename_predecessor_is_not_reused_after_restore(tmp_path):
    supplied(tmp_path)
    assert change(tmp_path, 'disable', 0).returncode == 0
    rename_supplied(tmp_path, REREAD, 'replacement-hook')
    linked = confirm_rename(tmp_path, REREAD, 'replacement-hook')
    assert json.loads(linked.stdout)['record']['renamed_from']['id'] == REREAD
    assert change(tmp_path, 'restore', 1, id='replacement-hook').returncode == 0
    rename_supplied(tmp_path, 'replacement-hook', 'unrelated-hook')
    assert selection(tmp_path, id='unrelated-hook')['effective']
    assert not selection(tmp_path)['enabled']


def test_rename_hold_respects_live_ids_and_source_boundary(tmp_path):
    from test_library_cli import draft, save
    supplied(tmp_path)
    assert change(tmp_path, 'disable', 0).returncode == 0
    rename_supplied(tmp_path, REREAD, 'replacement-hook', keep_old=True)
    assert selection(tmp_path, id='replacement-hook')['effective']
    assert confirm_rename(tmp_path, REREAD, 'replacement-hook').returncode == 2
    rename_supplied(tmp_path, REREAD, 'unrelated-hook', name='Different hook')
    assert selection(tmp_path, id='unrelated-hook')['effective']
    assert not selection(tmp_path, id='replacement-hook')['effective']

    assert save(tmp_path, draft(id='replacement-hook')).returncode == 0
    assert selection(tmp_path, source='saved', id='replacement-hook')['effective']
    assert confirm_rename(tmp_path, REREAD, 'replacement-hook', source='saved').returncode == 2


def test_rename_hold_lists_ambiguous_candidates_without_choosing(tmp_path):
    supplied(tmp_path)
    rename_supplied(tmp_path, REREAD, 'matching-hook-copy', keep_old=True)
    assert change(tmp_path, 'disable', 0).returncode == 0
    assert change(tmp_path, 'disable', 0, id='matching-hook-copy').returncode == 0
    rename_supplied(tmp_path, REREAD, 'replacement-hook')
    rename_supplied(tmp_path, 'matching-hook-copy', 'unrelated-hook', name='Different hook')

    assert selection(tmp_path, id='replacement-hook')['possible_previous_ids'] == ['matching-hook-copy', REREAD]
    assert selection(tmp_path, id='replacement-hook', history=True) == []
    assert confirm_rename(tmp_path, 'matching-hook-copy', 'replacement-hook').returncode == 0
    lineage = selection(tmp_path, id='replacement-hook')['record']['renamed_from']
    assert lineage == {'id': 'matching-hook-copy', 'revision': 1}
    assert selection(tmp_path, id='replacement-hook')['enabled'] is False


def test_library_skill_selection_command_runs(tmp_path, monkeypatch):
    skill = ROOT / 'skills/harness/harness-library/READ.md'
    template, = re.findall(r'`(library (?:[^`\n]+ )?selection [^`\n]+)`',
                           skill.read_text(encoding='utf-8'))
    store = tmp_path / 'selected library.sqlite3'
    command = template.replace('<selected-path>', shlex.quote(str(store))).replace('<id>', REREAD)
    monkeypatch.setenv('PATH', str(CLI.parent), prepend=os.pathsep)

    missing = subprocess.run(command, shell=True, capture_output=True, text=True)
    assert (missing.returncode, missing.stdout) == (2, '')
    assert f'Store is missing: {store}' in missing.stderr
    assert not store.exists()

    initialize_empty_store(store)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['effective'] is True


def test_exclusion_survives_supplied_update_and_explicit_restore_preserves_provenance(tmp_path):
    supplied(tmp_path)
    consumer = tmp_path / 'consumer.md'
    consumer.write_text('Applied original hook policy\n')
    assert selection(tmp_path)['enabled'] is True
    assert selection(tmp_path, history=True) == []
    assert not (tmp_path / 'library.sqlite3').exists()
    disabled = change(tmp_path, 'disable', 0)
    assert disabled.returncode == 0, disabled.stderr
    before = selection(tmp_path)
    assert before['enabled'] is False and before['revision'] == 1
    update_supplied(tmp_path)
    result = invoke(tmp_path, 'search', REREAD, '--kit-dir', tmp_path / 'kit')
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['matches'] == []
    assert selection(tmp_path)['record'] == before['record']
    restored = change(tmp_path, 'restore', 1)
    assert restored.returncode == 0, restored.stderr
    result = json.loads(invoke(tmp_path, 'search', REREAD, '--kit-dir', tmp_path / 'kit').stdout)
    assert result['matches'][0]['name'] == 'Updated hook policy'
    history = selection(tmp_path, history=True)
    assert [r['enabled'] for r in history] == [False, True]
    assert history[0] == before['record']
    assert history[0]['snapshot'] != history[1]['snapshot']
    assert history[1]['owner'] == 'Report author'
    assert history[1]['continuation'] == 'Inspect selection before further changes.'
    assert consumer.read_text() == 'Applied original hook policy\n'


@pytest.mark.parametrize('command', ['selection', 'selection-history', 'search'])
def test_reads_fail_when_store_symlink_target_goes_missing(tmp_path, command):
    supplied(tmp_path)
    disabled = change(tmp_path, 'disable', 0)
    assert disabled.returncode == 0, disabled.stderr
    store = tmp_path / 'library.sqlite3'
    link = tmp_path / 'store-link'
    link.symlink_to(store.name)
    args = (command, REREAD, '--kit-dir', tmp_path / 'kit')
    if command != 'search':
        args += ('--source', 'supplied')

    live = run(CLI, '--store', link, *args)
    assert live.returncode == 0, live.stderr

    store.rename(tmp_path / 'offline.sqlite3')
    failed = run(CLI, '--store', link, *args)
    assert failed.returncode == 2, failed.stdout
    assert not failed.stdout
    assert f'Store symlink target is missing: {link}' in failed.stderr
    assert not store.exists()


def test_configured_missing_store_never_restores_excluded_search_result(tmp_path):
    supplied(tmp_path)
    identity = 'evidence-labels'
    disabled = change(tmp_path, 'disable', 0, id=identity)
    assert disabled.returncode == 0, disabled.stderr
    store = tmp_path / 'library.sqlite3'
    typo = tmp_path / 'libary.sqlite3'
    before = store.read_bytes(), set(tmp_path.iterdir())

    for args in [('selection', identity, '--source', 'supplied'), ('search', identity)]:
        legacy = run(CLI, '--store', typo, *args)
        assert legacy.returncode == 0, legacy.stderr
        result = json.loads(legacy.stdout)
        if args[0] == 'selection':
            assert result['effective'] is True
        else:
            assert [match['id'] for match in result['matches']] == [identity]

        failed = run(CLI, '--store', typo, '--require-existing-store', *args)
        assert failed.returncode == 2
        assert failed.stdout == ''
        assert f'Store is missing: {typo}' in failed.stderr

        live = run(CLI, '--store', store, '--require-existing-store', *args)
        assert live.returncode == 0, live.stderr
        result = json.loads(live.stdout)
        if args[0] == 'selection':
            assert (result['effective'], result['revision']) == (False, 1)
        else:
            assert result['matches'] == [] and result['excluded'] == 1
            inspected = run(CLI, '--store', store, '--require-existing-store', *args, '--include-disabled')
            assert inspected.returncode == 0, inspected.stderr
            assert [(match['id'], match['enabled']) for match in json.loads(inspected.stdout)['matches']] == [(identity, False)]
            failed = run(CLI, '--store', typo, '--require-existing-store', *args, '--include-disabled')
            assert (failed.returncode, failed.stdout) == (2, '')

    assert (store.read_bytes(), set(tmp_path.iterdir())) == before


def test_resume_distinguishes_existing_empty_history_from_missing_store(tmp_path):
    store = tmp_path / 'library.sqlite3'
    initialize_empty_store(store)
    missing = tmp_path / 'offline.sqlite3'
    link = tmp_path / 'store-link'
    link.symlink_to(missing.name)
    directory = tmp_path / 'directory'
    directory.mkdir()
    not_sqlite = tmp_path / 'not.sqlite3'
    not_sqlite.write_bytes(b'not a SQLite database')
    empty = tmp_path / 'empty.sqlite3'
    empty.touch()
    truncated = tmp_path / 'truncated.sqlite3'
    truncated.write_bytes(store.read_bytes()[:100])
    before = store.read_bytes(), set(tmp_path.iterdir())

    for command in ('selection', 'selection-history'):
        args = (command, REREAD, '--source', 'supplied')
        legacy_ready = run(CLI, '--store', store, *args)
        legacy_missing = run(CLI, '--store', missing, *args)
        assert legacy_ready.returncode == legacy_missing.returncode == 0
        assert legacy_ready.stdout == legacy_missing.stdout

        live = run(CLI, '--store', store, '--require-existing-store', *args)
        assert live.returncode == 0, live.stderr
        result = json.loads(live.stdout)
        if command == 'selection-history':
            assert result == []
        else:
            assert (result['revision'], result['record'], result['effective']) == (0, None, True)

        for path, state in [(missing, 'missing'), (link, 'missing'), (directory, 'unreadable'),
                            (not_sqlite, 'unreadable'), (empty, 'unreadable'), (truncated, 'unreadable')]:
            failed = run(CLI, '--store', path, '--require-existing-store', *args)
            assert (failed.returncode, failed.stdout) == (2, '')
            assert f'Store is {state}: {path}' in failed.stderr

    assert (store.read_bytes(), set(tmp_path.iterdir())) == before
    assert link.is_symlink() and os.readlink(link) == missing.name
    assert not_sqlite.read_bytes() == b'not a SQLite database'
    assert empty.read_bytes() == b''
    assert truncated.read_bytes() == before[0][:100]
    assert list(directory.iterdir()) == []


def test_strict_read_leaves_wal_sidecars_uncreated(tmp_path):
    store = tmp_path / 'library.sqlite3'
    with closing(sqlite3.connect(store)) as db:
        assert db.execute('PRAGMA journal_mode=WAL').fetchone() == ('wal',)
    before = store.read_bytes()
    assert list(tmp_path.iterdir()) == [store]

    failed = run(CLI, '--store', store, '--require-existing-store', 'search', REREAD)
    assert (failed.returncode, failed.stdout) == (2, '')
    assert f'Store is unreadable: {store}' in failed.stderr
    assert list(tmp_path.iterdir()) == [store]
    assert store.read_bytes() == before


@pytest.mark.parametrize('args', [('show', REREAD), ('save', '--input', 'missing.json', '--expect-revision', '0')])
def test_require_existing_store_rejects_other_commands(tmp_path, args):
    failed = run(CLI, '--store', tmp_path / 'library.sqlite3', '--require-existing-store', *args)
    assert (failed.returncode, failed.stdout) == (2, '')
    assert '--require-existing-store applies only to search, selection and selection-history' in failed.stderr
    assert list(tmp_path.iterdir()) == []


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
    origin = dict(reference='kit:reread-source-before-write', revision='old-origin', snapshot='Original hook policy')
    assert save(tmp_path, draft(id=REREAD, name='Personal hook', origin=origin)).returncode == 0
    assert change(tmp_path, 'disable', 0).returncode == 0
    found = json.loads(invoke(tmp_path, 'search', REREAD, '--kit-dir', tmp_path / 'kit').stdout)
    assert [r['origin'] for r in found['matches']] == ['saved']
    assert change(tmp_path, 'disable', 0, source='saved').returncode == 0
    assert save(tmp_path, draft(id=REREAD, name='Personal hook', content='Independent customization edit', origin=origin), 1).returncode == 0
    assert not selection(tmp_path, source='saved')['effective']
    assert change(tmp_path, 'restore', 1, source='saved').returncode == 0
    assert not selection(tmp_path)['effective']
    content = json.loads(invoke(tmp_path, 'show', REREAD).stdout)
    assert content['revision'] == 2 and content['resource']['content'] == 'Independent customization edit'
    assert content['resource']['origin'] == origin
    assert len(json.loads(invoke(tmp_path, 'history', REREAD).stdout)) == 2


def test_exclusion_survives_absence_reappearance_and_store_relocation(tmp_path):
    supplied(tmp_path)
    assert change(tmp_path, 'disable', 0).returncode == 0
    path = tmp_path / 'kit/legos.csv'
    original = path.read_text()
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader()
        writer.writerows(row for row in rows if row['id'] != REREAD)
    state = selection(tmp_path)
    assert not state['available'] and not state['enabled']
    assert change(tmp_path, 'restore', 1).returncode != 0
    assert len(selection(tmp_path, history=True)) == 1
    path.write_text(original)
    moved = tmp_path / 'moved'; moved.mkdir()
    shutil.copytree(tmp_path / 'kit', moved / 'kit')
    shutil.copy2(tmp_path / 'library.sqlite3', moved / 'library.sqlite3')
    assert not selection(moved)['effective']
    result = json.loads(invoke(moved, 'search', REREAD, '--kit-dir', moved / 'kit', '--include-disabled').stdout)
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
    assert invoke(tmp_path, 'search', REREAD, '--kit-dir', tmp_path / 'kit').returncode != 0


def test_competing_selection_writers_preserve_one_decision(tmp_path):
    import subprocess
    import sys
    supplied(tmp_path)
    payload = decision(tmp_path)
    command = [sys.executable, '-I', str(CLI), '--store', str(tmp_path / 'library.sqlite3'),
               'disable', REREAD, '--source', 'supplied', '--kit-dir', str(tmp_path / 'kit'),
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
    assert save(tmp_path, draft(id=REREAD)).returncode == 0
    edit = tmp_path / 'edit.json'; edit.write_text(json.dumps(draft(id=REREAD, content='Independent updated content')))
    base = [sys.executable, '-I', str(CLI), '--store', str(tmp_path / 'library.sqlite3')]
    commands = [base + ['save', '--input', str(edit), '--expect-revision', '1'],
                base + ['disable', REREAD, '--source', 'saved', '--kit-dir', str(tmp_path / 'kit'),
                        '--input', str(decision(tmp_path)), '--expect-selection-revision', '0']]
    writers = [subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for c in commands]
    results = [(p.communicate(), p.returncode) for p in writers]
    assert all(code == 0 for _, code in results), results
    assert not selection(tmp_path, source='saved')['effective']
    current = json.loads(invoke(tmp_path, 'show', REREAD).stdout)
    assert current['revision'] == 2 and current['resource']['content'] == 'Independent updated content'


def test_direct_saved_retrieval_exposes_exclusion_without_hiding_provenance(tmp_path):
    from test_library_cli import draft, save
    supplied(tmp_path)
    assert save(tmp_path, draft(id=REREAD)).returncode == 0
    assert change(tmp_path, 'disable', 0, source='saved').returncode == 0
    current = json.loads(invoke(tmp_path, 'show', REREAD).stdout)
    assert current['selection']['enabled'] is False
    assert current['resource']['content'] == draft()['content']
    assert current['revision'] == 1
