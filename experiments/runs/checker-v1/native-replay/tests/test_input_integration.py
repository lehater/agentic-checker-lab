"""Настоящие границы input → sources → application, без внутренних моков."""

from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from examples.input_usage import check_document, check_file
from src.acl_checker.application.types import ExpectedApplicationFailure
from src.acl_checker.cli.main import main
from src.acl_checker.domain.application.check import check
from src.acl_checker.input.document import load_request_document
from src.acl_checker.input.types import ExpectedInputFailure, ValidatedInvocation
from src.acl_checker.input.validation import validate_document


@pytest.fixture
def request_document() -> dict:
    path = Path(__file__).resolve().parents[1] / 'examples/input_request.json'
    return json.loads(path.read_text(encoding='utf-8'))


def test_file_and_memory_apis_preserve_complete_evidence(tmp_path, request_document):
    original = deepcopy(request_document)
    path = tmp_path / 'request.json'
    content = json.dumps(request_document).encode('utf-8')
    path.write_bytes(content)
    for invocation in (load_request_document(path), validate_document(request_document)):
        assert isinstance(invocation, ValidatedInvocation)
        assert invocation.flow == original['flow']
        pairs = invocation.relevance('10.0.0.1', '192.0.2.10')
        assert pairs == original['relevance'][:3]
        pairs.clear()
        assert invocation.relevance('10.0.0.1', '192.0.2.10') == original['relevance'][:3]
        for snapshot in original['snapshots']:
            assert invocation.snapshot(snapshot['device'], snapshot['acl']) == snapshot
        groups = check(invocation.flow, invocation.relevance, invocation.snapshot)
        assert groups == [
            {'device': 'fw-a', 'acl': 'outside', 'status': 'MATCHES',
             'placements': [{'interface': 'wan0', 'direction': 'in'}],
             'rules': original['snapshots'][0]['rules'][:2]},
            {'device': 'fw-a', 'acl': 'inside', 'status': 'NO_MATCH',
             'placements': [{'interface': 'lan0', 'direction': 'out'}], 'rules': []},
            {'device': 'fw-b', 'acl': 'global', 'status': 'NO_MATCH',
             'placements': [{'global': True}], 'rules': []},
        ]
    assert request_document == original
    assert path.read_bytes() == content


@pytest.mark.parametrize(('changes', 'expected_ids'), [
    ({'protocol': 'udp'}, ['a-permit', 'udp-only']),
    ({'source': '10.0.0.0'}, ['z-deny', 'a-permit']),
    ({'source': '10.0.0.255'}, ['z-deny', 'a-permit']),
    ({'source_port': 49999}, ['a-permit']),
    ({'destination_port': 440}, ['a-permit']),
    ({'destination_port': 450}, ['a-permit']),
    ({'destination_port': 451}, []),
    ({'source_port': 0, 'destination_port': 65535}, []),
])
def test_validated_values_reach_matching(tmp_path, request_document, changes, expected_ids):
    # Fixed expectations from accepted SC-* cases, not computed by matches().
    request_document['flow'].update(changes)
    path = tmp_path / 'request.json'
    path.write_text(json.dumps(request_document), encoding='utf-8')
    groups = check_file(path)
    assert [r['id'] for group in groups for r in group['rules']] == expected_ids
    assert [group['status'] for group in groups] == [
        'MATCHES' if expected_ids else 'NO_MATCH', 'NO_MATCH',
        'MATCHES' if changes.get('protocol') == 'udp' else 'NO_MATCH',
    ]


@pytest.mark.parametrize('defect', ['missing-port', 'boolean-port', 'scalar-range',
                                     'unknown-predicate', 'missing-snapshot',
                                     'invalid-unused', 'duplicate-snapshot'])
def test_schema_failures_cross_file_and_cli_boundaries(tmp_path, request_document, defect):
    if defect == 'missing-port':
        del request_document['flow']['source_port']
    elif defect == 'boolean-port':
        request_document['flow']['destination_port'] = True
    elif defect == 'scalar-range':
        request_document['snapshots'][0]['rules'][0]['source_ports'] = 50000
    elif defect == 'unknown-predicate':
        request_document['snapshots'][0]['rules'][0]['negate'] = True
    elif defect == 'missing-snapshot':
        request_document['snapshots'].pop(2)
    elif defect == 'invalid-unused':
        request_document['snapshots'][-1]['placements'] = [{'global': 1}]
    else:
        request_document['snapshots'].append(deepcopy(request_document['snapshots'][0]))
    before = deepcopy(request_document)
    with pytest.raises(ExpectedInputFailure) as direct:
        validate_document(request_document)
    path = tmp_path / 'invalid.json'
    payload = json.dumps(request_document).encode('utf-8')
    path.write_bytes(payload)
    with pytest.raises(ExpectedInputFailure) as loaded:
        load_request_document(path)
    assert loaded.value.reason == direct.value.reason
    stdout, stderr = StringIO(), StringIO()
    assert main(['--input', str(path), '--format', 'json'], stdout=stdout, stderr=stderr) == 2
    assert stdout.getvalue() == ''
    assert stderr.getvalue() == f'Checker error: {direct.value.reason}\n'
    assert path.read_bytes() == payload
    assert request_document == before


@pytest.mark.parametrize(('payload', 'cause'), [
    (b'\xff', UnicodeDecodeError), (b'{"version":', json.JSONDecodeError),
    (b'{"version": NaN}', ValueError), (b'{"version": Infinity}', ValueError),
])
def test_decode_errors_remain_expected_and_silent(tmp_path, capsys, payload, cause):
    path = tmp_path / 'invalid.json'
    path.write_bytes(payload)
    with pytest.raises(ExpectedInputFailure) as failure:
        load_request_document(path)
    assert isinstance(failure.value.__cause__, cause)
    assert str(path) in failure.value.reason
    assert path.read_bytes() == payload
    assert capsys.readouterr() == ('', '')


def test_io_failure_becomes_cli_diagnostic(tmp_path):
    path = tmp_path / 'denied.json'
    error = PermissionError('access denied')
    with patch.object(Path, 'read_text', autospec=True, side_effect=error):
        with pytest.raises(ExpectedInputFailure) as failure:
            load_request_document(path)
        assert failure.value.__cause__ is error
        stdout, stderr = StringIO(), StringIO()
        assert main(['--input', str(path)], stdout=stdout, stderr=stderr) == 2
    assert stdout.getvalue() == ''
    assert stderr.getvalue() == f'Checker error: {failure.value.reason}\n'


def test_requests_are_isolated_across_success_failure_success(tmp_path, request_document):
    path = tmp_path / 'request.json'
    path.write_text(json.dumps(request_document), encoding='utf-8')
    first = load_request_document(path)
    expected = check(first.flow, first.relevance, first.snapshot)
    empty = deepcopy(request_document)
    empty.update(relevance=[], snapshots=[])
    path.write_text(json.dumps(empty), encoding='utf-8')
    assert check_file(path) == []
    second = load_request_document(path)
    with pytest.raises(ExpectedApplicationFailure):
        second.snapshot('fw-a', 'outside')
    empty['flow']['source_port'] = None
    path.write_text(json.dumps(empty), encoding='utf-8')
    with pytest.raises(ExpectedInputFailure):
        load_request_document(path)
    assert check(first.flow, first.relevance, first.snapshot) == expected
    assert check_document(request_document) == expected


def test_usage_examples_agree_and_propagate_failures(tmp_path, request_document):
    path = tmp_path / 'request.json'
    path.write_text(json.dumps(request_document), encoding='utf-8')
    assert check_file(path) == check_document(request_document)
    request_document['snapshots'] = []
    path.write_text(json.dumps(request_document), encoding='utf-8')
    with pytest.raises(ExpectedInputFailure, match='missing snapshot'):
        check_file(path)
    with pytest.raises(ExpectedInputFailure, match='missing snapshot'):
        check_document(request_document)
