from __future__ import annotations
from ipaddress import IPv4Address, IPv4Network

from src.acl_checker.domain.types import Flow, OriginalRule


def matches(flow: Flow, rule: OriginalRule) -> bool:
    """Проверить совпадение проверенного потока с сохранённым правилом.

    Args:
        flow: Flow с IPv4-адресами, протоколом tcp/udp и двумя обязательными
            целыми портами 0..65535, исключая bool.
        rule: OriginalRule с IPv4 hosts или canonical CIDR, протоколом
            tcp/udp/any и двумя включительными диапазонами портов.
            Каждый диапазон содержит ровно две упорядоченные границы.

    Returns:
        bool: Конъюнкция принадлежности обоих адресов предикатам правила,
            совпадения протокола либо any и принадлежности обоих портов
            соответствующим включительным диапазонам.

    IPv4 host трактуется как /32; крайние адреса сети включены.
    Action и id не влияют на результат. Внешний адаптер предварительно
    проверяет схему и значения: неподдержанные предикаты не означают False.
    Функция чистая, не изменяет аргументы и не обращается к источникам.
    Вызывается collect_matching_evidence для каждого правила снимка.
    """
    return (
        IPv4Address(flow['source']) in IPv4Network(rule['source'])
        and IPv4Address(flow['destination']) in IPv4Network(rule['destination'])
        and rule['protocol'] in ('any', flow['protocol'])
        and rule['source_ports'][0] <= flow['source_port'] <= rule['source_ports'][1]
        and rule['destination_ports'][0]
        <= flow['destination_port']
        <= rule['destination_ports'][1]
    )
