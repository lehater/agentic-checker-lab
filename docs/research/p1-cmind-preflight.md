# TASK-003 — CoderMind installation and scratch preflight

Status: **PREPARED / NOT RUN ON OPERATOR UBUNTU**.

Цель: проверить установку именно закреплённой версии Microsoft CoderMind, работоспособность CLI и шаблонов в изолированном Ubuntu-окружении **без генерации Checker** и без изменения Git hooks лаборатории.

Источники: [CLI](https://github.com/microsoft/RPG-ZeroRepo/blob/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885/CoderMind/docs/cli-reference.md), [layout](https://github.com/microsoft/RPG-ZeroRepo/blob/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885/CoderMind/docs/project-structure.md), [configuration](https://github.com/microsoft/RPG-ZeroRepo/blob/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885/CoderMind/docs/configuration.md), [pins](../../tooling/versions.yaml).

Запуск после открытия отдельной ветки:

```bash
git switch tooling/task-003-cmind-preflight
make check
make cmind-preflight
```

Скрипт устанавливает `cmind-cli` из Git SHA в локальное uv-окружение под `~/.cache/agentic-checker-lab/venvs/`, проверяет фактический commit по `direct_url.json`, выполняет `cmind version` и `cmind script --list`, затем создаёт одноразовый synthetic workspace в `~/.cache/agentic-checker-lab/runs/`. Параметры `--no-git --no-mcp --no-encode --ignore-agent-tools` запрещают создание Git-репозитория фикстуры, настройку MCP, построение RPG и зависимость от установленного агента. **Изменения в основной репозиторий не вносятся**.

Результат `PREFLIGHT_PASS_AGENT_NOT_VERIFIED` подтверждает только работоспособность установки/шаблонов. CoderMind официально проверен с Claude Code и GitHub Copilot CLI; Codex пока не подтверждён end-to-end. Вывод `cmind check` сохраняется, его наличие не является доказательством авторизации CLI. Для реального `requirements → RPG → code` нужен отдельный эксперимент и выбор агентного CLI. Временные версии, stdout/stderr и summary.json не следует путать с Git-артефактами.

**Критерии:** pin SHA совпадает; CLI и bundled scripts доступны; scratch config существует; главный репозиторий и Checker не изменены; повторный запуск без интерактивного удаления venv. Ошибка provenance — блокер, а не повод проигнорировать пин.