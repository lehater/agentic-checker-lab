from __future__ import annotations
from src.acl_checker.application.types import (
    DeviceAclPair,
    RelevanceSource,
    Snapshot,
    SnapshotSource,
)
from src.acl_checker.domain.types import Flow


def retrieve_relevant_pairs(
    flow: Flow,
    relevance: RelevanceSource,
) -> list[DeviceAclPair]:
    """Получить уникальные релевантные пары для проверенного потока.

    Args:
        flow: Flow с проверенными IPv4-строками source и destination.
            Протокол и оба обязательных порта не участвуют в релевантности.
        relevance: RelevanceSource, принимающий две IPv4-строки и
            возвращающий проверенный список DeviceAclPair данного запроса.

    Returns:
        list[DeviceAclPair]: Новый список пар без повторов по совокупности
            device и acl, в порядке первого появления. Пустой ответ даёт [].

    Raises:
        ExpectedApplicationFailure: Ожидаемый отказ внедрённого источника;
            распространяется без fallback и частичного результата.

    Вызывается check ровно один раз на запрос. Вызывает relevance ровно
    один раз с flow['source'], flow['destination']. Не читает снимки,
    не выводит сетевой путь и не изменяет flow, список источника или пары.
    """
    pairs = relevance(flow['source'], flow['destination'])
    seen: set[tuple[str, str]] = set()
    unique_pairs: list[DeviceAclPair] = []
    for pair in pairs:
        key = (pair['device'], pair['acl'])
        if key not in seen:
            seen.add(key)
            unique_pairs.append(pair)
    return unique_pairs


def retrieve_required_snapshot(
    pair: DeviceAclPair,
    snapshot: SnapshotSource,
) -> Snapshot:
    """Получить обязательный снимок одной уникальной релевантной пары.

    Args:
        pair: Проверенная DeviceAclPair, выбранная retrieve_relevant_pairs.
        snapshot: SnapshotSource с контрактом возврата проверенного Snapshot
            для device/acl либо ExpectedApplicationFailure при отсутствии.

    Returns:
        Snapshot: Полный предоставленный снимок именно запрошенной пары,
            сохраняющий placements, порядок правил и все исходные значения.

    Raises:
        ExpectedApplicationFailure: Источник не располагает требуемым
            снимком или сообщает другой ожидаемый отказ получения.
            Ошибка распространяется до check и внешней границы CLI.

    Вызывается check один раз на каждую уникальную пару в порядке выбора.
    Вызывает snapshot(pair['device'], pair['acl']) ровно один раз.
    None не предусмотрен контрактом источника. Отсутствие снимка нельзя
    заменить пустым снимком или NO_MATCH. Retry, fallback, мутации и
    подавление ошибок программиста исключены. check публикует результат
    только после успешного завершения всего запроса.
    """
    return snapshot(pair['device'], pair['acl'])
