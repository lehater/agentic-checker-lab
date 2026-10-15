# Harness ↔ RPG: экспериментальный контракт

Статус: **HYPOTHESIS**, не реализован. Уточняется после P1 CoderMind inspection.

## Разделение истины

| Контур | Владеет | Не вправе |
| --- | --- | --- |
| Принятые docs | Проблема, требования, инварианты, архитектурные ограничения, test intent | Механически повторять legacy файлы |
| Harness | Authority, Capabilities, Questions, зависимость/полнота инженерных знаний | Присваивать знания о предметной области из чужих исходников |
| RPG/CoderMind | Функциональная структура, компоненты, файлы, interfaces, задачи codegen | Переопределять требования или гарантировать оптимальность дизайна |
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
