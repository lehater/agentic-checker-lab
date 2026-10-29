# Checker L1 — bounded specification-reconciliation handoff

**Status:** `PROPOSED_NEXT_ENGINEERING_TASK`; Quality Gate: [completed, L1 acceptance blocked](quality-gate.md). No new owner interview or code/model runs authorized.

## Objective

Produce a **single coherent proposed OpenSpec/CLI/synthetic-data contract** that preserves the owner meanings **recorded** in experimental PR #48. Do this on a separate scoped engineering PR, not by merging PR #48 wholesale. Requirements approval, independent oracle custody, environment preflight and final implementation authorization remain per [L1 issue #32](https://github.com/lehater/agentic-checker-lab/issues/32).

### Exact corrections to propose

| Concern | Historical owner meaning to preserve (source PR #48) | Concrete engineering artifact | Required independent *candidate* test |
| --- | --- | --- | --- |
| **Query fields** | D-001/D-009/D-011: one-way source/destination IP, TCP/UDP; blank source/dest ports default `any` and do not filter that port | Select explicit wire encoding for omitted/any ports; choose documented IPv4-only subset as engineering choice; reject invalid/missing required IP/proto | Omitted `sport` vs explicit `any`, concrete numeric source port, unsupported proto; reverse not auto-evaluated |
| **Relevance and hierarchy** | D-002/D-003/D-007/D-010/D-012: all relevant FW, all relevant ACL with **relevant placements**, then matched rows; preserve parents with empty children | Synthetic provider representation admits FW with **zero ACL**; ACL with zero rows; multiple attachments; route calculation remains out of first slice | No relevant FW; relevant FW no ACL; ACL no matches; same ACL on two bindings; irrelevant binding excluded |
| **Matching and extras** | D-004/D-005: all matching rows in order including permit/deny; supplemental conditions displayed without checking their applicability | Distinguish match-critical supported five-field predicates from display-only opaque attributes; specify rejection vs unsupported mandatory predicate; no end-to-end verdict | Time-range/extra field retained; unsupported required predicate not guessed; identical-text rule occurrences preserved |
| **Snapshots** | D-006/D-008: per-ACL last-successful timestamp, no history, preserve successful evidence/date on failed collection | Minimal complete synthetic snapshot model with timestamp; no actual collector/persistence necessary. Define **missing-first-snapshot vs no-match** explicitly as an engineering contract (fail-atomic is candidate) | Two ACLs with distinct timestamps; empty valid snapshot; missing initial snapshot does not return false `NO_MATCH`; corrupt input fails explicitly |
| **Interface and failure** | Original brief expressly delegates interface/JSON/CLI and minimal predicate subset; historic Q/D does **not** accept existing OpenSpec wire format | Draft narrow versioned CLI/JSON and error contract (including no partial successful result if choosing fail-atomic), justify consequences | Exact executable black-box inputs/outputs, error stderr/nonzero policy, no device/network access |

Existing [proposed spec](../../../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) and [CHK catalog](../../../evaluation/checker-acceptance-catalog.json) are **starting points for revision, not authoritative acceptance**. Its "both integer ports required" conflicts with recorded D-009; provider-as-only-pairs cannot preserve zero-ACL FW; supplemental fields and last-success dates need contract treatment.

## Authority / approval routing

1. **Developer owns** concrete narrow data grammar, port/JSON representation, clean architecture, provider API, fail-atomic engineering proposal, deterministic test fixtures; cite brief's delegation instead of asking owner individual formatting questions.
2. **Owner reviews in one package** the corrected observable scope, compatibility with recorded D-001..D-012, and any genuine new semantic conflict. Do **not** re-ask approved Q-001..009 or infer fresh approval from user silence.
3. **Independent reviewer/oracle custodian** verifies examples and expected behavior, freezes held-out fixtures before model implementation agents see them. Existing CHK-001..010 are proposals/NOT_RUN, not held-out.
4. **Local operator** verifies required installed OpenSpec/Codex integration and supported runtime separately; prior L1 notes reported OpenSpec absent locally and Node 18 vs CI Node 22. Don't assert these are fixed without a current local run.

## Current decision index

The accepted-source *evidence* is preserved on [unmerged PR #48](https://github.com/lehater/agentic-checker-lab/pull/48), not recopied into `main` here as product approval. This application has created **no new D IDs** and **no new Q IDs**, only read-only QG findings. Use a task ledger only if new owner-reviewed decisions are actually elicited.

**Stop gate:** do not commence codegen, L4 comparison or accept independent oracle until a coherent candidate spec and contract have separate owner/independent review. Existing L1, L2–L5 roadmap and PR #47 are unchanged.

**Next action:** draft *one* spec reconciliation PR from main, with a trace matrix and proposed acceptance fixtures, then request **one consolidated** owner review. This handoff is not that acceptance.
