# Git, PR и работа агентов

Статус: **ACCEPTED** — политика лаборатории, но не доказательство применения серверных GitHub Rulesets.

## Git contract

1. main — каноническая интеграционная ветка; её содержимое отражает текущую принятую истину.
2. Одноразовое исключение: **первоначальная подготовка пустого репозитория прямо в main разрешена владельцем**. После bootstrap прямой push запрещён.
3. На каждую задачу — отдельная ветка от актуального main: research/, design/, tooling/, feat/, fix/, eval/.
4. На каждую завершённую задачу — Pull Request, описание цели, scope, входных источников, результатов, проверок и нерешённых рисков.
5. **Только squash-and-merge**; один смысловой коммит в main на PR. Удалять ветку после merge. Force-push и переписывание main запрещены.
6. Нет merge при красном CI, незакрытом блокирующем вопросе или самовольном изменении принятой предметной семантики.
7. Для больших работ могут быть промежуточные PR с цельными проверяемыми результатами; не требовать одного гигантского PR на целую фазу.

## Рекомендуемые GitHub настройки — действие владельца

- Settings → General → Pull Requests: Allow squash merging **ON**, Allow merge commits **OFF**, Allow rebase merging **OFF**. Можно включить Automatically delete head branches.
- Settings → Rules → Rulesets (или Branch protection) для main: Require a pull request before merging; Required status checks после появления первого успешного job **repository / check**; Block force pushes; Block branch deletions; Require linear history; по возможности Disable bypass.
- Настройка обязательного review — по решению владельца. Review важен для семантической истины, но автоматические тесты не заменяют такое решение.

**Текст правил не защищает main физически.** Нужна отдельная настройка GitHub. Официальная документация: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets .

## Принятая истина и изменение

- Источником текущих знаний служит Git, а не история чатов. При возобновлении работы из нового чата агент читает AGENTS.md → docs index → current-state → документы текущей задачи.
- Все существенные изменения требований/архитектуры требуют ссылки на evidence, мотивированного решения и анализа affected outputs.
- Отдельное мнение агента или генерация RPG не превращает предложение в ACCEPTED.
- Запрещено скрыто подгонять независимые acceptance tests под сгенерированный код.
- Для экспериментов фиксируются SHA исходников/инструментов, входные данные, run logs с удалёнными секретами, стоимость и результаты.
- Не переписывать Product, SSSR, NAPMS или Harness ради этого эксперимента без отдельной явной задачи.
- Без явного разрешения — никакого настоящего опроса устройств, изменения firewall config, приватной инвентаризации и секретов.

## Минимальный PR контракт

Goal/TASK, affected canonical authorities/artifacts, sources, changes, unresolved questions, actually executed verification with outputs, impact on acceptance oracle, status update if necessary. Pull request template: [PR template](../../.github/pull_request_template.md).

## OpenAI практики

Короткий AGENTS.md как навигатор; документация репозитория — system of record; контекст подбирается по задаче; запросы оформляются как конкретные Issue/PR с входом и критерием результата. Источники:
- https://openai.com/index/harness-engineering/
- https://openai.com/business/guides-and-resources/how-openai-uses-codex/
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

Практика должна оставаться адаптируемой к новым инструментам и моделям; не делать из agent prompt огромную энциклопедию.
