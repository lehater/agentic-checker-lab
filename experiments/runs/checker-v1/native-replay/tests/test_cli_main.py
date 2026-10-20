import json
import runpy
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

import src.acl_checker.cli.main as cli
from src.acl_checker.application.types import ExpectedApplicationFailure
from src.acl_checker.input.types import ExpectedInputFailure


@pytest.mark.parametrize('extra, expected', [([], 'text'), (['--format', 'text'], 'text'),
                                            (['--format', 'json'], 'json')])
def test_parse_options_without_reading_file(extra, expected, capsys):
    stdout = StringIO()
    with patch.object(Path, 'read_text', autospec=True) as read:
        options = cli.parse_invocation(['--input', '-', *extra], stdout)
    assert options.input_path == Path('-')
    assert options.format == expected
    read.assert_not_called()
    assert stdout.getvalue() == ''
    assert capsys.readouterr() == ('', '')


@pytest.mark.parametrize('argv', [[], ['--input'], ['--format', 'json'],
                                 ['--input', 'x', '--format', 'xml'],
                                 ['--input', 'x', '--unknown'], ['--inp', 'x']])
def test_parse_errors_are_silent_expected_failures(argv, capsys):
    stdout = StringIO()
    with pytest.raises(ExpectedInputFailure) as failure:
        cli.parse_invocation(argv, stdout)
    assert failure.value.reason
    assert stdout.getvalue() == ''
    assert capsys.readouterr() == ('', '')


@pytest.mark.parametrize('flag', ['-h', '--help'])
def test_help_uses_supplied_stdout_without_loading(flag):
    stdout, stderr = StringIO(), StringIO()
    with patch.object(cli, 'load_request_document', autospec=True) as load:
        assert cli.main([flag], stdout=stdout, stderr=stderr) == 0
    load.assert_not_called()
    help_text = stdout.getvalue()
    for term in ('python3 -m checker --input PATH [--format text|json]',
                 'synthetic', 'IPv4', 'TCP/UDP', 'live', 'verdict',
                 'placements', 'SLA', 'TTL'):
        assert term in help_text
    assert stderr.getvalue() == ''


@pytest.fixture
def accepted_request():
    # Fixed SC-ALL facts from docs/requirements.md, independent of production helpers.
    return {
        'version': 1,
        'flow': dict(source='10.0.0.1', destination='192.0.2.10', protocol='tcp',
                     source_port=50000, destination_port=443),
        'relevance': [dict(device=d, acl=a) for d, a in
                      [('fw-a', 'outside'), ('fw-a', 'inside'),
                       ('fw-b', 'global'), ('fw-a', 'outside')]],
        'snapshots': [
            dict(device='fw-a', acl='outside',
                 placements=[dict(interface='wan0', direction='in')], rules=[
                     dict(id='z-deny', source='10.0.0.0/24', destination='192.0.2.10/32',
                          protocol='tcp', source_ports=[50000, 50000],
                          destination_ports=[443, 443], action='deny'),
                     dict(id='a-permit', source='0.0.0.0/0', destination='192.0.2.0/24',
                          protocol='any', source_ports=[0, 65535],
                          destination_ports=[440, 450], action='permit'),
                     dict(id='wrong-source', source='10.0.1.0/24', destination='0.0.0.0/0',
                          protocol='any', source_ports=[0, 65535],
                          destination_ports=[0, 65535], action='permit')]),
            dict(device='fw-a', acl='inside', placements=[dict(interface='lan0', direction='out')], rules=[]),
            dict(device='fw-b', acl='global', placements=[{'global': True}], rules=[
                dict(id='udp-only', source='0.0.0.0/0', destination='0.0.0.0/0',
                     protocol='udp', source_ports=[0, 65535],
                     destination_ports=[0, 65535], action='permit')]),
            dict(device='irrelevant', acl='unused', placements=[], rules=[]),
        ],
    }


@pytest.mark.parametrize('changes, ids', [
    ({}, ['z-deny', 'a-permit']), ({'protocol': 'udp'}, ['a-permit', 'udp-only']),
    ({'source': '10.0.0.0'}, ['z-deny', 'a-permit']),
    ({'source': '10.0.0.255'}, ['z-deny', 'a-permit']),
    ({'source': '10.0.2.1'}, ['a-permit']), ({'destination': '198.51.100.10'}, []),
    ({'source_port': 49999}, ['a-permit']), ({'source_port': 50001}, ['a-permit']),
    ({'destination_port': 440}, ['a-permit']), ({'destination_port': 450}, ['a-permit']),
    ({'destination_port': 451}, []),
])
@pytest.mark.parametrize('format_args', [[], ['--format', 'text'], ['--format', 'json']])
def test_public_module_fixed_scenarios(tmp_path, monkeypatch, accepted_request, changes, ids, format_args):
    accepted_request['flow'].update(changes)
    path = tmp_path / 'request.json'
    content = json.dumps(accepted_request)
    path.write_text(content, encoding='utf-8')
    stdout, stderr = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'argv', ['checker', '--input', str(path), *format_args])
    monkeypatch.setattr(sys, 'stdout', stdout)
    monkeypatch.setattr(sys, 'stderr', stderr)
    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module('checker', run_name='__main__')
    assert exit_info.value.code == 0
    expected = []
    for snapshot in accepted_request['snapshots'][:3]:
        rules = [rule for rule in snapshot['rules'] if rule['id'] in ids]
        expected.append({**snapshot, 'rules': rules, 'status': 'MATCHES' if rules else 'NO_MATCH'})
    if format_args == ['--format', 'json']:
        assert json.loads(stdout.getvalue()) == {'version': 1, 'groups': expected}
    else:
        lines = stdout.getvalue().splitlines()
        for group in expected:
            assert lines.pop(0) == f"{group['device']} / {group['acl']} — {group['status']}"
            assert json.loads(lines.pop(0).removeprefix('placements: ')) == group['placements']
            for rule in group['rules']:
                assert json.loads(lines.pop(0)) == rule
        assert lines == []
    assert stderr.getvalue() == ''
    assert path.read_text(encoding='utf-8') == content


def test_main_input_failures_and_empty_reports(tmp_path, monkeypatch, accepted_request):
    monkeypatch.chdir(tmp_path)
    path = Path('-')
    bad_documents = ['{', 'NaN', 'Infinity', '{}']
    for field, value in [('source', '::1'), ('source_port', 65536), ('source_port', True)]:
        document = json.loads(json.dumps(accepted_request))
        document['flow'][field] = value
        bad_documents.append(json.dumps(document))
    document = json.loads(json.dumps(accepted_request))
    document['snapshots'].pop(0)
    bad_documents.append(json.dumps(document))
    accepted_request['snapshots'][0]['rules'][0]['negate'] = True
    bad_documents.append(json.dumps(accepted_request))
    for content in bad_documents:
        path.write_text(content, encoding='utf-8')
        stdout, stderr = StringIO(), StringIO()
        assert cli.main(['--input', '-'], stdout=stdout, stderr=stderr) == 2
        assert stdout.getvalue() == ''
        assert stderr.getvalue().startswith('Checker error: ')
        assert len(stderr.getvalue().splitlines()) == 1
    for argv in ([], ['--input', 'missing'], ['--input', '-', '--format', 'xml']):
        stdout, stderr = StringIO(), StringIO()
        assert cli.main(argv, stdout=stdout, stderr=stderr) == 2
        assert stdout.getvalue() == ''
        assert stderr.getvalue().startswith('Checker error: ')
    accepted_request.update(relevance=[], snapshots=[])
    path.write_text(json.dumps(accepted_request), encoding='utf-8')
    for extra, expected in [([], 'Нет релевантных ACL (synthetic source).\n'),
                            (['--format', 'json'], '{"version": 1, "groups": []}\n')]:
        stdout, stderr = StringIO(), StringIO()
        assert cli.main(['--input', '-', *extra], stdout=stdout, stderr=stderr) == 0
        assert stdout.getvalue() == expected
        assert stderr.getvalue() == ''


def test_main_passes_existing_sources_once(tmp_path, accepted_request):
    path = tmp_path / 'request.json'
    path.write_text(json.dumps(accepted_request), encoding='utf-8')
    stdout, stderr = StringIO(), StringIO()
    with patch.object(cli, 'load_request_document', autospec=True,
                      wraps=cli.load_request_document, side_effect=cli.load_request_document) as load:
        with patch.object(cli, 'check', autospec=True, side_effect=cli.check) as check:
            assert cli.main(['--input', str(path)], stdout=stdout, stderr=stderr) == 0
    load.assert_called_once_with(path)
    check.assert_called_once()
    flow, relevance, snapshot = check.call_args.args
    assert flow == accepted_request['flow']
    assert relevance(flow['source'], flow['destination']) == accepted_request['relevance'][:3]
    assert snapshot('fw-a', 'outside') == accepted_request['snapshots'][0]


def test_expected_failures_escape_lines_and_programming_errors_propagate(tmp_path, accepted_request):
    path = tmp_path / 'request.json'
    path.write_text(json.dumps(accepted_request), encoding='utf-8')
    for boundary in ('load_request_document', 'check', 'render_text_report'):
        for error in (ExpectedInputFailure('bad\rline\nnext'),
                      ExpectedApplicationFailure('bad\rline\nnext'), RuntimeError('bug')):
            stdout, stderr = StringIO(), StringIO()
            with patch.object(cli, boundary, autospec=True, side_effect=error):
                if isinstance(error, RuntimeError):
                    with pytest.raises(RuntimeError) as failure:
                        cli.main(['--input', str(path)], stdout=stdout, stderr=stderr)
                    assert failure.value is error
                    assert stderr.getvalue() == ''
                else:
                    assert cli.main(['--input', str(path)], stdout=stdout, stderr=stderr) == 2
                    assert stderr.getvalue() == 'Checker error: bad\\rline\\nnext\n'
            assert stdout.getvalue() == ''
