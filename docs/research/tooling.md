# Harness и RPG: технологический план исследований

Статус: **PLANNED, NOT INSTALLED**. Целевые пины: [tooling/versions.yaml](../../tooling/versions.yaml).

## Harness

Смысл: источник инженерной топологии, Authority ownership, Capabilities, Questions, provider/consumer closure, impact и engineering execution context. Документ:
https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/integration-contract-v0.md

NAPMS закрепляет прежний Harness SHA d85bbf9, примерно на 107 коммитов старше выбранной текущей точки 442db85. Не копировать его прежнюю интеграцию автоматически. Исследовать прямую декларацию либо adapter projection; не менять Harness Core ради конкретного Checker.

## RPG / Microsoft CoderMind

Официально https://github.com/microsoft/RPG-ZeroRepo/blob/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885/CoderMind/README.md . Нужны Ubuntu/Linux, Git, uv, Python 3.12+, **аутентифицированный Claude Code или GitHub Copilot CLI** по опубликованному списку проверенных agent interfaces. Совместимость с OpenAI Codex CLI требует отдельного исследования, она не подтверждена самим наличием MCP.

Пример закреплённой установки для эксперимента:

    uv tool install cmind-cli --from "git+https://github.com/microsoft/RPG-ZeroRepo.git@a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885#subdirectory=CoderMind"
    cmind check

До использования cmind init и encode изучить help установленной версии. Не кодировать пустой documentation scaffold как будто это уже Checker. Фактическое местоположение RPG/workspace и метод экспортирования снимков установить проверкой; локальные скрытые файлы не являются долговременной историей.

## P1 проверки

1. Clean Ubuntu checkout, Python/uv и выбранный поддерживаемый CLI.
2. Harness из закреплённого checkout: engineering graph validate, evaluate, Graph Doctor на маленьком consumer.
3. CoderMind: cmind check, графовый smoke в отдельной временной директории.
4. Экспорт и восстановление графового состояния, связь со SHA источника и SHA генерации.
5. Совместимость агента с RPG tool interface; блокировка попытки самовольного semantic rewrite.
6. Документировать установку, версии, output logs и решение go/no-go на toolchain.

Режим исполнения TOOLCHAIN_NOT_RUN до фактической проверки.
