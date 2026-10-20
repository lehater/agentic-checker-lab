"""Системные проверки границ и объёма без подпроцессов и временных порогов."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from examples.cli_usage import capture_report
from examples.contract_usage import report_document


EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'


@pytest.mark.parametrize('changes, expected_ids', [
    ({}, ['z-deny', 'a-permit']),
    ({'protocol': 'tcp'}, ['z-deny']),
    ({'source_port': 1}, ['a-permit']),
    ({'destination_port': 65534}, ['a-permit']),
    ({'source': '0.0.0.1'}, ['z-deny']),
    ({'destination': '255.255.255.254'}, ['a-permit']),
    ({'protocol': 'tcp', 'source_port': 1}, []),
])
def test_fixed_boundary_example_through_file_and_memory(
    tmp_path: Path, changes: dict, expected_ids: list[str],
) -> None:
    document = json.loads((EXAMPLES / 'boundary_request.json').read_text(encoding='utf-8'))
    expected = json.loads((EXAMPLES / 'boundary_expected.json').read_text(encoding='utf-8'))
    document['flow'].update(changes)
    group = expected['groups'][0]
    group['rules'] = [rule for rule in group['rules'] if rule['id'] in expected_ids]
    group['status'] = 'MATCHES' if expected_ids else 'NO_MATCH'
    original = deepcopy(document)
    path = tmp_path / 'boundary.json'
    payload = json.dumps(document).encode('utf-8')
    path.write_bytes(payload)

    code, output, diagnostic = capture_report(path)

    assert (code, diagnostic) == (0, '')
    assert json.loads(output) == expected
    assert json.loads(report_document(document)) == expected
    assert document == original
    assert path.read_bytes() == payload


@pytest.fixture
def volume_document() -> dict:
    """12 ACL × 200 правил; пары повторены, порядок снимков обращён."""
    base = json.loads((EXAMPLES / 'boundary_request.json').read_text(encoding='utf-8'))
    template = base['snapshots'][0]['rules'][1]
    pairs, snapshots = [], []
    for index in range(12):
        pair = {'device': f'fw-{index // 3}', 'acl': f'acl-{index}'}
        pairs.append(pair)
        rules = [dict(template, id=f'r-{199 - number:03}',
                      protocol='udp' if number % 2 == 0 else 'tcp',
                      action='deny' if number % 4 == 0 else 'permit')
                 for number in range(200)]
        snapshots.append(dict(pair, placements=[{'global': True}], rules=rules))
    base.update(relevance=pairs + deepcopy(pairs), snapshots=snapshots[::-1])
    return base


@pytest.mark.parametrize('output_format', ['json', 'text'])
def test_volume_preserves_every_group_and_matching_rule(
    tmp_path: Path, volume_document: dict, output_format: str,
) -> None:
    path = tmp_path / 'volume.json'
    payload = json.dumps(volume_document).encode('utf-8')
    path.write_bytes(payload)
    expected = []
    # The oracle uses the fixture's alternating positions, never production matches.
    for snapshot in reversed(volume_document['snapshots']):
        expected.append(dict(snapshot, status='MATCHES', rules=snapshot['rules'][::2]))

    code, output, diagnostic = capture_report(path, output_format)

    assert (code, diagnostic) == (0, '')
    if output_format == 'json':
        assert json.loads(output) == {'version': 1, 'groups': expected}
    else:
        lines = output.splitlines()
        assert len(lines) == 12 * 102
        for index, group in enumerate(expected):
            block = lines[index * 102:(index + 1) * 102]
            assert block[0] == f"{group['device']} / {group['acl']} — MATCHES"
            assert block[1] == 'placements: [{"global": true}]'
            assert [json.loads(line) for line in block[2:]] == group['rules']
    assert path.read_bytes() == payload


@pytest.mark.parametrize('output_format', ['json', 'text'])
def test_late_invalid_rule_rejects_volume_then_corrected_file_recovers(
    tmp_path: Path, volume_document: dict, output_format: str,
) -> None:
    path = tmp_path / 'volume.json'
    valid_payload = json.dumps(volume_document).encode('utf-8')
    volume_document['snapshots'][-1]['rules'][-1]['destination_ports'] = [0, True]
    invalid_payload = json.dumps(volume_document).encode('utf-8')
    path.write_bytes(invalid_payload)

    code, output, diagnostic = capture_report(path, output_format)

    assert (code, output) == (2, '')
    assert diagnostic.startswith(
        'Checker error: snapshots[11].rules[199].destination_ports[1]:'
    )
    assert len(diagnostic.splitlines()) == 1
    assert path.read_bytes() == invalid_payload
    path.write_bytes(valid_payload)
    code, output, diagnostic = capture_report(path)
    assert (code, diagnostic) == (0, '')
    report = json.loads(output)
    assert len(report['groups']) == 12
    assert all(len(group['rules']) == 100 for group in report['groups'])
    assert path.read_bytes() == valid_payload
