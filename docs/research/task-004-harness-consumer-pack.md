# TASK-004 — штатный Harness Consumer Pack: внедрение и probe

Статус: **PREPARED / OPERATOR EXECUTION NOT_YET_REPORTED**.

После успешного пробного разрешения восьми маршрутов из *полного исходного checkout* Harness, нужен отдельный тест **дистрибутива Consumer Pack**. Это официальный способ установки агентных процедур в целевой проект: [source contract](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/harness-consumer-pack-v1.md), [wrapper contract](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/harness-consumer-wrapper-v1.md).

## Реализация

- `.harness/harness-binding.json` — строго `consumer_api=v1`, источник `lehater/harness`, полный SHA `442db854c3a736a5e500b4a41664b80981b0d94c`. Это **tooling binding**, не Core, не принятая Checker семантика.
- `.harness/harnessw.py` — **без изменений скопирован** из `lehater/harness/distribution/harnessw.py` того же SHA (Git blob `991b923093017874fffd5c70e3bdd39203daaead`). Нормативный wrapper, а не самописный Harness loader.
- `make harness-pack-preflight` — явно запущенный оператором bootstrap `sync`, штатный `validate-pack`, девять публичных Consumer/Artifact route проверок и отрицательная проверка отсутствия Maintainer routes. Route `instruction_contracts` должны реально существовать в pack.
- Логи — в `~/.cache/agentic-checker-lab/runs/harness-consumer-pack.XXXXXX`; pack — в `~/.cache/harness/v1/<SHA>/` по умолчанию.

Первый вызов wrapper может **подключиться к GitHub, скачать конкретный SHA и установить PyYAML==6.0.3** в собственную cache venv (если его там нет); требуется проверенное оператором разрешение на такой запуск. Следующие вызовы переиспользуют валидированный cached pack. Этот процесс **не** вызывает LLM, не запускает продуктовый код, не принимает требования, не меняет Git `main` или `Harness` source checkout.

## Ubuntu

```sh
git switch main
git pull --ff-only
git fetch origin
git switch --track origin/tooling/task-004-consumer-pack
make check
make harness-pack-preflight
```

Ожидание: `CONSUMER_PACK_PREFLIGHT_PASS_ONLY` с `maintainer_route_unavailable=true`, `agent_workflow_executed=false` и pin. Следующий отдельный этап — agent-driven `project-bootstrap-reconcile`, Profile/Graph/Engineering Coverage и создание **кандидата** `problem-evidence` из [источников](task-004-harness-source-intake.md).

## Граница свидетельства

CLI `validate-pack` подтверждает целостность дистрибутива; route probe — корректность процедурного входа. Ни то, ни другое не подтверждает семантическую приёмку, полный жизненный цикл Harness, полноту Consumer, работоспособность CoderMind bridge или правильность будущего Checker. Не повышать статус без следующего живого agent run.
