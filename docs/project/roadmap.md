# Дорожная карта и тактика исполнения

Статус: **PROPOSED REVISION на основе [аудита](../research/methodology-integration-audit-2026-10.md)**. Не изменять фактический [current-state.yaml](current-state.yaml) до отдельного принятия новой тактики; P1 остаётся ограниченно проверенным.

Миссия [strategy](strategy.md) сохраняется: методика от реальной задачи до кода и изменения. **Лабораторные фазы — рамки эксперимента, а не дублирующий план работы над знаниями.** Harness Project Frontier, Engineering Graph, applicable coverage и Questions определяют доступные действия; не создавать/не запускать Authorities по фиксированному списку.

| Фаза / гейт | Назначение | Независимое доказательство |
| --- | --- | --- |
| P0 Foundation — сделано | Изолированная лаборатория, Git/CI, стратегия | Git snapshots; required checks в ruleset ещё не настроены |
| P1 Tool feasibility — сделано с ограничениями | Pinned Harness структурный smoke, CoderMind + Codex и начальный forward RPG | [P1 RPG review](../research/p1-synthetic-rpg-review.md), **не** полный Harness loop и не кодогенерация |
| **P2 Harness discovery & requirements** | От исходного SCN-006/свидетельств запуск `project-bootstrap-reconcile`, consumer scope и Project Frontier; через агентный skill получить и принять применимые Problem Evidence/Requirements; неизвестное оставить Question | Source-bounded provenance, REQ IDs, rejected/inapplicable/missing sources, семантическая приёмка, отсутствие выдуманных ACL ответов |
| **P3 Harness closure to implementation** | Продолжать только по актуальному frontier: применимые Domain/Application/Architecture/Interface/Verification/Test/Implementation Design и acceptance | Coverage+semantic+consumer closure; терминальные verification dispositions, Test Design, исключённые/неприменимые concerns, blocking Questions отсутствуют |
| **P3b Handoff/authority safety** | Сопоставление принятой модели с CoderMind feature_spec, проверка изменений/исключений, Git isolation/privileges | Положительный и негативный synthetic case; репозиторий лаборатории не затронут |
| **P4 CoderMind guarded implementation** | Полный Phase 2, ограниченный codegen в disposable Git, независимый oracle/traceability | Output из scratch через PR; все critical oracle cases PASS; архитектурный drift остановлен или явно принят |
| **P5 Controlled change** | Новый source/change request в Harness → affected/revalidation → ограниченный RPG edit/code | Сверка before/after source/decisions/RPG/code/test; missing affected edges как дефект |
| **P6 Controlled comparison** | Раздельные E1 (problem-to-code) и E2 (accepted-baseline-to-code); A/B/C/D | Pre-registered budgets, одинаковая информация внутри каждого эксперимента, все runs, isolated hidden oracle |
| **P7 Conclusion** | Обобщение условий применимости и проверка на другой области | GO / CONDITIONAL / NO-GO на фактах, включая стоимость/неуспехи |

## Ближайший backlog

- **TASK-004 (P2):** настоящий Harness consumer на Checker SCN-006 начиная с исходной проблематики. Сначала исследовать действующие consumer operations, проверить project-owned canonical truth и применимость scope. Сформировать evidence, а не заранее принять спецификацию.
- **TASK-005 (P3):** продолжить Harness-generated frontier до принятого *для выбранного consumer* инженерного knowledge closure. Никакого `TargetState.COMPLETE` как самостоятельного признака готовности к codegen.
- **TASK-005b (P3b):** minimal read-only handoff spike на независимом synthetic fixture: missing REQ/invalid SHA/forbidden behavior/architecture conflict; [contract hypothesis](../integration/handoff-pilot.md).
- **TASK-006 (P4):** CoderMind `plan` complete, `code_gen` в scratch repo, transfer через review PR, independent accepted oracle.
- **TASK-007 (P5):** управляемое изменение с сохранением Authority boundary и воспроизводимых impact links.
- **TASK-008 (P6):** отдельная pre-registration E1/E2, затем контролируемое сравнение A/B/C/D.
- **TASK-009 (P7):** честный сравнительный отчёт и переносимость.
- **Tooling follow-up:** GitHub required status check `repository/check` фактически пуст в ruleset; запросить настройку владельцем. Не запускать silent `cmind update`.

## Дисциплина

- Каждая реализуемая независимая задача — отдельная branch / PR / squash. Принятые проверки фиксируются отдельно от вывода LLM.
- Артефакты создаются агентом **через принятые входы и routed Harness skills**; Harness Core структурирует и ограничивает их, но не является автономной моделью смысла.
- Отсутствие принятого semantic owner или authoritative oracle даёт Question/BLOCKED, а не LLM guess.
- В E1 одинаковые **исходные** problem/evidence/decision access; в E2 одинаковые **принятые** requirements/design/test-intent входы. Результаты E1/E2 не усреднять.
- До codegen запрещено автоматическое изменение `main` лаборатории любыми upstream tools, включая post-commit hooks и CoderMind batch merges.
- Никаких длительных legacy-аудитов и универсальных моделей без проверяемого consumer need.
