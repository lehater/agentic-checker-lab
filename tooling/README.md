# Tooling и Ubuntu

Закреплённые версии и состояние реальных Ubuntu проверок: [versions.yaml](versions.yaml). Установка Harness и CoderMind подтверждена терминальным выводом оператора; это не подтверждает RPG/codegen.

P1 — последовательность:
1. Чистая Ubuntu, Python 3.12+, Git, uv, authenticated supported coding agent CLI.
2. Закреплённый Harness checkout, commands Engineering Graph validate/evaluate/Graph Doctor на тестовом consumer.
3. CoderMind на пине, проверить cmind check и графовый smoke без кодирования docs scaffold.
4. Определить фактический layout RPG, backup/export и привязку к Git SHA.
5. Исследовать ограничения CLI: Claude Code/GitHub Copilot проверены авторами; OpenAI Codex совместимость не предполагается автоматически.
6. Зафиксировать **реальные** команды, версии, output/logs, несовместимости и решение о дальнейшем использовании.

Пример ручной установки закреплённой версии (TASK-003 использовал изолированное окружение, а не эту глобальную команду):

    uv tool install cmind-cli --from "git+https://github.com/microsoft/RPG-ZeroRepo.git@a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885#subdirectory=CoderMind"
    cmind check

Не копировать Harness или весь Microsoft RPG в дерево приложения. Не превращать временный CoderMind workspace в незарегистрированное место хранения итоговых графов.


[Результат CoderMind preflight](../docs/research/p1-cmind-preflight.md): установленный Codex CLI найден, но авторизация и выполнение pipeline не проверены. Следующее исследование — проверить `codex exec` и CoderMind LLMClient на отдельном scratch workspace, без изменения корня лаборатории.

## Кандидат Codex из Microsoft PR #96

Подготовлена отдельная [проверка кандидата](../docs/research/p1-codex-pr96.md): `make cmind-codex-smoke` в ветке `tooling/task-003-codex-pr96-spike`. Использует SHA `3303a222...` из поля `rpg_codex_pr96_candidate`, не заменяя уже проверенную версию CoderMind `a4e6966...` и не меняя приложение. Проверяет Codex CLI и запуск адаптера **без реального обращения к модели**.
