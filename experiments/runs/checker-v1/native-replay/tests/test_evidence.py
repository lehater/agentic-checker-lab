from copy import deepcopy
from unittest.mock import create_autospec

import pytest

from src.acl_checker.application.evidence import (
    retrieve_relevant_pairs,
    retrieve_required_snapshot,
)
from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import ExpectedApplicationFailure


@pytest.fixture
def flow():
    return {'source': '10.0.0.1', 'destination': '192.0.2.10',
            'protocol': 'tcp', 'source_port': 0, 'destination_port': 65535}


def test_relevant_pairs_preserve_first_seen_order_and_inputs(flow):
    pairs = [{'device': 'fw-b', 'acl': 'outside'},
             {'device': 'fw-a', 'acl': 'outside'},
             {'device': 'fw-b', 'acl': 'outside'},
             {'device': 'fw-b', 'acl': 'inside'}]
    before = deepcopy((flow, pairs))
    source = create_autospec(create_relevance_provider(pairs), return_value=pairs)

    result = retrieve_relevant_pairs(flow, source)

    source.assert_called_once_with(flow['source'], flow['destination'])
    assert result == [pairs[0], pairs[1], pairs[3]]
    assert result is not pairs
    assert (flow, pairs) == before


def test_empty_relevance_returns_new_list(flow):
    pairs = []
    source = create_autospec(create_relevance_provider(pairs), return_value=pairs)

    result = retrieve_relevant_pairs(flow, source)

    source.assert_called_once_with(flow['source'], flow['destination'])
    assert result == []
    assert result is not pairs


@pytest.mark.parametrize('error', [ExpectedApplicationFailure('unavailable'),
                                 RuntimeError('source bug')])
def test_relevance_failure_propagates_without_retry(flow, error):
    before = deepcopy(flow)
    source = create_autospec(create_relevance_provider([]), side_effect=error)

    with pytest.raises(type(error)) as failure:
        retrieve_relevant_pairs(flow, source)

    assert failure.value is error
    source.assert_called_once_with(flow['source'], flow['destination'])
    assert flow == before


@pytest.mark.parametrize('empty', [False, True])
def test_required_snapshot_preserves_full_evidence(empty):
    pair = {'device': 'fw-a', 'acl': 'outside'}
    rules = [
        {'id': identifier, 'source': '10.0.0.0/24',
         'destination': '192.0.2.10', 'protocol': 'any',
         'source_ports': [0, 65535], 'destination_ports': [440, 450],
         'action': action}
        for identifier, action in [('z-deny', 'deny'), ('a-permit', 'permit')]
    ]
    value = {**pair, 'placements': [] if empty else [
        {'interface': 'wan0', 'direction': 'in'}, {'global': True}],
        'rules': [] if empty else rules}
    before = deepcopy((pair, value))
    source = create_autospec(create_snapshot_provider([value]), return_value=value)

    result = retrieve_required_snapshot(pair, source)

    source.assert_called_once_with('fw-a', 'outside')
    assert result == before[1]
    assert (pair, value) == before


@pytest.mark.parametrize('error', [ExpectedApplicationFailure('missing fw-a/outside'),
                                 RuntimeError('source bug')])
def test_snapshot_failure_propagates_without_fallback(error):
    pair = {'device': 'fw-a', 'acl': 'outside'}
    before = deepcopy(pair)
    source = create_autospec(create_snapshot_provider([]), side_effect=error)

    with pytest.raises(type(error)) as failure:
        retrieve_required_snapshot(pair, source)

    assert failure.value is error
    source.assert_called_once_with('fw-a', 'outside')
    assert pair == before
