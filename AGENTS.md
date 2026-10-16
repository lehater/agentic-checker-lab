# Checker — agent entrypoint

Start with [the owner's problem statement](docs/scenario/owner-problem-brief.md). Treat Checker as a real software engineering assignment, not a predesigned implementation.

## Harness Consumer API v1

Run `python3 .harness/harnessw.py sync` to materialize the pinned Consumer Pack at `.harness/harness-binding.json`. Route operations through `harness.application.skill_router` from that pack. Read returned `instruction_contracts` and the selected SKILL.md. Do not use Maintainer skills for project work.

Select applicable Authorities and Capabilities according to Harness rules, not from a preset list. Follow dependencies, required semantic admission and publication. Ask the owner about material domain uncertainty; do not invent ACCEPTED or CURRENT. Produce an appropriate small working vertical slice on synthetic data.

Use RPG/CoderMind for implementation planning and coding based on accepted Harness outputs; independently verify executable behavior. Do not access real firewalls.

## Navigation

- [Owner's problem](docs/scenario/owner-problem-brief.md)
- [Project state](docs/project/current-state.yaml)
- [Repository governance](docs/project/governance.md)
- [Harness–RPG interface](docs/integration/README.md)

Historical research and experimental runs are not accepted product requirements.
