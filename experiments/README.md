# Experiments and historical evidence

Репозиторий `main` сохраняет [первый синтетический RPG](runs/rpg-synthetic-v1/manifest.json) и его [независимый аудит](../docs/research/p1-synthetic-rpg-review.md). Отдельный, значительно более полный Checker run и код находятся в **открытом, не слитом [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27)**. Ни один из них не доказывает преимущества RPG над direct Codex.

Следующие прогоны следуют [новому протоколу сравнения](../docs/project/experiment-design.md), с фиксированными входами, версиями/коммитами, architecture gate, independent oracles, sanitized logs, временем, токенами при фактическом учёте (иначе UNKNOWN) и вмешательствами. Все результаты сохраняются, включая отрицательные; не загружать credentials, приватные данные устройств и сырые сессии без проверки.

Harness-ориентированные исследования и старые идентификаторы режимов — **исторические**, не текущие обязательные зависимости.
