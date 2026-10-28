# Agentic Checker Lab

Experimental repository for **measuring and improving specification-driven agentic software engineering** from problem statement and accepted design to code, independent verification, and controlled change.

The project compares:
- **Baseline:** accepted specifications + Codex directly.
- **Candidate:** the same specifications + Microsoft RPG-ZeroRepo / CoderMind planning and code generation.
- **Later optimization:** tracing, controlled process improvements and adaptive model routing (Codex/local models).

[Engineering Policy](docs/engineering/policy.md) requires Clean Architecture, SOLID, KISS and YAGNI, with explicit separation of machine-checkable constraints from human/LLM design review. OpenSpec is the **selected candidate for specification/change management**, not yet an installed or E2E-verified project dependency.

**Harness is retired from the active method.** Old Harness-related files, experiments and [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27) remain historical evidence; no Harness operations are required for new work. The PR is not merged and its test results must not be presented as verified main.

Entry points: [documentation map](docs/README.md), [strategy](docs/project/strategy.md), [current state](docs/project/current-state.yaml), [roadmap](docs/project/roadmap.md), [comparison protocol](docs/project/experiment-design.md).

Static repository checks (no model calls): `make check`.
