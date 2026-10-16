# TASK-004 — CREATE checker.requirements

**Результат: BLOCKED по содержательным Product Questions, не по полномочиям.** База main `c8eb169`, новая ветка `design/task-004-checker-requirements`. Рабочее дерево при старте чистое, пользовательских незакоммиченных изменений не было. Использован неизменный Harness Consumer Pack `442db854c3a736a5e500b4a41664b80981b0d94c`.

## Исполнение и результат

Прочитаны AGENTS/docs index, PDEC-001/002/003, Project Publication, reconciliation и необходимые source fixtures. Sync/validate-pack выполнены, публичные bootstrap-reconcile/status и product-requirements routes разрешены; instruction contracts и selected skills прочитаны. Сохранены их hashes вместо повторных копий.

В project-owned graph по принятому PDEC-003 добавлены PRODUCT-REQUIREMENTS → checker.requirements, единственный prerequisite checker.problem и технический CHECKER-REQUIREMENTS-ADMISSION. Перед новым production Roadmap действительно READY/CREATE, checker.problem CURRENT по актуальному policy fingerprint. Это не полный product Consumer. ADR-0003 фиксирует границу и Question/publication contract, не добавляя downstream Authority.

В [review](review.md) сохранены source-by-source disposition и выполненные semantic checks. Выделены REQ-CHECKER-001..007: placements, подходящие сохранённые ACL, их порядок, достоверность источников, NOT_REQUIRED universal verdict, запрет вывода DENY/ALLOW из одного отсутствия match и запрет общесистемного effective verdict из одного наличия правила. Отрицательные ограничения не превращены в запрет всех scoped interpretations. Исторические функции/fields/live/tuple не приняты автоматически.

Подготовлен managed product-requirements/v1 **кандидат**, каждый REQ со source_refs и partial acceptance criteria. Реальный `harness.workspace.workspace validate-artifact` — valid true. Его schema-level ACCEPTED у строк относится к individually reviewed intent subset, не к приёмке всего knowledge artifact. Canonical provider не зарегистрирован, законченный canonical requirements artifact не заявляется. Не используется PROPOSED вместо допустимых schema ACCEPTED/RETIRED, но и schema PASS не выдаётся за semantic acceptance.

Semantic Review REJECTED: наблюдаемая проверка всего поведения невозможна без выбора поддерживаемого product slice и условий достоверности/неполных результатов. Открытая неизвестность не объявлена неприменимой и не устранена тайным сужением Capability до произвольного удобного subset. Приёмка только высокоуровневого subset под видом завершённого checker.requirements оставила бы downstream без условий успеха. Это stop condition product-requirements skill steps 7/11, не требование решить всю архитектуру или все будущие функции.

Настоящий `admit_artifact` выполнен **до добавления новых blockers**, с actual CURRENT prerequisite, его canonical source artifact/Authority и machine-readable assertions. Результат: REJECTED, findings SEMANTIC_REVIEW_REQUIRED и SEMANTIC_REVIEW_REJECTED. Первый код означает отсутствие ACCEPTED review, а не отсутствие выполненного review. Allowed source Authorities DISCOVERY/PRODUCT-REQUIREMENTS, accepted_prerequisites содержат настоящую identity checker.problem. Decision Exploration/Governance/Execution Assurance — NOT_REQUIRED по pinned contract. Lifecycle assertion для requirements не возвращён. Аргумент acceptance_id — заранее вычисленный id реальной неуспешной попытки, не принятая identity; не выдаётся за successful acceptance.

Созданы настоящие unresolved Core Questions:

- **Q-PR-001 → PRODUCT-REQUIREMENTS:** минимальный принимаемый product slice: поддерживаемые потоки/contexts, какие сведения являются входом и обязательным результатом, продуктовая граница relevant placements и подходящих правил. Нужен observable contract, не алгоритм или UI.
- **Q-PR-002 → PRODUCT-REQUIREMENTS:** как оператор различает надёжные, неизвестные, неполные/устаревшие свидетельства и какой результат допустим при их недостатке в этом slice. Не придумывать freshness thresholds или universal verdict.

Они блокируют только checker.requirements через blocks_capabilities; blocks для Discovery пуст. Q-REC-002 уточнён этими вопросами, не закрыт. Q-REC-001 по-прежнему закрыт PDEC-003, повторное делегирование не требуется.

`prepare_reconciliation_publication` проверил terminal outcomes checker.problem CURRENT / checker.requirements BLOCKED. Штатный `publish_project_publication` выполнил atomic CAS от принятой ревизии к `sha256:b252cfbe6ef33d213aa0c6919a463fa31e891075a1ba0e7d191a8ae2ad010fb8`. Это revision **публикации блокировки**, не успешной приёмки requirements. Read-back равен подготовленному snapshot. Existing artifacts, accepted evaluations, lifecycle и failure components сохранены; изменён только Core Question state. Rejected admission evidence не помещён в accepted publication как оценка несуществующего provider. Это штатный BLOCKED outcome по делегированию, не обход условия CURRENT.

Lifecycle checker.problem CURRENT, acceptance_id `task-004-checker-problem-aa7cd410ffb83daf218e` неизменён; checker.requirements не имеет lifecycle provider и в raw lifecycle_states возвращает UNKNOWN (coverage unavailable). Его оперативный статус BLOCKED устанавливают реальные Core blockers и Roadmap, не выдуманная lifecycle row BLOCKED.

Пересчитаны Roadmap (BLOCKED / CORE_QUESTION), Semantic Closure (BLOCKED), Coverage (completion_ready false, 15 concerns/16 work items, subject_inventory QUESTION теперь допустим с существующим Core Question), Frontier. Frontier агрегирует READY Coverage actions одновременно с blocked checker.requirements: READY не отменяет Product Questions и не разрешает Domain/Architecture work. Authority assessment PRODUCT-REQUIREMENTS UNRESOLVED с evidence Questions; DISCOVERY REQUIRED сохранён; остальные 21 UNASSESSED. Новых NOT_APPLICABLE нет.

## Воспроизведение и проверки

Из корня: `PYTHONDONTWRITEBYTECODE=1 python3 experiments/runs/harness-requirements-v1/produce.py`. Скрипт содержит точные API inputs/вызовы, сохраняет real validation/router command exit/stdout/stderr, admission, source assertions, candidate и компактные read models в evidence.json. publication-before.yaml — immutable baseline для воспроизведения: при replay равный финальный snapshot не перезаписывается. Replay проверяет тот же результат без повторной публикации или новых acceptance identities.

Исправлена техническая ошибка первого вызова: canonical_references был списком строк; pinned validate_extracted_references требует mappings с referenced_path. Получен AttributeError 'str' object has no attribute 'get'; исправлен только producer adapter, затем strict admission реально завершился REJECTED по содержательной причине. Harness не менялся. При добавлении evidence before_roadmap также исправлен лишний keyword в вызове compose_project_frontier (TypeError); после исправления replay полностью прошёл, принятую публикацию ошибка не меняла. Initial read-only команды не заявляются отдельным полным transcript.

`verification.json` фиксирует replay, make check и diff check, неизменность accepted Discovery components и отклонение ложного CURRENT без provider. Независимый product oracle не создан и не переписан. Domain Design, Architecture, CoderMind/codegen и устройства не выполнялись; metadata inference model/tokens/cost недоступны (null).

**Следующее действие:** владелец продукта отвечает на Q-PR-001/002 либо подтверждает узкий первый slice и поведение при недостаточных данных. Затем в рамках уже предоставленных полномочий — доработка тех же REQ IDs, повторный CREATE/review/admission и coherent publication с настоящими Core Question resolution identities. Checker.problem не пересоздавать; полный subject inventory не объявлять до принятия атомов scope.
