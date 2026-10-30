# Agent harness platform candidates for full Agentic SDLC — 2026-10-30

**Status:** RESEARCH / FUTURE CANDIDATES — **NOT ADOPTED**, **NOT BENCHMARKED**. This is a watchlist and evaluation plan, not a new active workflow, architectural decision, product requirement, or authorization for installation/model calls. `main` strategy, the existing S0–S7 roadmap and design D0–D6 gates retain authority.

## Why keep this research

Our objective is a reproducible **end-to-end Agentic SDLC**, not just the Discovery interview: problem/discovery → owner-approved spec → domain/architecture/design → independent review → tasks → implementation → verification → optimization/change. An agent harness may support several stages, but it **does not replace** product authority, GitHub provenance, OpenSpec, independent reviews or held-out acceptance. We should remember strong upstream ideas and investigate them only when there is a demonstrable gap.

In particular, distinguish two prospective uses of “multi-user”:
1. **Multi-stakeholder Discovery:** different subject-matter experts, business owners and reviewers answer, disagree and approve within an attributable scope. This is a possible future capability of the **SDLC workflow**, not part of Checker L1.
2. **Multi-user operation of a resulting service:** identities, isolation, permissions, concurrent work and audit in the **delivered product**. Whether a product needs these is itself an owner-controlled requirement, **not** inferred from a harness choice. Do not conflate platform user roles with Checker domain ACL rules.

## Primary sources inspected (2026-10-30)

| Candidate | Source, snapshot | Relevant capability | Plausible SDLC stage | Disposition |
| --- | --- | --- | --- | --- |
| **Prime Agent** (Prime Intellect) | [Repository at 9cf0d47](https://github.com/PrimeIntellect-ai/prime-agent/tree/9cf0d47e2f1775379af9b105ef1f9d5e9f7dd25d), [README](https://github.com/PrimeIntellect-ai/prime-agent/blob/9cf0d47e2f1775379af9b105ef1f9d5e9f7dd25d/README.md), [author announcement](https://www.primeintellect.ai/blog/prime-agent) | Recursive Language Model (context as programmatic data), persistent REPL/subagents, long-running sessions, versioned continual harness and `/refine` | Design/review orchestration, coding runs, stage telemetry and **bounded** process improvement (D4/D6, S4–S7) | **RESEARCH LATER**, no automatic self-modification of normative requirements or accepted process |
| **OpenJarvis** (Stanford ecosystem) | [Repository at c452da8](https://github.com/open-jarvis/OpenJarvis/tree/c452da822de0d0f37ed963c5aef823b1cc7fcb69), [skills guide](https://github.com/open-jarvis/OpenJarvis/blob/c452da822de0d0f37ed963c5aef823b1cc7fcb69/docs/user-guide/skills.md), [project](https://github.com/open-jarvis/OpenJarvis) | Local/model engine abstraction, skill discovery, trace-based skill optimization, controlled skill benchmarks and non-destructive overlays | Model/skill optimization and local/cloud comparisons (S5–S6); deployment exploration in **AI Lab** only on consumer demand | **HIGHEST RESEARCH RELEVANCE** to measured improvement; do not assume claimed benchmark transfer |
| **QM** (YC Software) | [Repository at 2e5a12f](https://github.com/yc-software/qm/tree/2e5a12f3ff0e313771669f04b0370fd2fcc7c8ee), [README](https://github.com/yc-software/qm/blob/2e5a12f3ff0e313771669f04b0370fd2fcc7c8ee/README.md), [docs](https://qm.ycombinator.com/) | Per-person/per-room scoped and durable agent workspaces, shared context with controlled access, Slack/web surfaces, background tasks | Multi-stakeholder Discovery/approval; later collaborative engineering and operating workflows | **RESEARCH LATER** for multi-party needs; not necessary for single-owner Checker interview |

These are upstream **capability claims / source observations**, not completed installations or measured benefits in this lab. APIs, backend support, subscription terms, privacy posture and license obligations must be checked at the exact version before a future trial. In particular, QM documentation/backend support can change between releases; do not assume standalone Codex/OpenCode harness compatibility from a README. Prime Agent's effective license/redistribution terms require confirmation before reuse.

## Where each idea might add value — and what it does not solve

| SDLC concern | Existing authority / approach | Candidate hypothesis, not a decision |
| --- | --- | --- |
| Discovery and semantic authority | Evidence-Gated Discovery v0.1, owner-approved Q/D evidence, GitHub checkpoints; separate spec gate | QM may help collect **attributed, permission-scoped** input from multiple stakeholders. Must handle conflicting answers, authority precedence and explicit approval; shared memory is **not** approval. |
| Requirements and design | OpenSpec `spec-driven`, D1/D2 minimum design stack, independent D4 review | Prime Agent may support longer research/review tasks, but its editable harness must never rewrite owner decisions or declare its own review independent. |
| Implementation/verification | Direct Codex baseline, optional RPG, architecture CI, hidden oracle, fixed budgets | Prime Agent may be a **later experimental arm**, not a drop-in replacement for the already planned controlled comparison. |
| Improvement/model choice | Recorded real time/tokens/quality and safe fallback; S5/S6 | OpenJarvis's `jarvis optimize skills` and `jarvis bench skills` are worth a small isolated pilot with frozen quality tests and measured wall-clock/quota; not an unbounded self-improvement loop. |
| Collaboration / eventual delivered product | Currently no adopted multi-user Checker service requirement | QM provides architectural references for workspace scopes, audit, roles, separation and isolation. Product multi-tenancy is a **separate owner discovery** if a future product needs it. |

**Non-negotiable invariants for any later adoption:** GitHub accepted artifacts remain the durable source of truth; no automatic promotion of chat summaries/memory to owner-approved semantics; no model-generated test as independent oracle; no exposure of held-out oracle to executors; no unsupervised modification of canonical prompts or gates; no credentials or private stakeholder transcripts in a public repo; one bounded experiment/PR at a time.

## Small, staged investigation backlog (not scheduled implementation)

- **R-H01 — Multi-stakeholder requirements workflow (QM reference):** when a real second decision-maker appears, compare current GitHub Q/D/approval workflow against QM's scoped users/rooms. Test attribution, conflicting opinions, authority rules, access isolation, revocation, durable checkpoints and recovery after chat change. Produce a minimal role-and-approval contract **before** choosing a UI or service.
- **R-H02 — Skill improvement and local/cloud model efficiency (OpenJarvis):** after frozen acceptance and authentic baseline traces exist, pin an OpenJarvis revision; test no-skills vs original vs optimized skills on the **same unseen tasks**, with observed time, cost/quota, quality and failure cases. AI Lab may later own installation; Checker Lab owns method/evidence.
- **R-H03 — Long-running orchestration and bounded self-refinement (Prime Agent):** only after baseline D4–D6, compare one recoverable long task against the existing runner in isolation. Audit tool permissions, mutable harness surfaces, logs, rollback and independent verification. Reject if no measured incremental benefit.
- **R-H04 — Multi-user delivered-service design (product discovery):** independently ask future product owners whether accounts, isolation, collaboration and audit are needed. If accepted, capture requirements, architecture and tests via normal SDLC. QM is a reference, **not** a product-spec substitute.

**Entry gate:** a real use case, baseline, explicit experiment budget, upstream revision/license/security review and agreed success measures. **Exit:** decision record `ADOPT | ADAPT | REJECT | DEFER` with actual evidence and references. Absence of evidence means `DEFER`, not `ADOPT`.

## Immediate action / non-action

Keep current [Discovery v0.1](../discovery/README.md), [S3D design plan](../project/design-stage-plan.md), [D2 stack](../project/design-stack.md), owner L1 and independent D4/D5 gates unchanged. **Do not install any of the three frameworks, alter active roadmap sequencing, change `current-state.yaml`, merge Checker spec or start model experiments on the strength of this note.**
