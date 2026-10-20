"""Интеграция реального matching с use case и локальными источниками."""

from copy import deepcopy

import pytest

from examples.domain_usage import investigate_saved_acl
from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import (
    DeviceAclPair, ExpectedApplicationFailure, Snapshot,
)
from src.acl_checker.domain.application.check import (
    build_evidence_group, check, collect_matching_evidence,
    determine_evidence_status,
)
from src.acl_checker.domain.matching import matches
from src.acl_checker.domain.types import Flow, OriginalRule


@pytest.fixture
def values() -> tuple[Flow, Snapshot]:
    flow: Flow = {
        'source': '10.0.0.0', 'destination': '192.0.2.255',
        'protocol': 'udp', 'source_port': 100, 'destination_port': 200,
    }
    rule: OriginalRule = {
        'id': 'z-deny', 'source': '10.0.0.0/24',
        'destination': '192.0.2.0/24', 'protocol': 'udp',
        'source_ports': [100, 110], 'destination_ports': [190, 200],
        'action': 'deny',
    }
    return flow, {
        'device': 'fw-a', 'acl': 'outside',
        'placements': [{'interface': 'wan0', 'direction': 'in'}, {'global': True}],
        'rules': [rule],
    }


def test_all_public_domain_operations_preserve_complete_evidence(values) -> None:
    flow, saved = values
    deny = saved['rules'][0]
    # Каждое исключаемое правило нарушает ровно одно условие конъюнкции.
    misses = [
        dict(deny, id='source', source='10.0.1.0/24'),
        dict(deny, id='destination', destination='192.0.3.0/24'),
        dict(deny, id='protocol', protocol='tcp'),
        dict(deny, id='source-port', source_ports=[101, 110]),
        dict(deny, id='destination-port', destination_ports=[190, 199]),
    ]
    permit = dict(deny, id='a-permit', action='permit', protocol='any')
    saved['rules'] = [deny, *misses, permit]
    before = deepcopy((flow, saved))
    expected = {
        'device': 'fw-a', 'acl': 'outside', 'placements': saved['placements'],
        'status': 'MATCHES', 'rules': [deny, permit],
    }
    assert [matches(flow, rule) for rule in saved['rules']] == [
        True, False, False, False, False, False, True,
    ]
    selected = collect_matching_evidence(flow, tuple(saved['rules']))
    assert selected == [deny, permit]
    assert determine_evidence_status(selected) == 'MATCHES'
    assert build_evidence_group(flow, saved) == expected
    result = check(flow, create_relevance_provider([
        {'device': 'fw-a', 'acl': 'outside'},
        {'device': 'fw-a', 'acl': 'outside'},
    ]), create_snapshot_provider([saved]))
    assert result == [expected]
    assert result[0]['rules'][0] is deny
    assert result[0]['rules'][1] is permit
    assert (flow, saved) == before


@pytest.mark.parametrize(('changes', 'expected_status'), [
    ({'source_port': 110, 'destination_port': 190}, 'MATCHES'),
    ({'source_port': 99}, 'NO_MATCH'),
    ({'source_port': 111}, 'NO_MATCH'),
    ({'destination_port': 189}, 'NO_MATCH'),
    ({'destination_port': 201}, 'NO_MATCH'),
    ({'source': '10.0.0.255', 'destination': '192.0.2.0'}, 'MATCHES'),
    ({'source': '10.0.1.0'}, 'NO_MATCH'),
    ({'destination': '192.0.3.0'}, 'NO_MATCH'),
])
def test_boundaries_propagate_to_group_status(values, changes, expected_status) -> None:
    flow, saved = values
    flow.update(changes)
    before = deepcopy((flow, saved))
    result = check(flow, create_relevance_provider([
        {'device': 'fw-a', 'acl': 'outside'},
    ]), create_snapshot_provider([saved]))
    assert result == [{
        'device': 'fw-a', 'acl': 'outside', 'placements': saved['placements'],
        'status': expected_status,
        'rules': saved['rules'] if expected_status == 'MATCHES' else [],
    }]
    assert (flow, saved) == before


@pytest.mark.parametrize(('source_port', 'destination_port'), [(0, 65535), (65535, 0)])
def test_host_and_full_ipv4_ranges_with_extreme_ports(values, source_port, destination_port) -> None:
    flow, saved = values
    flow.update(source='0.0.0.0', destination='255.255.255.255',
                source_port=source_port, destination_port=destination_port)
    saved['rules'][0].update(
        source='0.0.0.0', destination='255.255.255.255/32', protocol='any',
        source_ports=[0, 65535], destination_ports=[0, 65535],
    )
    saved['rules'].append(dict(saved['rules'][0], id='all-ipv4',
                               source='0.0.0.0/0', destination='0.0.0.0/0'))
    assert build_evidence_group(flow, saved) == {
        'device': 'fw-a', 'acl': 'outside', 'placements': saved['placements'],
        'status': 'MATCHES', 'rules': saved['rules'],
    }


def test_empty_and_nonmatching_snapshots_remain_distinct_contexts(values) -> None:
    flow, saved = values
    saved['rules'][0]['protocol'] = 'tcp'
    empty: Snapshot = dict(saved, acl='inside', placements=[], rules=[])
    other: Snapshot = dict(empty, device='fw-b')
    unused: Snapshot = dict(saved, device='unused')
    pairs: list[DeviceAclPair] = [
        {'device': item['device'], 'acl': item['acl']}
        for item in (empty, saved, empty, other)
    ]
    result = check(flow, create_relevance_provider(pairs),
                   create_snapshot_provider([unused, other, saved, empty]))
    assert result == [
        {'device': 'fw-a', 'acl': 'inside', 'placements': [], 'status': 'NO_MATCH', 'rules': []},
        {'device': 'fw-a', 'acl': 'outside', 'placements': saved['placements'],
         'status': 'NO_MATCH', 'rules': []},
        {'device': 'fw-b', 'acl': 'inside', 'placements': [], 'status': 'NO_MATCH', 'rules': []},
    ]


def test_late_missing_snapshot_raises_and_next_invocation_recovers(values, capsys) -> None:
    flow, saved = values
    pairs: list[DeviceAclPair] = [
        {'device': 'fw-a', 'acl': 'outside'},
        {'device': 'fw-a', 'acl': 'missing'},
    ]
    before = deepcopy((flow, saved, pairs))
    provider = create_snapshot_provider([saved])
    with pytest.raises(ExpectedApplicationFailure, match='Missing snapshot') as failure:
        check(flow, create_relevance_provider(pairs), provider)
    assert 'fw-a' in failure.value.reason
    assert 'missing' in failure.value.reason
    assert isinstance(failure.value.__cause__, KeyError)
    assert (flow, saved, pairs) == before
    assert capsys.readouterr() == ('', '')
    assert check(flow, create_relevance_provider(pairs[:1]), provider) == [
        dict(saved, status='MATCHES'),
    ]


def test_domain_usage_example_returns_both_actions() -> None:
    result = investigate_saved_acl()
    assert result == [{
        'device': 'fw-demo', 'acl': 'outside', 'status': 'MATCHES',
        'placements': [{'interface': 'wan0', 'direction': 'in'}],
        'rules': [
            {'id': 'z-deny', 'source': '10.0.0.0/24', 'destination': '192.0.2.10',
             'protocol': 'tcp', 'source_ports': [49000, 51000],
             'destination_ports': [443, 443], 'action': 'deny'},
            {'id': 'a-permit', 'source': '10.0.0.0/24', 'destination': '192.0.2.10',
             'protocol': 'any', 'source_ports': [49000, 51000],
             'destination_ports': [443, 443], 'action': 'permit'},
        ],
    }]
    assert investigate_saved_acl() == result
