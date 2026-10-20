from copy import deepcopy

import pytest

from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import ExpectedApplicationFailure


def test_relevance_preserves_order_duplicates_and_returns_fresh_lists():
    pairs = [{'device': 'fw-b', 'acl': 'outside'},
             {'device': 'fw-a', 'acl': 'inside'},
             {'device': 'fw-b', 'acl': 'outside'}]
    before = deepcopy(pairs)
    provider = create_relevance_provider(pairs)

    first = provider('10.0.0.1', '192.0.2.10')
    second = provider('10.0.0.1', '192.0.2.10')

    assert first == second == before
    assert first is not second
    assert first is not pairs
    first.clear()
    assert provider('10.0.0.1', '192.0.2.10') == before
    assert pairs == before


@pytest.mark.parametrize('pairs', [[], ()])
def test_empty_relevance_returns_fresh_empty_lists(pairs):
    provider = create_relevance_provider(pairs)

    first = provider('10.0.0.1', '192.0.2.10')
    second = provider('10.0.0.1', '192.0.2.10')

    assert first == second == []
    assert first is not second
    assert first is not pairs


def test_snapshot_preserves_full_evidence_and_selects_exact_pair():
    rules = [
        {'id': identifier, 'source': '10.0.0.0/24',
         'destination': '192.0.2.10/32', 'protocol': 'any',
         'source_ports': [0, 65535], 'destination_ports': [440, 450],
         'action': action}
        for identifier, action in [('z-deny', 'deny'), ('a-permit', 'permit')]
    ]
    snapshots = [
        {'device': 'fw-a', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'},
                        {'global': True}], 'rules': rules},
        {'device': 'fw-a', 'acl': 'inside', 'placements': [], 'rules': []},
        {'device': 'fw-b', 'acl': 'outside', 'placements': [], 'rules': []},
    ]
    before = deepcopy(snapshots)
    provider = create_snapshot_provider(tuple(snapshots))

    for expected in before:
        assert provider(expected['device'], expected['acl']) == expected
    assert provider('fw-a', 'outside') == before[0]
    assert snapshots == before


@pytest.mark.parametrize('snapshots', [[], ()])
def test_empty_snapshot_source_fails_only_when_called(snapshots):
    provider = create_snapshot_provider(snapshots)

    with pytest.raises(ExpectedApplicationFailure) as failure:
        provider('missing-device', 'missing-acl')

    assert 'missing-device' in failure.value.reason
    assert 'missing-acl' in failure.value.reason


def test_missing_exact_pair_reports_both_identifiers_and_keeps_source_usable():
    snapshots = [
        {'device': 'fw-a', 'acl': 'inside', 'placements': [], 'rules': []},
        {'device': 'fw-b', 'acl': 'outside', 'placements': [], 'rules': []},
    ]
    before = deepcopy(snapshots)
    provider = create_snapshot_provider(snapshots)

    with pytest.raises(ExpectedApplicationFailure) as failure:
        provider('fw-a', 'outside')

    assert 'fw-a' in failure.value.reason
    assert 'outside' in failure.value.reason
    assert provider('fw-a', 'inside') == before[0]
    assert snapshots == before


def test_providers_keep_each_invocation_isolated():
    pair = {'device': 'fw-a', 'acl': 'outside'}
    first = {**pair, 'placements': [{'global': True}], 'rules': []}
    second = {**pair, 'placements': [], 'rules': []}
    relevance_a = create_relevance_provider((pair, pair))
    snapshot_a = create_snapshot_provider((first,))
    relevance_b = create_relevance_provider(())
    snapshot_b = create_snapshot_provider((second,))

    assert relevance_a('10.0.0.1', '192.0.2.10') == [pair, pair]
    assert snapshot_a('fw-a', 'outside') == first
    assert relevance_b('10.0.0.2', '192.0.2.20') == []
    assert snapshot_b('fw-a', 'outside') == second
    assert relevance_a('10.0.0.1', '192.0.2.10') == [pair, pair]
    assert snapshot_a('fw-a', 'outside') == first
