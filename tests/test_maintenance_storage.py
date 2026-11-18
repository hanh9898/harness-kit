"""Supplemental maintenance checks through existing public library operations.

These qualify native local persistence, not host reasoning or remote stores.
"""
import json
import subprocess
import sys

from conftest import run
from test_library_cli import CLI, draft, save


def test_competing_corrections_reconcile_and_retain_both_attributable_results(tmp_path):
    assert save(tmp_path, draft(content='Accepted: 9. Review: pending.')).returncode == 0
    store = tmp_path / 'library.sqlite3'
    writers = []
    for actor, content in [('A', 'Accepted: 7. Review: pending.'),
                           ('B', 'Accepted: 9. Review: Mira required.')]:
        payload = tmp_path / f'{actor}.json'
        payload.write_text(json.dumps(draft(content=content,
            correction={'actor': actor, 'supersedes_revision': 1,
                        'reason': 'Reconcile the count' if actor == 'A' else 'Name the accuracy reviewer'})))
        writers.append((actor, subprocess.Popen([sys.executable, '-I', str(CLI), '--store', str(store),
            'save', '--input', str(payload), '--expect-revision', '1'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)))
    results = [(actor, p.communicate(), p.returncode) for actor, p in writers]
    assert sorted(code for _, _, code in results) == [0, 2]
    loser = next(actor for actor, _, code in results if code == 2)
    winner = next(actor for actor, _, code in results if code == 0)
    current = json.loads(run(CLI, '--store', store, 'show', 'report-rule').stdout)
    assert current['revision'] == 2
    # Semantic reconciliation is explicit: retain A's fact and B's independent
    # review responsibility, never replace the winner with the stale payload.
    combined = draft(content='Accepted: 7. Review: Mira required.',
        correction={'actor': loser, 'supersedes_revision': 2,
                    'retains_actor': winner, 'reason': 'Integrate both independent corrections'})
    assert save(tmp_path, combined, expected=2).returncode == 0
    history = json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout)
    assert [v['revision'] for v in history] == [1, 2, 3]
    assert history[0]['resource']['content'] == 'Accepted: 9. Review: pending.'
    assert history[1]['resource']['correction']['actor'] == winner
    assert history[2]['resource']['correction']['actor'] == loser
    assert history[2]['resource']['content'] == 'Accepted: 7. Review: Mira required.'
    assert history[2]['resource']['correction']['supersedes_revision'] == 2


def test_archive_keeps_history_and_live_read_reconciles_lost_acknowledgement(tmp_path):
    assert save(tmp_path, draft(name='Archived unique rule')).returncode == 0
    store = tmp_path / 'library.sqlite3'
    prior = json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout)
    decision = {'owner': 'report author', 'scope': 'personal',
        'decision': {'authority': 'Disposable fixture grant: archive this rule, never delete history',
                     'rationale': 'Retire future selection; retain referenced audit evidence',
                     'methods': [], 'standards': ['retain evidence']},
        'evidence': ['Fixture references inspected; prior revision remains audit evidence'],
        'continuation': 'Read live selection and histories after missing acknowledgement'}
    payload = tmp_path / 'archive.json'
    payload.write_text(json.dumps(decision))
    # Deliberately discard the operation response. A later caller has an uncertain
    # acknowledgement, not evidence that persistence failed; reconcile via reads.
    result = subprocess.run([sys.executable, '-I', str(CLI), '--store', str(store),
        'disable', 'report-rule', '--source', 'saved', '--input', str(payload),
        '--expect-selection-revision', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert result.returncode == 0
    selection = json.loads(run(CLI, '--store', store, 'selection', 'report-rule', '--source', 'saved').stdout)
    assert selection['enabled'] is False and selection['revision'] == 1
    assert json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout) == prior
    assert json.loads(run(CLI, '--store', store, 'show', 'report-rule').stdout)['revision'] == 1
    hidden = json.loads(run(CLI, '--store', store, 'search', 'Archived unique rule').stdout)
    assert not hidden['matches']
    assert len(json.loads(run(CLI, '--store', store, 'selection-history', 'report-rule', '--source', 'saved').stdout)) == 1
    # An attempted stale replay is rejected without a duplicate archival event.
    replay = run(CLI, '--store', store, 'disable', 'report-rule', '--source', 'saved',
                 '--input', payload, '--expect-selection-revision', 0)
    assert replay.returncode == 2
    assert len(json.loads(run(CLI, '--store', store, 'selection-history', 'report-rule', '--source', 'saved').stdout)) == 1


def test_failed_persistence_preserves_unknown_state_and_does_not_claim_correction(tmp_path):
    store = tmp_path / 'library.sqlite3'
    store.write_bytes(b'Unreadable prior store; preserve for recovery.')
    result = save(tmp_path, draft(content='New assertion'), expected=1, store=store)
    assert result.returncode == 2 and not result.stdout
    assert store.read_bytes() == b'Unreadable prior store; preserve for recovery.'
    assert run(CLI, '--store', store, 'history', 'report-rule').returncode == 2
