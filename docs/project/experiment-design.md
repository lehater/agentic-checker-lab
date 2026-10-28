# Experiment design — spec-first Agentic SDLC

**PROPOSED / NOT YET RUN.** Freeze inputs and numerical targets before executing comparisons.

## Hypotheses

H1: A deterministic architecture gate rejects invalid RPG plans before expensive codegen.
H2: CoderMind has measurable marginal value over direct Codex given the *same* accepted specification and tool/model budget.
H3: Telemetry-guided changes (context size, reviews, retry limits, routing) reduce quality-adjusted time/cost relative to unchanged baseline.

## Arms

- **A — Direct:** specification, accepted architecture and oracle; Codex implements without CoderMind.
- **B — RPG:** identical inputs and oracle; CoderMind plans/generates using the same available models.
- **C — Optimized (later):** same B pipeline with exactly one declared process adjustment per comparison.
- **D — Adaptive routing (later):** same constraints, route local/cloud by observed completion latency, reliability and subscription budget.

No Harness active arm. Preserve old A/B/C/D Harness protocol as historical research rather than falsely treating it as the new experiment.

## Validity

- Freeze requirements, architecture, fixtures and hidden independent oracle before any code generation.
- Capture git SHA, model+CLI versions/config, runtime environment, exact task scope, prompts/config hashes, wall-clock, per-stage attempts and verified tokens (else UNKNOWN).
- Equal wall-clock ceilings and comparable quotas; record blocked runs without hidden retries.
- Same architecture gate for A and B **after codegen**; for B additionally gate RPG skeleton/interfaces **before codegen**.
- Analyze both initial implementation and a bounded change request; separate pre-code design quality from codegen quality.
- Assess correctness (critical oracles), dependency violations, unnecessary entities, manual intervention, elapsed time and model usage.
- Repeat and report all runs where feasible; no cherry-picked success, no changed oracle to fit implementation.

## Optimization objective

Minimize time-to-verified-result and expected rework subject to hard correctness/architecture gates and actual subscription budget. More local-model calls are not automatically better; use no LLM for deterministic parsing where possible.

## Existing evidence

[PR #27](https://github.com/lehater/agentic-checker-lab/pull/27) is a non-blinded historical run: first RPG plan 1039.6s; repeated plan 1118.8s; native codegen ~46 minutes; model cost counters unverified. It is a **diagnostic benchmark**, not a controlled direct-vs-RPG result.
