# ADR-0002 (предложение): Harness — процесс принятия знаний, CoderMind — ограниченная реализация

Статус: **PROPOSED — не принято владельцем, решение не вступает в силу до отдельной приёмки.**

## Проблема

Лабораторный план разделял независимую подготовку требований (P2) и использование Harness (P3). Однако на закреплённом Harness SHA `442db854...` уже есть действующие agent skills: Problem Evidence, Product Requirements, Verification Strategy, Test Design, Implementation Design, Decision Pipeline, Project Frontier и Human Documentation Projection. В CoderMind SHA `3303a222...` feature_spec, feature_build/refactor, data-flow, interface и task planning тоже могут принимать реализационные решения. Простое последовательное использование рискует создать два источника принятого смысла.

Подробности и ссылки: [аудит](../research/methodology-integration-audit-2026-10.md).

## Предлагаемое решение

1. Истина о продукте и проектных обязательствах принадлежит **каноническим артефактам целевого проекта**. Harness с агентом организует их получение, принятие, происхождение, семантические решения, Questions, coverage и готовность к реализации. Сам Harness Core не выводит произвольные продуктовые факты.
2. Работа начинается с исходной проблематики/свидетельств и выбранного implementation Consumer. `project-bootstrap-reconcile` + Engineering Graph/Project Frontier определяют, какие знания применимы и какая capability READY; фазы лаборатории — исследовательские checkpoints, **не** дублирующий workflow Harness.
3. Сбор независимых oracle входит в Verification/Test Design, но проверка эталонных ответов внешним экспертом/отдельным reviewer и хранение скрытой части испытаний обязательны. Внутренние CoderMind TDD тесты не заменяют oracle.
4. Принятое знание и допустимую реализационную свободу передавать CoderMind в **read-only versioned source-bounded handoff**. Он может предлагать feature/spec/architecture изменения, но **не** может менять принятые требования или решения самостоятельно. Любое противоречие возвращается через Question/owner decision в Harness.
5. Не утверждать нативную поддержку контрактов Harness в Microsoft RPG: нужен отдельный compatibility spike и отрицательные тесты пропущенных/добавленных требований.
6. Кодогенерацию CoderMind изолировать в отдельном scratch Git-репозитории. Штатный `run_batch` может автоматически делать commit/merge в main и `cmind update` может выполнить самообновление; любые изменения в лабораторию попадают только через проверенный PR/squash. Запрещены сетевые device operations/production secrets.
7. RPG, code, task plans и traceability manifest — **производные реализации/проверочные проекции**, не второе каноническое хранилище исходных обязательств. Не создавать новую универсальную DSL без доказанной необходимости.

## Отклонённые альтернативы

- Сначала вручную принять спецификацию Checker, потом «передать её в Harness» — не позволяет испытать собственный Discovery/Requirements процесс Harness.
- Признать RPG новым хозяином требований/архитектуры — дублирование и возможный drift.
- Считать `TargetState.COMPLETE` единственным разрешением codegen — не учитывает semantic closure, engineering coverage и Test Design.
- Разрешить штатный CoderMind codegen напрямую внутри рабочего `main` лаборатории — противоречит веточной политике.

## Непроверенные гипотезы

- Возможность создать CoderMind `feature_spec` из уже принятого Harness knowledge без неприемлемого loss/reinterpretation.
- Способ верифицировать полноту и ownership links после `feature_refactor`, `build_data_flow`, `design_interfaces`.
- Изоляция всех git/subprocess/LLM side effects в реальном codegen и change workflow.
- Стоимость и преимущество связки относительно простого агента.

## Условия принятия

Должно быть согласовано: кто принимает требования; две модели экспериментов E1/E2; security boundary; кодогенерационный и обратный change-contract. Принятие этого ADR не означает, что Checker requirements уже приняты или интеграция реализована.
