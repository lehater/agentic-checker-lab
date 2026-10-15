# Tooling и Ubuntu

Планируемые, но **не установленныe в лаборатории** ревизии: [versions.yaml](versions.yaml).

P1 — последовательность:
1. Чистая Ubuntu, Python 3.12+, Git, uv, authenticated supported coding agent CLI.
2. Закреплённый Harness checkout, commands Engineering Graph validate/evaluate/Graph Doctor на тестовом consumer.
3. CoderMind на пине, проверить cmind check и графовый smoke без кодирования docs scaffold.
4. Определить фактический layout RPG, backup/export и привязку к Git SHA.
5. Исследовать ограничения CLI: Claude Code/GitHub Copilot проверены авторами; OpenAI Codex совместимость не предполагается автоматически.
6. Зафиксировать **реальные** команды, версии, output/logs, несовместимости и решение о дальнейшем использовании.

Пример **ещё не выполненной** установки:

    uv tool install cmind-cli --from "git+https://github.com/microsoft/RPG-ZeroRepo.git@a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885#subdirectory=CoderMind"
    cmind check

Не копировать Harness или весь Microsoft RPG в дерево приложения. Не превращать временный CoderMind workspace в незарегистрированное место хранения итоговых графов.
