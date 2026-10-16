# TASK-004 — checker.requirements CURRENT

**Результат: CURRENT для первого slice PDEC-CHECKER-004.** База: main `e2690dc`; ветка `design/task-004-requirements-current`. При старте рабочее дерево чистое, пользовательских незакоммиченных изменений не было. Прежние candidate/review/admission evidence PR #18 сохранены неизменными, Discovery, делегирование и исторические исследования не повторялись.

## Принятый результат

Канонический managed artifact — `.harness/knowledge/checker-requirements.yaml`, product-requirements/v1. Сохранены исходные ID **REQ-CHECKER-001..007**, statements и provenance; уточнены acceptance criteria по принятому PDEC-004. Новые атомы **008..028** добавлены только для независимых обязательств нового решения: адреса/протоколы/порты, provided contexts/snapshots, принадлежность context, происхождение/date/completeness, unknown metadata, допустимость partial и видимые ограничения/неустановленные факты, complete no-match vs missing/unknown, обоснованный stale/отсутствие TTL/unknown date, независимая проверяемость matching.

Кандидат продолжен с тем же artifact id CHECKER-REQUIREMENTS; managed canonical path применяется впервые, поскольку прежний кандидат не был Core provider. Исходные statements 001..007 сравниваются автоматически. Non-goals исключают live devices, ICMP, IPv6, route discovery и NAT только из первой версии; будущие расширения не запрещены. Product не выбирает ACL syntax/algorithm, CLI/API, architecture, data model или runtime. Не вводится новый universal Permit/Deny.

[Содержательный review](review.md) отображает каждый принятый statement PDEC-004 на требования/явный non-goal/downstream disposition. Все пять checks PASS: source-discipline, authority-boundary, no-invention, observable-product-level, no-downstream-design-promotion. Это реальный agent review по PDEC-003, не независимая человеческая подпись. Acceptance clauses не являются выполненными runtime tests; independent matching examples/точная семантика остаются обязанностью последующей конкретизации до реализации. Это прямо предусмотрено новым owner decision и не требует повторного Product Question в текущем first-slice scope.

## Контракты и переход

Закреплённый Harness Consumer Pack: `442db854c3a736a5e500b4a41664b80981b0d94c`. Sync/validate-pack и typed public bootstrap/status + artifact product-requirements routes выполнены; returned instruction contracts загружены перед skills. Workspace validate-artifact: **valid true**. Полномочия PDEC-003 повторно не запрашивались; Engineering Graph не менялся.

Исходная publication содержит unresolved Q-PR-001/002. Core caller/integration отвечает за семантическую действительность identities; `Core.resolve_question` требует same-owner provider и разные acceptance/superseded identities, поддерживает ABSENT при отсутствии прежнего принятия. Для strict admission подготовлен **неопубликованный** согласованный snapshot:

1. Предложен CHECKER-REQUIREMENTS CanonicalArtifact с depends_on CHECKER-PROBLEM-EVIDENCE.
2. Для каждой существующей Question вызван штатный resolve_question с anticipated identity этой реальной попытки и supersedes_acceptance_id **ABSENT**. В прошлом не было принятого requirements provider; REJECTED attempt из PR #18 не является superseded acceptance.
3. Записи Questions сохранены целиком (включая blocks_capabilities и answer_from); добавлена только resolution. Никакие blockers не удалены, answer_from не подделан. Сам факт принятия owner PDEC не присвоен как acceptance identity.
4. В этом staged контексте вызван настоящий `admit_artifact`: prerequisite checker.problem проверен CURRENT по актуальной policy, strict canonical источники принадлежат реальному DISCOVERY provider. Новые Product decisions — original PRODUCT-REQUIREMENTS assertions по PDEC-004 с source_refs; PDEC-004 не превращён в фиктивный canonical prerequisite.
5. Admission **ACCEPTED**, findings пусты, возвращён настоящий lifecycle_assertion и accepted_prerequisites с прежней checker.problem identity. Decision Exploration/Governance/Execution Assurance реально NOT_REQUIRED по pinned product-requirements contract.
6. Только после успеха подготовлен prepare_reconciliation_publication с terminal outcomes CURRENT для обеих Capabilities. Semantic Evaluation, lifecycle, Core provider и resolution identities совпадают. Atomic CAS publish выполнен от исходной BLOCKED publication; read-back равен полностью подготовленному snapshot.

До ACCEPTED admission исходная публикация сохраняла свои bytes, включая blockers. Staged Core не является второй канонической публикацией. Если admission/terminal validation отвергает подготовку, projected resolution не становится опубликованной истиной. Такой цикл не снимает Questions произвольной ручной записью.

**Acceptance ID:** `task-004-requirements-3219d4ef86d53466a04bb4e9`.

**Publication:** `sha256:94bc167d0108b5b4b90dcea6cefd0af3f5ba5132091f0ee20756163127da9852`.

**Parent:** `sha256:b252cfbe6ef33d213aa0c6919a463fa31e891075a1ba0e7d191a8ae2ad010fb8`.

Q-PR-001 и Q-PR-002 обе разрешены через CHECKER-REQUIREMENTS и эту acceptance identity; provenance принятого artifact явно ведёт к соответствующим разделам PDEC-004. Неразрешённых Product Questions в опубликованном Core нет. `checker.problem` остаётся CURRENT; его accepted evaluation, lifecycle row и identity `task-004-checker-problem-aa7cd410ffb83daf218e` неизменны.

## Пересчитанные read models и границы

Из одной прочитанной опубликованной ревизии:

- Decision Roadmap: COMPLETE для CHECKER-REQUIREMENTS-ADMISSION, обе Capabilities CURRENT, ready/blocked/failed пусты.
- Semantic Closure: COMPLETE в этой же технической closure, semantic/currentness gaps пусты.
- Coverage: completion_ready false, 15 concerns / 16 work items. Subject inventory явно REQUIRED, DEFINE_SUBJECT_OBLIGATIONS. Наличие 28 принятых product atoms ещё не является принятым subject-obligation routing contract.
- Frontier: READY для Coverage actions, без нового ready Capability pipeline. Work-item candidate roles/claims не принимаются автоматически. Эти concerns не превращаются в новые обязательные подсистемы.

Applicability registry: PRODUCT-REQUIREMENTS переведён UNRESOLVED → REQUIRED на основании реального canonical provider; DISCOVERY REQUIRED сохранён; прочие 21 UNASSESSED сохранены, NOT_APPLICABLE не введён. Registry validated. Q-REC-002 сохраняется открытым для subject inventory/полноты, несмотря на принятый bounded first-slice intent.

Это **не** полнота всего будущего Checker, не готовность реализации и не приёмка Domain/Architecture/Verification. Следующее допустимое действие — классифицировать принятые first-slice атомы в subject-obligation inventory и согласовать действительно необходимый downstream knowledge/ownership, включая точную supported matching semantics и независимые examples. Новые Authorities или Capabilities в этом исполнении не назначены.

## Воспроизведение

Из корня: `PYTHONDONTWRITEBYTECODE=1 python3 experiments/runs/harness-requirements-current-v1/execute.py`.

Скрипт читает canonical artifact и immutable publication-before.yaml, сохраняет exact subprocess argv/cwd/exit/output, pinned instruction/source hashes и компактные read models в evidence.json. Точные API inputs присутствуют в скрипте и admission-candidate/staged-core. Identity связывает actual artifact (включая критерии/non-goals), review и owner decision hashes. Replay заново выполняет admission/проверки и принимает существующую равную публикацию без перезаписи, новой ревизии или новых identities. Зависимости: Python/PyYAML и закреплённый Consumer Pack через wrapper.

verification.json содержит фактические результаты replay, make check, diff check, проверки совпадения Question/admission/lifecycle identities, отрицательных stale CAS/mixed identity/illegal Core resolutions. Metadata inference model/tokens/cost недоступны (null), новых model subprocess calls нет. Ранние read-only инспекции сессии не выдаются за отдельный полный transcript. Значимых технических ошибок исполнения не возникло.

Существующая integration boundary ADR-0002/0003 не менялась: новые архитектурные решения не принимались. Domain Design, implementation, CoderMind, кодогенерация, network/device operations и изменения Harness не выполнялись. Merge не выполняется.
