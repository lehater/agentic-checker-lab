# Design stage — OpenSpec-centered Agentic SDLC plan

**Status:** WORKING PLAN (process research and design preparation only). **Date:** 2026-10-29.
**Higher authorities:** [strategy](strategy.md), [roadmap](roadmap.md), [current state](current-state.yaml), [engineering policy](../engineering/policy.md) and owner-approved product decisions. This plan does **not** approve a Checker architecture, hidden oracle or model run.
**Current Checker context:** [L1 issue #32](https://github.com/lehater/agentic-checker-lab/issues/32); [Draft PR #51](https://github.com/lehater/agentic-checker-lab/pull/51) holds the reconciled *candidate* Checker spec and a record of owner approval of the synthetic L1 scope. It is not merged into main; the independent oracle and local preflight remain pending.

## Objective and established direction

Assemble and evaluate a **minimal reproducible Agentic SDLC using existing tools**, with original additions only for evidenced gaps:

**Evidence-Gated Discovery → OpenSpec specification → domain/architecture/detailed design → independent Design Review → tasks → Direct Codex or optional RPG+Codex → independent verification → controlled change.**

- Use built-in **OpenSpec Design/Tasks** as the baseline; audit extensions before installing or writing a new framework.
- Apply **DDD, C4, ADR and contract design only as appropriate** to risk and domain complexity. Clean Architecture, SOLID, KISS and YAGNI remain project policy.
- OpenCode/Codex are possible executors. **Microsoft RPG/CoderMind is an optional implementation-comparison arm**, not an architect, product authority or required dependency. Harness is retired.
- Distinguish product meaning (owner decision), architectural engineering choices (reviewed design), structure checks (CI), and behavior evidence (independent oracle). Never replace one by another.
- This document authorizes **planning, source inspection and documentation only**. Model calls, subscription quota, Checker codegen and live device access need their separately established approvals.

## Tasks, gates and evidence

| ID | Deliverable | Evidence / exit condition | State |
| --- | --- | --- | --- |
| D0 | Persist the recoverable plan | This document linked in roadmap and current-state; docs-only PR checked and merged | **DONE** — merged PR #53 |
| D1 | Audit ready-made tools | Evidence-linked review of upstream source, skills/templates, licenses, maintenance and enforcement; ADOPT / ADAPT / REJECT | **DONE** — [PR #56](https://github.com/lehater/agentic-checker-lab/pull/56), [report](../research/openspec-design-stack.md) |
| **D2** | **Select smallest working design stack** | [Minimal workflow contract](design-stack.md), role handoffs, checklist, [paper-only dry-run](../research/design-stack-d2-dry-run.md) and rationale | **CANDIDATE SELECTED** — merged only after D2 PR review/CI; no independent reviewer claimed |
| D3 | Prepare Checker L1 domain/architecture/detailed design | Domain terms/invariants, use cases, module boundaries and dependency direction, interface/error contracts, justified C4/ADR, traceable to reconciled L1 spec | **NEXT after D2 merge**; candidate until final L1 semantics/spec acceptance |
| D4 | Independent Design Review and repair | Separate evaluator checks source trace, architecture ownership, cycles, missing evidence and unnecessary complexity; bounded correction and recorded outcome | TODO |
| D5 | Freeze implementation inputs and preflight | Approved spec/design hashes, independently authored and privately held oracle hash, real local tool versions and access recorded | BLOCKED: pending independent oracle and operator evidence |
| D6 | Controlled implementation comparison | Direct Codex baseline vs optional RPG+Codex using the same accepted design, oracle, budget and quality gates; authentic outcomes and token/time evidence | BLOCKED by D4+D5 |

**Dependencies:** D1 → D2 → D3 → D4. L1 spec review, private oracle custody and operator preflight may proceed **in parallel** with D1–D3, but no codegen before D4+D5. D3 is a *candidate* until the product spec is approved and reconciled. This plan complements existing S3→S4 roadmap and L1→L5 handoff; it does **not** supersede them.

## D1 — completed source audit (retained historical instruction)

Inspect these **candidates**, not pre-approved dependencies:

1. [Intent-Driven Template](https://github.com/intent-driven-dev/intent-driven-template) — OpenSpec schema/workflow, C4/ADR skills, independent review, dependencies.
2. [DDD Skills](https://github.com/ForceInjection/domain-driven-design-skills) — domain discovery, strategic/tactical design, quality review and DDD-to-OpenSpec bridge.
3. [Anvil / OpenSpec Schemas](https://github.com/jikkujoyce/openspec-schemas) — architectural review and test-plan workflow.
4. Baseline: **unmodified OpenSpec Design/Tasks** plus existing engineering policy and repo CI.

Inspect actual upstream revision, source templates/prompts, examples, license, maintenance, installation and compatibility, artifact contract, overlap and costs. Do not combine incompatible workflow schemas. Separate author-reported benchmarks from independent evidence.

**D1 output:** [source-linked research](../research/openspec-design-stack.md) merged through [PR #56](https://github.com/lehater/agentic-checker-lab/pull/56). No installation or model calls. **D2 selected process (candidate):** [design-stack.md](design-stack.md), with [bounded paper trace](../research/design-stack-d2-dry-run.md). D2 is accepted as a working process only after its scoped PR passes CI/review and is merged; independent design evaluation remains D4.

## Proportional design quality

- **Domain model / DDD when useful:** entities, identity, invariants, terminology; bounded contexts and aggregates only if justified.
- **Architecture / C4 when useful:** coherent module/component map, ownership, dependencies and boundaries.
- **Decisions / ADR when useful:** durable significant tradeoffs, alternatives and consequences; do not create ceremonial ADRs.
- **Contracts:** typed inputs/outputs and explicit errors; distinguish no match from unavailable evidence.
- **Independent review:** requirement-to-design coverage, layer violations, needless abstraction, missing cases and unresolved risk. A green OpenSpec/schema test is **not** a semantic review.
- **Design exit:** independent implementer could follow approved observable semantics without inventing business choices.

## Recovery from a new chat — GitHub only

1. Read [AGENTS.md](../../AGENTS.md) → [docs index](../README.md) → [current-state.yaml](current-state.yaml) → [roadmap](roadmap.md) → **this plan** → [engineering policy](../engineering/policy.md).
2. Check live GitHub **PR #51**, **issue #32** and any newer design-task PR. Main is accepted merged authority; Draft PR is proposal/evidence, never automatically main.
3. Resume the **first unfinished D-step with satisfied prerequisites**. Before creating a branch, inspect if another PR already executes it. One small branch/PR per deliverable.
4. At each pause save a GitHub checkpoint: completed actions, verified results/links/SHAs, outstanding decisions, blockers and exact next task. Update main-owned state/roadmap through PR when statuses materially change.
5. Do not infer owner approval from “continue”, assert hidden oracle availability or run codegen/model calls from this plan.

**Ready-to-paste new-chat prompt:**

> Recover the Agentic SDLC design-stage work using GitHub repo lehater/agentic-checker-lab as the ONLY source of state. Read AGENTS.md, docs/project/current-state.yaml, docs/project/roadmap.md and docs/project/design-stage-plan.md. Inspect active relevant PRs/issues and report evidence, next D-step and blockers. Then execute the next permitted small task in a scoped PR, preserving existing gates. Do not invent approval, disclose hidden acceptance, run paid models or start Checker codegen.

## Change control

Keep **one canonical roadmap**, not a competing sequence. This is the detailed execution aid for its design-stage work. Move verified tool findings into the research document and later selected engineering decisions into their appropriate authority; revise this plan only on relevant evidence. A future research result is not an approved product or architecture decision.
