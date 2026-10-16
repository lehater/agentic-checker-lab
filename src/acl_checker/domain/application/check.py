from __future__ import annotations
from collections.abc import Sequence
from typing import Literal

from src.acl_checker.application.types import (
    RelevanceSource,
    ReportGroup,
    ReportGroups,
    Snapshot,
    SnapshotSource,
)
from src.acl_checker.domain.matching import matches
from src.acl_checker.domain.types import Flow, OriginalRule


def collect_matching_evidence(
    flow: Flow,
    rules: Sequence[OriginalRule],
) -> list[OriginalRule]:
    """Собрать все совпавшие правила в порядке предоставленной последовательности.

    Args:
        flow: Предварительно проверенный конкретный IPv4-поток.
        rules: Проверенные полные правила одного снимка в исходном порядке.

    Returns:
        list[OriginalRule]: Новый список всех правил, для которых matches
            возвращает True; исходные объекты и все их поля сохраняются.
            Пустая последовательность или отсутствие совпадений дают [].

    Вызывается build_evidence_group. Проверяет каждое правило ровно один раз,
    включая правила после первого совпадения. Не сортирует, не удаляет
    совпадения по action и не синтезирует implicit deny.
    Поток, последовательность правил и вложенные значения не изменяются.
    """
    return [rule for rule in rules if matches(flow, rule)]


def determine_evidence_status(
    matching_rules: Sequence[OriginalRule],
) -> Literal['MATCHES', 'NO_MATCH']:
    """Определить статус группы по уже собранным совпадениям.

    Args:
        matching_rules: Полная последовательность совпавших правил одного
            корректного полученного снимка; значения не изменяются.

    Returns:
        Literal['MATCHES', 'NO_MATCH']: MATCHES для непустой
            последовательности, иначе NO_MATCH.

    Вызывается build_evidence_group. Статус не зависит от action и не является
    общим permit/deny verdict. Ошибки источников и отсутствие снимка нельзя
    представлять пустой последовательностью для получения NO_MATCH.
    """
    return 'MATCHES' if matching_rules else 'NO_MATCH'


def build_evidence_group(flow: Flow, snapshot: Snapshot) -> ReportGroup:
    """Собрать одну группу свидетельств для предоставленного снимка ACL.

    Args:
        flow: Предварительно проверенный конкретный IPv4-поток.
        snapshot: Корректный снимок выбранной пары device/acl с placements
            и полным упорядоченным списком правил.

    Returns:
        ReportGroup: Группа ровно с полями device, acl, placements, status,
            rules. Контекст и placements берутся из snapshot; rules содержит
            полные совпавшие исходные объекты в порядке снимка.

    Вызывается check. Делегирует отбор collect_matching_evidence, а статус —
    determine_evidence_status. Пустой список правил даёт NO_MATCH.
    Пустые placements допустимы; они не означают отсутствие сетевых привязок.
    Места применения не создают копий правил. Входные и вложенные значения
    не изменяются. Общий verdict и синтетические правила не добавляются.
    """
    matching_rules = collect_matching_evidence(flow, snapshot['rules'])
    return {
        'device': snapshot['device'],
        'acl': snapshot['acl'],
        'placements': snapshot['placements'],
        'status': determine_evidence_status(matching_rules),
        'rules': matching_rules,
    }


def check(
    flow: Flow,
    relevance: RelevanceSource,
    snapshot: SnapshotSource,
) -> ReportGroups:
    """Исследовать сохранённые правила всех уникальных релевантных ACL.

    Args:
        flow: Проверенный конкретный IPv4-поток без допуска None-портов.
        relevance: Внедрённый callable(source: str, destination: str),
            возвращающий список проверенных DeviceAclPair для адресов flow.
        snapshot: Внедрённый callable(device: str, acl: str), возвращающий
            проверенный Snapshot запрошенной пары или поднимающий
            ExpectedApplicationFailure при отсутствии требуемого снимка.

    Returns:
        ReportGroups: Полный список групп в порядке первых появлений
            уникальных пар relevance. Пустая релевантность возвращает [].
            Для каждой пары включена группа, даже если совпадений нет.

    Raises:
        ExpectedApplicationFailure: Ожидаемый отказ любого источника,
            включая отсутствие необходимого снимка; отказ распространяется
            вызывающему коду без успешного частичного результата.

    Публичная точка входа для внешней CLI-композиции и интеграционных тестов.
    Вызывает relevance ровно один раз с двумя адресами flow; дедуплицирует
    пары по обоим полям с сохранением первого появления; вызывает snapshot
    ровно один раз для каждой уникальной пары и build_evidence_group для
    полученного снимка. Нерелевантные снимки не запрашивает.
    Источники предоставляются внешней композицией после проверки всего ввода.
    Функция не импортирует адаптеры, не валидирует JSON, не сериализует и
    не печатает результат. Нет retry, fallback, подавления ошибок
    программиста, общего verdict или мутаций переданных данных.
    """
    pairs = relevance(flow['source'], flow['destination'])
    seen: set[tuple[str, str]] = set()
    groups: ReportGroups = []
    for pair in pairs:
        key = (pair['device'], pair['acl'])
        if key in seen:
            continue
        seen.add(key)
        groups.append(build_evidence_group(flow, snapshot(*key)))
    return groups
