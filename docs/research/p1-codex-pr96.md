# P1 / TASK-003-CODEX-PR96 — Microsoft CoderMind Codex candidate

Status: **RESEARCHED / candidate prepared; Ubuntu probe NOT_RUN**.

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

Реальный Codex CLI у оператора обнаружен в PATH. Его версия, авторизация и flags пока **не проверены**. Sandbox bypass в PR #96 включается только явной переменной `CMIND_CODEX_BYPASS_SANDBOX`; лаборатория запрещает её при проверках. `--approve-for-me` не тождественен полному отказу от sandbox.

## Безопасная структурная проверка на Ubuntu

```bash
git switch tooling/task-003-codex-pr96-spike
make check
make cmind-codex-smoke
```

Скрипт устанавливает **только candidate SHA** в **новое отдельное** `uv` venv под `~/.cache/agentic-checker-lab/venvs/cmind-codex-pr96`, проверяет wheel provenance; парсит CLI flags без model call; создаёт scratch workspace **вне репозитория**; проверяет создание skills/MCP config/backend и непосредственный Python-контракт CodexSessionManager, не запуская real LLM. Evidence/outputs и stderr — в отдельном per-run каталоге. Не делает `cmind init .` на Checker repo; не затрагивает main/hooks/AGENTS.md. Повторный запуск использует venv без удаления.

**Ожидаемый статус при успешной структурной проверке:** `STRUCTURAL_PASS_LIVE_AGENT_NOT_TESTED`. Не путать с подтверждённой авторизацией Codex, созданием RPG или codegen.

## Дополнительные проверки до принятия кандидата

1. Структурный smoke на Ubuntu и реальная версия `codex --version`; повторить без запроса уничтожения venv.
2. Проверка подлинной авторизации Codex и **одного** дешёвого read-only prompt в scratch workspace; полномочия и стоимость контролируются пользователем.
3. Синтетический pipeline `requirements → RPG → code` с сохранением graph snapshot и независимым тестом. Не делать в основном Checker до принятия P2 требований.
4. Негативная проверка того, что Codex/CMind не переписывают AGENTS, не запускают device mutations и не меняют семантику; отдельное review рисков PR #99.
5. Только после этого предложить обновление основного `rpg_zerorepo` pin отдельным PR и повторить существующий preflight, сохранив baseline comparison.

## Go/no-go

**USE AS CANDIDATE** прямо сейчас: да. **PROMOTE TO CANONICAL TOOLCHAIN**: пока нет (модельный и кодогенерационный E2E не подтверждены в нашей лаборатории). Если smoke провалится — записать точную причину; не переключать runtime/сбросить pin без мотивированного решения.
