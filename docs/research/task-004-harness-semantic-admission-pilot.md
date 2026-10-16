# TASK-004B — semantic admission of confirmed Checker problem intent

Статус: **PREPARED / LIVE AGENT NOT RUN**. Предпосылка: [PDEC-CHECKER-001](../scenario/problem-framing-decision.md) принята владельцем как **problem framing**; [первый Harness Discovery pilot](task-004-harness-agent-review.md) проверен `PASS WITH LIMITATIONS`. Ни `checker.problem` CURRENT, ни Project Publication, ни полный Checker requirements пока не приняты.

## Цель

Проверить **реальную** границу Harness: от подтверждённой проблемы и кандидатного Problem Evidence к проектной strict semantic admission. Установить, допускают ли существующие свидетельства подтверждённую регистрацию либо требуются отдельное Authority/acceptance решение и/или пересмотр кандидатной топологии. Не подменять принятие пользовательской проблемы автоматическим `ACCEPTED` от валидатора.

Pinned Harness: `442db854c3a736a5e500b4a41664b80981b0d94c`, Consumer Pack v1. Контракты: `skills/artifacts/problem-evidence/SKILL.md`, `src/harness/application/semantic_admission.py`, `docs/design/project-publication-v0.md`, `docs/design/project-frontier-v0.md`.

## Ubuntu — отдельный bounded agent run

```bash
git switch main
git pull --ff-only
git fetch origin
git switch --track origin/research/task-004-harness-semantic-admission
make check

codex exec --sandbox workspace-write -C "$PWD" \
  - < tooling/prompts/task-004-harness-semantic-admission.md

git status --short
cat experiments/runs/harness-discovery-admission-v1/outcome.json
```

Запуск использует модель Codex и её квоту. Prompt запрещает изменять canonical project truth, использовать другие tool sources, автоматически публиковать Harness state или разрешать незакрытые user questions. Временные артефакты только `experiments/runs/harness-discovery-admission-v1/`. Отрицательный результат (нет Authority, нет артефактного `acceptance_id`, нет source authority) является **обязательным честным результатом**, а не причиной выдумать свидетельство.

После запуска просмотреть raw logs и `git diff`, убедиться в отсутствии секретов, добавить/зафиксировать **только** новую run directory в исследовательскую ветку; после публикации выполнить независимый audit по реальным stdout/JSON и принятым источникам.

## Условие продолжения

- Если strict admission невалидна: сохранить blocker и адресовать **конкретный** вопрос владельцу/Authority, не запускать Product Requirements.
- Если валидна в scratch: проверить semantic review, provider/lifecycle acceptance identity и Project Publication CAS; не считать `CURRENT` до отдельного reviewer/PR по проектному owner.
- Инструментальный `status: READY` и `owner_problem_framing_confirmed: true` не заменяют статус `semantic_evaluation.ACCEPTED`.

Этот run — **инженерный испытательный прогон Harness**. Он не участвует в E1/E2 независимом сравнении и не меняет стратегию из PR #7.
