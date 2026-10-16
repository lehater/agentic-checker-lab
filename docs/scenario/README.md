# Checker — границы первой предметной задачи

Статус: **потребность верхнего уровня подтверждена владельцем** ([PDEC-CHECKER-001](problem-framing-decision.md)); полномочия DISCOVERY и PRODUCT-REQUIREMENTS заданы [PDEC-CHECKER-002](discovery-authority-delegation.md) и [PDEC-CHECKER-003](product-requirements-delegation.md). Предлагаемый вертикальный срез и target requirements — **CANDIDATE / NOT ACCEPTED**.

## Пользовательская проблема

Нормативная подтверждённая формулировка: [PDEC-CHECKER-001](problem-framing-decision.md). Исторические уточнения ниже остаются исходными свидетельствами; они не расширяют автоматически принятое решение.


Оператору требуется объяснимое свидетельство по конкретному сетевому потоку: источник, назначение, протокол, порты → релевантные места применения сетевой политики, сохранённые подходящие ACL правила, порядок, происхождение и свежесть данных. Историческая реализация в Product использует Django, SQL и возможную живую диагностику устройства; не копировать её техническую архитектуру.

## Предполагаемый минимальный вертикальный срез

- Input: source/destination IPv4, IP protocol, source/destination ports когда имеют смысл.
- Подготовленные fixture providers: известные enforcement attachments и нормализованные ACL snapshot rules. **На первой итерации не вычислять реальную топологию и не читать устройства.**
- Output: все covering ACL в policy order, permit/deny как сведения конкретных правил, source ID, timestamp/freshness/completeness, explicit no-match/unknown.
- Независимая проверка, защищающая от универсального allow/deny: отсутствие matching rule никогда само по себе не значит DENIED.
- Небольшой самостоятельный CLI или API; UI, БД и конкретный runtime stack выбираются позднее при достаточном основании.

Это **исследовательское сужение**, а не утверждение, что legacy-checker обладал только такой функциональностью.

## Вне первой задачи

Автоматический route discovery/NAT, опрос реальных МСЭ, vendor packet-tracer, создание ACL/config, изменение сетевых устройств, полный lifecycle NAPMS и весь набор его Bounded Contexts. Возможности разнородного импорта и business-need/provenance могут стать **следующими change requests**, а не обязательной частью первой версии.

## Критические семантические границы

RELEVANT FIREWALL ≠ MATCHING RULE ≠ PERMIT. Stored snapshot ≠ live operational truth. NO_MATCH ≠ DENY. UNKNOWN ≠ EMPTY POLICY. All matching permit/deny ACL rules retain their order.

Исторические evidence: [SCN-006 extraction](../research/legacy-checker.md). Принятые target requirement IDs, ownership, actor, contracts и oracle **пока не определены**; подготовить в P2 до codegen.
