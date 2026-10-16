# Agent entrypoint — documentation map

Persistent truth lives in the linked repository documents, not in this file.

1. [Documentation index](docs/README.md)
2. [Purpose and strategy](docs/project/strategy.md)
3. [Current verified state](docs/project/current-state.yaml)
4. [Roadmap and next tasks](docs/project/roadmap.md)
5. [Repository governance](docs/project/governance.md)
6. [Checker scenario](docs/scenario/README.md)
7. [Harness–RPG integration](docs/integration/README.md)
8. [Evaluation protocol](docs/evaluation/README.md)

[Research and sources](docs/research/README.md) · [Decisions](docs/decisions/README.md)

## Harness Consumer API v1 (tooling only)

Before agent-operated Harness work, run `python3 .harness/harnessw.py sync` to materialize the pinned Consumer Pack at the revision in `.harness/harness-binding.json`. Invoke Consumer operations through `harness.application.skill_router` **from that pack**, read returned `instruction_contracts` then the selected SKILL.md; do not route target tasks through Harness Maintainer skills. This step does not accept project semantics; [intake](docs/research/task-004-harness-source-intake.md) is source evidence only. See [Consumer Pack pilot](docs/research/task-004-harness-consumer-pack.md).
