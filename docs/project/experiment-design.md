# Контролируемое сравнение A/B/C/D — проект предрегистрации E1/E2

Статус: **PROPOSED**, исследовательский дизайн. Число повторов, бюджеты, версии моделей, выбранный scope и пороги успеха **не утверждены**; их необходимо заморозить перед любыми сравнительными прогонами. Варианты ниже не являются выполненными результатами.

## Что сравниваем

| Arm | Инженерный процесс | Планирование/реализация |
| --- | --- | --- |
| **A** baseline | Coding agent без Harness | Coding agent без RPG |
| **B** Harness | Agent + Harness Problem→Requirements→применимые Design/Test/Implementation contracts | Coding agent без RPG |
| **C** CoderMind | Без Harness, agent-driven исследование смысла как часть его доступного workflow | CoderMind RPG/feature planning/codegen |
| **D** связка | Agent + Harness accepted engineering knowledge и контроль Questions | CoderMind, ограниченный Harness handoff и oracle |

Архитектурное предположение об улучшении D не является исходом тестирования.

## E1 — полный процесс от проблематики

Одинаковый необработанный problem statement/legacy evidence с одинаковыми разрешёнными источниками всем четырём arms. Для A/C нет принятого Harness artifact bundle. B/D запускают Harness *с problem stage*. Цель: способность вытащить смысл, вопросы, решения, реализовать и изменить приложение. Измеряется **вся** стоимость процесса, включая подготовку Harness graph, discovery, human reviews, принятие тестов и handoff.

Контроль справедливости: одинаковая доступность владельца/эксперта, протокол выдачи решений для каждого arm, immutable original evidence, развязка решений/ответов между запусками. Чтобы не утечь accepted requirements из B/D в A/C, обеспечить отдельные рабочие копии и независимые session contexts. Главный hidden oracle задаётся **независимо от сравниваемых агентов** и до запуска реализации; он не возникает из кода arm.

В E1 Harness может успешно остановить реализацию из-за неизвестного критического факта; это правильная safety outcome, а не обязательная неудача. Сравнивать по правилам безопасного `BLOCKED` наряду с функциями кода.

## E2 — одинаковая принятая baseline, разные реализации

Для всех arms один и тот же замороженный accepted product/design/verification **информационный пакет**, без скрытого дополнительного ограничения только для B/D. A/C получают содержимое в нейтральном проектном формате; B/D могут дополнительно использовать Harness для охраны принятых obligations/traceability. Это изучает **downstream enforcement, planning, cost, codegen, change impact**, а не способность Harness сформировать исходные требования.

Фиксированная архитектура может искусственно уменьшить свободу CoderMind и обычного агента. Применять только действительно принятые architecture constraints, остальное явно оставить `implementation_freedoms`, одинаковые для четырёх arms. В оценке отдельно показывать соблюдение обязательных границ и качество выбора внутри свобод.

## Общие контроли

- Ровно одинаковый набор критических acceptance obligations *внутри E1 или E2*, с отложенным/скрытым holdout-набором; независимая корректность ожидаемых результатов, минимизация тестовой утечки.
- Контроль модельной версии, prompting/agent skill/CLI pins, инструментария, seed/temperature где возможно, environment/container, Git SHA, бюджета, максимума попыток и wall-clock.
- Один запрограммированный change request после исходной реализации; source revision и oracle baseline фиксируются заранее. Изменённые обязательства принимаются через тот же предусмотренный канал, что и исходные.
- Единые разрешения инструментов и boundary на запись Git; native CoderMind commit/merge допускается **только** внутри isolated scratch Git.
- Сохранить все run manifests, заблокированные/ошибочные запуски, токены и расходы по возможности, human questions/ответы и артефакты, включая подготовительные затраты.
- Контроль order/learning effects: копии и session isolation, рандомизированный/чередуемый порядок вариантов, несколько повторений при доступном бюджете.
- Заморозить threshold и N прежде, чем увидеть сравнительные результаты. Никакого объявления лучшего arm по двум игрушечным successful runs.

## Метрики и интерпретация

1. Correctness/safety: число критических правильных исходов, ложных allow/deny вместо unknown, обязательные questions, серьезные unsafe tool actions.
2. Discovery quality (E1): оправданные/пропущенные требования, источники, semantic decisions, non-goals; распознаны ли существенные неизвестные.
3. Engineering completeness: нарушения принятой архитектуры, unresolved semantic authority, Test Design/verification obligations и их conformance.
4. Traceability/change: полнота и точность требования→решение→RPG/код/тест links, affected nodes, regressions и объяснение изменений.
5. Cost: discovery/architecture/handoff/codegen/repair human & agent labor, tokens, tool calls, wall-clock, retry и graph overhead.
6. Reproducibility: clean checkout & manifest, re-run with pinned versions, no silent cache dependence.

**Результаты E1 и E2 не соединять в один «победитель D».** Обозначения: PASS/FAIL/BLOCKED/INCONCLUSIVE с явными limitations. Условие качества для каждого arm — независимый oracle; для методологии дополнительно фиксировать стоимость, ошибки authority и изменение.

См. [success criteria](success-criteria.md), [oracle candidates](../evaluation/oracle-plan.md) и [audit](../research/methodology-integration-audit-2026-10.md).
