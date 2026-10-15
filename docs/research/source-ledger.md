# Источники и закреплённые версии

Статус: **EVIDENCE**. Эти источники сами по себе не являются утверждённой новой спецификацией Checker.

| Источник | Закреплённый Git SHA / материал | Назначение | Доверие |
| --- | --- | --- | --- |
| Product Django | [lehater/product at 891d751](https://github.com/lehater/product/tree/891d751d50d85a260544c43e776dc51496bdd8db) | Фактические legacy entrypoints/checker/шаблоны | Source observation, не target |
| Product discovery | [access assessment at 759fcd7](https://github.com/lehater/product/blob/759fcd7b773b12144a14f4a990cfba11bddc3527/docs/discovery/access-assessment-as-is.md) | Восстановленные зависимые Python/SQL маршруты | Research, не runtime test |
| SSSR XLAM | [SCN-006 at d1abb6f](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/docs/legacy/requirements/SCN-006-traffic-check.md) | Автором подтверждённые historic requirements REQ-034..040, RULE-018..022 | Domain historical evidence |
| NAPMS | [Strategic BC at 4248157](https://github.com/lehater/napms/blob/42481577fab7f795cf3a2118b7b6f1c3c075d066/docs/model/strategic/bounded-contexts.yaml) | Развитие идеи SSSR и поздние требования | Новый предметный scope, не готовый MVP checker |
| Harness | [Integration Contract at 442db85](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/docs/design/integration-contract-v0.md) | Закреплённый Engineering Graph/Core контракт | Pin исследуемой версии, не установлен |
| Microsoft | [RPG-ZeroRepo at a4e6966](https://github.com/microsoft/RPG-ZeroRepo/tree/a4e6966c4ff59d84299bc56d6a47ae1f4f7b2885) | CoderMind/RPG Encoder/ZeroRepo | Pin исследуемой версии, не установлен |
| OpenAI | https://openai.com/index/harness-engineering/ | AGENTS as map, repository as source of truth | Рекомендации, не продуктовые требования |
| OpenAI | https://openai.com/business/guides-and-resources/how-openai-uses-codex/ | Issue-shaped agent tasks / persistent context | Рекомендации |

Исполняемые/сравнительные claims требуют своего run-manifest. Никакого автоматического обновления version pin до более нового main без отдельного PR и совместимых тестов.
