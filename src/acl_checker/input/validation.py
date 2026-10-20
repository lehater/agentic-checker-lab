from __future__ import annotations
from ipaddress import IPv4Address, IPv4Network

from typing import cast

from src.acl_checker.application.sources import (
    create_relevance_provider,
    create_snapshot_provider,
)
from src.acl_checker.application.types import DeviceAclPair, Snapshot
from src.acl_checker.domain.types import Flow
from src.acl_checker.input.types import ExpectedInputFailure, ValidatedInvocation


def validate_document(document: object) -> ValidatedInvocation:
    """Проверить весь документ v1 и подготовить источники одного запуска.

    Args:
        document: Недоверенное разобранное JSON-значение; object требует
            проверки типов до доступа к полям и не предполагает корректную схему.

    Returns:
        ValidatedInvocation: Проверенный Flow и узкие RelevanceSource,
            SnapshotSource для передачи в check(flow, relevance, snapshot).
            Источники замыкают локальные проверенные данные без глобального кеша.

    Raises:
        ExpectedInputFailure: Любое нарушение описанной ниже схемы.
            Проверяются все снимки, включая нерелевантные; частичного
            результата при ошибке нет. reason содержит понятную причину
            и место нарушения.

    Корневой объект содержит ровно version, flow, relevance, snapshots.
    version — int со значением 1, не bool. Все поля вложенных объектов
    обязательны; неизвестные поля отвергаются на каждом уровне.
    relevance_records и неподдержанные предикаты не допускаются.

    Flow содержит ровно source, destination, protocol, source_port,
    destination_port. Адреса — строки IPv4 без CIDR; protocol — tcp или udp.
    Оба порта обязательны: int в пределах 0..65535, исключая bool.

    relevance — список объектов ровно с device и acl, непустыми строками.
    Повторные пары допустимы; источник возвращает уникальные пары в порядке
    первого появления. Пустой список допустим. Его source и destination —
    IPv4-строки проверенного потока; предоставленная релевантность относится
    только к этому потоку и не является универсальным адресным индексом.

    snapshots — список объектов ровно с device, acl, placements, rules.
    Пары device/acl уникальны, обе строки непустые. placements — список
    объектов ровно {interface, direction}, где interface — непустая строка,
    direction — in или out, либо ровно {global: true}, где true — bool.
    Пустые placements и rules допустимы.

    Каждое правило содержит ровно id, source, destination, protocol,
    source_ports, destination_ports, action. id — непустая строка,
    уникальная внутри снимка. Адресные строки — IPv4 hosts либо canonical
    IPv4 CIDR с нулевыми host bits; значения не нормализуются.
    protocol — tcp, udp или any; action — permit или deny.
    Каждый портовый предикат — список ровно из двух int, не bool,
    с 0 <= lower <= upper <= 65535; обе границы включительны.
    Скалярные порты, None, IPv6 и неподдержанные формы отвергаются.

    Исходный документ не изменяется. Полные значения правил, placements
    и порядок правил сохраняются. SnapshotSource возвращает снимок по
    точной паре и поднимает ExpectedApplicationFailure при его отсутствии,
    никогда не возвращая None. Только запрошенные приложением релевантные
    снимки участвуют в отчёте. Источники не выполняют matching, файловый
    ввод-вывод или сетевые операции и не изменяют сохранённые значения.
    """
    root = _object(document, {'version', 'flow', 'relevance', 'snapshots'}, '$')
    if type(root['version']) is not int or root['version'] != 1:
        _fail('version', 'expected integer version 1')

    flow = _object(root['flow'], {
        'source', 'destination', 'protocol', 'source_port', 'destination_port'
    }, 'flow')
    for field in ('source', 'destination'):
        _address(flow[field], f'flow.{field}', allow_network=False)
    _choice(flow['protocol'], ('tcp', 'udp'), 'flow.protocol')
    for field in ('source_port', 'destination_port'):
        _port(flow[field], f'flow.{field}')

    pairs: list[DeviceAclPair] = []
    seen_pairs: set[tuple[str, str]] = set()
    for index, item in enumerate(_list(root['relevance'], 'relevance')):
        path = f'relevance[{index}]'
        pair = _object(item, {'device', 'acl'}, path)
        key = _pair(pair, path)
        if key not in seen_pairs:
            pairs.append(cast(DeviceAclPair, pair))
            seen_pairs.add(key)

    snapshots: list[Snapshot] = []
    snapshot_keys: set[tuple[str, str]] = set()
    for index, item in enumerate(_list(root['snapshots'], 'snapshots')):
        path = f'snapshots[{index}]'
        snapshot = _object(item, {'device', 'acl', 'placements', 'rules'}, path)
        key = _pair(snapshot, path)
        if key in snapshot_keys:
            _fail(path, f'duplicate snapshot pair {key!r}')
        snapshot_keys.add(key)
        for placement_index, placement in enumerate(
            _list(snapshot['placements'], f'{path}.placements')
        ):
            placement_path = f'{path}.placements[{placement_index}]'
            fields = {'global'} if isinstance(placement, dict) and 'global' in placement else {'interface', 'direction'}
            value = _object(placement, fields, placement_path)
            if fields == {'global'}:
                if value['global'] is not True:
                    _fail(f'{placement_path}.global', 'expected boolean true')
            else:
                _string(value['interface'], f'{placement_path}.interface')
                _choice(value['direction'], ('in', 'out'), f'{placement_path}.direction')
        ids: set[str] = set()
        for rule_index, rule in enumerate(_list(snapshot['rules'], f'{path}.rules')):
            rule_path = f'{path}.rules[{rule_index}]'
            value = _object(rule, {
                'id', 'source', 'destination', 'protocol',
                'source_ports', 'destination_ports', 'action'
            }, rule_path)
            identifier = _string(value['id'], f'{rule_path}.id')
            if identifier in ids:
                _fail(f'{rule_path}.id', f'duplicate rule id {identifier!r}')
            ids.add(identifier)
            for field in ('source', 'destination'):
                _address(value[field], f'{rule_path}.{field}', allow_network=True)
            _choice(value['protocol'], ('tcp', 'udp', 'any'), f'{rule_path}.protocol')
            _choice(value['action'], ('permit', 'deny'), f'{rule_path}.action')
            for field in ('source_ports', 'destination_ports'):
                bounds_path = f'{rule_path}.{field}'
                bounds = _list(value[field], bounds_path)
                if len(bounds) != 2:
                    _fail(bounds_path, 'expected inclusive two-bound range')
                for bound_index, bound in enumerate(bounds):
                    _port(bound, f'{bounds_path}[{bound_index}]')
                if bounds[0] > bounds[1]:
                    _fail(bounds_path, 'lower bound must not exceed upper bound')
        snapshots.append(cast(Snapshot, snapshot))

    for index, pair in enumerate(pairs):
        key = (pair['device'], pair['acl'])
        if key not in snapshot_keys:
            _fail(f'relevance[{index}]', f'missing snapshot for {key!r}')
    return ValidatedInvocation(
        flow=cast(Flow, flow),
        relevance=create_relevance_provider(pairs),
        snapshot=create_snapshot_provider(snapshots),
    )


def _fail(path: str, reason: str) -> None:
    raise ExpectedInputFailure(f'{path}: {reason}')


def _object(value: object, fields: set[str], path: str) -> dict:
    if not isinstance(value, dict):
        _fail(path, 'expected object')
    if set(value) != fields:
        missing = fields - set(value)
        extra = set(value) - fields
        _fail(path, f'missing fields {sorted(missing)!r}; unknown fields {sorted(map(str, extra))!r}')
    return value


def _list(value: object, path: str) -> list:
    if not isinstance(value, list):
        _fail(path, 'expected list')
    return value


def _string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(path, 'expected nonempty string')
    return value


def _pair(value: dict, path: str) -> tuple[str, str]:
    return (_string(value['device'], f'{path}.device'),
            _string(value['acl'], f'{path}.acl'))


def _choice(value: object, choices: tuple[str, ...], path: str) -> None:
    if not isinstance(value, str) or value not in choices:
        _fail(path, f'expected one of {choices!r}')


def _port(value: object, path: str) -> None:
    if type(value) is not int or not 0 <= value <= 65535:
        _fail(path, 'expected integer port 0..65535, excluding bool')


def _address(value: object, path: str, *, allow_network: bool) -> None:
    _string(value, path)
    try:
        if allow_network and '/' in value:
            parsed = IPv4Network(value, strict=True)
            if str(parsed) != value:
                _fail(path, 'expected canonical IPv4 CIDR')
        else:
            IPv4Address(value)
    except ValueError as error:
        raise ExpectedInputFailure(f'{path}: expected IPv4 host' +
                                   (' or canonical CIDR' if allow_network else '')) from error
