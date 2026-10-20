from copy import deepcopy

import pytest

from src.acl_checker.application.sources import create_snapshot_provider
from src.acl_checker.application.types import ExpectedApplicationFailure
from src.acl_checker.domain.application.check import (
    build_evidence_group,
    check,
    collect_matching_evidence,
    determine_evidence_status,
)


def evidence_values():
    flow = {'source': '10.0.0.1', 'destination': '192.0.2.10',
            'protocol': 'tcp', 'source_port': 50000, 'destination_port': 443}
    deny = {'id': 'z-deny', 'source': '10.0.0.0/24',
            'destination': '192.0.2.10/32', 'protocol': 'tcp',
            'source_ports': [50000, 50000], 'destination_ports': [443, 443],
            'action': 'deny'}
    permit = dict(deny, id='a-permit', action='permit', protocol='any')
    miss = dict(deny, id='udp-only', protocol='udp')
    snapshot = {'device': 'fw-a', 'acl': 'outside',
                'placements': [{'interface': 'wan0', 'direction': 'in'},
                               {'global': True}],
                'rules': [deny, miss, permit]}
    return flow, snapshot


def test_collect_preserves_all_original_rules_and_order():
    flow, snapshot = evidence_values()
    before = deepcopy((flow, snapshot))
    result = collect_matching_evidence(flow, tuple(snapshot['rules']))
    assert result == [snapshot['rules'][0], snapshot['rules'][2]]
    assert result[0] is snapshot['rules'][0]
    assert result[1] is snapshot['rules'][2]
    assert (flow, snapshot) == before


def test_collect_empty_and_nonmatching_rules():
    flow, snapshot = evidence_values()
    assert collect_matching_evidence(flow, []) == []
    assert collect_matching_evidence(flow, [snapshot['rules'][1]]) == []


def test_status_depends_only_on_presence_of_evidence():
    _, snapshot = evidence_values()
    assert determine_evidence_status(()) == 'NO_MATCH'
    for rule in snapshot['rules']:
        assert determine_evidence_status((rule,)) == 'MATCHES'


def test_group_has_exact_fields_and_does_not_multiply_rules_by_placements():
    flow, snapshot = evidence_values()
    before = deepcopy((flow, snapshot))
    assert build_evidence_group(flow, snapshot) == {
        'device': 'fw-a', 'acl': 'outside',
        'placements': [{'interface': 'wan0', 'direction': 'in'}, {'global': True}],
        'status': 'MATCHES', 'rules': [snapshot['rules'][0], snapshot['rules'][2]],
    }
    assert (flow, snapshot) == before


def test_group_keeps_empty_placements_and_no_match_snapshots():
    flow, snapshot = evidence_values()
    for rules in ([], [snapshot['rules'][1]]):
        empty = dict(snapshot, placements=[], rules=rules)
        assert build_evidence_group(flow, empty) == {
            'device': 'fw-a', 'acl': 'outside', 'placements': [],
            'status': 'NO_MATCH', 'rules': [],
        }


def test_check_calls_sources_once_per_unique_pair_and_preserves_inputs():
    flow, first = evidence_values()
    second = dict(first, acl='inside', placements=[], rules=[])
    third = dict(second, device='fw-b')
    pairs = [{'device': item['device'], 'acl': item['acl']}
             for item in (first, second, first, third, second)]
    snapshots = [first, second, third]
    before = deepcopy((flow, pairs, snapshots))
    events = []
    provider = create_snapshot_provider(snapshots)

    def relevance(source, destination):
        events.append(('relevance', source, destination))
        return pairs

    def snapshot(device, acl):
        events.append(('snapshot', device, acl))
        return provider(device, acl)

    result = check(flow, relevance, snapshot)
    assert result == [
        dict(first, status='MATCHES', rules=[first['rules'][0], first['rules'][2]]),
        dict(second, status='NO_MATCH'), dict(third, status='NO_MATCH'),
    ]
    assert events == [('relevance', '10.0.0.1', '192.0.2.10'),
                      ('snapshot', 'fw-a', 'outside'),
                      ('snapshot', 'fw-a', 'inside'),
                      ('snapshot', 'fw-b', 'inside')]
    assert (flow, pairs, snapshots) == before


def test_check_empty_relevance_does_not_request_snapshots():
    flow, _ = evidence_values()
    calls = []

    def relevance(source, destination):
        calls.append((source, destination))
        return []

    def snapshot(device, acl):
        pytest.fail('No snapshot should be requested')

    assert check(flow, relevance, snapshot) == []
    assert calls == [(flow['source'], flow['destination'])]


def test_check_propagates_source_failures_without_retry_or_partial_result():
    flow, first = evidence_values()
    before = deepcopy((flow, first))
    for error in (ExpectedApplicationFailure('missing snapshot'), RuntimeError('bug')):
        for failing_source in ('relevance', 'snapshot'):
            events = []

            def relevance(source, destination):
                events.append('relevance')
                if failing_source == 'relevance':
                    raise error
                return [{'device': 'fw-a', 'acl': acl}
                        for acl in ('outside', 'missing', 'unvisited')]

            def snapshot(device, acl):
                events.append(acl)
                if acl == 'missing':
                    raise error
                return first

            with pytest.raises(type(error)) as failure:
                check(flow, relevance, snapshot)
            assert failure.value is error
            assert events == (['relevance'] if failing_source == 'relevance'
                              else ['relevance', 'outside', 'missing'])
            assert (flow, first) == before
