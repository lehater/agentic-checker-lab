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

## First-slice Domain / Verification после PDEC-CHECKER-005

Оба направления доведены до обоснованного BLOCKED: [run и evidence](../../experiments/runs/harness-domain-verification-v1/README.md).
Сначала владелец проекта обеспечивает accepted Strategic Domain ownership
(Q-DV-001), затем DOMAIN-USE-CASE-DESIGN принимает минимальный matching contract
с независимыми match/non-match labels (Q-DV-002). После этого завершаются
Verification Strategy, admission и acceptance scenarios. Восемь metadata/empty-set
scenario drafts и dispositions всех 28 требований уже подготовлены.

Новый scoped Decision Roadmap и Semantic Closure — BLOCKED; Coverage неполон.
Project Frontier READY означает наличие дальнейших coverage reconciliation actions,
а не готовность Checker к реализации. Общая инвентаризация не выполнялась.

## Product Requirements correction after PR #22

[Requirements revision](../../experiments/runs/harness-requirements-revision-v1/README.md) is genuinely admitted CURRENT with 13 active product obligations, 19 historical RETIRED (including REQ-028 moved to Verification). Previous run's 28-requirement strategy and eight scenarios are retained as **historical BLOCKED drafts**, not accepted downstream knowledge. Q-DV-001/002 remain blockers, and new Verification Strategy must map to active requirements after domain semantics are accepted. No architecture or code generation authorized.
