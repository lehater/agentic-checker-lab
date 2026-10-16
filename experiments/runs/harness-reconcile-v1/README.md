# TASK-004 — ограниченное Project Reconciliation

Результат: **reconciliation завершён; продолжение разработки BLOCKED на Q-REC-001**. База: актуальный main `2bedc05` (PR #15). Рабочее дерево при старте чистое; новая ветка `research/task-004-project-reconciliation`. Закреплённый Consumer Pack `442db854c3a736a5e500b4a41664b80981b0d94c`, sync/validate-pack и маршруты исполнены. Использованы returned instruction contracts, bootstrap-reconcile и project-engineering-status skills. Product Requirements skill прочитан только для проверки следующего контракта и его предусловий, production не исполнялся.

## Что требовало reconciliation

`CHECKER-PROBLEM-ADMISSION` — технический Consumer, чья closure содержит только checker.problem. `CHECKER-PROBLEM` — технический subject этой проверки. Ни один из них не задаёт границу самостоятельного Checker, предусмотренного стратегией. Принятый problem provider не является полным product scope или списком atomic requirements. Исторический пятиузловой граф и fixture-only вертикальный срез остаются предложениями.

Штатная activation-policy имеет 10 baseline concerns и 5 conservative manual applicability concerns для software implementation readiness. Она применяет их также к техническому Consumer; это объясняет 15 concerns/16 work items, но не доказывает необходимость немедленного исполнения всех работ. Одинаковая роль `product` для DISCOVERY и PRODUCT-REQUIREMENTS в reference bindings объясняет candidate_authorities: DISCOVERY для intent.scope/behavior. Нельзя дописать claims к CURRENT problem provider и выдать это за принятые product behavior/scope.

[Проектная запись](../../../../docs/scenario/checker-scope-reconciliation.yaml) отделяет scope, вопросы полномочий и все 16 dispositions. Из неё не создаются новые Capabilities или требования.

| Work items | Классификация | Обоснованный следующий шаг |
| --- | --- | --- |
| intent.scope, intent.behavior | Нужны сейчас; неполное моделирование scope/producer | Предлагаемый PRODUCT-REQUIREMENTS → checker.requirements, после Q-REC-001; не расширять DISCOVERY |
| meta.subject-inventory | Нужен сейчас явный статус; inventory продукта ещё не готов | Q-REC-002: определить bounded product scope, затем классифицировать принятые атомы; не выдумывать REQ/subjects |
| application.failures, engineering.error-handling | Последующие этапы | Сначала наблюдаемая product failure policy, затем техническое handling; не создавать две обязанности без независимой ценности |
| architecture.structure, architecture.boundaries | Последующие этапы | Дизайн после определения продуктового поведения; число Authority/документов ещё не задано |
| verification.strategy, verification.requirement-traceability, verification.functional, verification.architecture | Последующие этапы | Отдельная проверка принятых требований и затем архитектуры; не четыре обязательных новых артефакта |
| governance.external-obligations, governance.privacy | Решение владельца / уполномоченного профильного владельца | Классификация реальных ограничений и данных; не автоматическое назначение legal/privacy Authority |
| specialized.ai, specialized.regulated, specialized.safety | Решение владельца / уполномоченного профильного владельца | Lab agentic tooling не доказывает AI в продукте; regulation/harm неизвестны. Ни mandatory capability, ни NOT_APPLICABLE пока не обоснованы |

Итого: 3 актуальных reconciliation findings (также имеют причину incomplete scope modeling), 8 downstream concern gaps, 5 applicability decisions. Сами applicability screenings можно обсуждать при определении product scope; они не требуют заранее создавать runtime AI, regulation или safety подсистемы. Ни один старый work item не требует сейчас исполнять новую Capability в принятом графе.

## Что изменено и пересчитано

Добавлены проектная scope/reconciliation запись и точечно подключаемый `.harness/coverage-reconciliation.yaml`. Штатный `subject_inventory: REQUIRED` заменяет неявный MISSING/DECLARE_SUBJECT_INVENTORY на явный MISSING/DEFINE_SUBJECT_OBLIGATIONS. Это не утверждение, что технический Consumer требует product inventory; overlay фиксирует недостающий prerequisite для claims о полноте Checker, которые нельзя делать по этому Consumer. Он не снимает concern gaps, не подменяет неизвестность DEFERRED и не закрывает coverage.

Authority registry reconciled и validated: DISCOVERY REQUIRED сохранён; 22 UNASSESSED сохранены; NOT_APPLICABLE не введён. Предлагаемый PRODUCT-REQUIREMENTS не повышен до REQUIRED только по roadmap или reference catalog: canonical product knowledge пока отсутствует. Production assignments и полномочия — отдельный owner gate.

Проверен существующий coordinated snapshot штатным read_project_publication, validate_realization и lifecycle_states с актуальными acceptance-policy fingerprints. checker.problem остаётся CURRENT; revision и байты publication, graph, assessments и принятого Problem Evidence сохранены. Re-admission/revalidation и CAS не нужны: ни принятый смысл, ни входящие в публикацию компоненты не менялись. Изменение scope-routing metadata не создаёт новую semantic acceptance.

Из одного read-back snapshot заново вычислены Decision Roadmap, Semantic Closure, Coverage и Project Frontier. Roadmap/Closure COMPLETE для технического Consumer, нет ready Capability pipeline. Coverage всё ещё false, 15 concerns/16 work items. Frontier всё ещё READY для Coverage actions, не для выполнения Product Requirements. Число gaps намеренно не уменьшено без новых принятых знаний. Реальный полный product Frontier **недоступен**: нет принятого product Consumer/production contract. Его отсутствие явно записано в evidence, вместо переименования технического Frontier.

## Проверенный технический контракт

Попытка выразить project-owner Q-REC-002 через overlay `subject_inventory: QUESTION` при текущем опубликованном Core завершилась `harness.project_model.core.CoreError: unknown question: Q-REC-002` из question_frontier. По контракту QUESTION требует существующий Core Question, одного durable текста недостаточно. Ошибка изучена по coverage_obligations / engineering_coverage / core, Harness не изменён. Без принятого адресата вне DISCOVERY не добавлен фиктивный Core Question и не опубликована произвольная мутация. Использован штатный REQUIRED; owner questions остаются явно открытыми в проектной записи. Это техническое ограничение representation, не новый блокер смысла проблемы. Несуществующие пути spec subject-obligations-v1.yaml / design engineering-coverage-v0/v1.md найдены через rg и заменены реальным docs/design/engineering-coverage-subject-obligations.md.

## Конкретное продолжение

**Q-REC-001 — минимальный следующий owner gate:** назначить PRODUCT-REQUIREMENTS producer для `checker.requirements` с prerequisite `checker.problem`; принять это соответствие в graph и назначить/делегировать production, semantic review/admission, conditional coherent publication (либо указать reviewer/acceptor). PDEC-CHECKER-002 этих прав не даёт, текущий запрос явно запрещает переход без них.

**После этого выполнять ровно `CREATE checker.requirements`** по routed product-requirements skill: источник — уже CURRENT checker.problem; результат — product-requirements/v1 с атомарными REQ/source_refs, observable scope/behavior/acceptance, либо узкие Product Questions по неизвестным решениям. Для доказательства subject completeness затем потребуется inventory по принятым атомам. Не нужно заранее изобретать промежуточную user-needs Capability, полную пятиузловую топологию или назначать все 22 Authority. Q-REC-002 не требует получить все ответы до начала разрешённого requirements work.

Предлагаемая Capability ещё не является adopted/actionable CREATE. Для перехода к ней нужны указанные права и production contract; не достаточно READY старого Frontier. Никаких новых требований, реализации, oracle или live access в этой задаче не создано.

## Воспроизводимость и существенные evidence

Из корня: `PYTHONDONTWRITEBYTECODE=1 python3 experiments/runs/harness-reconcile-v1/reconcile.py`. Скрипт использует только pinned API, валидирует сохранённые assessments и CURRENT, проверяет охват dispositions всех 16 items и неизменность публикации. Повторный запуск идемпотентен по evidence; команды sync/validate/router, hashes sources/instructions и компактные read models — в `evidence.json`. Полные повторные копии старых logs/skills/fixtures не добавляются. Модель, tokens и стоимость inference недоступны; новых model subprocess calls нет. Последние проверки — `verification.json`.

Изменения уточняют routing/classification и не меняют архитектурные границы или integration persistence; действует ADR-0002. Merge не выполняется.
