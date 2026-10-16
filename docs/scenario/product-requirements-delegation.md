# PDEC-CHECKER-003 — делегирование Product Requirements для `checker.requirements`

**Статус: OWNER-AUTHORIZED, SCOPED TO CHECKER REQUIREMENTS.** Дата: 2026-10-16.

## Основание

После принятия `checker.problem CURRENT` и [reconciliation](checker-scope-reconciliation.yaml) (PR #16), владелец подтвердил прямой запрос:

> Делегировать агенту Authority `PRODUCT-REQUIREMENTS` для `checker.requirements`, с непосредственной зависимостью от `checker.problem`. Агент вправе самостоятельно формировать требования, проводить Semantic Review, строгую приёмку и атомарную публикацию только тех требований, которые подтверждены источниками и действующими решениями. Неопределённые продуктовые вопросы возвращать на согласование, не превращать в придуманные требования.

Ответ владельца: **«Да, подтверждаю»**. Этим решён **Q-REC-001** — вопрос полномочий. Это **не** подтверждение какой-либо конкретной спецификации требований.

## Утверждённый производственный контракт и полномочия

- **Authority:** `PRODUCT-REQUIREMENTS`.
- **Capability:** `checker.requirements`, knowledge kind `product-requirements`.
- **Непосредственный prerequisite:** только `checker.problem` (уже CURRENT); не выдумывать промежуточные user-needs или зависимости от непроверенных источников.
- **Graph:** разрешено внести ровно это производство и его непосредственную зависимость в project-owned Engineering Graph, с корректным разрешением потребителя для новой Capability, не выдавая новый технический Consumer за полный implementation/product scope.
- **Production:** инженерный агент может запускать штатный routed `product-requirements` skill, формировать атомарные `REQ-*` с `source_refs`, вести source-by-source disposition, определять наблюдаемое поведение, подтверждённые ограничения и проверяемые критерии приёмки.
- **Review/admission:** агенту делегирован содержательный semantic review по применимому pinned contract, вызов настоящего strict Semantic Admission, сохранение lifecycle/Question/failure state и допустимая атомарная CAS Project Publication.
- **Validation:** предыдущий `checker.problem` должен остаться CURRENT по актуальным policy fingerprints; после результата пересчитать Roadmap, Semantic Closure, Engineering Coverage и Frontier. Все изменения через отдельную ветку, evidence, PR и CI; без самостоятельного merge.

## Содержательные границы

- Источники: accepted `checker.problem` и [PDEC-CHECKER-001](problem-framing-decision.md), плюс исторические SSSR/Product исключительно как **source evidence**, не как автоматически принятые target requirements. Не приписывать старым документам статус product owner decision.
- Допустима приёмка **только** тех требований, которые логически следуют из принятой проблемной постановки или отдельных явных продуктовых решений. Обязательно сохранять отрицательные и NOT_REQUIRED ограничения (например, отсутствие обязанности вычислять единый универсальный Permit/Deny), не подменяя их запретом любой специфичной диагностической интерпретации.
- Незакрытый **Q-REC-002** (bounded product scope, subject inventory и продуктовые атомы) разрешается исследовать в этом Product Requirements цикле. Существенные неизвестные product choices — отдельные адресные Questions владельцу; их нельзя угадывать, скрывать или заявлять полную product completeness.
- Не утверждены offline/fixture-only, полный входной tuple, IP/protocol semantics, matching, freshness/completeness thresholds, live device access, UI/API, архитектура, дизайн, oracle, сроки, AI/runtime, regulatory/privacy/safety dispositions.
- Делегирование `PRODUCT-REQUIREMENTS` **не** назначает Domain/Architecture/Implementation/Verification Authorities и не меняет существующие 22 `UNASSESSED` только на основании этого решения. Допустимо применимо оценить Product Authority в собственном scope без маскировки остальных пробелов.
- Если допустимый нормативный набор не удовлетворяет строгим требованиям `product-requirements/v1` и нет разрешённых решений для завершения, сохранить честное `BLOCKED` с минимальными предметными Questions. Нельзя фабриковать источник, статус `ACCEPTED` или publication revision.
- Не изменять `lehater/harness`; не запускать CoderMind, кодогенерацию, работу с устройствами или секретами.

## Критерий исполнения

Либо подлинная строгая приёмка и согласованная публикация `checker.requirements CURRENT` в принятом ограниченном scope с доказанной трассировкой к `checker.problem` и конкретными `REQ-*`, либо узкие адресные Product Questions, препятствующие честной приёмке. Это решение устанавливает полномочия, но **не создаёт** requirements artifacts или Lifecycle CURRENT само по себе.
