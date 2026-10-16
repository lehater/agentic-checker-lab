# TASK-004 — Consumer route preflight before real Harness design

Статус: **PREPARED / NOT RUN ON OPERATOR UBUNTU**. Из-за обнаруженной в P1 неполноты наша следующая проверка предназначена только для *официального routing surface* Harness на уже закреплённом checkout, **не** для принятия требований.

Входной реестр источников: [checker discovery intake](task-004-harness-source-intake.md). Предложенный процесс: [audit](methodology-integration-audit-2026-10.md).

## Зачем

Наш ранний smoke проверил лишь `engineering_graph validate/profile/evaluate` и `Graph Doctor` на маленьком искусственном графе. Он не проверил skills: `project-bootstrap-reconcile`, `design-profile`, `decision-pipeline` и `problem-evidence`, `product-requirements`, `verification-strategy`, `test-design`, `implementation-design`.

Официальный закреплённый `harness.application.skill_router` (код SHA `442db854...`) реализует `operation --surface consumer --operation NAME --root CHECKOUT` и `artifact --knowledge-kind KIND --root CHECKOUT`. Скрипт проверяет, что все эти восемь маршрутов существуют и ссылаются на реальные файлы навыков.

## Ubuntu

```bash
git switch main
git pull --ff-only
git fetch origin
git switch --track origin/research/task-004-harness-intake-preflight
make check
make harness-consumer-preflight
```

Если кэш Harness `~/.cache/agentic-checker-lab/sources/harness-$SHA` или `venvs/harness-smoke` отсутствует, скрипт **останавливается** и предлагает отдельно повторить `make harness-smoke`. Он не устанавливает новые зависимости/агенты автоматически.

## Evidence / pass

`ROUTING_PREFLIGHT_PASS_ONLY`, SHA совпадает, восемь маршрутов распознаны, пути к SKILL.md принадлежат pinned checkout. Локальный JSON в отдельном `~/.cache/agentic-checker-lab/runs/harness-consumer-routing.XXXXXX`.

Скрипт **не** вызывает модель, не создаёт проектную Engineering Graph/Core, не считает требования принятыми, не пишет в git, не подтверждает semantic closure. Следующее доказательство — фактическая `project-bootstrap-reconcile` и agent-driven `Problem Evidence` с source attribution и Questions. Сначала маршрут, затем содержательная работа.
