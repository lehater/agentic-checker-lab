# TASK-004 — первый агентный Harness Discovery, экспериментальный запуск

Статус: **PREPARED / LIVE AGENT NOT_RUN**. Предыдущий Consumer Pack v1 preflight PASS, но `agent_workflow_executed=false`.

Эта задача **не** заменяет принятый roadmap: это безопасный ограниченный pilot после P1, выполняемый только по явному запуску оператора. Исторические файлы снабжены provenance и не являются To-Be требованиями. [Исходники](../../tooling/fixtures/checker-intake/README.md) · [инструкция агенту](../../tooling/prompts/task-004-harness-discovery.md).

## Операторский запуск на отдельной исследовательской ветке

```bash
git switch main
git pull --ff-only
git fetch origin
git switch --track origin/research/task-004-harness-agent-bootstrap
make check
git status --short

# One real Codex agent run: uses model quota; sandboxed workspace write.
codex exec --sandbox workspace-write -C "$PWD" \
  - < tooling/prompts/task-004-harness-discovery.md

git status --short
```

В этом варианте вызывается `codex exec` с реальной моделью, работающей в выбранной ветке и ограниченной workspace-write sandbox. Это **не** фоновый процесс ChatGPT и не инструмент из GitHub. У агента есть инструкции не изменять ничего за пределами `experiments/runs/harness-intake-v1/`, не делать `git push/commit/merge`, не принимать проектную истину без семантической приёмки. Sandbox — дополнительная граница, но не доказательство невозможности нежелательных изменений внутри рабочего дерева: **проверить diff перед любым commit**. При отказе доступа к Pack не переключаться в опасный режим и не отключать sandbox.

Провести один bounded run; если CLI сообщит о синтаксической несовместимости с установленной версией, посмотреть `codex exec --help` и зафиксировать blocker, не запускать `--dangerously-bypass-approvals-and-sandbox`.

## Критерии результата

- Фактический вызов модели (или честный `BLOCKED`), верный pinned Consumer Pack и использование **public** `project-bootstrap-reconcile`.
- Указаны реальные вызовы Harness и CLI outputs; не объявлять operation выполненной по одному routing result.
- Если агент создал candidate Engineering Graph/Core, отличать `CREATE` от `COMPLETE`, предъявить raw evaluation. Если не смог выполнить Coverage/Semantic Closure — зафиксировать конкретную недостающую предпосылку.
- Source-bounded `problem-evidence-candidate.md` создаётся только при оправданной CREATE. Без нормализации нетипичных ACL правил и без выдуманных product requirements.
- Candidate остаётся неaccepted до независимого анализа источников и решения пользователя об owner-owned вопросах. Отсутствие проблемного codegen не является проверкой CoderMind.

После запуска оператор может отправить `outcome.json` и `run-report.md` или после просмотра/редакции секретов закоммитить **только** `experiments/runs/harness-intake-v1/` в эту же ветку для чтения через GitHub. Не коммитить локальные session/agent traces без ревизии.
