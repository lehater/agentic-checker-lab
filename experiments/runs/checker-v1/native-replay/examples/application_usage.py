"""Отбор снимков и полный отчёт для заранее проверенных synthetic данных."""

from collections.abc import Sequence

from src.acl_checker.application.evidence import (
    retrieve_relevant_pairs,
    retrieve_required_snapshot,
)
from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import DeviceAclPair, ReportGroups, Snapshot
from src.acl_checker.domain.application.check import check
from src.acl_checker.domain.types import Flow


def select_snapshots(
    flow: Flow, pairs: Sequence[DeviceAclPair], snapshots: Sequence[Snapshot],
) -> list[Snapshot]:
    """Получить полные снимки уникальных пар в порядке релевантности.

    Все значения должны быть предварительно проверены внешним адаптером.
    ExpectedApplicationFailure передаётся вызывающему коду без partial success.
    """
    relevance = create_relevance_provider(pairs)
    snapshot = create_snapshot_provider(snapshots)
    return [
        retrieve_required_snapshot(pair, snapshot)
        for pair in retrieve_relevant_pairs(flow, relevance)
    ]


def investigate_snapshots(
    flow: Flow, pairs: Sequence[DeviceAclPair], snapshots: Sequence[Snapshot],
) -> ReportGroups:
    """Передать проверенные локальные данные основному use case check."""
    return check(
        flow, create_relevance_provider(pairs), create_snapshot_provider(snapshots),
    )
