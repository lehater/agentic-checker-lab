"""Публичная композиция с наблюдением только на границах источников."""

import json
import runpy
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import call, create_autospec, patch

import pytest

from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import ExpectedApplicationFailure


@pytest.fixture
def invocation(tmp_path, monkeypatch):
    document = json.loads(
        (Path(__file__).resolve().parents[1] / 'examples/input_request.json')
        .read_text(encoding='utf-8')
    )
    path = tmp_path / 'request.json'
    payload = json.dumps(document).encode('utf-8')
    path.write_bytes(payload)
    stdout, stderr = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'argv', [
        'checker', '--input', str(path), '--format', 'json',
    ])
    return path, payload, document, stdout, stderr


def test_public_request_calls_validated_sources_and_publishes_evidence(invocation, monkeypatch):
    path, payload, document, stdout, stderr = invocation
    monkeypatch.setattr(sys, 'stdout', stdout)
    monkeypatch.setattr(sys, 'stderr', stderr)
    relevance = create_autospec(
        create_relevance_provider([]),
        side_effect=create_relevance_provider(document['relevance']),
    )
    snapshot = create_autospec(
        create_snapshot_provider([]),
        side_effect=create_snapshot_provider(document['snapshots']),
    )
    # Factories are adapter boundaries; validation, matching and CLI remain real.
    with patch('src.acl_checker.input.validation.create_relevance_provider',
               autospec=True, return_value=relevance) as relevance_factory, \
         patch('src.acl_checker.input.validation.create_snapshot_provider',
               autospec=True, return_value=snapshot) as snapshot_factory:
        with pytest.raises(SystemExit) as result:
            runpy.run_module('checker', run_name='__main__')

    assert result.value.code == 0
    relevance_factory.assert_called_once_with(document['relevance'][:3])
    snapshot_factory.assert_called_once_with(document['snapshots'])
    relevance.assert_called_once_with('10.0.0.1', '192.0.2.10')
    assert snapshot.call_args_list == [
        call('fw-a', 'outside'), call('fw-a', 'inside'), call('fw-b', 'global'),
    ]
    assert json.loads(stdout.getvalue()) == {'version': 1, 'groups': [
        dict(document['snapshots'][0], status='MATCHES',
             rules=document['snapshots'][0]['rules'][:2]),
        dict(document['snapshots'][1], status='NO_MATCH'),
        dict(document['snapshots'][2], status='NO_MATCH', rules=[]),
    ]}
    assert stderr.getvalue() == ''
    assert path.read_bytes() == payload


@pytest.mark.parametrize('expected_failure', [True, False])
def test_public_relevance_failure_stops_before_snapshots(invocation, expected_failure, monkeypatch):
    path, payload, _, stdout, stderr = invocation
    monkeypatch.setattr(sys, 'stdout', stdout)
    monkeypatch.setattr(sys, 'stderr', stderr)
    error_type = ExpectedApplicationFailure if expected_failure else RuntimeError
    error = error_type('источник\nнедоступен')
    relevance = create_autospec(create_relevance_provider([]), side_effect=error)
    snapshot = create_autospec(create_snapshot_provider([]))
    with patch('src.acl_checker.input.validation.create_relevance_provider',
               autospec=True, return_value=relevance), \
         patch('src.acl_checker.input.validation.create_snapshot_provider',
               autospec=True, return_value=snapshot):
        if expected_failure:
            with pytest.raises(SystemExit) as result:
                runpy.run_module('checker', run_name='__main__')
            assert result.value.code == 2
            assert stderr.getvalue() == 'Checker error: источник\\nнедоступен\n'
        else:
            with pytest.raises(RuntimeError) as result:
                runpy.run_module('checker', run_name='__main__')
            assert result.value is error
            assert stderr.getvalue() == ''

    relevance.assert_called_once_with('10.0.0.1', '192.0.2.10')
    snapshot.assert_not_called()
    assert stdout.getvalue() == ''
    assert path.read_bytes() == payload
