# Audit-2026-10-16 — пересмотр стратегии Harness × RPG × Agent

Статус: **RESEARCH / PROPOSED CORRECTIONS — NOT ACCEPTED STRATEGY**. Никаких изменений в принятую миссию, каноническую дорожную карту или правила сравнения этим документом не вносится.

## 0. Основание, границы и метод

Запрос владельца: перепроверить исходную стратегию, последовательность работ, реальную роль Harness и RPG/CoderMind после обнаруженного ошибочного упрощения Harness до графа Capabilities.

Проверены первичные документы лаборатории: [strategy](../project/strategy.md), [roadmap](../project/roadmap.md), [experiment-design](../project/experiment-design.md), [success criteria](../project/success-criteria.md), [oracle-plan](../evaluation/oracle-plan.md), [integration hypothesis](../integration/README.md), [P1 review](p1-synthetic-rpg-review.md). Сопоставлены с **зафиксированными** версиями источников:

- Harness `442db854c3a736a5e500b4a41664b80981b0d94c`: [README](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/README.md), [Agent Artifact Workbench](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/agent-artifact-workbench-v0.md), [Engineering Graph](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/engineering-graph-v0.md), [Integration Contract](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/integration-contract-v0.md), [Design Profile](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/agent/design-profile/SKILL.md), [Problem Evidence](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/problem-evidence/SKILL.md), [Product Requirements](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/product-requirements/SKILL.md), [Verification Strategy](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/verification-strategy/SKILL.md), [Test Design](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/test-design/SKILL.md), [Implementation Design](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/implementation-design/SKILL.md), [Human Documentation Projection](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/human-documentation-projection-v1.md), [Project Frontier](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/project-frontier-v0.md), [Bootstrap/Reconcile](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/agent/project-bootstrap-reconcile/SKILL.md).
- CoderMind baseline `a4e6966...` и experimental Codex PR #96 `3303a222eaec42c6a178bddd46ad63d9026ab8fa`: [README](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/README.md), [commands](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/docs/commands.md), [configuration](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/docs/configuration.md), [CLI reference](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/docs/cli-reference.md), [codegen](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/templates/commands/code_gen.md), [RPG edit](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/templates/commands/rpg_edit.md), [git ops](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/scripts/code_gen/git_ops.py), [feature-spec schema](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/scripts/feature/schemas/spec.py). Upstream PR [#96](https://github.com/microsoft/RPG-ZeroRepo/pull/96), separate execution-authority PR [#99](https://github.com/microsoft/RPG-ZeroRepo/pull/99).

**Ограничение:** это целевой документальный и исходно-кодовый аудит критических контрактов, а не построчная проверка всего корпуса Harness (~1000 файлов), всех модулей Microsoft и не новая интеграционная E2E-реализация. Ни один непроверенный интеграционный путь не объявляется работоспособным.

## 1. Сохраняемые стратегические решения

Сохранять **без смены миссии**: `problem → accepted engineering knowledge → realization → code → independent verification → controlled change`; meaning-first; минимальный ограниченный Checker; source ≠ accepted requirement; независимые oracle; tracked source SHA; 4 варианта A/B/C/D; честные negative results; запрет подмены unknown на permit/deny; runtime приложения без Harness/CoderMind.

Проверки P1 **не отменяются**: pinned Harness Core/Engineering Graph structural smoke, Codex live adapter, feature_spec/feature_tree/build_skeleton и первый versioned RPG (31 узел/18 feature-листьев/0 non-containment edges) действительно были испытаны. Но они **не проверяли**:
- настоящий цикл agent-driven Harness из Problem Evidence до принятых Design/Test/Implementation артефактов;
- full CoderMind Phase-2 (`build_data_flow`, `design_base_classes`, `design_interfaces`, `plan_tasks`) и `code_gen`;
- связь/принуждение принятых Harness решений в CoderMind;
- безопасность веток/auto-write внутри реального codegen, change impact и поведенческое качество Checker.

Поэтому формулировка `P1 tool feasibility passed` корректна; `complete toolchain E2E`, `Harness validated design method`, `ready for codegen` — нет. Документ `docs/research/tooling.md` ещё носит устаревший статус `PLANNED, NOT INSTALLED`; его нужно позже согласованно обновить со ссылкой на текущий state, а не скрывать исторический статус.

## 2. Реальная функциональная область двух систем

| Concern | Harness (зафиксированный контракт) | CoderMind PR #96 | Граница для лаборатории |
| --- | --- | --- | --- |
| Problem/discovery | `problem-evidence` skill; источник, actor, outcome, evidence, scope, unresolved Questions | Отдельного аналога с таким контрактом в проверенном forward pipeline нет | Harness/проект сохраняет acceptance owner; CoderMind не выводит продуктовые факты из кода |
| Requirements | `product-requirements/v1`, `REQ-*`, provenance, atomicity, unresolved Questions, semantic acceptance | `feature_spec` генерирует собственную схему из docs/текста с возможными evidence ссылками | `feature_spec` — кандидат производного input к планированию, не второе решение о требованиях |
| Decomposition & design | Authorities, producer/consumer topology, Governance, Domain, Architecture, Interface, Component и `implementation-design` | `feature_build`, `feature_refactor`, skeleton, data-flow, base classes, interfaces, task batches | Согласовать на уровне контрактов/инвариантов, не только имен узлов |
| Verification | `verification-plan/v1`: dispositions на каждый REQ; `test-design/v1` перед code, independently accepted oracles | Agent-generated TDD pytest, batch verification и global review | Независимый oracle не заменяется CoderMind-тестами; его исходный контракт принадлежит принятому знанию |
| Coordination | Engineering Graph, Core, Project Frontier, Questions, semantic/coverage closure, atomic publication | RPG и `rpg_edit` для code-centric impact/change | Не создавать второй state/status graph в Harness ради тех же результатов |
| Documentation | Canonical artifacts + disposable source-bounded human projection | rpg visualization, planning artifacts, generated code | Документы Harness — продукт принятого знания; RPG/docs — realization snapshots/проекции |
| Change | Authority-owned revision; re-evaluate dependent capabilities, semantic freshness | `rpg_edit`, `update_rpg`, post-commit hooks и code updates | Source change по принятому request, downstream projections ревалидируются, код не переопределяет смыслы |

**Уточнение:** Harness не автономный генератор идей/документов без агента; сам Core не анализирует произвольный предметный текст. Agent/skills создают кандидатов, Harness задаёт права, границы, признаки достаточности и правила принятия. Engineering Graph — **нормативная топология знания**, не вручную назначенная последовательность фаз. Текущая модель `project_frontier` вычисляет следующий допустимый action; `COMPLETE` по одной структурной проверке не есть полная semantic coverage или coding authorization.

## 3. Ошибки и пропуски текущего плана

### F-01 CRITICAL — P2 «ручные требования» искусственно вынесены перед Harness

Текущий [roadmap](../project/roadmap.md) определяет `P2 scenario acceptance` → `P3 Harness engineering closure`, а TASK-004 — `SCN-006 → independent target specification`. Но Problem Evidence, Product Requirements, семантическая приёмка и создание Questions — уже задачи Harness agent workbench. Это устраняет возможность измерить **полный** процесс Harness в вариантах B/D.

**Коррекция:** после получения исходной задачи сразу bootstrap/reconcile Harness-проект, выбрать минимальный implementation Consumer / применимый scope, проверить применимость Authorities/concerns, дать `Project Frontier` вывести необходимые `CREATE/WAIT/BLOCKED` действия. Requirements, Verification и Test Design производить через соответствующие artifact skills. Входной SCN-006 остаётся непринимаемым без решения свидетельством, не готовой спецификацией. Одинаковые человеческие решения фиксировать при действительно спорных вопросах, не менять смысл молча.

### F-02 CRITICAL — два независимых владельца смысловой декомпозиции

CoderMind `feature_spec` и `feature_build` могут дополнять требования и «production relevant» функциональность, `feature_refactor` и Phase-2 design могут повторно выбирать границы, интерфейсы, физическую структуру. Harness уже имеет Domain, Architecture, Interface и Implementation Design. Если оба контура принимают решения, нарушается project source of truth.

**Коррекция:** зафиксировать `input contract` (accepted source revision/identities, scope, constraints, verification refs, allowed freedoms) и `output contract` (proposed RPG nodes/tasks, omissions/additions/conflicts, evidence links). Запуск CoderMind после Harness должен **предлагать** производную реализацию, не принимать новые продуктовые/архитектурные решения. Не утверждать, что Microsoft поддерживает нативный imported locked Harness spec: **совместимость не доказана**, нужен отдельный compatibility spike на копии принятого fixture.

### F-03 HIGH — ошибочное представление RPG как только кодового графа

CoderMind поддерживает **три рабочих направления**: forward `feature_spec → feature_build → feature_refactor → skeleton → data flow → base classes → interfaces → tasks → codegen`; reverse code → graph; surgical graph-aware edits. Это шире «нарисовать граф → написать код». Интеграция должна учитывать его агентов, skills, implicit execution rights и side effects.

**Коррекция:** провести discovery всей CoderMind Phase-2, `code_gen`, `rpg_edit`, MCP query и синхронизации, а не считать initial `rpg.json` финальной моделью. Не требовать «100% кодовых узлов» до появления кода.

### F-04 CRITICAL — прямой codegen CoderMind противоречит Git-политике лаборатории

Проверенный upstream `code_gen` создаёт batch branches и **локально merge --no-ff обратно в main**, а `git_ops.ensure_on_main` может auto-commit рабочие изменения. Наша лаборатория использует PR-only, squash и main ruleset. Кроме того, `cmind init` может ставить hooks, `cmind update` по умолчанию выполняет silent self-upgrade. Upstream PR #99 execution authority отдельно **не** включён в экспериментальный PR #96.

**Коррекция:** запускать кодогенерацию/graph edits **только** в отдельном временном git-репозитории/isolated worktree с отдельной политикой авторизации/интерфейса, а не в `agentic-checker-lab`. Импортировать только санитизированный output через PR. Проверить write surface/субагентов, hooks, branch changes, stop/recovery, subprocess permissions, package updates, tool credentials. Самого PR #96 пока недостаточно для security GO.

### F-05 CRITICAL — A/B/C/D сравнение смешивает две причинные задачи

Если baseline requirements и oracle заранее были подготовлены через Harness и одинаково отданы A/C, сравнительный тест измеряет **только downstream implementation**, а не вклад Harness в обнаружение/принятие requirements. Если A/C получают более слабую problem statement, а B/D — готовую спецификацию, сравнение нечестно. «Та же модель» и «тот же бюджет» не гарантируют сопоставимого количества доказательств/подготовительной работы.

**Коррекция:** два отдельно предзарегистрированных, не смешиваемых протокола:
- **E1 — end-to-end methodology:** одинаковое начальное problem/evidence bundle всем четырём arms, одинаковые допустимые каналы уточнения у человека, одинаковые независимые скрытые oracle checks, фиксировать *весь* бюджет discovery→implementation→change. B/D применяют Harness с самого problem stage; A/C должны самостоятельно, но без утечки B/D artifacts, добыть необходимые знания. Для blocked cases фиксировать вопросы и время на решения.
- **E2 — downstream realization:** всем четырём arms выдать **одну и ту же принятую** requirement/architecture/test-intent baseline; измерять только конструирование, реализацию и изменения. Здесь Harness contribution — enforcement/impact/traceability, а не качество discovery. Дорогие повторные расчёты Harness учесть полностью.
Результаты E1 и E2 не объединять в одну таблицу победителя. Общие требования к фиксации models/budgets, randomization, isolation, signed oracle и full runs остаются; установить пороги/число повторов **до** замеров.

### F-06 HIGH — автоматически «потерявшийся» смысл не восстанавливается одним RPG

Реальный synthetic P1: 31 nodes, 18/18 feature-name match, **0 non-containment edges**, `meta.description`/`meta.content` пусты у 18 листьев RPG; полные описания и provenance находятся в нескольких исходных JSON. Даже CoderMind `FeatureSpec` делает `evidence` optional. Метрики `coverage_percentage=100` и `assigned_leaf_count=18` не доказывают semantic completeness.

**Коррекция:** versioned *derived traceability projection* (source assertions/REQ IDs → accepted capability/artifact identities → CoderMind spec/feature/graph IDs → code/test evidence). Результирующие связи не должны становиться новым каноническим владельцем смыслов. Сначала выяснить, какие ссылки/кросс-мапы доступны штатно; не начинать с разработки нового универсального graph DSL.

### F-07 HIGH — Oracle должен быть результатом принятого Verification/Test Design, но оставаться независимым от генератора

Нынешний `oracle-plan.md` уже содержит полезные 9 candidate cases, но не является accepted semantics. В Harness Verification Strategy требует disposition для каждого принятого REQ, Test Design определяет precondition, operation, oracle, negative, property checks и трассировку. CoderMind TDD создает собственные тесты **по своей** декомпозиции — они не independent oracle.

**Коррекция:** при создании тестов Harness может помогать формировать их контракты, но hidden execution oracle должен быть проверен человеком/независимой процедурой и заморожен **до** реализации. Избегать подгонки под codegen. Не объявлять девять предложенных тест-кейсов уже принятыми.

### F-08 HIGH — недооценены Harness admission, coverage, Project Frontier, Human Projection

Harness позволяет делать decision exploration и governance, semantic admission, project publication, engineering coverage, quality checks, Test Design и human-readable projections. Цикл нельзя заменить вручную написанным YAML graph smoke.

**Коррекция:** отдельная проверка настоящего *agent-operated Harness consumer*: problem→requirements→verification→implementation-design в нужном минимальном scope, `Question` negative case, incremental reevaluation, machine validation, human documentation; не требовать всех Authority без доказанного consumer need.

### F-09 MEDIUM — «P1 завершён» требует квалификации

Текущий `current-state.yaml` корректно фиксирует ограничения initial RPG, но `phase: P2` и `status: P1_SYNTHETIC_RPG_ACCEPTED_WITH_LIMITATIONS` могут ошибочно читаться как доказательство полной готовности стека к интеграции. Пин Harness проверял только tiny graph smoke; CoderMind codegen не проверялся.

**Коррекция:** не откатывать P1; сохранить `P1 tool feasibility: accepted with limitations`; в backlog явно добавить `P1b integration contract/security spike` и end-to-end Harness artifact loop как prereq к реальному кодированию. Не скрывать исторические evidence-факты.

### F-10 MEDIUM — версии, Git и стоимость

Upstream PR #96 и #99 по состоянию на проверку открыты. `cmind update` потенциально меняет установленный инструмент; модель Codex и её entitlement/температура не зафиксированы внутри мантифеста P1; журналы могут содержать приватные prompt traces. GitHub ruleset main содержит `required_status_checks: []` даже при успешных CI jobs.

**Коррекция:** materialize immutable install SHA, CLI/model version, usage data по возможности, prompt/skills SHA, tool permissions, start/end git tree, artifact hashes, private logs policy; запрет непроверенных апгрейдов; назначить реально required `repository/check` в Settings. Не считать успешное CI «обязательной» защитой пока ruleset пустой.

## 4. Предлагаемый новый workflow (не нормативный до принятия)

```text
Problem/evidence boundary (legacy and stakeholder sources, UNACCEPTED)
    ↓
Harness consumer/bootstrap/reconcile + Engineering Graph / Project Frontier
    ↓
CREATE: Problem Evidence → Product Requirements → relevant Domain/Application/
        Architecture/Interface/Component/Verification/Test/Implementation Design
    ↺ Question → owner decision → accept/revalidate → frontier
    ↓
Harness-owned semantic acceptance + engineering coverage/handoff closure
    ↓
A minimal, immutable, versioned *realization input projection*
    ├─ accepted requirements/IDs, non-goals, invariant and safety boundary
    ├─ accepted design constraints + implementation freedoms
    └─ accepted test obligations (some independent/hidden)
    ↓
CoderMind compatibility adapter in isolated git workspace
    ↺ feature_spec/feature_build proposals → compare to accepted input, not overwrite
    ↓
CoderMind full Phase-2 RPG planning / interface/task design
    ↺ architectural conflict → Harness owning Question/decision, not silent change
    ↓
CoderMind code generation + local TDD in sandboxed scratch repository
    ↓
Independent oracle + diff audit + link projection + source/provenance verification
    ↓
Reviewed PR into lab target baseline (no automatic main merges)
    ↓
Change request routed through Harness first → affected accepted knowledge
    ↓
Constrained RPG edit/update and repeat acceptance
```

Оговорка: этот конвейер **логический**. Реальная последовательность выполняется из Harness-derived actionable frontier, а не по вручную назначенным стадиям; не всякая задача потребует полного списка Authorities. Уточнение: production implementation acceptance требует всех applicable Harness closure предикатов, не только `TargetState.COMPLETE`. CoderMind `feature_spec` может оказаться неизбежной стадией реализации; его output тогда `proposal` и валидируется против принятых требований.

## 5. Пересмотр roadmap и экспериментальных задач — предложение

| Гейт | Предлагаемая ответственность и результат | Не допускает продолжения, если |
| --- | --- | --- |
| **Audit gate (сейчас)** | Утвердить границу Harness/CoderMind, протокол E1/E2, источник истины, нормы write authority | Дублирующая truth/неконтролируемый codegen |
| **TASK-004-R / P2+P3** | Для Checker от problem evidence запустить настоящий Harness consumer; coverage/frontier-driven acceptance всего **применимого** knowledge closure; принять независимые verification/test contracts | Unresolved Questions, неподтверждённые REQ или verification |
| **TASK-005-I** | Минимальный Harness→CoderMind adapter spike на synthetic accepted fixture; canary intentional conflict and omission | Добавлены требования, проигнорированы constraints, lost provenance |
| **TASK-006-R** | Full CoderMind Phase-2 + guarded codegen в отдельном scratch git, сброс/восстановление, независимые тесты | Codegen пишет в lab main, нативный merge несовместим с PR-only, missing accepted semantic constraints |
| **TASK-007-C** | End-to-end Checker + change case; accepted source rev, RPG/code/test hashes, backward/forward links | Oracle failure или не объяснён drift |
| **TASK-008-E1/E2** | Предзарегистрированные раздельные сравнения *full problem-to-code* и *same accepted baseline-to-code* | Утечка знаний между arms; неконтролируемые модель/бюджеты/интервенции |
| **TASK-009** | На основании evidence — scope-limited decision GO/CONDITIONAL/NO-GO и holdout task | Только toy example или marketing claim вместо доказательства |

**Нумерация выше — предложенная**, не заменяет автоматически существующие TASK-004..009 и P2..P7. Главное изменение: не самостоятельное написание requirements перед Harness, а Harness-produced acceptance как часть измеряемого процесса, с отдельным E2 для изоляции эффекта кодогенерации.

## 6. Контрольные вопросы на этапе принятия новой стратегии

1. В E1 измеряем весь путь с одинаковой *сырой проблемой*, а в E2 реализацию с одинаковой *принятой моделью*? Это различает вклад discovery и реализацию.
2. Какие accepted architecture/implementation freedoms передавать CoderMind, чтобы не принуждать его к дублирующей архитектуре и сохранить место для настоящих сравнений?
3. CoderMind может потребить принятую Harness спецификацию без обязательной смысловой регенерации? Пока **NOT_VERIFIED**.
4. Какие локальные операции Codex/CoderMind действительно разрешены? На что настроены sandbox, hooks, git permissions? Пока **NOT_VERIFIED** для codegen.
5. Как связывать зафиксированные требования с графом, если RPG не сохраняет requirement IDs? Сначала минимальная проверяемая projection, не новая универсальная теория.
6. Как сохранить человеческую компетенцию в принятии спорных Product/Domain решений, не превращая её в скрытое дополнительное преимущество B/D?

## 7. Решение, которое предлагает этот аудит

- **KEEP:** миссия лаборатории, meaning-first, bounded Checker, independent oracle, 4 arms и исторический P1 evidence.
- **REVISE:** дорожная карта P2/P3: вести requirements/verification/design **через Harness agent loop**, не перед ним.
- **REVISE:** модель интеграции: derivative proposal/adapter with validation, not second source of truth.
- **REVISE:** сравнительный протокол как раздельные E1 и E2 с предрегистрацией.
- **BLOCK UNTIL VERIFIED:** запуск CoderMind codegen в реальном репозитории; full Phase-2; execution authority; cross-tool semantic governance.
- **NEXT:** после рассмотрения отчёта оформить *отдельный* decision/roadmap PR и маленький integration spike; этот аудит не является автоматически принятым решением владельца.

Результат аудита свидетельствует о **существенных пропусках в архитектуре эксперимента, но не опровергает миссию**. Настоящая ценность исследования — проверить, может ли Harness владеть жизненным циклом принятого знания, а CoderMind безопасно и эффективно реализовывать эту истину без повторного определения предметного смысла.
