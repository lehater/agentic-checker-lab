from __future__ import annotations
from collections.abc import Sequence

from src.acl_checker.application.types import (
    DeviceAclPair,
    ExpectedApplicationFailure,
    RelevanceSource,
    Snapshot,
    SnapshotSource,
)


def create_relevance_provider(
    pairs: Sequence[DeviceAclPair],
) -> RelevanceSource:
    """Создать синтетический источник релевантности одного запроса.

    Args:
        pairs: Полностью проверенная последовательность DeviceAclPair
            из relevance документа v1 для flow текущего запроса.
            Порядок и повторения являются частью предоставленных данных.

    Returns:
        RelevanceSource: Callable(source: str, destination: str)
            -> list[DeviceAclPair]. Принимает проверенные IPv4-адреса
            текущего flow и возвращает новый список предоставленных пар
            в исходном порядке, включая повторы. Пустой вход даёт [].

    Вызывается validate_document после проверки всего документа.
    Возвращённый callable вызывается retrieve_relevant_pairs, который
    выполняет дедупликацию. Список относится только к текущему flow:
    фабрика не строит адресный индекс и не вычисляет сетевую релевантность.
    Дополнительный relevance_records не поддерживается. Фабрика и callable
    не изменяют аргументы; потребители не изменяют вложенные значения.
    Захваченное состояние локально для запуска, без глобального кеша,
    файлового ввода, сети или зависимости от внешнего валидатора.
    """
    saved_pairs = tuple(pairs)

    def relevance(source: str, destination: str) -> list[DeviceAclPair]:
        return list(saved_pairs)

    return relevance

def create_snapshot_provider(
    snapshots: Sequence[Snapshot],
) -> SnapshotSource:
    """Создать локальный источник проверенных снимков одного запроса.

    Args:
        snapshots: Полностью проверенная последовательность Snapshot.
            Уникальность пар device/acl и корректность всех снимков,
            включая нерелевантные, обеспечены внешним валидатором.

    Returns:
        SnapshotSource: Callable(device: str, acl: str) -> Snapshot,
            возвращающий полный снимок точной пары без изменения placements,
            порядка правил, их полей или исходных сериализованных значений.

    Raises:
        ExpectedApplicationFailure: Возвращённый callable поднимает этот
            отказ при отсутствии запрошенной пары. reason явно указывает
            отсутствующие device и acl. Сама фабрика не требует наличия
            снимков для ещё не запрошенных релевантных пар.

    Вызывается validate_document после проверки всего документа.
    Возвращённый callable вызывается retrieve_required_snapshot.
    Пустая последовательность допустима; любой запрос к ней завершается
    ожидаемым отказом. Отсутствие не представляется None, пустым снимком
    или NO_MATCH. Данные не изменяются и не дополняются. Захваченные
    значения принадлежат одному запуску; глобальные кеши, ввод-вывод,
    retry, fallback и blanket except Exception исключены.
    """
    by_pair = {(item['device'], item['acl']): item for item in snapshots}

    def snapshot(device: str, acl: str) -> Snapshot:
        try:
            return by_pair[device, acl]
        except KeyError as error:
            raise ExpectedApplicationFailure(
                f'Missing snapshot for device {device!r}, acl {acl!r}'
            ) from error

    return snapshot
