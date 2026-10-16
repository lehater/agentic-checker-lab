# TASK-004: исходные свидетельства для Harness Discovery

Статус: **SOURCE INTAKE, NOT ACCEPTED PRODUCT REQUIREMENTS**. Это набор исходных свидетельств для агентного `problem-evidence` skill, а не вручную принятая спецификация Checker или результат работы Harness.

## Якорные версии первичных документов

- [SSSR SCN-006](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/docs/legacy/requirements/SCN-006-traffic-check.md): реконструкция исторического сценария; автором подтверждённые моменты имеют отдельный статус. Не тождественно требованиям нового продукта.
- [Product Access Assessment As-Is](https://github.com/lehater/product/blob/759fcd7b773b12144a14f4a990cfba11bddc3527/docs/discovery/access-assessment-as-is.md): наблюдённые Python/SQL/UI интеграционные шаги, ограниченная уверенность о развёрнутых SQL/данных, не To-Be решение.
- [Кандидатный scope лаборатории](../scenario/README.md): новая гипотеза о fixture-based offline Checker, ещё не принятая продуктовая семантика.
- [План oracle](../evaluation/oracle-plan.md): предложенные негативные/положительные случаи, **не** принятые тестовые результаты.

Ни один пункт ниже не должен получить статус `ACCEPTED` только потому, что содержится в этом обзоре. Harness agent должен использовать только допустимые source_refs, сформировать Problem Evidence и передать unresolved choices в их Authority.

## Реестр смысловых источников (кандидатный, не requirement registry)

| ID источника | Документ / якорь | Что действительно поддерживается источником | Что **не** следует из него автоматически |
| --- | --- | --- | --- |
| SRC-01 | SSSR / REQ-034 | Исторический операторский host-to-host tuple с IP/protocol и портами where applicable | Формат нового API, IPv6 и default source port |
| SRC-02 | SSSR / REQ-035, SCN-002 | Релевантные firewall placements вычислялись из общего routing/correction контекста | Что новый fixture-based движок уже умеет вычислять реальную топологию |
| SRC-03 | SSSR / REQ-036, RULE-019 | Исторически показывались **все** covering stored ACL rules, в policy order, обе action категории | Единственный общий эффективный allow/deny verdict |
| SRC-04 | SSSR / REQ-037, RULE-018/020 | Relevant firewall ≠ matching rule ≠ permit; no-match остаётся свидетельством | Implicit deny, автоматически выбранный block point |
| SRC-05 | SSSR / REQ-038 | Дополнительные UI сведения могут помогать объяснению | Что это обязательный core acceptance scope |
| SRC-06 | SSSR / REQ-039, RULE-022 | Live vendor diagnostic — отдельно от stored snapshot, где поддерживается | Право выполнять packet-tracer или подключаться к реальному устройству |
| SRC-07 | SSSR / REQ-040, RULE-022 | Важны источник и свежесть routing/policy/live evidence | Нормативная новейшая бизнес-политика TTL/блокирования устаревшего снимка |
| SRC-08 | Product / request/form and SQL flow | Auth/UI, возможный live-check, внутренние SQL FindFirewallMain/FindACLMatch, максимум 10 устройств для одного live пути — **As-Is** | Требуемый Django/SQL дизайн нового продукта или universal device limit |
| SRC-09 | Product / observed UI | Отдельные таблицы firewall/policy/context/live; результат может требовать интерпретации оператором | Единый бинарный вердикт |
| SRC-10 | Lab / candidate scope | Offline normalized fixture providers, no device interactions, небольшое CLI/API — **проектная гипотеза** | Принятая граница или уже определённый контракт ввода |

## Открытые вопросы для владельцев знаний

- Какая **продуктовая проблема** и успешный пользовательский исход определяют минимальный исследовательский Checker?
- Принимается ли `fixture-based/offline` ограничение для первого сценария, несмотря на историческую связь с SCN-002 и SCN-004? Как обрабатывается неизвестный/неполный набор релевантных placements?
- Где применимы source port, ICMP и другие протоколы? Какая поддерживаемая семантика match/no-match/range для первой версии?
- Как определяются `unknown`, полнота, stale и provenance без создания новой «permission» логики?
- Какие спорные product/domain решения вправе принять агент по делегированным правилам, а что нужно эскалировать человеку?
- Какие test obligations должны использовать независимый oracle, а какие достаточны для INSPECTION/ANALYSIS?

Для каждой неопределённости Harness должен либо получить подтверждение из авторитетных источников, либо создать Question с owning Authority и оставить downstream работу блокированной. Нельзя заполнять ответы догадками по существующему коду.

## Первая операция Harness (оператор/агент)

1. Прочитать [корневой AGENTS](../../AGENTS.md), текущий [state](../project/current-state.yaml), scope и настоящий источник SCN-006, не объявляя этот ledger каноническим Requirements.
2. Из закреплённого Harness consumer route вызвать `project-bootstrap-reconcile`; не вызывать внутренний `bootstrap-existing-project` как публичную операцию.
3. Выбрать implementation Consumer и минимальный scope; проверить существование допустимой проектной реализации графа и applicable Engineering Coverage. Отсутствие — `UNASSESSED`, не `NOT_APPLICABLE`.
4. Выполнять `READY` действия `Project Frontier` через соответствующие routed skills; первый содержательный продукт ожидается `Problem Evidence`, если frontier его действительно требует.
5. Принятые решения фиксировать в target canonical artifacts/Core с validator+semantic admission. Человек подтверждает действительно неразрешённую существенную семантику. Не начинать CoderMind codegen и не считать `TargetState.COMPLETE` единственной готовностью.

Этот документ — **исходные данные для Harness**, не его результат и не отдельный «ручной P2». Результат настоящего цикла пока `NOT_RUN`.
