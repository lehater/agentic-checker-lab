"""Согласованность контрактов validation → application → serialization → CLI."""

from copy import deepcopy
from io import StringIO
import json
from pathlib import Path

import pytest

from examples.contract_usage import report_document
from src.acl_checker.cli.main import main
from src.acl_checker.input.document import load_request_document
from src.acl_checker.input.types import ExpectedInputFailure
from src.acl_checker.input.validation import validate_document


@pytest.fixture
def document() -> dict:
    path = Path(__file__).resolve().parents[1] / 'examples/input_request.json'
    return json.loads(path.read_text(encoding='utf-8'))


@pytest.mark.parametrize('defect, location', [
    ('boolean-lower', 'snapshots[0].rules[0].source_ports[0]'),
    ('boolean-upper', 'snapshots[0].rules[0].destination_ports[1]'),
    ('duplicate-id', 'snapshots[0].rules[1].id'),
    ('unused-cidr', 'snapshots[3].rules[0].source'),
])
def test_rejections_agree_across_boundaries_and_allow_corrected_request(
    tmp_path: Path, document: dict, defect: str, location: str,
) -> None:
    valid = deepcopy(document)
    rules = document['snapshots'][0]['rules']
    if defect == 'boolean-lower':
        rules[0]['source_ports'][0] = False
    elif defect == 'boolean-upper':
        rules[0]['destination_ports'][1] = True
    elif defect == 'duplicate-id':
        rules[1]['id'] = rules[0]['id']
    else:
        document['snapshots'][3]['rules'] = [dict(rules[0], source='10.0.0.1/24')]
    before = deepcopy(document)
    path = tmp_path / 'request.json'
    payload = json.dumps(document).encode('utf-8')
    path.write_bytes(payload)

    with pytest.raises(ExpectedInputFailure) as direct:
        validate_document(document)
    assert direct.value.reason.startswith(location + ':')
    with pytest.raises(ExpectedInputFailure) as loaded:
        load_request_document(path)
    with pytest.raises(ExpectedInputFailure) as example:
        report_document(document)
    assert loaded.value.reason == example.value.reason == direct.value.reason
    for output_format in ('json', 'text'):
        stdout, stderr = StringIO(), StringIO()
        assert main(['--input', str(path), '--format', output_format],
                    stdout=stdout, stderr=stderr) == 2
        assert stdout.getvalue() == ''
        assert stderr.getvalue() == f'Checker error: {direct.value.reason}\n'
    assert document == before
    assert path.read_bytes() == payload

    path.write_text(json.dumps(valid), encoding='utf-8')
    stdout, stderr = StringIO(), StringIO()
    assert main(['--input', str(path), '--format', 'json'],
                stdout=stdout, stderr=stderr) == 0
    assert stderr.getvalue() == ''
    report = json.loads(stdout.getvalue())
    assert [group['status'] for group in report['groups']] == [
        'MATCHES', 'NO_MATCH', 'NO_MATCH',
    ]
    assert [rule['id'] for rule in report['groups'][0]['rules']] == [
        'z-deny', 'a-permit',
    ]


def test_rule_identifiers_are_scoped_to_acl_through_public_json(
    tmp_path: Path, document: dict,
) -> None:
    # Одинаковый ID в разных ACL допустим: уникальность локальна снимку.
    outside = document['snapshots'][0]
    inside = document['snapshots'][1]
    inside['rules'] = [dict(outside['rules'][0], action='permit')]
    document['snapshots'].reverse()
    before = deepcopy(document)
    path = tmp_path / 'scoped.json'
    payload = json.dumps(document).encode('utf-8')
    path.write_bytes(payload)
    stdout, stderr = StringIO(), StringIO()
    assert main(['--input', str(path), '--format', 'json'],
                stdout=stdout, stderr=stderr) == 0
    expected = {'version': 1, 'groups': [
        {'device': 'fw-a', 'acl': 'outside', 'placements': outside['placements'],
         'status': 'MATCHES', 'rules': outside['rules'][:2]},
        {'device': 'fw-a', 'acl': 'inside', 'placements': inside['placements'],
         'status': 'MATCHES', 'rules': inside['rules']},
        {'device': 'fw-b', 'acl': 'global', 'placements': [{'global': True}],
         'status': 'NO_MATCH', 'rules': []},
    ]}
    assert json.loads(stdout.getvalue()) == expected
    assert json.loads(report_document(document)) == expected
    assert stderr.getvalue() == ''
    assert document == before
    assert path.read_bytes() == payload


def test_json_example_preserves_escaped_values_and_has_no_output(
    document: dict, capsys: pytest.CaptureFixture[str],
) -> None:
    identifier = 'verdict="данные"\n\\rule'
    document['snapshots'][0]['rules'][0]['id'] = identifier
    before = deepcopy(document)
    serialized = report_document(document)
    report = json.loads(serialized)
    assert set(report) == {'version', 'groups'}
    assert report['groups'][0]['rules'][0] == before['snapshots'][0]['rules'][0]
    assert report['groups'][0]['rules'][0]['id'] == identifier
    assert len(serialized.splitlines()) == 1
    assert serialized.endswith('\n')
    assert document == before
    assert capsys.readouterr() == ('', '')


def test_empty_example_still_validates_flow(document: dict) -> None:
    document.update(relevance=[], snapshots=[])
    assert json.loads(report_document(document)) == {'version': 1, 'groups': []}
    document['flow']['source_port'] = None
    with pytest.raises(ExpectedInputFailure, match='flow.source_port'):
        report_document(document)
