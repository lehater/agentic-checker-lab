# Implementation Design — реализованный синтетический Checker

Основания: REQ-CHECKER-101..104, DOM-1/2, ARCH-1, IF-1, COMP-1, POL-1,
TD-BEHAVIOR и TD-BOUNDARIES. Варианты сформированы и проверены до этого candidate:
[exploration](../../experiments/runs/checker-v1/implementation-options.yaml).

Выбор инженерного агента в рамках поручения владельца: один небольшой вертикальный
slice с независимым oracle до кода; Python package `checker`, внешний composition
root `checker.__main__`, отдельные domain/application/input adapter функции;
runtime standard library, без сетевых зависимостей. `unittest` для независимой
приёмки; CoderMind может использовать pytest как dev tool, не runtime dependency.

RPG/CoderMind получает только принятые Harness contracts и frozen expected cases
через bridge manifest. Порядок: feature construct → plan (все 5 стадий) → проверка
RPG на semantic drift → code generation по штатным scripts → перенос проверенного
source в task branch → независимая CLI и dependency проверка. Tool-generated tests
не заменяют oracle. Обновлять accepted requirements/ожидания из-за output запрещено.
Private helper names/representations остаются свободой генерации в рамках COMP-1.

Снимки — input fixtures, не миграция базы. Нет совместимости с историческим Checker
или production rollout. Откат — обычный revert task change; deployment/merge не
выполняется этим планом. Ручное тестирование полезно дополнительно, но не заменяет
версионированный `make check` в PR CI. Отдельный benchmark не нужен: нет SLA.

Обязательные completion evidence: независимые CLI сценарии и error cases PASS,
source substitution/no mutation и deterministic import boundary checks PASS,
Harness test-realization conformance ACCEPTED для каждой OP/OR obligation,
полный актуальный Harness closure и coverage, действительные RPG artifacts и
checksums, provenance до source/tests. Результаты перечислены ниже; CURRENT устанавливается только фактической Harness admission/publication.

Validation execution review: только быстрые детерминированные suites на synthetic
входе, один общий trigger PR/push main, без selective execution или model calls в CI.
`make check` — воспроизводимый authoritative gate; локально та же команда.
Model-driven tool work — отдельные явные запуски, результаты экспортируются, а не
повторяются недетерминированно на каждом PR. Структурные правила проверяются AST,
schema/semantic tooling — pinned Harness при явном запуске с отдельным evidence.
Runtime dependency inventory: Python stdlib only; CoderMind/Harness остаются dev
инструментами с pin. Увеличение dependency footprint требует пересмотра решения.

## Фактическое размещение и границы

Публичный launcher — `checker/__main__.py`; он делегирует внешнему
`src/acl_checker/cli/main.py`. В `src/acl_checker/domain/` находятся типы и чистый
matcher, в `domain/application/check.py` — use case; `application/` содержит
узкие источники и ошибки, `input/` — чтение и строгую валидацию, `cli/rendering.py`
— представление. Название каталога не задаёт зависимости: transitive AST-проверка
от функций `matches` и `check` механически запрещает обращение ядра к CLI,
адаптерам, файловым и сетевым модулям. Пакеты импортируются из checkout без установки.
Это выбранный package-вариант с root launcher; внутреннее имя `src.acl_checker`
— свобода реализации, а не требование installed src-layout или новый API.

Независимые проверки находятся в `tests/test_checker_*.py`; frozen JSON — точная
проекция принятого `docs/checker/scenarios.yaml`. CoderMind tests экспортируются
отдельно как воспроизводимое development evidence и не подменяют independent oracle.
Все поддерживаемые runtime-файлы используют только Python stdlib; Python 3.10+
и UTF-8 JSON достаточны для checkout. Пины Harness/CoderMind — в binding/tooling;
их установка не нужна для пользовательского запуска и быстрого CI.

## Gate и повторная проверка

Авторитетный gate предлагаемого изменения — GitHub job `repository / check` на PR
в main; локальный `make check` исполняет тот же набор: документационная целостность,
публичные/структурные unittest, шесть контролируемых семантических мутаций во временных
копиях и проверка хешей completion evidence. Все suites выполняются без выборочного
пропуска; длительность порядка нескольких секунд не оправдывает отдельный scheduler,
кэширование результатов или второй dependency graph. Нативные model-driven проверки
запускаются явно перед приёмкой; CI проверяет их привязку к source/tests, не повторяет
LLM-вызовы. Это SUPPORTED execution review по фактическому времени запусков.

Публикация — source-only ветка/PR; deployment, пакетный релиз и миграция отсутствуют.
В main допускается только squash после зелёного gate и review согласно governance;
автоматически merge не выполняется. Серверное enforcement branch protection требует
отдельной настройки владельцем и не следует из текста политики. Откат — revert
интегрированного squash; данные и snapshots на диске не изменяются.

При upstream-изменении нужно пересчитать Harness currentness/affected outputs,
пересмотреть RPG и source mapping, повторить `make check`, Test Design conformance
и explicit native review для изменённого кандидата, обновить хеши доказательств
и повторно допустить затронутые capabilities. Старые зелёные статусы не переносятся
на новый source только по совпадению имён файлов. Это правило повторной проверки,
а не утверждение, что change-impact эксперимент P5 уже проведён.

## Ограниченное исправление dev-инструмента

Базовый native global review ошибочно требует screenshots для CLI и завершился
FAIL после 10 итераций с успешными функциональными checks/post-pytest. Этот FAIL
сохраняется как `native-global-review-upstream.json`. По [ADR-0004](../decisions/0004-cmind-cli-review.md)
применяется изолированный hash-checked patch к двум файлам dev-инструмента:
явная CLI-область исключает только неприменимую visual-проверку. Default visual,
падение pytest, stubs и unresolved features остаются блокирующими; восемь
regression probes это подтверждают. Настоящий global review повторяется через
штатный runner из изолированной копии; его результат отделён от upstream FAIL.
Критерии Checker и независимый oracle не ослабляются. Базовый установленный
пакет не меняется; итог не заявляется как успех неизменённого upstream.


## Completion evidence (2026-10-20)

- Native generation: 30/30 задач; `native-codegen-status.json` и неизменяемый
  source commit в `native-provenance.json`.
- Base final-test: 197 PASS, smoke imports/entrypoint/stubs PASS;
  `native-final-test.json`. Exported native suite повторён в отдельном временном
  workspace против кода репозитория: 197 PASS (2 предупреждения runpy в тестах).
- Base global review FAIL из-за визуального guard; реальный CLI-review с patch
  PASS, 5/5 functional groups, post-pytest PASS, stubs 0:
  `native-global-review-upstream.json`, `native-global-review.json` и ADR-0004.
- Независимые pre-code scenarios и boundary suite PASS:
  `TD-BEHAVIOR-execution.json`, `TD-BOUNDARIES-execution.json`.
- Official Test Design conformance ACCEPTED для обоих контрактов; полностью
  покрыты OP/OR. Отрицательные probes отвергают missing operation и failed execution.
- Baseline + все 6 semantic mutants: PASS/DETECTED; оригинальные source неизменны.
- `traceability.json` — SOURCE_BOUND с действительными function symbols и hashes,
  все четыре REQ связаны с RPG, source и независимыми test contracts.
- Bridge hashes неизменны, изменённый вход не может повторно использовать identity.

Записи находятся в `experiments/runs/checker-v1/`; механический gate связывает
их с текущими файлами через `completion.json`. Соответствие executable assertions
проверено инженерным агентом; внешняя независимая/слепая аттестация не заявлена.
Финальная Harness closure/currentness проверяется `verify.py`; PR CI остаётся
отдельной проверкой предлагаемой интеграционной ревизии, не утверждением о merge.
