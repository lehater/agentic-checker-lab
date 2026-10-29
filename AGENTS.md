# Agentic Checker Lab — agent entrypoint

The accepted main branch is the source of truth. Read [docs/README.md](docs/README.md), [current state](docs/project/current-state.yaml), [strategy](docs/project/strategy.md), and [roadmap](docs/project/roadmap.md) before work.

**LOCAL EXECUTOR START HERE:** [Local executor handoff](docs/project/local-executor-handoff.md). Start with **L1** and GitHub [issue #32](https://github.com/lehater/agentic-checker-lab/issues/32); follow L2-L5 in order. The OpenSpec Checker scope and acceptance oracle are NOT approved yet. Do not run model-driven implementation, spend subscription quota, or claim live verification before recording the required owner decisions and bounded experiment.

Current direction: **OpenSpec-style specification-first engineering + direct Codex baseline versus optional Microsoft CoderMind/RPG**, independently evaluated. Harness is NOT part of the active workflow. Historical Harness/RPG runs remain evidence, not active instructions.

Read [Engineering Policy](docs/engineering/policy.md) before design or code changes: Clean Architecture, SOLID, KISS, YAGNI. A structurally valid RPG or passing generated tests is never sufficient proof of architectural or behavioral correctness.

One small task/branch/PR, explicit change scope, independent checks and evidence. No live firewall access or secrets. Model-driven commands and consumption of subscription quota require an explicit bounded experiment; CI must remain model-free.

## Evidence-Gated Requirements Discovery v0.1 (experimental practice)

For a **new feature or a material change in owner-visible behavior**, follow [Discovery entrypoint](docs/discovery/README.md): **Fast batch interview → compact evidence-backed Quality Gate → Deep only for documented risk**. Apply [Authority Gate](docs/discovery/authority-gate.md) to classify every candidate issue before asking the owner. Reuse already approved decisions; do not repeat questions, invent product answers or treat engineering decisions as owner requirements.

For a refactor or an already accepted task, do **not** run a ceremonial interview. Use [the quick-start and recovery procedure](docs/discovery/usage.md) when Discovery is actually required. Keep the Q/D ledger and checkpoints in a **task branch/PR**; approve normalized answers once per batch, preserve stable decision IDs and hand off to a **separate** specification/acceptance review.

**Scope protection:** This practice does not retroactively accept the Checker ledger in experimental PR #48, does not approve Checker OpenSpec or independent oracles, and **does not lift L1–L5 or model-run budget gates**. A method PR is not product approval; keep main and code unchanged without their normal review.
