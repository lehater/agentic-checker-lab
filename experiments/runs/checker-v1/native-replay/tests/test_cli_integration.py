"""Сквозные проверки публикации: реальные адаптеры, use case и renderer."""

import json
import runpy
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import create_autospec, patch

import pytest

from examples.cli_usage import capture_report
from src.acl_checker.application.sources import create_snapshot_provider
from src.acl_checker.application.types import ExpectedApplicationFailure


@pytest.fixture
def request_file(tmp_path):
    document = json.loads(
        (Path(__file__).resolve().parents[1] / 'examples/input_request.json')
        .read_text(encoding='utf-8')
    )
    path = tmp_path / 'запрос.json'
    path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
    return path, document


@pytest.mark.parametrize('output_format', ['text', 'json'])
def test_public_module_preserves_unicode_context_and_multiple_placements(
    request_file, monkeypatch, output_format,
):
    path, document = request_file
    document['snapshots'][0]['placements'].append({'interface': 'канал', 'direction': 'out'})
    document['snapshots'][0]['rules'][0]['id'] = 'запрет'
    # Snapshot order is deliberately different from selection order.
    document['snapshots'].reverse()
    path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
    original = path.read_bytes()
    stdout, stderr = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'argv', ['checker', '--input', str(path), '--format', output_format])
    monkeypatch.setattr(sys, 'stdout', stdout)
    monkeypatch.setattr(sys, 'stderr', stderr)

    with pytest.raises(SystemExit) as result:
        runpy.run_module('checker', run_name='__main__')

    assert result.value.code == 0
    assert stderr.getvalue() == ''
    outside = document['snapshots'][3]
    if output_format == 'json':
        assert json.loads(stdout.getvalue()) == {'version': 1, 'groups': [
            {'device': 'fw-a', 'acl': 'outside', 'placements': outside['placements'],
             'status': 'MATCHES', 'rules': outside['rules'][:2]},
            {'device': 'fw-a', 'acl': 'inside',
             'placements': [{'interface': 'lan0', 'direction': 'out'}],
             'status': 'NO_MATCH', 'rules': []},
            {'device': 'fw-b', 'acl': 'global', 'placements': [{'global': True}],
             'status': 'NO_MATCH', 'rules': []},
        ]}
    else:
        lines = stdout.getvalue().splitlines()
        assert lines[0] == 'fw-a / outside — MATCHES'
        assert json.loads(lines[1].removeprefix('placements: ')) == outside['placements']
        assert [json.loads(line) for line in lines[2:4]] == outside['rules'][:2]
        assert lines[4:] == [
            'fw-a / inside — NO_MATCH',
            'placements: [{"interface": "lan0", "direction": "out"}]',
            'fw-b / global — NO_MATCH', 'placements: [{"global": true}]',
        ]
    assert path.read_bytes() == original


@pytest.mark.parametrize('output_format', ['text', 'json'])
def test_late_snapshot_source_failure_never_publishes_first_group(request_file, output_format):
    path, _ = request_file
    original = path.read_bytes()
    real_factory = create_snapshot_provider
    providers = []

    def failing_factory(snapshots):
        provider = real_factory(snapshots)

        def retrieve(device, acl):
            if acl == 'inside':
                raise ExpectedApplicationFailure('снимок\r\nнедоступен')
            return provider(device, acl)

        source = create_autospec(provider, side_effect=retrieve)
        providers.append(source)
        return source

    with patch('src.acl_checker.input.validation.create_snapshot_provider',
               autospec=True, side_effect=failing_factory):
        assert capture_report(path, output_format) == (
            2, '', 'Checker error: снимок\\r\\nнедоступен\n',
        )
    assert [call.args for call in providers[0].call_args_list] == [
        ('fw-a', 'outside'), ('fw-a', 'inside'),
    ]
    assert path.read_bytes() == original


@pytest.mark.parametrize('content, reason', [
    (b'\xff', 'Invalid UTF-8'), (b'{', 'Invalid JSON'), (b'NaN', 'Invalid JSON'),
])
def test_document_decode_failures_reach_cli_without_report(tmp_path, content, reason):
    path = tmp_path / 'invalid.json'
    path.write_bytes(content)
    code, stdout, stderr = capture_report(path)
    assert (code, stdout) == (2, '')
    assert stderr.startswith(f'Checker error: {reason}')
    assert len(stderr.splitlines()) == 1
    assert path.read_bytes() == content


def test_read_error_is_translated_at_document_boundary(request_file):
    path, _ = request_file
    with patch.object(Path, 'read_text', autospec=True,
                      side_effect=PermissionError('доступ запрещён')) as read:
        code, stdout, stderr = capture_report(path)
    read.assert_called_once_with(path, encoding='utf-8')
    assert (code, stdout) == (2, '')
    assert stderr.startswith('Checker error: Cannot read ')
    assert 'доступ запрещён' in stderr


@pytest.mark.parametrize('output_format', ['text', 'json'])
def test_invalid_unused_snapshot_rejects_whole_request(request_file, output_format):
    path, document = request_file
    document['snapshots'][-1]['placements'] = [{'global': False}]
    path.write_text(json.dumps(document), encoding='utf-8')
    code, stdout, stderr = capture_report(path, output_format)
    assert (code, stdout) == (2, '')
    assert stderr.startswith('Checker error: snapshots[3].placements[0].global:')


def test_usage_example_isolates_success_failure_and_empty_runs(request_file):
    path, document = request_file
    success = capture_report(path)
    assert success[0] == 0 and success[2] == ''
    assert [rule['id'] for rule in json.loads(success[1])['groups'][0]['rules']] == [
        'z-deny', 'a-permit',
    ]
    original = path.read_bytes()
    document['snapshots'].pop(2)  # Failure after valid earlier snapshot entries.
    path.write_text(json.dumps(document), encoding='utf-8')
    code, stdout, stderr = capture_report(path)
    assert (code, stdout) == (2, '')
    assert 'missing snapshot' in stderr and 'fw-b' in stderr
    document['relevance'] = []
    path.write_text(json.dumps(document), encoding='utf-8')
    assert capture_report(path, 'text') == (
        0, 'Нет релевантных ACL (synthetic source).\n', '',
    )
    assert capture_report(path) == (0, '{"version": 1, "groups": []}\n', '')
    path.write_bytes(original)
    assert capture_report(path) == success
