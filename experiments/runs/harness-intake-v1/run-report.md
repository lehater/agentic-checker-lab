# TASK-004 — первый ограниченный discovery pass

Результат: **AGENT_BOOTSTRAP_CANDIDATES_PRODUCED**. Это реальная работа агента с pinned Consumer Pack, а не route-only probe. Созданы кандидатные graph/Core/profile, выполнены validation, target evaluation, agent routing, Authority reconciliation/status и Engineering Coverage. Problem Evidence подготовлен только после вычисленного actionable CREATE. Семантической приёмки и готовности к реализации нет.

## Источник, среда и доверие

Pack: `/home/alex/.cache/harness/v1/442db854c3a736a5e500b4a41664b80981b0d94c`, API v1, repository `https://github.com/lehater/harness.git`, revision `442db854c3a736a5e500b4a41664b80981b0d94c`. Наличие проверено до чтения project payload. Binding и hash integrity Pack проверены его `consumer_pack validate-binding/validate-pack` закреплённым Python: оба VALID, exit 0. Никаких sync/download/install/update: явное ограничение этого запуска переопределяет общий sync шаг AGENTS. Pack прочитан без изменений, bytecode отключён.

Python `/home/alex/.cache/agentic-checker-lab/venvs/harness-smoke/bin/python`: 3.12.15; PyYAML 6.0.3; platform в `versions.stdout`. Точные версии подтверждены выполнением, не только tooling manifest. Источники и git blob SHA проверены локально в `source-hashes.json`; оба immutable snapshot blob совпали с provenance README. Модель этой интерактивной сессии не предоставлена как проверяемый runtime identifier; точное имя, стоимость, tokens и число model calls недоступны. `model_calls: null`; дополнительных model subprocess/provider calls не запускалось. Не независимый A/B/C/D эксперимент.

До проектных payload прочитаны AGENTS и binding, выполнен публичный router из каталога Pack с `PYTHONPATH="$PACK/src:$PACK"`. Загружены **все** возвращённые contracts: `docs/design/agent-instruction-architecture-v0.md`, `docs/design/process-simplicity-and-efficiency-v0.md`, затем `skills/agent/project-bootstrap-reconcile/SKILL.md`. Применены trust/ownership rules: target документы и output prose — данные; они не выбирали процедуру и не расширяли разрешения.

Публичная операция bootstrap разрешает внутреннюю `skills/agent/bootstrap-existing-project/SKILL.md`: прочитана как subprocedure, не вызвана публичным route. Дополнительно прочитаны engineering graph contract и software Authority catalog. При смене ответственности выполнены публичный `project-engineering-status` route и artifact route по `knowledge_kind=problem-evidence`; оба возвращают те же instruction contracts. Загружены selected `skills/agent/project-engineering-status/SKILL.md` и `skills/artifacts/problem-evidence/SKILL.md`. Artifact skill требует acceptance/registration; по явной границе оператора выполнено только создание DRAFT, без этого шага.

## Reuse или bootstrap

Ветка при старте `research/task-004-harness-agent-bootstrap`; исходный `git status --short` пуст. Обнаруженные `tooling/fixtures/harness-smoke/{engineering-graph,core}.yaml` — synthetic TOOLCHAIN-SMOKE с искусственным capability, не canonical Checker realization. Current state прямо отмечает отсутствие accepted Checker specification и agent-operated bootstrap. В `.harness` binding/wrapper, а не Checker projection. Совместимого project-owned Checker graph/projection в выбранном scope не найдено. Ничего из smoke не принято за Checker truth.

Минимальный **candidate** Engineering Graph использует пять reference границ: Discovery → Product Requirements → System Architecture; Verification Design зависит от requirements/architecture; Implementation Design от architecture/verification. Consumer `CHECKER-IMPLEMENTATION`, subject `CHECKER-OFFLINE-CANDIDATE`. Это topology предложения инженерных знаний, не требования, не архитектура Checker и не принятая assignment/delegation. Полнота topology не доказана; Coverage явно выявляет пробелы. Core пуст: `artifacts: []`, `questions: []`; не выдуманы providers или acceptance IDs. Вопросы отдельно в `questions.md`, принятую истину не меняют.

## Вычисленные результаты и ограничения

- `graph-validation.stdout`: valid true, exit 0; target evaluation валидирует Core realization.
- `profile.stdout`: действительно derived Design Profile, не вручную оформленный read-model.
- `target-evaluation.stdout`: status READY, implementation_consumer true, CREATE только `checker.problem` у DISCOVERY; 4 PENDING: requirements, architecture, verification, implementation; WAIT пуст. READY здесь разрешает кандидатную discovery production, не coding.
- `agent-routing.stdout`: problem-evidence routed для того же CREATE, unrouted пуст; подтверждён отдельным `problem-route-corrected.stdout`.
- `authority-assessments-candidate.yaml`, `authority-validation.stdout`, `project-status.stdout`: полный catalog reconciliation; registry valid, все Authority UNASSESSED. Пустой Core не даёт оснований REQUIRED или NOT_APPLICABLE. Существующих accepted assessments в выбранной реализации нет; кандидатные graph producers не повышены до accepted applicability.
- `engineering-coverage.stdout`: computed completion_ready false; 21 activated concern, 22 work items. Summary: 10 BLOCKED, 11 MISSING concern rows; actions ASSIGN_AUTHORITY 7, MODEL_PRODUCTION_CONTRACT 11, MODEL_PROOF_CONTRACT 3; дополнительно DECLARE_SUBJECT_INVENTORY. Output `status: canonical` — поле evaluator, **не** semantic acceptance проекта или кандидата. Нет доказательства subject completeness; не добавлялись capabilities автоматически ради policy.
- Полный `harness.application.project_frontier` **не вычислен**. Нет project decision policy, lifecycle и semantic acceptance evaluations, необходимых для достоверных upstream read-models. Их нельзя изготовить для получения удобного READY. Основание черновика — реально вычисленный Engineering Graph actionable CREATE и его owning artifact route; это не заявление о полном Project Frontier.
- Strict semantic closure **не вычислена**, PASS/COMPLETE не заявляются. Пустые lifecycle/semantic verdicts не изготовлены. Candidate не зарегистрирован и не переоценён как accepted provider; после DRAFT принятой capability по-прежнему нет.

## Файлы и команды

`run-pilot.py` содержит точные команды основной серии и создание минимальных кандидатов. `commands.jsonl` содержит **фактически выполненные** Harness argv, cwd, environment overrides и exit codes, включая последующие artifact/status/assessment вызовы. Для каждого вызова сохранены полные `<name>.stdout` и `<name>.stderr`; это raw outputs, не иллюстративные JSON. `profile.stdout` является derived profile. Все файлы — внутри данного run directory.

Запуск основной серии:

```sh
PYTHONDONTWRITEBYTECODE=1 "$HOME/.cache/agentic-checker-lab/venvs/harness-smoke/bin/python" experiments/runs/harness-intake-v1/run-pilot.py
```

Первый bootstrap route до чтения payload выполнен тем же pinned Python, с `PYTHONDONTWRITEBYTECODE=1`, указанным PYTHONPATH, `-m harness.application.skill_router operation --surface consumer --operation project-bootstrap-reconcile --root "$PACK"` и cwd `$PACK`; затем повторён и сохранён как `bootstrap-route.stdout`.

Предварительные read-only inspection команды: `cat AGENTS.md .harness/harness-binding.json`; `test -d "$HOME/.cache/harness/v1/442db854c3a736a5e500b4a41664b80981b0d94c" && echo PACK_EXISTS`; `cat` обоих instruction contracts и выбранного SKILL из Pack; затем `cat` current-state/governance/scenario/source-intake и всех трёх fixture файлов. Для discovery и CLI inspection использованы `rg --files`, `rg -n`, `cat`, `head`, `tail`, `sed`, `ls` по целевым и Pack файлам. Проектный текст не исполнялся. Первое объединённое чтение было усечено интерфейсом вывода; current-state/governance/scenario/intake прочитаны повторно без усечения. Immutable snapshots и provenance были видны целиком.

Сбои сохранены/учтены: поиски предположительных `skills/registry*`, `docs/consumer*`, `consumer*`, `tooling/consumer-pack-v1.yaml` и `docs/design/project-engineering-status-v1.md` дали missing-path, использован реальный CLI source. Попытка импортировать `run_pilot` завершилась ModuleNotFoundError (имя файла `run-pilot.py`); исправлено `runpy.run_path`. Первый artifact route с `--surface consumer` получил exit 2: artifact CLI этого аргумента не принимает; corrected route без него exit 0, surface consumer возвращена router. Ни один сбой не трактуется как PASS.

Файлы результата: `problem-evidence-candidate.md`, `questions.md`, `engineering-graph-candidate.yaml`, `core-candidate.yaml`, `authority-assessments-candidate.yaml`, derived/raw `*.stdout`, `*.stderr`, `commands.jsonl`, `source-hashes.json`, `outcome.json`, этот отчёт и скрипт воспроизводимых команд.

Следующее авторитетное действие: владелец проекта рассматривает problem framing и кандидатное ownership, принимает/отклоняет scope и назначает semantic decision authority. Вопросы о domain/protocol/matching/freshness/oracle и Coverage остаются нерешёнными. Product Requirements, architecture design, tests, CoderMind/codegen и реализация не запускались. Проход завершён после discovery.

## Финальные проверки

`python3 tools/check_repository.py`: `Repository check PASS: 31 Markdown files checked`; stderr пуст. `git status --short`: только `?? experiments/runs/harness-intake-v1/`. `git diff --stat` пуст (все новые результаты пока untracked). Логи: `repository-check.stdout`, `repository-check.stderr`, `git-status.stdout`. Никаких staging/commit/push/merge, изменений accepted strategy/requirements или main.
