# P1 / TASK-003-CODEX-PR96 — Microsoft CoderMind Codex candidate

Status: **STRUCTURAL PASS — user-reported Ubuntu execution on 2026-10-16; live LLM and RPG still NOT_TESTED**.

## Исследовательский вопрос

Можно ли использовать [Microsoft RPG-ZeroRepo PR #96](https://github.com/microsoft/RPG-ZeroRepo/pull/96) вместо установки Claude/Copilot, сохраняя проверенный baseline CoderMind 0.1.9 в `main` до получения доказательств?

**Закреплённые версии**: baseline `a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885` (operator preflight PASS); Codex candidate `3303a222eaec42c6a178bddd46ad63d9026ab8fa`, branch `feat/codermind-codex-support`, PR open since 2026-08-24. Candidate прописан отдельно в [tooling/versions.yaml](../../tooling/versions.yaml); не обновлять рабочий baseline преждевременно.

## Что реализовано в PR #96 (по исходникам)

- `CodexSessionManager` посылает prompt через stdin в `codex exec`, поддерживает повторную отправку и использует `--approve-for-me --ephemeral --skip-git-repo-check -`.
- `cmind init --ai codex` создаёт project-scoped `.agents/skills/cmind-*/SKILL.md` (15 skills) и `.codex/config.toml` с MCP `rpg-tools`, `cmind-mcp`.
- `cmind config show/set-agent` переключает активный backend без уничтожения остальных интеграций.
- Добавлены unit/integration tests, фиксация результатов RPG edits и дополнительные улучшения генерации/восстановления.

[Исходник менеджера](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/scripts/common/session_manager.py), [тест менеджера](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/tests/test_codex_session_manager.py), [документация CLI](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/docs/cli-reference.md).

Автор PR заявляет: 1526 прошедших CoderMind tests; 243 cmbench tests; Codex Encoder E2E PASS; Codex Decoder E2E 48/48 задач и 178 тестов PASS. Это **авторское заявление**, не повторённое нами. GitHub checks PR head: CLA success, markdownlint failure; PR пока не объединён. Другой upstream PR [#99](https://github.com/microsoft/RPG-ZeroRepo/pull/99) отдельно исправляет границы AI execution authority и hooks; нельзя считать эти изменения уже присутствующими в PR #96.

## Совместимость с нашей версией

Коммит PR основан на `f0947723`, а `main=a4e6966` отличается от него только одним коммитом markdownlint для Windows fixture README. PR #96 содержит 10 новых коммитов и изменяет 43 файла. Это **малое расхождение исходной базы**, но не гарантия готовности PR.

Реальный Codex CLI у оператора обнаружен в PATH. `codex --version` и `codex exec --approve-for-me --ephemeral --skip-git-repo-check --help` завершились успешно в структурном smoke, однако значение версии и действительная поддержка параметров при **модельном вызове** в переданном выводе не видны; авторизация не проверена. Sandbox bypass в PR #96 включается только явной переменной `CMIND_CODEX_BYPASS_SANDBOX`; лаборатория запрещает её при проверках. `--approve-for-me` не тождественен полному отказу от sandbox.

## Безопасная структурная проверка на Ubuntu

```bash
git switch tooling/task-003-codex-pr96-spike
make check
make cmind-codex-smoke
```

Скрипт устанавливает **только candidate SHA** в **новое отдельное** `uv` venv под `~/.cache/agentic-checker-lab/venvs/cmind-codex-pr96`, проверяет wheel provenance; парсит CLI flags без model call; создаёт scratch workspace **вне репозитория**; проверяет создание skills/MCP config/backend и непосредственный Python-контракт CodexSessionManager, не запуская real LLM. Evidence/outputs и stderr — в отдельном per-run каталоге. Не делает `cmind init .` на Checker repo; не затрагивает main/hooks/AGENTS.md. Повторный запуск использует venv без удаления.

**Полученный результат структурной проверки:** `STRUCTURAL_PASS_LIVE_AGENT_NOT_TESTED` по успешному завершению последовательности и проверкам скрипта. Скрипт сохраняет этот JSON в `summary.json`; предыдущая версия не печатала его в терминал. Не путать с подтверждённой авторизацией Codex, созданием RPG или codegen.

## Дополнительные проверки до принятия кандидата

1. Структурный smoke на Ubuntu и реальная версия `codex --version`; повторить без запроса уничтожения venv.
2. Проверка подлинной авторизации Codex и **одного** дешёвого read-only prompt в scratch workspace; полномочия и стоимость контролируются пользователем.
3. Синтетический pipeline `requirements → RPG → code` с сохранением graph snapshot и независимым тестом. Не делать в основном Checker до принятия P2 требований.
4. Негативная проверка того, что Codex/CMind не переписывают AGENTS, не запускают device mutations и не меняют семантику; отдельное review рисков PR #99.
5. Только после этого предложить обновление основного `rpg_zerorepo` pin отдельным PR и повторить существующий preflight, сохранив baseline comparison.

## Go/no-go

**USE AS CANDIDATE** прямо сейчас: да. **PROMOTE TO CANONICAL TOOLCHAIN**: пока нет (модельный и кодогенерационный E2E не подтверждены в нашей лаборатории). Если smoke провалится — записать точную причину; не переключать runtime/сбросить pin без мотивированного решения.

## Evidence: operator execution (2026-10-16)

Владелец проекта выполнил `make check` и `make cmind-codex-smoke` в Ubuntu, ветка `tooling/task-003-codex-pr96-spike`. `make check` выдал `Repository check PASS: 23 Markdown files checked`. Последовательно и **без ошибок** завершились:

```text
Running: install
Running: provenance
Running: codex-version
Running: codex-flags
Running: cmind-version
Running: cmind-scripts
Running: init
Running: active-backend
Running: session-path
Running: assertions
Complete. Local evidence: ~/.cache/agentic-checker-lab/runs/codex-pr96.fkqjWi
No model invocation, no generated RPG and no changes to project hooks/source.
```

**Достоверно из выполненных assertions:** совпадение source commit кандидата `3303a222eaec42c6a178bddd46ad63d9026ab8fa`; в synthetic workspace выбран `codex exec`; созданы 15 skills; MCP `rpg-tools` → `cmind-mcp`; CodexSessionManager посылает входной текст через stdin и использует ожидаемые аргументы без sandbox bypass. Raw stdout/stderr/summary.json существуют **только на машине оператора** и непосредственно нами не прочитаны. На одном запуске повторно-используемое venv ещё не проверено. Объяснение симптома «нет JSON в терминале»: `run_step assertions` записывал stdout в `assertions.stdout`, не выводя на экран; в этой же ветке исправлен вывод `summary.json` после успеха.

Это подтверждает **структурный контракт**, не реальную авторизацию CLI, стабильность `codex exec` при запросе к модели или генерацию RPG. Следующая отдельная задача должна ограниченно проверить живой LLM-контракт, затем независимый синтетический граф и security constraints.
