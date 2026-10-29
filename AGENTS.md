# Agentic Checker Lab — agent entrypoint

The accepted main branch is the source of truth. Read [docs/README.md](docs/README.md), [current state](docs/project/current-state.yaml), [strategy](docs/project/strategy.md), and [roadmap](docs/project/roadmap.md) before work.

**LOCAL EXECUTOR START HERE:** [Local executor handoff](docs/project/local-executor-handoff.md). Start with **L1** and GitHub [issue #32](https://github.com/lehater/agentic-checker-lab/issues/32); follow L2-L5 in order. The **owner's synthetic L1 scope/semantics approval** is recorded in [Draft PR #51](https://github.com/lehater/agentic-checker-lab/pull/51), but its candidate OpenSpec is **not accepted in main**, and no independent oracle is frozen. Do not conflate these gates. Do not run model-driven implementation, spend subscription quota, or claim live verification before recording the required owner decisions and bounded experiment.

Current direction: **OpenSpec-style specification-first engineering + direct Codex baseline versus optional Microsoft CoderMind/RPG**, independently evaluated. Harness is NOT part of the active workflow. Historical Harness/RPG runs remain evidence, not active instructions.

**DESIGN STACK RESEARCH / NEW CHAT:** [canonical design-stack plan](docs/project/agentic-sdlc-design-stack-plan.md) — recover from GitHub and perform DS-01 source audit first. This is parallel preparatory research, not authorization to skip L1/oracle gates or run models.

Read [Engineering Policy](docs/engineering/policy.md) before design or code changes: Clean Architecture, SOLID, KISS, YAGNI. A structurally valid RPG or passing generated tests is never sufficient proof of architectural or behavioral correctness.

One small task/branch/PR, explicit change scope, independent checks and evidence. No live firewall access or secrets. Model-driven commands and consumption of subscription quota require an explicit bounded experiment; CI must remain model-free.

**DISCOVERY v0.1:** [Guide](docs/discovery/README.md) for ambiguous owner-visible changes; avoid repeat questions. No automatic L1/spec/oracle approval.
