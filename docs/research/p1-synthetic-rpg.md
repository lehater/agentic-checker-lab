# P1: first forward RPG from synthetic requirements

Status: **INITIAL RPG EXPORTED TO OPERATOR WORKING TREE — operator-reported on Ubuntu, 2026-10-16; structural and semantic review PENDING.**

This stage deliberately verifies **requirements → feature specification → feature tree → skeleton → initial RPG**, not the existing-code RPG encoder, full Phase 2 or Checker code generation.

Source of truth for this probe: [synthetic requirements](../../tooling/fixtures/rpg-synthetic/requirements.md), which are *not* accepted Checker requirements. CoderMind reference: [forward pipeline and commands](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/docs/commands.md).

## Phase 1 — зафиксированный результат (16 октября 2026)

Оператор выполнил `make cmind-rpg-phase1` и `make cmind-rpg-status` на Ubuntu. **Источник — предоставленный терминальный вывод; сырые JSON пока доступны только в локальном хранилище оператора.**

- `feature_spec.py`: успешно получил вход из `docs/` (один документ), провёл проверку `FeatureSpecOutput`, создал `feature_spec.json`. В отчёте: `word-count-lab`, 3 top-level features, 2 background items, 4 NFR items.
- `feature_construct.py`: проверил и пропустил уже актуальную спецификацию; успешно завершил `feature_build` (58.6 с) и `feature_refactor` (36.7 с). Суммарная вторая команда 95.3 с.
- `status`: `initialized=true`, `feature_spec=true`, `feature_build=true`, `feature_tree=true`, `skeleton=false`, `rpg=false`.
- Файлы CoderMind: `~/.cmind/workspaces/home-alex-cache-agentic-checker-lab-runs-rpg-synthetic-v1-workspace/data/`.
- Локальные логи runner: `~/.cache/agentic-checker-lab/runs/rpg-synthetic-v1/`.

**Проверено:** успешное выполнение первого прохода CoderMind через Codex и наличие выходных файлов. **Не проверено на этой стадии:** содержательная точность декомпозиции, покрытие `R-SYN-01..06`, отсутствие посторонних требований, экспорт и репозиторная фиксация. **Обновление ниже:** файлы RPG/skeleton позже появились по статусу оператора.

### Просмотр результатов перед построением RPG

Выполнить локально:

```bash
DATA="$HOME/.cmind/workspaces/home-alex-cache-agentic-checker-lab-runs-rpg-synthetic-v1-workspace/data"
python3 -m json.tool "$DATA/feature_tree.json" | less
```

При проверке искать смысловые функции чтения UTF-8 файла, ASCII-only распознавания слов, нормализации регистра, детерминированного JSON, ошибок ввода. Не считать просто три верхнеуровневые группы доказательством покрытия.

## Initial RPG — факт наличия файлов (16 октября 2026)

Оператор передал вывод `make cmind-rpg-status` после этапа skeleton: `initialized=true`, все пять `files` равны `true`, в том числе `skeleton` и `rpg`. Это подтверждает **наличие файлов по операторскому статусу**, но не их валидность, число узлов, происхождение содержимого, полноту требований или успешность выполнения `check_skeleton.py`: сам журнал skeleton пока не предъявлен. Не помечать `RPG_STRUCTURAL_PASS` до экспорта и независимой проверки.

Следующие ворота: экспорт пяти JSON, SHA256 manifest и чтение графа из Git; только затем семантический аудит против [R-SYN-01..06](../../tooling/fixtures/rpg-synthetic/requirements.md). Ранний `status=false` для skeleton/rpg в блоке Phase 1 — исторический, не текущий.

## 2026-10-16 — Export succeeded, Make audit wrapper defect

Оператор выполнил `make cmind-rpg-export` и получил `EXPORTED_FOR_REVIEW`. Все пять JSON и `manifest.json` скопированы в локальную рабочую директорию `experiments/runs/rpg-synthetic-v1/`; артефакты **ещё не отправлены в GitHub**, их семантика не оценивалась.

Первый запуск `make cmind-rpg-audit > /tmp/rpg-synthetic-audit.json` перенаправил **stdout команды GNU Make вместе с JSON**. Последующее чтение `json.load` завершилось `JSONDecodeError`. Это ошибка отсутствующего `@` перед командой в Makefile, а не результат проверки RPG. Рецепт исправлен так, чтобы вывод содержал исключительно JSON; добавлен регрессионный тест Make target на синтетическом минимальном графе.

**Повторять экспорт или генерацию RPG не требуется.** После обновления ветки:

```bash
make cmind-rpg-audit > /tmp/rpg-synthetic-audit.json
python3 -m json.tool /tmp/rpg-synthetic-audit.json | head -60
```

Пока результат аудита не показан, `STRUCTURE_PASS` остаётся **NOT_VERIFIED**.

## Staged commands

Run from branch `tooling/task-003-synthetic-rpg`:

```bash
make check
make cmind-rpg-init
make cmind-rpg-status
```

The init stage uses the already installed **pinned PR #96** candidate, creates a synthetic workspace outside the repository (`~/.cache/agentic-checker-lab/runs/rpg-synthetic-v1/workspace`), copies the test specification and **does not call a model**. It does not initialize Git, MCP or any RPG.

After inspecting readiness, run **only when ready to consume real Codex model usage** (multiple calls, no guaranteed spending limit):

```bash
make cmind-rpg-phase1
make cmind-rpg-status
```

This runs `feature_spec.py --docs <synthetic-docs>` and the feature construction orchestrator with a limited review/refactor iteration budget. Inspect the actual produced feature tree; **do not assume quality or complete semantics because the script exited zero**.

Only after inspecting Phase 1:

```bash
make cmind-rpg-skeleton
make cmind-rpg-status
```

This runs `build_skeleton.py --max-iterations 2` and `check_skeleton.py`; the former should create `rpg.json`. Test verifies JSON parses and CoderMind's skeleton checker succeeds, **not** that architecture/coverage is correct. Scripts preserve logs/stdout/stderr in the synthetic run directory and use CoderMind's authoritative `~/.cmind/workspaces/<workspace-id>/data` storage. Any failed stage stops; no uncontrolled retry/force.

To prepare graph artifacts for repository evidence (modifies only the current task branch working tree):

```bash
make cmind-rpg-export
```

The explicit export creates `experiments/runs/rpg-synthetic-v1` with five JSON files and a SHA256 manifest; it **does not commit or push**. Выполнять только в ветке `tooling/task-003-synthetic-rpg`. Review generated content, privacy and scope before committing the result in this task branch. For reproducibility, keep the PR #96 source SHA, original requirements checksum, and export hashes. После экспорта выполнить `python3 tools/audit_synthetic_rpg.py experiments/runs/rpg-synthetic-v1 > /tmp/rpg-synthetic-audit.json` и проверить `status` в JSON. Скрипт читает nested `root`, уникальность ID и endpoint-и non-containment `edges`; он **не может** определить семантическое покрытие требований. The developer must separately assess generated nodes, relationships, required behavior and unforeseen extra features; a parseable graph is not a verified graph.

**Security:** no sandbox bypass allowed; scripts run only on an isolated test workspace; no real network device data, no Checker implementation, no Git hooks. Model calls are made *only* when the phase1/skeleton targets are explicitly launched. The user-installed global Codex configuration is not overridden.

**Completion criterion:** operator-reported working forward RPG, structural validation, saved artifacts for review, and explicit caveats. Full interfaces/tasks/code generation belongs to a later, separately gated phase.
