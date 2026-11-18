"""Public library observations around real SIGKILL; no injected product hooks.

A held native SQLite write lock prevents the first effect. Backpressure on a large
public response lets the second process be killed after its commit, before a full
acknowledgement. Neither case establishes power-loss or remote-store durability.
"""
import json
import select
import signal
import sqlite3
import subprocess
import sys

from conftest import run
from test_library_cli import CLI, draft, save


def test_killed_before_effect_preserves_prior_revision_then_continues_once(tmp_path):
    store = tmp_path / 'library.sqlite3'
    assert save(tmp_path, draft(), store=store).returncode == 0
    value = draft(content='Keep source ownership beside every report fact.')
    payload = tmp_path / 'next.json'
    payload.write_text(json.dumps(value))
    command = [sys.executable, '-I', str(CLI), '--store', str(store), 'save',
               '--input', str(payload), '--expect-revision', '1']
    # Real native contention, not a fake CLI response. The process cannot commit
    # while this connection holds the write reservation.
    with sqlite3.connect(store) as owner:
        owner.execute('BEGIN IMMEDIATE')
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert not select.select([process.stdout, process.stderr], [], [], 0.3)[0]
        process.kill()
        process.communicate(timeout=5)
        assert process.returncode == -signal.SIGKILL
    history = json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout)
    assert [r['revision'] for r in history] == [1]
    assert history[0]['resource']['content'] == draft()['content']
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0
    history = json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout)
    assert [r['revision'] for r in history] == [1, 2]
    assert history[-1]['resource']['content'] == value['content']


def kill_after_commit(project, cli=CLI):
    """Return observed process/receipt facts for the host's interrupted-library case."""
    store = project / 'notes/library.sqlite3'
    payload = project / 'notes/save.json'
    value = draft(content='Attribute each fact. ' * 100000)
    value['decision']['authority'] = 'Fixture owner: save report-rule once in notes/library.sqlite3'
    payload.write_text(json.dumps(value))
    command = [sys.executable, '-I', str(cli), '--store', str(store), 'save',
               '--input', str(payload), '--expect-revision', '0']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert select.select([process.stdout], [], [], 10)[0], 'No native response prefix'
        prefix = process.stdout.read(1)
        assert prefix == b'{'
        # The full JSON cannot fit in the undrained OS pipe. First response byte
        # follows the completed transaction; interrupt the real CLI, not a model.
        assert process.poll() is None
        process.kill()
        remainder, error = process.communicate(timeout=5)
        assert process.returncode == -signal.SIGKILL
        try:
            json.loads(prefix + remainder)
        except json.JSONDecodeError:
            pass
        else:
            raise AssertionError('Acknowledgement unexpectedly complete')
        return {'command': command, 'signal': 'SIGKILL', 'returncode': process.returncode,
                'acknowledgement_bytes': len(prefix + remainder),
                'complete_json_acknowledgement': False, 'stderr': error.decode(),
                'fault': 'Real CLI killed after commit while stdout blocked; not host/runner/power failure'}
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)


def test_killed_after_commit_reopens_one_history_and_rejects_stale_replay(tmp_path):
    (tmp_path / 'notes').mkdir()
    receipt = kill_after_commit(tmp_path)
    assert receipt['returncode'] == -signal.SIGKILL
    store = tmp_path / 'notes/library.sqlite3'
    current = json.loads(run(CLI, '--store', store, 'show', 'report-rule').stdout)
    history = json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout)
    assert current['revision'] == 1 and len(history) == 1
    assert current['resource'] == json.loads((tmp_path / 'notes/save.json').read_text())
    replay = run(CLI, '--store', store, 'save', '--input', tmp_path / 'notes/save.json', '--expect-revision', 0)
    assert replay.returncode == 2
    assert json.loads(run(CLI, '--store', store, 'history', 'report-rule').stdout) == history
