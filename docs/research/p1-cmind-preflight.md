# TASK-003 — CoderMind installation and scratch preflight

Status: **PREFLIGHT PASS — operator-reported Ubuntu run, 2026-10-16**. Full RPG/codegen, Codex authorization and integration are still NOT_VERIFIED.

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

## Фактический результат P1/TASK-003 (2026-10-16)

**Evidence type: operator-reported terminal output**, run after `git switch --track origin/tooling/task-003-cmind-preflight`. Это не вывод собственного исполнения ассистентом на удалённой Ubuntu: оригинальные stdout/stderr файлы и `summary.json` существуют только у оператора.

```text
CPython 3.12.15
Repository check PASS: 22 Markdown files checked
Running: install
Running: provenance
Running: version
Running: scripts
Running: init
status: PREFLIGHT_PASS_AGENT_NOT_VERIFIED
source_sha: a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885
scratch_config: true
agent_auth: NOT_TESTED
rpg_generation: NOT_TESTED
checker_implemented: false
claude: absent
copilot: absent
codex: present (authentication unknown)
```

Evidence location: `~/.cache/agentic-checker-lab/runs/cmind-preflight.BeK5yl/`, machine-local, not committed. The script validated the wheel provenance via `direct_url.json`, performed commands and scratch initialization, then emitted `PREFLIGHT_PASS_AGENT_NOT_VERIFIED`. An additional successful consecutive preflight run was **not** reported; detailed raw files and `cmind check` contents not inspected here.

The repository check passed but Python warned about the Markdown-link regular expression; the warning was an unrelated code-quality issue, fixed within this PR. The warning does not invalidate preflight.

### Decision for next experiment

The active environment has only a `codex` executable according to PATH checks. CoderMind's pinned CLI docs mark Claude Code and Copilot as verified assistants, while the [configuration documentation](https://github.com/microsoft/RPG-ZeroRepo/blob/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885/CoderMind/docs/configuration.md) mentions the `codex exec` command without claiming an end-to-end verification. Pinned [LLM client](https://github.com/microsoft/RPG-ZeroRepo/blob/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885/CoderMind/scripts/common/llm_client.py) includes a codex detector and subprocess command path.

Thus **Codex integration is feasible to investigate, but not VERIFIED**. Do not make `codex` the canonical agent or assume authorization on PATH presence alone. The next bounded task is a separate Codex compatibility and graph-serialization spike on a synthetic workspace.
