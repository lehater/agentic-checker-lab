# Harness ↔ RPG: экспериментальный контракт

Статус: **HYPOTHESIS**, не реализован. P1 проверил initial RPG (31 узел, 18 feature leaves, 0 явных dependency edges); полный CoderMind planning/codegen и Harness→RPG handoff не проверены. См. [аудит](../research/methodology-integration-audit-2026-10.md).

## Разделение истины

| Контур | Владеет | Не вправе |
| --- | --- | --- |
| Project canonical artifacts | Принятая проблема, требования, инварианты, архитектура, Test Design и ограничения реализации | Механически повторять legacy файлы, считать derivations новой истиной |
| Harness + агент и skills | Получение/принятие Problem Evidence/Requirements/Design/Test knowledge, Authority/Capabilities/Questions, completeness, provenance и human documentation | Принимать произвольные факты из кода за авторитетные, считать структурное COMPLETE достаточным для codegen |
| RPG/CoderMind | Производные feature specification/decomposition, компоненты, file/data flow/interfaces, codegen и graph-aware edits | Переопределять принятый проектный смысл; считать output graph доказательством полноты |
| Приложение | Исполняемый результат Checker | Служить первичной истиной о продукте |
| Independent oracle | Проверка принятых требований | Принимать только агентные тесты к его собственному коду |

Движение в штатном направлении: accepted engineering knowledge → constrained To-Be RPG → implementation. Обратная связь — diagnostics/Question/review request; **не** автоматическое изменение предметной истины из кода.

## Кандидат bridge manifest

Пример смыслового (не совместимого пока с CLI) контракта:

    input_revision: <git-sha>
    harness_consumer: CHECKER-IMPLEMENTATION
    harness_evaluation: COMPLETE
    requirement_refs: [REQ-CHECK-...]
    accepted_decision_refs: [docs/...]
    output_revision: <git-sha>
    rpg_snapshot: experiments/runs/<id>/rpg.json
    traceability:
      requirement: REQ-CHECK-...
      capability: engineering.checker....
      rpg_nodes: [...]
      code_locations: [...]
      oracle_cases: [...]

Это **не спецификация формата Microsoft**, названия и протокол подлежат проверке. Связь многие-ко-многим; не требуется один узел RPG на requirement/BC/file.

## Контрактные инварианты

1. Доступен только accepted knowledge; блокирующий Question останавливает зависимое кодирование.
2. RPG может предложить другую организацию модулей, но не менять предметный результат.
3. Каждый критический requirement имеет проверяемую link-chain до independent oracle.
4. Неуспешный or incomplete graph snapshot не маскируется как готовность.
5. Изменение требований пересчитывает affected engineering nodes и affected RPG/code; различия требуют анализа.
6. Графы и код принадлежат фиксированным Git ревизиям; перенос между чатами восстанавливает состояние из репозитория.
7. Ни RPG, ни Harness не требуются runtime для готового Checker.

## Приёмка интеграции

До перевода HYPOTHESIS в ACCEPTED нужны: положительный сквозной run, негативный случай с запрещённым semantic override, повторимое восстановление и change-impact с независимыми oracle cases. Отдельный отказ CoderMind/agent CLI требует BLOCKED, а не подмены доказательства mock output.

## Исправленная граница интеграции

**Единый источник принятых обязательств:** проектные канонические артефакты. Не смешивать `Harness Core` (структурная модель), действия инженерного агента по artifact skills и semantic acceptance. Project Frontier/coverage определяют допустимый объём работы; CoderMind получает версионированную, неизменяемую на время прогона проекцию применимых принятых знаний.

CoderMind `feature_spec` сам генерирует требования/декомпозицию: результат сначала **предложение**, которое сверяется с canonical accepted requirements/constraints/implementation freedoms. Принять новый смысл вправе только проектный Authority через Harness, не CoderMind. Источники и негативные ограничения не должны теряться. Подробный [план пилота](handoff-pilot.md).

При codegen не использовать lab Git repo непосредственно: upstream `code_gen`/RPG edit имеют собственные branch/commit/merge workflows. Запускать в изолированном disposable repo, сканировать diff, переносить результат только через PR/squash. Включить негативные тесты unauthorized write, stale source, missing requirement и архитектурного конфликта.

Сквозная link projection и RPG snapshots **не становятся вторым canonical truth**. Исследовать минимальную модель идентификаторов и ссылок по фактическому CoderMind output, без изобретения универсальной DSL.
