from __future__ import annotations
from copy import deepcopy

from src.acl_checker.domain.matching import matches
from src.acl_checker.domain.types import Flow, OriginalRule


def test_predicate_boundaries() -> None:
    """Проверить matches по независимой фиксированной таблице Flow/OriginalRule.

    Параметры отсутствуют; pytest вызывает тест, результат None.
    Для каждого проверенного входа сравнивает bool с заранее заданным
    ожиданием и аргументы с deepcopy. Покрывает оба адреса, host и /32,
    /0, крайние адреса CIDR, tcp/udp/any, конъюнкцию всех пяти условий,
    обе включительные границы каждого диапазона, соседние значения,
    равные границы и порты 0/65535. Проверяет независимость от id/action.
    Невалидные значения проверяются отдельно внешним валидатором;
    expected не вычисляется через matches или production helpers.
    Несовпадение либо мутация вызывает AssertionError.
    """
    cases: list[tuple[str, Flow, OriginalRule, bool]] = []
    flow, rule = matching_values()
    cases.append(('all-five-predicates', flow, rule, True))

    # Только проверенные значения; oracle задан вручную по контракту.
    address_cases = [
        ('10.0.0.0/24', '10.0.0.0', True),
        ('10.0.0.0/24', '10.0.0.255', True),
        ('10.0.0.0/24', '9.255.255.255', False),
        ('10.0.0.0/24', '10.0.1.0', False),
        ('10.0.0.1', '10.0.0.1', True),
        ('10.0.0.1', '10.0.0.0', False),
        ('10.0.0.1', '10.0.0.2', False),
        ('10.0.0.1/32', '10.0.0.1', True),
        ('10.0.0.1/32', '10.0.0.0', False),
        ('10.0.0.1/32', '10.0.0.2', False),
        ('0.0.0.0/0', '0.0.0.0', True),
        ('0.0.0.0/0', '255.255.255.255', True),
    ]
    port_cases = [
        ([100, 200], 99, False),
        ([100, 200], 100, True),
        ([100, 200], 150, True),
        ([100, 200], 200, True),
        ([100, 200], 201, False),
        ([443, 443], 442, False),
        ([443, 443], 443, True),
        ([443, 443], 444, False),
        ([0, 65535], 0, True),
        ([0, 65535], 65535, True),
        ([0, 0], 0, True),
        ([0, 0], 1, False),
        ([65535, 65535], 65535, True),
        ([65535, 65535], 65534, False),
    ]
    for field in ('source', 'destination'):
        for predicate, address, expected in address_cases:
            flow, rule = matching_values()
            flow[field] = address
            rule[field] = predicate
            cases.append((f'{field}: {predicate}, {address}', flow, rule, expected))
        for bounds, port, expected in port_cases:
            flow, rule = matching_values()
            flow[f'{field}_port'] = port
            rule[f'{field}_ports'] = bounds
            cases.append((f'{field} port: {bounds}, {port}', flow, rule, expected))

    for protocol, predicate, expected in [
        ('tcp', 'tcp', True), ('tcp', 'udp', False), ('tcp', 'any', True),
        ('udp', 'tcp', False), ('udp', 'udp', True), ('udp', 'any', True),
    ]:
        flow, rule = matching_values()
        flow['protocol'] = protocol
        rule['protocol'] = predicate
        cases.append((f'protocol: {protocol}, {predicate}', flow, rule, expected))

    for label, flow, original_rule, expected in cases:
        # Меняем id и action независимо, для совпадений и несовпадений.
        for identifier in ('z-deny', 'a-permit'):
            for action in ('permit', 'deny'):
                rule = deepcopy(original_rule)
                rule.update(id=identifier, action=action)
                before = deepcopy((flow, rule))
                context = (label, identifier, action)
                assert matches(flow, rule) is expected, context
                assert (flow, rule) == before, context


def matching_values() -> tuple[Flow, OriginalRule]:
    return (
        {'source': '10.0.0.1', 'destination': '192.0.2.10',
         'protocol': 'tcp', 'source_port': 50000, 'destination_port': 443},
        {'id': 'z-deny', 'source': '10.0.0.0/24',
         'destination': '192.0.2.0/24', 'protocol': 'tcp',
         'source_ports': [49000, 51000], 'destination_ports': [440, 450],
         'action': 'deny'},
    )


def test_each_predicate_is_required() -> None:
    for field, value in [
        ('source', '10.0.1.1'), ('destination', '198.51.100.10'),
        ('protocol', 'udp'), ('source_port', 48999),
        ('source_port', 51001), ('destination_port', 439),
        ('destination_port', 451),
    ]:
        flow, rule = matching_values()
        flow[field] = value
        before = deepcopy((flow, rule))
        assert matches(flow, rule) is False, (field, value)
        assert (flow, rule) == before


def test_address_hosts_and_network_boundaries() -> None:
    cases = [
        ('10.0.0.0/24', '10.0.0.0', True),
        ('10.0.0.0/24', '10.0.0.255', True),
        ('10.0.0.0/24', '9.255.255.255', False),
        ('10.0.0.0/24', '10.0.1.0', False),
        ('10.0.0.1', '10.0.0.1', True),
        ('10.0.0.1', '10.0.0.2', False),
        ('10.0.0.1/32', '10.0.0.1', True),
        ('10.0.0.1/32', '10.0.0.0', False),
        ('0.0.0.0/0', '0.0.0.0', True),
        ('0.0.0.0/0', '255.255.255.255', True),
    ]
    for field in ('source', 'destination'):
        for predicate, address, expected in cases:
            flow, rule = matching_values()
            flow[field] = address
            rule[field] = predicate
            assert matches(flow, rule) is expected, (field, predicate, address)


def test_inclusive_port_ranges() -> None:
    cases = [
        ([100, 200], 99, False), ([100, 200], 100, True),
        ([100, 200], 150, True), ([100, 200], 200, True),
        ([100, 200], 201, False), ([443, 443], 443, True),
        ([443, 443], 442, False), ([443, 443], 444, False),
        ([0, 65535], 0, True), ([0, 65535], 65535, True),
        ([0, 0], 0, True), ([65535, 65535], 65535, True),
    ]
    for field in ('source', 'destination'):
        for bounds, port, expected in cases:
            flow, rule = matching_values()
            flow[f'{field}_port'] = port
            rule[f'{field}_ports'] = bounds
            assert matches(flow, rule) is expected, (field, bounds, port)


def test_protocol_and_rule_metadata() -> None:
    for protocol in ('tcp', 'udp'):
        for rule_protocol in ('tcp', 'udp', 'any'):
            for identifier, action in [('z-deny', 'deny'), ('a-permit', 'permit')]:
                flow, rule = matching_values()
                flow['protocol'] = protocol
                rule.update(id=identifier, action=action, protocol=rule_protocol)
                before = deepcopy((flow, rule))
                expected = rule_protocol == 'any' or rule_protocol == protocol
                assert matches(flow, rule) is expected
                assert (flow, rule) == before
