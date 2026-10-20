# Дорожная карта и тактика исполнения

Статус: **ACCEPTED**. Фактическая стадия: [current-state.yaml](current-state.yaml). План не является утверждением, что этапы выполнены.

| Фаза | Задачи | Результат | Exit / Gate |
| --- | --- | --- | --- |
| **P0 — Foundation** | Репозиторий, стратегия, AGENTS map, правила PR, документационные проверки, пины источников | Коммит с канонической навигацией и CI | Make check, реальный GitHub CI; branch protection настроен владельцем |
| **P1 — Toolchain spike** | Чистая Ubuntu, Harness, CoderMind, проверенный coding-agent CLI, экспорт RPG и версионирование | Smoke logs + решение по интеграции | Graph/CLI доступны, версии фиксированы; либо честный BLOCKED |
| **P2 — Scenario acceptance** | Один Checker job, пользователи, граница, semantics, negative cases, независимые tests | Утверждённая целевая спецификация Checker | Нет незадекларированной доменной неопределённости, важной для реализации |
| **P3 — Harness engineering closure** | Engineering Graph, требуемые решения и capability deps, вопросы, архитектурные варианты/контракты | Проверенный Harness consumer, tech constraints, test design | Target closure PASS с осмысленной независимой проверкой |
| **P4 — RPG + generation** | Contract bridge, To-Be RPG, интерфейсы/код, сценарий запуска, снимок графа | Самостоятельный Checker + link manifest | Критические независимые oracle cases PASS; архитектурные границы выдержаны |
| **P5 — Change impact** | Повторный смысловой запрос: новый источник свидетельств или stale evidence | Before/after: Harness/RPG/code/tests | Изменения объяснимы, нет скрытого semantic drift |
| **P6 — Controlled comparison** | Один и тот же сценарий для A агент, B Harness, C RPG, D оба | Полные прогоны, метрики, затратность | Сравнимые условия и прозрачные исключения |
| **P7 — Conclusion** | Trade-off, применимость, второй сценарий для переноса | Отчёт GO/CONDITIONAL/NO-GO + шаблон повторения | Вывод основан на evidence, не на впечатлениях |

## Текущая граница завершения

Checker v1 имеет работающий synthetic CLI, проверенный bridge/RPG/source и COMPLETE
Harness readiness; см. [прогон](../../experiments/runs/checker-v1/README.md).
Интеграция финального PR остаётся отдельным Git gate. Следующая содержательная
задача — TASK-007/P5: заранее определить новое требование и oracle, затем провести
управляемое изменение. P6/P7 и сравнительные выводы не выполнены. Прежние TASK-004
и TASK-005 реализованы в одном связанном engineering run; старые начальные номера
не являются текущими блокерами.

## Управление задачами

- Одна независимая инженерная задача = одна короткоживущая branch = один PR = один squash commit в main.
- Ветки: research/, design/, tooling/, feat/, fix/, eval/.
- Каждая задача связана с RQ-*, K-*, собственным TASK-* и проверкой результата.
- Несколько PR могут завершать одну фазу; фазы не заменяют реальные зависимости знания.
- При новом знании обновляются только канонические владельцы и затронутые downstream артефакты.
- Не запускать долгий аудит legacy без доказательства, что неопределённость блокирует выбранный сценарий.
- Решения о требованиях и критериях оценки принимаются **до** кодогенерации/тестового прогона, а не ретроспективно.

## Конкретный начальный backlog

- **TASK-001 (P0):** закончить структуру, проверить документы и GitHub CI, включить защиту main; затем закрыть P0 в current-state.
- **TASK-002 (P1):** чистый Ubuntu Harness checkout к pin, minimal Engineering Graph consumer, validate/evaluate/doctor.
- **TASK-003 (P1):** установленный CoderMind к pin; cmind check; определить поддерживаемый agent CLI и layout RPG snapshots.
- **TASK-004 (P2):** SCN-006 → независимая target specification + принятие спорных ограничений + oracle до генерации.
- **TASK-005 (P3):** Harness graph и минимальное domain/architecture/test design по принятым Checker требованиям.
- **TASK-006 (P4):** bridge Harness → To-Be RPG; сгенерировать и независимо проверить первую реализацию.
- **TASK-007 (P5):** регрессионный change experiment с изменением требований.
- **TASK-008 (P6):** выполнить контролируемое сравнение режимов A/B/C/D.
- **TASK-009 (P7):** оформить итоги и replication design.

Не считать DONE задачи, пока evidence не зафиксировано и проверки не запускались.
