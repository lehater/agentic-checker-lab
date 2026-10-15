# P1 / TASK-002 — Harness on Ubuntu: tooling spike

Status: **USER-REPORTED PASS on Ubuntu (2026-10-16)**; structural CI checks PASS. Raw JSON artifacts remain local to the operator environment.

## Зачем

До проектирования Checker проверить не бизнес-модель, а сам канал исполнения: pinned Harness Core, Engineering Graph validation/profile/evaluate, independent Graph Doctor. Синтетический fixture исключает попытку представить его как принятую Checker архитектуру.

## Входы

- Источник SHA: [tooling/versions.yaml](../../tooling/versions.yaml) — `harness`.
- Простой граф, где DISCOVERY публикует `checker-lab.smoke.problem`, VERIFICATION-DESIGN требует его и публикует `checker-lab.smoke.verification`.
- Core содержит один уже известный synthetic problem artifact; вторая capability **отсутствует преднамеренно**.
- Сценарий НЕ является implementation consumer. Нет разрешения разрабатывать Checker.

## Запуск в Ubuntu

Нужны Python 3.10+, `git`, `uv`, доступ к GitHub и PyPI. Установка производственного Checker не производится.

```bash
git clone https://github.com/lehater/agentic-checker-lab.git
cd agentic-checker-lab
bash tools/harness_smoke.sh
```

Скрипт сохраняет pinned Harness checkout, виртуальное окружение и **все диагностические JSON** в локальном `~/.cache/agentic-checker-lab` (можно изменить через `CHECKER_LAB_TOOL_CACHE`). Директория с результатами будет выведена в конце. Установка выполняется только при явном запуске. Нет коммитов, изменения других репозиториев и `cmind init`.

## Повторный запуск и предотвращённый сбой

Smoke-скрипт **повторно использует** исправное виртуальное окружение из кэша. Он не должен повторно выполнять `uv venv` для уже существующей директории и не применяет разрушающий `--clear`. При повреждённом/частично созданном окружении он сообщает точный путь и останавливается, не удаляя файлы автоматически.

**Регрессионный критерий:** запустить `make harness-smoke` дважды подряд; оба запуска должны закончиться `PASS` без интерактивного вопроса о замене virtual environment. При втором запуске должно выводиться `Reusing Harness virtual environment: ...`.

## Обнаруженный дефект smoke fixture (исправлен в этом PR)

Первоначальная `core.yaml` содержала только `artifacts` и `questions`, но не `authorities`. Операция `engineering_graph evaluate` может вывести Authorities из Engineering Graph в realised Core; `graph_doctor` проверяет исходную модель и возвращает `CORE_MODEL_INVALID` на несуществующего владельца `DISCOVERY`. Из-за перенаправления JSON в файл и `set -e` причина не показывалась в терминале. Теперь Authorities объявлены явно, каждый шаг называет себя, а ошибка сопровождается exit status, stderr, findings и путём сохранённых JSON.

Это вывод из чтения зафиксированного Harness `src/harness/project_model/core.py` и `src/harness/application/graph_doctor.py`. После исправления пользователь предоставил успешный вывод реального запуска; см. «Фактический результат» ниже.

## Фактический результат — Ubuntu, 2026-10-16

**Источник:** переданный владельцем проекта терминальный вывод после `git pull --ff-only; make harness-smoke` на ветке `tooling/task-002-harness-smoke` (SHA `c7365a27ff2135fb20d6e802886bd32110b96f1e`). Ниже не результаты CI и не вывод из неисполненного нами кода: это явно **operator-reported evidence**.

```text
Reusing Harness virtual environment: ~/.cache/agentic-checker-lab/venvs/harness-smoke
Running: Engineering Graph validation
Running: Consumer profile
Running: Core realization evaluation
Running: Graph Doctor
{
  "status": "PASS",
  "scope": "synthetic-toolchain-only",
  "harness_sha": "442db854c3a736a5e500b4a41664b80981b0d94c",
  "evaluation_status": "READY",
  "create_capabilities": ["checker-lab.smoke.verification"],
  "doctor_errors": 0,
  "source_of_truth": "tooling/versions.yaml",
  "checker_implemented": false
}
```

Локальный архив run: `~/.cache/agentic-checker-lab/runs/harness-smoke.Wjk5zq/` (не загружен в репозиторий). По выводу исполнен один успешный полный smoke-test **с повторным использованием** уже существовавшего виртуального окружения. Обязательный критический oracle этой задачи выполнен. Второй подряд успешный запуск **исправленного** скрипта и исходные JSON-файлы как отдельное доказательство пока не предоставлены. Точная версия Ubuntu/uv также не приложена; используется CPython 3.12.15 по предыдущему терминальному выводу. Не повышать эти неподтверждённые свойства до VERIFIED.

Вывод P1/TASK-002: закреплённый Harness CLI работоспособен в предъявленном проверочном сценарии, однако реальный engineering design Checker и его codegen не проверены.

## Ожидаемый oracle

- `validate.json`: `valid=true`.
- `profile.json`: список двух capabilities и dependency.
- `evaluate.json`: `READY`, `checker-lab.smoke.problem` удовлетворён, `checker-lab.smoke.verification` в CREATE.
- `doctor.json`: `summary.ERROR=0` (INFO о неполноте может существовать, это не ошибка).
- `summary.json`: `PASS` только после проверки всех перечисленных результатов.
- Полный 40-character Git SHA реально загруженного Harness совпадает с `tooling/versions.yaml`.

## Полнота сохраняемого evidence

Ubuntu version, Python/uv versions, Git SHA источника, команды, summary.json, relevant logs и факт отсутствия изменений в исходниках. `PASS` для инструмента не является `PASS` для реализации Checker. После smoke создать TASK-003 для **другого** CLI: CoderMind, Claude Code/Copilot или иной явно проверенной совместимости.

## Блокировки

Нет доступа к Ubuntu → `NOT_RUN`; нет uv/пакета/PyPI → `BLOCKED`; неподдерживаемый Harness checkout/import → `FAIL`. Не изменять pin без отдельного мотивированного PR.
