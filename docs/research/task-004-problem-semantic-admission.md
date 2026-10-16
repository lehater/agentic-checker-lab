# TASK-004 — gate for strict Problem Evidence semantic admission

Status: **RESEARCH VERIFIED AGAINST PINNED SOURCE / PROJECT ADMISSION NOT EXECUTED** (2026-10-16).

Scope: `checker.problem` only. This is an analysis of the published contracts and an instruction for a subsequent *real operator run*; it is **not** an ACCEPTED Harness semantic evaluation, capability transition, project publication, or authorization to implement Checker.

## Baseline

- Target repository `main` inspected at `870ab7bea51b6565815a7e153283d881b5a7b658`. Owner framing is **already** recorded in [PDEC-CHECKER-001](../scenario/problem-framing-decision.md), so do not reproduce/replace the decision.
- Frozen Harness Consumer Pack v1 SHA: `442db854c3a736a5e500b4a41664b80981b0d94c`; do not upgrade.
- [First pilot](task-004-harness-agent-review.md): candidate graph validated, structural `CREATE checker.problem`, Core `artifacts: []` and `questions: []`, 23 reference Authorities `UNASSESSED`, coverage `completion_ready: false`, no Project Frontier/semantic closure.
- PR #7 remained **open Draft** on inspection. Proposed Harness-first roadmap is not an accepted amendment to the canonical roadmap.

## 1. Source-bounded semantic disposition

The Discovery candidate is [problem-evidence-candidate.md](../../experiments/runs/harness-intake-v1/problem-evidence-candidate.md); it is not a canonical provider. Anchor the review to the actual [owner decision](../scenario/problem-framing-decision.md), the [SSSR fixture](../../tooling/fixtures/checker-intake/sssr-scn-006.md), the [Product As-Is fixture](../../tooling/fixtures/checker-intake/product-access-as-is.md), and the [questions](../../experiments/runs/harness-intake-v1/questions.md).

| Claim / fragment | Evidence status for **new** Checker | Disposition |
| --- | --- | --- |
| Operator needs an explainable investigation of network flow; show relevant policy placements, applicable saved ACL rules in processing order, and evidence credibility | **Owner-confirmed**, PDEC-CHECKER-001 | Discovery framing is accepted as *project intent*, subject to proper Harness admission |
| No obligation to emit one universal Permit/Deny verdict | **Owner-confirmed** | Retain the **absence of an obligation**, not a prohibition on all later scoped verdicts |
| Every stored matching Permit/Deny rule shown, strict no-match distinction, source timestamps | **Author-confirmed historical**, SCN-006 REQ-036/037/040, RULE-019/020/022; not independently accepted To-Be detail | Use as historical support. Do not silently promote `every`, concrete fields, freshness thresholds, no-match API behavior to Product Requirements |
| Specific tuple representation: IPv4, protocol and ports including source port; route/correction/NAT and precise policy-match semantics | Historical: REQ-034/035, RULE-021; Product As-Is SQL observation | Remain Product/Domain scope and semantics questions |
| Stored vs optional Cisco/live diagnostic, per-device permission, max 10 live devices, SQL/Django and UI tables | Historical: REQ-039/040; Product As-Is paths/branches | Source context only; no permission to contact real devices and no target runtime/design commitments |
| Offline fixture-only data, CLI/API, `CHECKER-OFFLINE-CANDIDATE` subject, five-Capability graph | **Lab proposals**, not owner-confirmed | Candidate/test-fixture boundaries only. Use a neutral Checker problem scope in any proposed canonical provider |
| Completeness/freshness/confidence policies, exact placement set, oracle and architecture | Unknown | Keep open; refer to corresponding downstream Authorities rather than settling in Discovery |

The original candidate's sentence `all covering stored rules`, `no-match as a separate fact`, and optional live diagnostics are **stronger/more specific** than the owner's new high-level wording. Their historical correctness does not make them independently accepted target requirements. Its `CHECKER-OFFLINE-CANDIDATE` subject is also not an accepted product-scope restriction. A scoped Discovery revision should express the confirmed need while preserving these details as historical context or Questions.

Q-01 is only partially resolved: owner/problem framing is settled; project-specific ownership, admissible reviewer and publication policy are still unconfirmed. Q-02..Q-13 are not automatically closed.

## 2. Contract trace — pinned Harness

All relative paths in this section refer to **`lehater/harness@442db854c3a736a5e500b4a41664b80981b0d94c`**.

1. `skills/agent/project-bootstrap-reconcile/SKILL.md`, steps 2–14: assess/reconcile existing canonical realization, assess applicable Authorities conservatively, run Engineering Coverage. **UNASSESSED is not NOT_APPLICABLE**. Coverage work items are not automatic graph nodes.
2. `skills/artifacts/problem-evidence/SKILL.md`, steps 1–10: require actionable CREATE and Discovery ownership; source-grounded problem, actor, outcome, boundary, downstream Questions; run common semantic acceptance before Core registration. Unknown product details need not block Discovery.
3. `spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml`: `problem-evidence` inherits `requires_assertion_authority`, `requires_source_authority`, `requires_semantic_review`; required checks are **`source-discipline`**, **`authority-boundary`**, **`no-invention`**, **`evidence-not-solution`**.
4. `src/harness/application/semantic_admission.py::admit_artifact`: actual inputs include **graph**, **Core model**, **skill registry**, **knowledge-kind contracts**, **capability**, **source assertions**, machine-readable **candidate assertions** and explicit **acceptance_id**; optional lifecycle/decision inputs follow context. It validates Authority context, candidate write scope, canonical source-reference permission, provenance/ownership, review and upstream baseline. `checker.problem` currently has no proposed graph prerequisites, so no prerequisite lifecycle is needed for **the admission call**, but lifecycle is essential for later published CURRENT.
5. **Strict root provenance:** `_validate_source_assertion_artifacts` accepts derived canonical semantic sources only from lifecycle-selected *declared prerequisites*. A root `checker.problem` cannot invent a canonical `source_artifact` for an SSSR document or for a chat confirmation. Historical fixtures and PDEC are inspectable evidence inputs; treating them as accepted prerequisite providers without a modeled/accepted prerequisite fails the strict provenance boundary. Original Discovery claims based on explicit owner intent must be independently reviewed for source discipline and no invention; prose citations do not automatically become canonical semantic authority.
6. `spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml` has **no required contract for `problem-evidence`** at this pin. `decision_preflight.py` + `semantic_admission.py` consequently permit `NOT_REQUIRED` Decision Exploration/Governance for this knowledge kind. This does **not** bypass owner-controlled decisions or allow invented autonomy: if the Discovery review finds a material unresolved owner question, retain it.
7. `src/harness/assurance/semantic_acceptance.py::evaluate_artifact` demands `semantic_review.status: ACCEPTED` and the four completed check IDs; deterministic checks cannot by themselves attest truthful semantic review. The owner's framing confirmation is **evidence for the review**, not the review execution or an authorization to self-approve another Authority's meaning.
8. `src/harness/application/project_publication.py` + `docs/design/project-publication-v0.md`: `ACCEPTED` admission output must be coupled with a Core CanonicalArtifact, matching lifecycle/acceptance identity, and failure/Question evidence. Only a validated complete next snapshot may be atomically published with compare-and-swap. Writing `core-candidate.yaml` and an `acceptance_id` separately is insufficient.
9. `src/harness/application/decision_pipeline.py`, `src/harness/application/semantic_closure.py`, `docs/design/project-frontier-v0.md`: after an actual successful publication, recompute Decision Roadmap, Semantic Closure, Engineering Coverage and Project Frontier. `checker.requirements` is next only if those read models allow it; old target `READY` is insufficient.

## 3. Authority assessment vs admission — precise boundary

The current trial graph says `DISCOVERY` owns `checker.problem`, but labels that ownership as **candidate only**. There are 23 `UNASSESSED` reference Authorities and no accepted project-owned applicability/subject inventory. The `admit_artifact` implementation **does not directly ingest the Authority Assessment registry**. Therefore an isolated strict API result on a *candidate* graph may be technically `ACCEPTED`; this must not be reported as accepted **project** knowledge or full bootstrap/coverage completion.

The owner confirmation is sufficient to support the narrow Discovery intent **if** a qualified reviewer explicitly performs and records the four semantic checks. It does not independently approve the project-owned DISCOVERY Authority assignment, review delegation, candidate graph, scope, or publication. Other Authorities need not all be marked REQUIRED to review one Discovery problem; their current `UNASSESSED` values nevertheless remain reconciliation/coverage gaps for whole-project closure.

**P1 gate:** first establish and record a defensible project-owned Discovery producer/Authority and reviewer permission (without inventing a signed approval), resolve any Discovery-level conflict, and execute actual Harness admission. If the acting agent lacks that authority, prepare the candidate/review and report the precise remaining owner decision instead of publishing.

## 4. Next bounded execution, not performed here

Use [the operator prompt](../../tooling/prompts/task-004-harness-problem-admission.md) on Ubuntu with the pinned Consumer Pack. It runs after the existing bootstrap pilot and writes a new experimental run directory, leaving historical `harness-intake-v1` immutable.

Expected audit bundle: version/source hash manifest; exact command exit codes and outputs; current vs proposed graph/assessments; project-owned authority/reviewer basis; machine-readable admission candidate and source assertions **if actually produced**; actual review decision/check record; `semantic-admission` output; publication revision and lifecycle **only if validly published**; recomputed read models **only if run**; explicit remaining Questions, tokens/model metadata if available, and operator `git status`.

Safety gates:
- Never fabricate semantic review, `acceptance_id`, an ACCEPTED status, CURRENT lifecycle or a publication revision.
- No extra owner confirmation of PDEC-CHECKER-001; ask only about a *genuinely unresolved* authority/review decision that cannot be delegated.
- Do not reinterpret historical source requirements as accepted To-Be behavior.
- Do not touch `lehater/harness`, launch CoderMind/codegen, access devices, or auto-push/merge.
- A green repository CI checks repository mechanics, not Discovery semantic validity.

**Current verdict: `ADMISSION NOT RUN / PROJECT TRANSITION INCOMPLETE`.** Next valid result is either verifiably published `checker.problem CURRENT`, or `BLOCKED / INCOMPLETE` with concrete contract findings; not a manually promoted document.
