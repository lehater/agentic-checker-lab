from __future__ import annotations

from copy import deepcopy

import pytest

from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import (
    DeviceAclPair,
    ExpectedApplicationFailure,
    ReportGroups,
    Snapshot,
)
from src.acl_checker.domain.application.check import check
from src.acl_checker.domain.types import Flow


def application_values() -> tuple[Flow, list[DeviceAclPair], list[Snapshot]]:
    """Фиксированные данные SC-ALL принятого контракта."""
    flow: Flow = {
        'source': '10.0.0.1', 'destination': '192.0.2.10',
        'protocol': 'tcp', 'source_port': 50000, 'destination_port': 443,
    }
    pairs: list[DeviceAclPair] = [
        {'device': 'fw-a', 'acl': 'outside'},
        {'device': 'fw-a', 'acl': 'inside'},
        {'device': 'fw-b', 'acl': 'global'},
        {'device': 'fw-a', 'acl': 'outside'},
    ]
    snapshots: list[Snapshot] = [
        {'device': 'fw-a', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'}],
         'rules': [
             {'id': 'z-deny', 'source': '10.0.0.0/24',
              'destination': '192.0.2.10/32', 'protocol': 'tcp',
              'source_ports': [50000, 50000], 'destination_ports': [443, 443],
              'action': 'deny'},
             {'id': 'a-permit', 'source': '0.0.0.0/0',
              'destination': '192.0.2.0/24', 'protocol': 'any',
              'source_ports': [0, 65535], 'destination_ports': [440, 450],
              'action': 'permit'},
             {'id': 'wrong-source', 'source': '10.0.1.0/24',
              'destination': '0.0.0.0/0', 'protocol': 'any',
              'source_ports': [0, 65535], 'destination_ports': [0, 65535],
              'action': 'permit'},
         ]},
        {'device': 'fw-a', 'acl': 'inside',
         'placements': [{'interface': 'lan0', 'direction': 'out'}], 'rules': []},
        {'device': 'fw-b', 'acl': 'global', 'placements': [{'global': True}],
         'rules': [
             {'id': 'udp-only', 'source': '0.0.0.0/0',
              'destination': '0.0.0.0/0', 'protocol': 'udp',
              'source_ports': [0, 65535], 'destination_ports': [0, 65535],
              'action': 'permit'},
         ]},
        {'device': 'irrelevant', 'acl': 'unused', 'placements': [], 'rules': []},
    ]
    return flow, pairs, snapshots


def expected_groups() -> ReportGroups:
    """Полный независимый oracle SC-ALL, без вызовов рабочего кода."""
    return [
        {'device': 'fw-a', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'}],
         'status': 'MATCHES', 'rules': [
             {'id': 'z-deny', 'source': '10.0.0.0/24',
              'destination': '192.0.2.10/32', 'protocol': 'tcp',
              'source_ports': [50000, 50000], 'destination_ports': [443, 443],
              'action': 'deny'},
             {'id': 'a-permit', 'source': '0.0.0.0/0',
              'destination': '192.0.2.0/24', 'protocol': 'any',
              'source_ports': [0, 65535], 'destination_ports': [440, 450],
              'action': 'permit'},
         ]},
        {'device': 'fw-a', 'acl': 'inside',
         'placements': [{'interface': 'lan0', 'direction': 'out'}],
         'status': 'NO_MATCH', 'rules': []},
        {'device': 'fw-b', 'acl': 'global', 'placements': [{'global': True}],
         'status': 'NO_MATCH', 'rules': []},
    ]


def test_interchangeable_providers() -> None:
    """Фабричные и независимые spy-callables дают ожидаемый полный отчёт."""
    flow, pairs, snapshots = application_values()
    expected = expected_groups()
    assert check(flow, create_relevance_provider(pairs),
                 create_snapshot_provider(snapshots)) == expected
    calls: list[tuple[str, str, str]] = []

    def relevance(source: str, destination: str) -> list[DeviceAclPair]:
        calls.append(('relevance', source, destination))
        return pairs

    def snapshot(device: str, acl: str) -> Snapshot:
        calls.append(('snapshot', device, acl))
        for item in snapshots:
            if (item['device'], item['acl']) == (device, acl):
                return item
        pytest.fail(f'Unexpected snapshot request: {device}/{acl}')

    assert check(flow, relevance, snapshot) == expected
    assert calls == [
        ('relevance', '10.0.0.1', '192.0.2.10'),
        ('snapshot', 'fw-a', 'outside'),
        ('snapshot', 'fw-a', 'inside'),
        ('snapshot', 'fw-b', 'global'),
    ]


def test_atomic_request_failure() -> None:
    """Ошибка прерывает запрос без частичного отчёта, retry или fallback."""
    flow, pairs, snapshots = application_values()
    for error in (ExpectedApplicationFailure('source unavailable'),
                  RuntimeError('source bug')):
        for stage in ('relevance', 'first-snapshot', 'late-snapshot'):
            calls: list[tuple[str, str, str]] = []
            provider = create_snapshot_provider(snapshots)

            def relevance(source: str, destination: str) -> list[DeviceAclPair]:
                calls.append(('relevance', source, destination))
                if stage == 'relevance':
                    raise error
                return pairs

            def snapshot(device: str, acl: str) -> Snapshot:
                calls.append(('snapshot', device, acl))
                if stage == 'first-snapshot' or acl == 'inside':
                    raise error
                return provider(device, acl)

            # Любой возврат, включая частичный отчёт или [], нарушает raises.
            with pytest.raises(type(error)) as failure:
                check(flow, relevance, snapshot)
            assert failure.value is error
            expected_calls = [('relevance', '10.0.0.1', '192.0.2.10')]
            if stage != 'relevance':
                expected_calls.append(('snapshot', 'fw-a', 'outside'))
            if stage == 'late-snapshot':
                expected_calls.append(('snapshot', 'fw-a', 'inside'))
            assert calls == expected_calls

    # Реальное отсутствие позднего снимка также не становится NO_MATCH.
    calls = []
    provider = create_snapshot_provider([snapshots[0]])

    def missing_snapshot(device: str, acl: str) -> Snapshot:
        calls.append(('snapshot', device, acl))
        return provider(device, acl)

    with pytest.raises(ExpectedApplicationFailure) as failure:
        check(flow, create_relevance_provider(pairs), missing_snapshot)
    assert 'fw-a' in failure.value.reason
    assert 'inside' in failure.value.reason
    assert calls == [('snapshot', 'fw-a', 'outside'),
                     ('snapshot', 'fw-a', 'inside')]


def test_invocation_isolation() -> None:
    """A/B/A с одинаковой парой и разными evidence не использует общий кеш."""
    flow_a, pairs, snapshots = application_values()
    flow_b: Flow = dict(flow_a, source='10.0.0.2', protocol='udp')
    relevance_a = create_relevance_provider(pairs)
    snapshot_a = create_snapshot_provider(snapshots)
    relevance_b = create_relevance_provider([{'device': 'fw-a', 'acl': 'outside'}])
    snapshot_b = create_snapshot_provider([
        {'device': 'fw-a', 'acl': 'outside', 'placements': [], 'rules': []},
    ])
    assert check(flow_a, relevance_a, snapshot_a) == expected_groups()
    assert check(flow_b, relevance_b, snapshot_b) == [
        {'device': 'fw-a', 'acl': 'outside', 'placements': [],
         'status': 'NO_MATCH', 'rules': []},
    ]
    assert check(flow_a, relevance_a, snapshot_a) == expected_groups()
    with pytest.raises(ExpectedApplicationFailure):
        check(flow_b, relevance_b, create_snapshot_provider([]))
    assert check(flow_a, relevance_a, snapshot_a) == expected_groups()
    calls: list[tuple[str, str]] = []

    def empty_relevance(source: str, destination: str) -> list[DeviceAclPair]:
        calls.append((source, destination))
        return []

    def forbidden_snapshot(device: str, acl: str) -> Snapshot:
        pytest.fail(f'Empty relevance must not request {device}/{acl}')

    assert check(flow_b, empty_relevance, forbidden_snapshot) == []
    assert calls == [('10.0.0.2', '192.0.2.10')]
    assert check(flow_a, relevance_a, snapshot_a) == expected_groups()


def test_application_input_immutability() -> None:
    """Прямые вложенные входы сохраняются при успехе и позднем отказе."""
    for fail_late in (False, True):
        flow, pairs, snapshots = application_values()
        before = deepcopy((flow, pairs, snapshots))
        calls: list[tuple[str, str]] = []
        error = ExpectedApplicationFailure('late snapshot unavailable')

        def relevance(source: str, destination: str) -> list[DeviceAclPair]:
            return pairs

        def snapshot(device: str, acl: str) -> Snapshot:
            calls.append((device, acl))
            if fail_late and acl == 'global':
                raise error
            for item in snapshots:
                if (item['device'], item['acl']) == (device, acl):
                    return item
            pytest.fail(f'Unexpected snapshot request: {device}/{acl}')

        if fail_late:
            with pytest.raises(ExpectedApplicationFailure) as failure:
                check(flow, relevance, snapshot)
            assert failure.value is error
        else:
            assert check(flow, relevance, snapshot) == expected_groups()
        assert calls == [('fw-a', 'outside'), ('fw-a', 'inside'), ('fw-b', 'global')]
        assert (flow, pairs, snapshots) == before
