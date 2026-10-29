# D2 — minimal design-stack contract (process selection)

**Status:** ENGINEERING PROCESS CANDIDATE — selected for the bounded design experiment; not Checker design acceptance. **Date:** 2026-10-29.
**Authority:** [strategy](strategy.md), [design-stage plan](design-stage-plan.md), [engineering policy](../engineering/policy.md); evidence: [D1 source audit](../research/openspec-design-stack.md), [D2 desk dry-run](../research/design-stack-d2-dry-run.md).

## Decision and why

**Keep exactly one OpenSpec schema:** the repository's existing `openspec/config.yaml` selects **`spec-driven`**. Its canonical change artifacts remain:
`proposal.md → specs/**/*.md → design.md → tasks.md`, with accepted/archived specs in `openspec/specs/` and changes in `openspec/changes/`. Git `main` remains the acceptance authority; OpenSpec files in a draft PR remain candidates.

**Smallest incremental capability:** a project-owned **design-review checklist and evidence handoff** recorded alongside the existing design artifacts in the relevant PR. It is a process/checklist, **not another OpenSpec schema, plugin, approval engine or automatic independent reviewer**. No external schema, agent skill, DDD pipeline, library, model or adapter is installed.

**Selection rationale:** existing OpenSpec and CI already cover artifact structure, scenario trace and some architecture constraints. D1 did not establish incremental outcome improvement for Intent-Driven, Anvil or a nine-skill DDD chain. Maintain one canonical artifact path and test the smallest missing property: independently challengeable design decisions with source links and explicit unresolved questions.

**Adopt/avoid decision:**
- **Use:** existing spec-driven schema, Engineering Policy AR-01..05, project architecture validator when an actual architecture contract exists, reference-based requirements trace and separate independent acceptance.
- **On demand:** DDD vocabulary/identity/invariants, one Mermaid C4-inspired component view, a short ADR for a durable decision, a typed input/output/error contract. These are techniques applied in `design.md`, not mandatory new deliverables.
- **Not selected:** copying entire Intent-Driven, Anvil or DDD-skill installations, forcing aggregates/events/outbox, switching root schema or installing additional model agents.
- **D2 experiment hypothesis:** a concise independent review packet can expose an invented product assumption or misplaced responsibility without a custom schema. No comparative improvement has yet been measured.

## Chain of responsibilities and handoffs

| Stage / authority | Inputs and who owns them | Output / responsibility | Gate before moving on |
| --- | --- | --- | --- |
| Discovery & product owner | Owner brief, decisions and evidence, source links | Owner-approved *observable* scope, deferred behavior, uncertainty log | Approval of exact semantics and revision; a conversation's generic "continue" is insufficient |
| OpenSpec spec author | Accepted discovery state only, original brief and declared engineering proposals | `proposal.md`, capability `spec.md` with normative scenarios and separate proposed choices | Source trace, no guessed product behavior, draft versus accepted status explicit |
| Design author (engineering) | Exact reviewed spec reference/SHA and Engineering Policy | `design.md`: domain terms/invariants, use-case ownership, module/dependency boundaries, typed contracts, alternatives, risks, open questions; selective C4/ADR | Reviewable, evidence-linked design, no unsupported abstraction |
| **Independent design reviewer** | Frozen design/spec revision, policy and original source **read-only**, without author transcript or held-out oracle | Separate review note: source coverage, severity P0–P3, layer/ownership/cycle findings, unjustified patterns, confidence and verdict | Actual independent person or fresh separate approved review context; author self-check may not assert independence |
| Author + owner as needed | Reviewer findings and source references | Repair and documented dispositions (fix, reject with rationale, defer/block) | Changed design invalidates prior review; disputed product meaning returns to owner |
| Task planner | Accepted spec and reviewed design hashes, resolved P0/P1 | `tasks.md`: each task with spec/design trace, architecture and independent verification steps | D4 design review accepted; spec/design and held-out oracle frozen, operator preflight satisfied before codegen |
| Implementation executor (future) | Accepted immutable inputs, bounded budget, local tools | Direct Codex baseline, optionally RPG+Codex proposal, real code/test/telemetry | Separate D5/D6 authorization; no model calls or live FW from D2 |

**Authority invariant:** product semantics are owner-owned; engineering design is reasoned/reviewed; structure is tested by CI; behavior is tested by an independently held oracle. No step may substitute for another.

## Design checklist (smallest reviewable contract)

A design candidate is **ready to request independent D4 review** only if all applicable checks have explicit evidence; `N/A` needs a concrete reason.

| ID | Question / expected evidence | Source |
| --- | --- | --- |
| DS-C01 | Every important behavior, invariant, flow and error has a precise source link and exact spec revision. Proposed decisions are labelled. | Product spec, issue/owner evidence |
| DS-C02 | Domain types and invariants are not mixed with CLI, JSON, files or network I/O. | AR-01 |
| DS-C03 | Application owns use-case ordering/coordination; adapters own external representations; dependency arrows point inward; cycles checked on realizable source when available. | AR-01/02 |
| DS-C04 | Each behavior has one declared owner; no misplaced responsibility hidden by filenames. | AR-03 |
| DS-C05 | Inputs, outputs and errors separate valid no match, missing evidence and unsupported predicates. Avoid silent success. | AR-04/05, spec |
| DS-C06 | All added ports, factories, caches, persistence and frameworks have current justifications; otherwise remove or label deferred. | SOLID, KISS, YAGNI |
| DS-C07 | A minimal module/flow view, alternative(s), tradeoffs and operational limits are comprehensible to a new implementer. Add C4 or ADR only where necessary. | Design |
| DS-C08 | Acceptance scenarios have trace into proposed tasks, and verification is explicitly independent of implementation. | AR-05 |
| DS-C09 | Reviewer identity/context, inputs and exact revision/commit, P0–P3 findings, disposition and verdict are recorded. A human- or model-authored note alone does not prove independence. | D4 review protocol |
| DS-C10 | Product approval, design review, local preflight and oracle freeze are four separate statuses; none is inferred from green CI. | L1 issue #32, D5 |

**Minimal review-record fields (no new framework):** `spec_ref`, `spec_sha`, `design_ref`, `design_sha`, `reviewer`, `independence_basis`, `review_scope`, `findings[{id,severity,source,reason,disposition}]`, `verdict=APPROVE|REVISE|INCONCLUSIVE`, `date`. Record refs and content hashes before review; after any changes, re-review changed content. Maintain held-out oracle outside implementation PR and reviewer context.

**Failure semantics:** P0/P1 unresolved or missing source/approval => `BLOCKED`. No independent reviewer => `NOT_RUN`, not `APPROVE`. Structural CI green => `STRUCTURAL_PASS` only. Never fabricate successful CLI, model or semantic output.

## Bounded synthetic dry-run

Read the [paper-only dry-run record](../research/design-stack-d2-dry-run.md). It tests a **single existing example** from the original brief and candidate L1 spec: preserve two matching rows with different actions and saved order; no global permit/deny. It demonstrates reference → role/boundary suggestion → independent-review request → task trace **on paper**. It is **not** approved Checker architecture or an executable spec/oracle.

- **Pass (documentation):** single schema identified; one scenario trace and candidate architecture ownership/contract; review questions/task trace reproducible from explicit source links; no extra dependency or code.
- **Not run:** real independent design review, model/human evaluator experiment, semantic acceptance tests, toolchain integration, model cost/time sampling, held-out oracle.
- **Design-stack selection:** minimal process **candidate selected for D3/D4 testing**, subject to reviewer findings and measured usefulness; do not claim stack efficacy.

## Recovery and next gate

1. Read [AGENTS.md](../../AGENTS.md) → [current state](current-state.yaml) → [roadmap](roadmap.md) → [design-stage plan](design-stage-plan.md) → this contract → [D2 dry-run](../research/design-stack-d2-dry-run.md).
2. Check current live [Draft PR #51](https://github.com/lehater/agentic-checker-lab/pull/51), [L1 issue #32](https://github.com/lehater/agentic-checker-lab/issues/32) and any newer D3 PR. A draft candidate is not merged authority.
3. **Next D3:** prepare *candidate* Checker L1 domain + architecture + detailed design, trace to a frozen explicitly identified L1 candidate revision and carry unresolved approvals. Then D4 independent review on exact artifacts. No codegen until D4+D5 and the separately approved bounded run.
