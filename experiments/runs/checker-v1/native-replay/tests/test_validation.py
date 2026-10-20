from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.acl_checker.application.types import ExpectedApplicationFailure
from src.acl_checker.input.document import load_request_document
from src.acl_checker.input.types import ExpectedInputFailure, ValidatedInvocation
from src.acl_checker.input.validation import validate_document


def document():
    return {
        'version': 1,
        'flow': {'source': '10.0.0.1', 'destination': '192.0.2.10',
                 'protocol': 'tcp', 'source_port': 0, 'destination_port': 65535},
        'relevance': [{'device': 'fw', 'acl': 'outside'},
                      {'device': 'fw', 'acl': 'inside'},
                      {'device': 'fw', 'acl': 'outside'}],
        'snapshots': [
            {'device': 'fw', 'acl': 'outside',
             'placements': [{'interface': 'wan0', 'direction': 'in'}, {'global': True}],
             'rules': [{'id': 'z', 'source': '10.0.0.0/24',
                        'destination': '192.0.2.10', 'protocol': 'any',
                        'source_ports': [0, 65535], 'destination_ports': [65535, 65535],
                        'action': 'deny'},
                       {'id': 'a', 'source': '0.0.0.0/0',
                        'destination': '192.0.2.10/32', 'protocol': 'udp',
                        'source_ports': [0, 0], 'destination_ports': [0, 65535],
                        'action': 'permit'}]},
            {'device': 'fw', 'acl': 'inside', 'placements': [], 'rules': []},
            {'device': 'unused', 'acl': 'extra', 'placements': [], 'rules': []},
        ],
    }


def test_valid_document_preserves_values_and_source_order():
    value = document()
    original = deepcopy(value)
    result = validate_document(value)
    assert isinstance(result, ValidatedInvocation)
    assert callable(result.relevance)
    assert callable(result.snapshot)
    assert result.flow == value['flow']
    pairs = result.relevance(result.flow['source'], result.flow['destination'])
    assert pairs == value['relevance'][:2]
    pairs.clear()
    assert result.relevance('10.0.0.1', '192.0.2.10') == value['relevance'][:2]
    for snapshot in value['snapshots']:
        assert result.snapshot(snapshot['device'], snapshot['acl']) == snapshot
    with pytest.raises(ExpectedApplicationFailure) as failure:
        result.snapshot('missing-device', 'missing-acl')
    assert 'missing-device' in failure.value.reason
    assert 'missing-acl' in failure.value.reason
    assert value == original


def test_empty_sources_and_rule_ids_scoped_to_snapshot():
    value = document()
    value['snapshots'][1]['rules'] = deepcopy(value['snapshots'][0]['rules'])
    validate_document(value)
    value['relevance'] = []
    value['snapshots'] = []
    result = validate_document(value)
    assert result.relevance('10.0.0.1', '192.0.2.10') == []
    with pytest.raises(ExpectedApplicationFailure):
        result.snapshot('fw', 'outside')


def test_invalid_values_include_location_and_leave_document_unchanged():
    cases = [
        ((), None), (('version',), True), (('version',), 2),
        (('flow',), []), (('relevance',), {}), (('snapshots',), {}),
        (('flow', 'source'), '::1'), (('flow', 'destination'), '10.0.0.0/24'),
        (('flow', 'source'), 1), (('flow', 'protocol'), 'any'),
        (('flow', 'source_port'), True), (('flow', 'source_port'), -1),
        (('flow', 'destination_port'), 65536), (('flow', 'destination_port'), 1.0),
        (('relevance', 0, 'device'), ''), (('relevance', 0, 'acl'), None),
        (('snapshots', 0, 'device'), ''), (('snapshots', 0, 'acl'), 1),
        (('snapshots', 0, 'placements'), None),
        (('snapshots', 0, 'placements', 0, 'interface'), ''),
        (('snapshots', 0, 'placements', 0, 'direction'), 'both'),
        (('snapshots', 0, 'placements', 1, 'global'), 1),
        (('snapshots', 0, 'rules'), {}),
    ]
    rule_path = ('snapshots', 0, 'rules', 0)
    cases += [(('flow', field), bad)
              for field in ('source_port', 'destination_port')
              for bad in (None, False, -1, 65536, 1.0, '80')]
    cases += [(rule_path + (field,), bad)
              for field in ('source_ports', 'destination_ports')
              for bad in (None, 80, [], [0], [0, 1, 2], [2, 1],
                          [False, 1], [0, True], [-1, 0], [0, 65536],
                          [0, 1.0], [0, None])]
    cases += [(rule_path + (field,), bad) for field, bad in [
        ('id', ''), ('source', '10.0.0.1/24'), ('source', '10.0.0.0/024'),
        ('destination', '::/0'), ('source', '10.0.0.0/255.255.255.0'),
        ('protocol', 'icmp'), ('action', 'accept'), ('source_ports', 80),
        ('source_ports', [0]), ('source_ports', [0, 1, 2]),
        ('source_ports', [2, 1]), ('source_ports', [False, 1]),
        ('destination_ports', [0, 65536]), ('destination_ports', [-1, 0]),
        ('destination_ports', [0, None]),
    ]]
    for path, bad in cases:
        value = document()
        if path:
            parent = value
            for key in path[:-1]:
                parent = parent[key]
            parent[path[-1]] = bad
        else:
            value = bad
        original = deepcopy(value)
        with pytest.raises(ExpectedInputFailure) as failure:
            validate_document(value)
        reason = failure.value.reason
        assert reason and ':' in reason, (path, bad, reason)
        if path:
            assert str(path[-1]) in reason, (path, reason)
        assert value == original


def test_exact_fields_at_every_object_boundary():
    paths = [(), ('flow',), ('relevance', 0), ('snapshots', 0),
             ('snapshots', 0, 'placements', 0),
             ('snapshots', 0, 'placements', 1), ('snapshots', 0, 'rules', 0)]
    for path in paths:
        original_target = document()
        for key in path:
            original_target = original_target[key]
        # Every required field matters, including both flow ports and ranges.
        for missing_field in (*original_target, None):
            value = document()
            target = value
            for key in path:
                target = target[key]
            if missing_field is not None:
                del target[missing_field]
            else:
                target['unsupported'] = True
            original = deepcopy(value)
            with pytest.raises(ExpectedInputFailure) as failure:
                validate_document(value)
            # Empty placement is ambiguous between the two allowed shapes.
            expected = 'placements' if missing_field == 'global' else (
                missing_field or 'unsupported'
            )
            assert expected in failure.value.reason
            assert value == original
    value = document()
    value['relevance_records'] = []
    with pytest.raises(ExpectedInputFailure, match='relevance_records'):
        validate_document(value)


def test_duplicate_and_missing_snapshots_and_invalid_unused_snapshot():
    for kind in ('pair', 'id', 'missing', 'unused'):
        value = document()
        if kind == 'pair':
            value['snapshots'].append(deepcopy(value['snapshots'][0]))
        elif kind == 'id':
            value['snapshots'][0]['rules'][1]['id'] = 'z'
        elif kind == 'missing':
            value['snapshots'].pop(1)
        else:
            value['snapshots'][2]['placements'] = [{'global': False}]
        original = deepcopy(value)
        with pytest.raises(ExpectedInputFailure) as failure:
            validate_document(value)
        assert failure.value.reason
        assert value == original


def test_request_validation(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """The real file boundary either yields a complete invocation or raises."""
    value = document()
    value['snapshots'][1]['placements'] = [
        {'interface': 'внутренний', 'direction': 'out'},
    ]
    original = deepcopy(value)
    path = tmp_path / 'request.json'
    content = json.dumps(value, ensure_ascii=False).encode('utf-8')
    path.write_bytes(content)

    result = load_request_document(path)

    assert isinstance(result, ValidatedInvocation)
    assert result.flow == original['flow']
    assert callable(result.relevance) and callable(result.snapshot)
    assert result.relevance('10.0.0.1', '192.0.2.10') == [
        {'device': 'fw', 'acl': 'outside'}, {'device': 'fw', 'acl': 'inside'},
    ]
    for snapshot in original['snapshots']:
        assert result.snapshot(snapshot['device'], snapshot['acl']) == snapshot
    assert value == original
    assert path.read_bytes() == content
    assert capsys.readouterr() == ('', '')

    invalid_documents = []
    for field in ('source_port', 'destination_port'):
        invalid = deepcopy(value)
        del invalid['flow'][field]
        invalid_documents.append((invalid, field))
    invalid = deepcopy(value)
    invalid['snapshots'].pop(1)
    invalid_documents.append((invalid, 'inside'))
    # A late, irrelevant snapshot must still invalidate the entire request.
    invalid = deepcopy(value)
    invalid['snapshots'][2]['rules'] = [dict(
        value['snapshots'][0]['rules'][0], destination_ports=443,
    )]
    invalid_documents.append((invalid, 'destination_ports'))
    invalid = deepcopy(value)
    invalid['relevance_records'] = []
    invalid_documents.append((invalid, 'relevance_records'))
    invalid = deepcopy(value)
    invalid['snapshots'][2]['placements'] = [
        {'global': True, 'interface': 'wan0', 'direction': 'in'},
    ]
    invalid_documents.append((invalid, 'placements'))

    bad_contents = [(json.dumps(item).encode('utf-8'), reason)
                    for item, reason in invalid_documents]
    bad_contents += [(b'\xff', 'UTF-8'), (b'{"version":', 'JSON')]
    # Put constants in an otherwise valid document so schema errors cannot mask
    # accidental acceptance by the JSON parser.
    for constant in ('NaN', 'Infinity', '-Infinity'):
        bad_contents.append((content[:-1] + b', "extra": ' +
                             constant.encode('ascii') + b'}', constant))
    for payload, reason in bad_contents:
        path.write_bytes(payload)
        with pytest.raises(ExpectedInputFailure) as failure:
            load_request_document(path)
        assert reason in failure.value.reason
        assert path.read_bytes() == payload
        assert capsys.readouterr() == ('', '')

    for unreadable in (tmp_path / 'missing.json', tmp_path):
        with pytest.raises(ExpectedInputFailure) as failure:
            load_request_document(unreadable)
        assert str(unreadable) in failure.value.reason
        assert isinstance(failure.value.__cause__, OSError)
    with patch.object(Path, 'read_text', autospec=True,
                      side_effect=PermissionError('access denied')):
        with pytest.raises(ExpectedInputFailure) as failure:
            load_request_document(path)
    assert 'access denied' in failure.value.reason
    assert isinstance(failure.value.__cause__, PermissionError)
    assert capsys.readouterr() == ('', '')
