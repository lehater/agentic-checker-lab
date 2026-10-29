# L1 independent oracle and semantic review — handoff

**Status:** `READY_FOR_INDEPENDENT_EVALUATOR_ASSIGNMENT`; **NOT** `ORACLE_FROZEN`, `IMPLEMENTATION_VERIFIED` or `L1_COMPLETE`.

This is the **next external review gate** after the owner approved the synthetic scope on 2026-10-29. The public [approval record](checker-l1-owner-review.md) quotes «Да, утверждаю, продолжай.» as a response to the entire L1 review package, with its provenance limitation. No new owner questions are warranted solely to recreate prior answers.

## Required independently reviewed inputs

- Original [owner brief](../scenario/owner-problem-brief.md), Git blob `0061b6f982c015785b59cad4b1b8c9fb95478617`.
- Historic approved-meaning evidence: [Q/D ledger D-001..D-012](https://github.com/lehater/agentic-checker-lab/blob/experiment/iterative-discovery-protocol/docs/discovery/checker/ledger.json), Git blob `6e25f5249416579d27462e2f54b26925339ee251`. **Unmerged PR #48** is evidence, not accepted specification.
- Current reviewed **candidate OpenSpec** `openspec/changes/checker-v1-baseline/specs/checker-query/spec.md`, concrete [synthetic input and output](checker-v1-contract-proposal.md), [draft input JSON Schema](checker-v1-input.schema.json) and [public validation checks](../../tests/test_checker_l1_input_contract.py). The evaluator records **final file hashes at assignment**, after no further contract edits.
- Public [CHK-001..CHK-016 ideas](checker-acceptance-catalog.json), all `NOT_RUN`, only for coverage reference; they are **not hidden**, and their descriptions alone are not oracle fixtures.

## Independence and custody rules

1. An evaluator **other than the contract author and implementation agent**, ideally with separately recorded review responsibility, must adjudicate meaning and expected outputs. A new chat run by the same prompt author is not automatically a proof of independent judgment. Record reviewer role, review date, materials' hashes and conflict-of-interest limits.
2. Provide the evaluator **only** frozen original requirements, approved scope, proposed spec/contract/schema, public coverage ideas and this handoff. Do not provide future generated code, tests, candidate outputs, historical failed implementation details, or developer reasoning.
3. The evaluator creates *new black-box fixture inputs* and independently derived expected outcomes, including both positive and negative boundary tests. Use the approved product semantics, **not** outputs of any implementation. Adjudicate ambiguities before freezing (do not guess).
4. Keep the **held-out** fixtures and expected-output labels in private, operator-controlled storage inaccessible to implementation agents and their tools. Public GitHub may contain only the evaluator protocol and nonsensitive **cryptographic hashes**, never file names/fixtures/labels that defeat the holdout.
5. Freeze after adjudication: compute SHA-256 of every private fixture and its expected output plus one SHA-256 of a canonical manifest/archive; record spec SHA, owner approval evidence and evaluator sign-off. Changing the source spec or oracle requires an explicit new version, not silent expectation rewrites.
6. Independently execute the frozen oracle **only after** a bounded model/implementation experiment is explicitly authorized, in a separate evaluator environment with withheld labels. Report PASS/FAIL/BLOCKED/INCONCLUSIVE, hash/version/command and authentic environment/tool evidence.
7. A public linter (like `tools/validate_checker_l1_input.py`) is **engineering-authored**, and a pass is not a substitute for an independent semantic oracle. Structural OpenSpec / repository CI is likewise necessary but insufficient.

## Required coverage and tension cases

| Group | Independent behavior to adjudicate | Owner/contract basis |
| --- | --- | --- |
| Input defaults | Both ports omitted vs explicit `any` vs concrete values; source/dest IP and protocol invalid | D-001/D-009 and reviewed L1 contract |
| Direction | A→B alone does not check B→A | D-011 |
| Ordering and multiplicity | Two identical row occurrences at different snapshot positions; permit and deny retained; ACL attached twice | D-005/D-010 |
| 0/1/many and hierarchy | No relevant FW; relevant FW without ACL; named ACL with zero matching rows | D-007/D-012 |
| Supplemental metadata | `extra` condition displayed without evaluating truth, while unsupported **mandatory** matcher fails explicitly | D-004 and engineering contract |
| Evidence unavailable | Relevant ACL with no first successful snapshot **not** treated as proved empty match | D-006/D-007/D-008/D-012, L1 fail-atomic proposal |
| Provenance | Two ACLs with distinct successful timestamps | D-006, L1 synthetic scope |
| Predicate boundaries | IPv4/CIDR containment, numeric ports/ranges, malformed CIDR, unsupported proto/port shape | Scoped engineering grammar |
| Relevance handoff | Preselected FW/ACL/placement facts used exactly without silently deriving live network path | D-002/D-003 and explicit L1 deferral |
| Failure behavior | Corrupt evidence or unknown mandatory matcher cannot produce partial success; no live device calls | L1 agreed scope and proposed error policy |

**Deferred and not falsely counted as verified:** real route computation (D-002), real ingress/egress ACL selection (D-003), durable snapshot replacement/history management (D-006), failed-refresh logger and last-success preservation (D-008). These require separate implementation/evaluation projects.

## Evaluator deliverables

A. **Semantic adjudication report:** for each decision D-001..D-012, `COVERED | PARTIAL_WITH_EXPLICIT_DEFERRAL | MATERIAL_CONFLICT | UNDECIDABLE`, and at least one counterexample for each material conflict; engineering choices tagged as such.  
B. **Private frozen oracle** (fixture/expected pairs, missing/corrupt input tests, versioned manifest), never in this public repository.  
C. **Public minimal evidence report:** reviewer role, baseline spec git blob SHA, date, number of verified cases (no hidden contents), frozen package SHA-256, independent semantic review status and limitations.  
D. **Local preflight** by the operator (separate role): `make check`, OpenSpec CLI 1.14.3 / Node 22, actual Codex integration and access; do not run model implementation until authorization.

## New-chat evaluator prompt (give only frozen sources, not generated implementation)

> Independently review the approved Checker L1 synthetic scope and candidate specification against D-001..D-012 and the original brief. Do not trust candidate OpenSpec or existing CHK test ideas as ground truth. Identify material semantic contradictions with concrete alternative outcomes and source references. Separately, privately prepare original input/expected black-box acceptance fixtures from approved meaning and explicitly documented engineering contract. Keep all held-out fixtures, oracle labels and hashes away from implementation agents. If the source cannot determine a result, mark UNDECIDABLE and require adjudication; do not silently invent requirements. Publish only a redacted review summary and cryptographic hashes, with reviewer identity/role and evidence limits. Do not execute any Checker implementation or model calls.

**Gate:** no unconditional `L1_PASS`, no claimed independent test or model deployment until these deliverables exist, are reviewed, and local operator preflight is verified.
