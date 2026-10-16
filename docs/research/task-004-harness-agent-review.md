# TASK-004 — независимый аудит первого agent-operated Harness Discovery pilot

Статус: **RESEARCH RUN ACCEPTED WITH LIMITATIONS; NO CHECKER KNOWLEDGE SEMANTICALLY ACCEPTED**. Дата аудита: 2026-10-16. Срез: PR #10, upstream branch commit `4a82dbedfdf82baf681cf58d3396fd4ed398a909` (operator push), frozen Harness `442db854c3a736a5e500b4a41664b80981b0d94c`.

Проверены **не слова агента из `outcome.json`**, а опубликованные исходники, исходные `*.stdout/*.stderr`, `commands.jsonl`, кандидатный граф/Core, source hash manifest, Problem Evidence и Questions. Метод: независимая инспекция опубликованных GitHub blobs с повторным сопоставлением с закреплёнными upstream документами, без запуска model/CLI на пользовательской Ubuntu. Публичный `ci` — отдельная проверка документов, не заменяющая семантический аудит.

## 1. Проверки и факты

| Контракт | Статус аудита | Проверяемое свидетельство / предел |
| --- | --- | --- |
| Дистрибутив | **PASS (recorded)** | `validate-binding.stdout` и `validate-pack.stdout` сообщают VALID на том же SHA; `commands.jsonl` содержит нулевые exit codes; это archived operator outputs, не независимая повторная установка. |
| Инструкция и routing | **PASS with limited observability** | `bootstrap-route.stdout` явно разрешает публичную `project-bootstrap-reconcile`, `instruction_contracts`, SKILL. `agent-routing.stdout` разрешает `problem-evidence`. Исправленная artifact route вернула 0 после первой ошибочной команды (`--surface consumer` для artifact CLI даёт exit 2). Порядок чтения всех инструкций известен из `run-report.md`, но **независимого agent session trace нет**. |
| Graph syntax | **PASS** | `graph-validation.stdout`: `valid: true`; `profile.stdout` содержит **5** expectations, derived из опубликованного `engineering-graph-candidate.yaml`. |
| Target state | **PASS, local graph only** | `target-evaluation.stdout` содержит `status: READY`, `implementation_consumer: true`, **одно CREATE** `checker.problem` (DISCOVERY) и **четыре PENDING**: requirements, architecture, verification, implementation; `satisfied: []`, `wait: []`. Это **не** authorization к написанию Checker. |
| Routing actionable CREATE | **PASS** | `agent-routing.stdout`: один routed `problem-evidence` для `checker.problem`, `unrouted: []`, четыре pending. |
| Coverage / applicability | **INCOMPLETE — correctly surfaced** | `engineering-coverage.stdout`: `activated_count: 21`, `completion_ready: false`, **22 work items**: 7 `ASSIGN_AUTHORITY`, 11 `MODEL_PRODUCTION_CONTRACT`, 3 `MODEL_PROOF_CONTRACT`, 1 `DECLARE_SUBJECT_INVENTORY`. Summary: **10 BLOCKED, 11 MISSING**. `project-status.stdout` оставляет **23 Authorities UNASSESSED**, т.е. ни одно назначение/применимость не принято. |
| Full Project Frontier / strict Semantic Closure | **NOT RUN** | Никаких файлов с валидным `project_frontier` или `semantic_closure` не опубликовано; агент открыто фиксирует отсутствие необходимых input acceptance/decision/lifecycle contracts. Нельзя трактовать `target-evaluation.READY` как `ProjectFrontier.COMPLETE`. |
| Источники | **PASS (Git blob identities)** | Четыре `source-hashes.json` Git blob SHA совпадают с реально извлечёнными GitHub blobs того же коммита: Harness binding, fixture README, `sssr-scn-006.md`, `product-access-as-is.md`. Два frozen fixture blobs совпадают с закреплёнными upstream исходниками. SHA256 заявлены в source manifest; самостоятельной независимой локальной проверкой sha256 run здесь не утверждаем. |
| Problem Evidence | **SOURCE-BOUNDED CANDIDATE / NOT ACCEPTED** | `problem-evidence-candidate.md` соответствует историческому SCN-006: конкретная tuple, релевантные placements, **все** stored covering Permit/Deny rules в policy order, no-match без универсального deny, stored vs live и freshness. `Product As-Is` не превращён в целевую Django/SQL архитектуру. Это допустимое problem framing **к рассмотрению**, не принятый продуктовый контракт. |
| Вопросы | **PASS as draft list, not Core Questions** | `questions.md`: Q-01..Q-13 адресуют scope, product/domain policy, actor, source port/protocol, consistency/freshness, oracle, ownership и coverage. `core-candidate.yaml` имеет пустые `artifacts: []` и `questions: []`, потому что acceptance/registration не выполнялись. Это ограничение пилота, не доказательство об отсутствии Questions. |
| Git isolation / model accounting | **PASS as operator report with limitations** | В `git-status.stdout` одна untracked run directory до явного операторского коммита; нет tracked source diff по этому свидетельству. Глобальный side-effect audit CLI вне scratch не проводился. `model_calls: null`, нет total token/cost/model id — comparative costing невозможен. |
| Checker/decision acceptance | **NOT RUN BY DESIGN** | `outcome.json`: `project_accepted=false`, `checker_implemented=false`. Нет `CanonicalArtifact` регистрации, semantic acceptance, `acceptance_id`, Test Design, oracle или CoderMind codegen. |

## 2. Граница действительного результата

**Доказано в этом эксперименте:** агент создал согласованные **предложения** Engineering Graph/Core на конкретном проектном источнике, вызвал реальные pinned Harness validation/evaluate/routing/status/coverage CLI и получил `CREATE checker.problem`; затем подготовил документ Problem Evidence, следуя контракту skill, сохранив явные вопросы и не регистрируя их как принятые данные.

**Не доказано:** полный `project-bootstrap-reconcile` как завершённая идемпотентная project realization; полнота нужного `Design Profile` (он автоматически выведен из предложенного графа, значит не независимый coverage oracle); полной Project Frontier или Semantic Closure; пригодность архитектурного handoff; корректность будущего Checker; эффективность/стоимость методики против A/B/C/D.

Отдельное замечание: в pinned Harness `project-bootstrap-reconcile` — **агентная процедура**, а не монолитный `execute_bootstrap` API. Записанная route resolution и ручное выполнение некоторых этапов подтверждают **частичное agent-operated исполнение**, но не все 14 steps процедуры. В частности, incomplete Coverage/Authority assessments исключают `bootstrap COMPLETE`.

## 3. Риски и наблюдения

- **A-01 (HIGH) — Достаточность графа не подтверждена.** Предложение содержит только пять capabilities (Problem, Requirements, System Architecture, Verification, Implementation). Оно не обязано содержать все reference Authorities, но уже выявленные Coverages concerns и отсутствие явного Test Design/Domain obligations означают, что нельзя утверждать design closure. До принятия графа нужно сконструировать минимальный project-owned Consumer policy/coverage с реальным ownership и разрешить/моделировать только применимые concerns.
- **A-02 (HIGH) — Нет семантических полномочий.** 23 Authorities `UNASSESSED`; Q-01/Q-07/Q-08/Q-09/Q-10 остаются нерешёнными. Graph owner `DISCOVERY` — предложенная роль, не документ о назначении человека/agent autonomy. Запрещено регистрировать candidate как accepted provider без authority и решения о framing.
- **A-03 (MEDIUM) — Маркер 'offline' в subject предшествует решению.** `CHECKER-OFFLINE-CANDIDATE` и proposed fixture scope — исследовательское ограничение, требующее явной фиксации. Наличие этого имени в derived profile не доказывает принятие offline-режима. Использовать нейтральный предметный scope до решения либо сохранить как явно предложенную candidate branch.
- **A-04 (MEDIUM) — Ограниченная воспроизводимость и логи.** `run-pilot.py` использует домашний каталог / pinned paths оператора; `commands.jsonl` хранит абсолютные локальные пути; модель, token counts и часть первоначальных чтений инструкций известны только из повествовательного отчёта. В следующем запуске собирать manifest/source hashes, санкционированный session summary без credentials, стоимость/время и переносимые overrides.
- **A-05 (MEDIUM) — Coverage 'blocked' не равен автоматически новым Capability.** 22 work items включают мета-инвентаризацию и proof contract; нельзя слепо создать 22 узла графа. Нужна проверка applicable concern, subject inventory и права Authority. `10 BLOCKED / 11 MISSING` — статусы оценщика для конкретного предложенного graph/consumer/scope, не универсальное состояние Product.
- **A-06 (LOW) — Ошибка команды восстановлена.** `problem-route.stderr` честно зафиксировала ошибочный `--surface`, последующий corrected route вернул 0. Не дефект Harness.

## 4. Итог и гейты

**Приёмка исследовательского прогона: PASS WITH LIMITATIONS.** Не означает принятие `problem-evidence-candidate.md`, `engineering-graph-candidate.yaml`, `authority-assessments-candidate.yaml` или User Questions. Их статусы остаются *DRAFT*, *UNASSESSED*, *UNRESOLVED*.

Следующее допустимое действие в TASK-004:

1. Сделать bounded **semantic review** именно `problem-evidence-candidate.md` по frozen первичным документам; вопросы о реальном пользовательском intent/decision authority адресовать владельцу, но **не** требовать выбирать архитектуру, UI, SQL и всю терминологию политики на этапе Discovery.
2. Уточнить project-specific Design Profile/Consumer scope, провести applicability/subject-inventory review против `engineering-coverage.stdout`, а не автоматически заводить все reference authorities и capabilities.
3. Проверить/довести реальную bootstrap/reconcile процедуру и выяснить, какие coverage read models, semantic admission/decision policy нужны для next authoritative publication. До этого ни `ProjectFrontier.COMPLETE`, ни readiness for CoderMind.
4. После явной принятой Authority/семантической границы — зарегистрировать только соответствующий accepted Problem Evidence provider с проверками; переоценить target и посмотреть, стало ли Product Requirements реально `CREATE`.
5. Провести отдельный negative source-change/missing-ownership тест перед переходом к кодированию; не смешивать этот эксперимент с E1/E2.

**Никакие требования Checker, дизайн, новые графовые абстракции или adapter CoderMind этим отчётом не принимаются.**
