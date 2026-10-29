# Карта знаний Agentic Checker Lab

**Git main — принятая история проекта.** Статусы PR/экспериментов не являются статусами main. Новые решения фиксируются в PR с проверками.

| Назначение | Документ |
| --- | --- |
| Миссия и границы | [Стратегия](project/strategy.md) |
| Текущее состояние и ограничения | [State](project/current-state.yaml) |
| Передача локальному исполнителю | [Handoff](project/local-executor-handoff.md) |
| Очерёдность небольших проверяемых шагов | [Roadmap](project/roadmap.md) |
| План проектирования: OpenSpec + готовые skills, этапы D1–D6 и восстановление в новом чате | [Design-stage plan](project/design-stage-plan.md) |
| D2: минимальный design stack, handoff и review checklist | [Design stack](project/design-stack.md) |
| Clean Architecture, SOLID, KISS, YAGNI | [Engineering Policy](engineering/policy.md) |
| Условия успеха | [Success criteria](project/success-criteria.md) |
| Экспериментальное сравнение | [Experiment design](project/experiment-design.md) |
| Порядок Git / PR | [Governance](project/governance.md) |
| Контракт spec → RPG | [Integration](integration/README.md) |
| Независимые проверки | [Evaluation](evaluation/README.md) |
| Трассировка OpenSpec → тестов | [Requirements trace](evaluation/requirements-trace.md) |
| Исходная постановка Checker | [Scenario](scenario/README.md) |
| Evidence-Gated Requirements Discovery v0.1 (experimental practice) | [Discovery](discovery/README.md) |
| Исследования и исторические результаты | [Research](research/README.md) |
| ADR | [Decisions](decisions/README.md) |

ACTIVE: только утверждённая в main методика. PROPOSED: непроверенный кандидат. VERIFIED: реальное проверенное выполнение с SHA и окружением. HISTORICAL: предыдущие эксперименты, включая Harness; не действующие инструкции.

RPG, сгенерированный код, журналы и отчёты — производные от спецификаций. Изменение требований требует явного согласования, а не тихого исправления generated output.
