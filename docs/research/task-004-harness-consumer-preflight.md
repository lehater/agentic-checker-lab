# TASK-004 — Consumer route preflight before real Harness design

Статус: **OPERATOR-REPORTED ROUTING_PREFLIGHT_PASS_ONLY на Ubuntu, 2026-10-16**. Из-за обнаруженной в P1 неполноты наша следующая проверка предназначена только для *официального routing surface* Harness на уже закреплённом checkout, **не** для принятия требований.

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

## Фактический запуск на Ubuntu — 2026-10-16

Оператор передал терминальный вывод после `make check; make harness-consumer-preflight` из ветки `research/task-004-harness-intake-preflight`:

- `Repository check PASS: 29 Markdown files checked`;
- три operation routes: `project-bootstrap-reconcile`, `design-profile`, `decision-pipeline`;
- пять artifact routes: `problem-evidence`, `product-requirements`, `verification-strategy`, `test-design`, `implementation-design`;
- `status: ROUTING_PREFLIGHT_PASS_ONLY`, `harness_sha: 442db854c3a736a5e500b4a41664b80981b0d94c`;
- `checker_problem_accepted=false`, `harness_workflow_executed=false`, `consumer_closure_verified=false`, `model_calls=0`;
- локальный каталог свидетельств: `/home/alex/.cache/agentic-checker-lab/runs/harness-consumer-routing.VC4o2g`.

Данные JSON отчёта в локальном каталоге нами напрямую **не прочитаны**, сведения выше — операторский вывод. Сообщённый PASS означает наличие и целостность путей восьми skills на закреплённом Harness SHA; **не** подтверждает качество skills, agent artifact lifecycle, project bootstrap, semantic acceptance, discovery Checker или implementation authorization. Следующая стадия должна быть отдельным task с реальным agent-operated `project-bootstrap-reconcile`.
