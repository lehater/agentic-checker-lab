"""Реальные sources → evidence → use case; подмены только на границах источников."""

from copy import deepcopy
from unittest.mock import call, create_autospec

import pytest

from examples.application_usage import investigate_snapshots, select_snapshots
from src.acl_checker.application.evidence import (
    retrieve_relevant_pairs,
    retrieve_required_snapshot,
)
from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import (
    DeviceAclPair, ExpectedApplicationFailure, Snapshot,
)
from src.acl_checker.domain.application.check import build_evidence_group, check
from src.acl_checker.domain.types import Flow


@pytest.fixture
def values() -> tuple[Flow, list[DeviceAclPair], list[Snapshot]]:
    flow: Flow = {
        'source': '10.0.0.1', 'destination': '192.0.2.10',
        'protocol': 'tcp', 'source_port': 0, 'destination_port': 65535,
    }
    pairs: list[DeviceAclPair] = [
        {'device': 'fw-b', 'acl': 'outside'},
        {'device': 'fw-a', 'acl': 'outside'},
        {'device': 'fw-b', 'acl': 'outside'},
        {'device': 'fw-b', 'acl': 'inside'},
    ]
    snapshots: list[Snapshot] = [
        {'device': 'unused', 'acl': 'outside', 'placements': [], 'rules': []},
        {'device': 'fw-b', 'acl': 'inside', 'placements': [], 'rules': []},
        {'device': 'fw-a', 'acl': 'outside', 'placements': [{'global': True}],
         'rules': [
             {'id': 'udp-only', 'source': '0.0.0.0/0',
              'destination': '0.0.0.0/0', 'protocol': 'udp',
              'source_ports': [0, 65535], 'destination_ports': [0, 65535],
              'action': 'permit'},
         ]},
        {'device': 'fw-b', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'},
                        {'interface': 'lan0', 'direction': 'out'}],
         'rules': [
             {'id': 'z-deny', 'source': '10.0.0.1',
              'destination': '192.0.2.0/24', 'protocol': 'tcp',
              'source_ports': [0, 0], 'destination_ports': [65535, 65535],
              'action': 'deny'},
             {'id': 'a-permit', 'source': '0.0.0.0/0',
              'destination': '192.0.2.10/32', 'protocol': 'any',
              'source_ports': [0, 65535], 'destination_ports': [0, 65535],
              'action': 'permit'},
         ]},
    ]
    return flow, pairs, snapshots


def test_sources_and_evidence_feed_complete_groups_in_selection_order(values) -> None:
    flow, pairs, snapshots = values
    before = deepcopy(values)
    relevance_provider = create_relevance_provider(tuple(pairs))
    snapshot_provider = create_snapshot_provider(tuple(snapshots))
    relevance = create_autospec(relevance_provider, side_effect=relevance_provider)
    snapshot = create_autospec(snapshot_provider, side_effect=snapshot_provider)

    selected = retrieve_relevant_pairs(flow, relevance)
    saved = [retrieve_required_snapshot(pair, snapshot) for pair in selected]

    assert selected == [
        {'device': 'fw-b', 'acl': 'outside'},
        {'device': 'fw-a', 'acl': 'outside'},
        {'device': 'fw-b', 'acl': 'inside'},
    ]
    assert saved == [snapshots[3], snapshots[2], snapshots[1]]
    relevance.assert_called_once_with('10.0.0.1', '192.0.2.10')
    assert snapshot.call_args_list == [
        call('fw-b', 'outside'), call('fw-a', 'outside'), call('fw-b', 'inside'),
    ]
    expected = [
        {'device': 'fw-b', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'},
                        {'interface': 'lan0', 'direction': 'out'}],
         'status': 'MATCHES', 'rules': deepcopy(snapshots[3]['rules'])},
        {'device': 'fw-a', 'acl': 'outside', 'placements': [{'global': True}],
         'status': 'NO_MATCH', 'rules': []},
        {'device': 'fw-b', 'acl': 'inside', 'placements': [],
         'status': 'NO_MATCH', 'rules': []},
    ]
    assert [build_evidence_group(flow, item) for item in saved] == expected
    assert check(flow, relevance_provider, snapshot_provider) == expected
    assert values == before


def test_empty_selection_never_requests_a_snapshot(values) -> None:
    flow, _, snapshots = values
    provider = create_snapshot_provider(snapshots)
    snapshot = create_autospec(provider, side_effect=provider)
    relevance = create_relevance_provider(())

    assert retrieve_relevant_pairs(flow, relevance) == []
    assert check(flow, relevance, snapshot) == []
    assert select_snapshots(flow, [], snapshots) == []
    snapshot.assert_not_called()


def test_missing_exact_pair_aborts_selection_and_sources_remain_usable(values) -> None:
    flow, pairs, snapshots = values
    # fw-a/outside отсутствует, хотя одноимённый ACL другого устройства есть.
    available = [snapshots[0], snapshots[1], snapshots[3]]
    before = deepcopy((flow, pairs, available))
    provider = create_snapshot_provider(available)
    snapshot = create_autospec(provider, side_effect=provider)
    selected = retrieve_relevant_pairs(flow, create_relevance_provider(pairs))

    with pytest.raises(ExpectedApplicationFailure) as failure:
        [retrieve_required_snapshot(pair, snapshot) for pair in selected]

    assert 'fw-a' in failure.value.reason
    assert 'outside' in failure.value.reason
    assert isinstance(failure.value.__cause__, KeyError)
    assert snapshot.call_args_list == [call('fw-b', 'outside'), call('fw-a', 'outside')]
    with pytest.raises(ExpectedApplicationFailure):
        check(flow, create_relevance_provider(pairs), provider)
    assert retrieve_required_snapshot(selected[0], provider) == snapshots[3]
    assert (flow, pairs, available) == before


@pytest.mark.parametrize('stage', ['relevance', 'snapshot'])
@pytest.mark.parametrize('error_type', [ExpectedApplicationFailure, RuntimeError])
def test_boundary_failures_propagate_unchanged_without_retry(values, stage, error_type) -> None:
    flow, pairs, snapshots = values
    before = deepcopy(values)
    error = error_type('source unavailable')
    relevance_provider = create_relevance_provider(pairs)
    snapshot_provider = create_snapshot_provider(snapshots)
    relevance = create_autospec(
        relevance_provider,
        side_effect=error if stage == 'relevance' else relevance_provider,
    )
    snapshot = create_autospec(snapshot_provider, side_effect=error)

    with pytest.raises(error_type) as failure:
        selected = retrieve_relevant_pairs(flow, relevance)
        [retrieve_required_snapshot(pair, snapshot) for pair in selected]

    assert failure.value is error
    relevance.assert_called_once_with('10.0.0.1', '192.0.2.10')
    if stage == 'relevance':
        snapshot.assert_not_called()
    else:
        snapshot.assert_called_once_with('fw-b', 'outside')
    assert values == before


def test_interleaved_sources_do_not_share_selection_or_snapshot_state(values) -> None:
    flow, pairs, snapshots = values
    relevance_a = create_relevance_provider(pairs)
    snapshot_a = create_snapshot_provider(snapshots)
    other: Snapshot = {
        'device': 'fw-b', 'acl': 'outside', 'placements': [{'global': True}], 'rules': [],
    }
    relevance_b = create_relevance_provider([{'device': 'fw-b', 'acl': 'outside'}])
    snapshot_b = create_snapshot_provider([other])

    for _ in range(2):
        selected_a = retrieve_relevant_pairs(flow, relevance_a)
        selected_b = retrieve_relevant_pairs(flow, relevance_b)
        assert retrieve_required_snapshot(selected_a[0], snapshot_a) == snapshots[3]
        assert retrieve_required_snapshot(selected_b[0], snapshot_b) == other
        selected_a.clear()
        assert len(retrieve_relevant_pairs(flow, relevance_a)) == 3
        assert retrieve_relevant_pairs(flow, relevance_b) == selected_b


def test_usage_examples_select_full_snapshots_and_report_only_matches(values) -> None:
    flow, pairs, snapshots = values
    before = deepcopy(values)
    assert select_snapshots(flow, pairs, snapshots) == [
        snapshots[3], snapshots[2], snapshots[1],
    ]
    groups = investigate_snapshots(flow, pairs, snapshots)
    assert [group['status'] for group in groups] == ['MATCHES', 'NO_MATCH', 'NO_MATCH']
    assert groups[0]['rules'] == snapshots[3]['rules']
    for example in (select_snapshots, investigate_snapshots):
        with pytest.raises(ExpectedApplicationFailure, match='fw-a'):
            example(flow, pairs, [snapshots[3]])
    assert values == before
