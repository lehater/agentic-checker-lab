"""Чистое исследование заранее проверенных синтетических значений."""

from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import ReportGroups, Snapshot
from src.acl_checker.domain.application.check import check
from src.acl_checker.domain.matching import matches
from src.acl_checker.domain.types import Flow, OriginalRule


def investigate_saved_acl() -> ReportGroups:
    """Вернуть оба совпадения: deny не прекращает поиск следующих правил.

    Здесь используются только корректные литералы. Внешние данные сначала
    должны пройти validate_document, как в examples.input_usage.
    """
    flow: Flow = {
        'source': '10.0.0.1', 'destination': '192.0.2.10',
        'protocol': 'tcp', 'source_port': 50000, 'destination_port': 443,
    }
    deny: OriginalRule = {
        'id': 'z-deny', 'source': '10.0.0.0/24',
        'destination': '192.0.2.10', 'protocol': 'tcp',
        'source_ports': [49000, 51000], 'destination_ports': [443, 443],
        'action': 'deny',
    }
    permit: OriginalRule = dict(deny, id='a-permit', protocol='any', action='permit')
    saved: Snapshot = {
        'device': 'fw-demo', 'acl': 'outside',
        'placements': [{'interface': 'wan0', 'direction': 'in'}],
        'rules': [deny, permit],
    }
    # matches отвечает только за предикат, без интерпретации action.
    assert matches(flow, deny) is True
    return check(
        flow,
        create_relevance_provider([{'device': 'fw-demo', 'acl': 'outside'}]),
        create_snapshot_provider([saved]),
    )
