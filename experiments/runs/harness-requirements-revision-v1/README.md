# TASK-004 — Product Requirements classification correction

## Decision and purpose

Fix the known review defect discovered after PR #20: source prose was split by independently testable fields and Verification obligations were counted as Product REQ. No new product decision: PDEC-CHECKER-001/004 remain normative, including bounds and negative verdict semantics. Official approved Harness product skill and specialised semantic review gate must be used.

## Normalization

Historical REQ-CHECKER-001..028 remain addressable; materially replaced/misclassified ones are RETIRED, never silently overwritten or ID-reused. Revised product obligations: 001, 002, 003, 006, 007, 012, 013, 014, 025, 029 (one flow input), 030 (credibility of source metadata), 031 (partial output), 032 (complete no-match/missing/unknown distinction). The other 19 historical IDs are retained as RETIRED.

Test verification obligation REQ-028 is no longer normative product behavior. Its independent expected match/non-match requirement remains an explicit verification handoff and Q-DV-002 remains unanswered. Universal Permit/Deny NOT_REQUIRED is a non-goal; no user function is implied. No ACL match grammar or algorithm is chosen.

The requirements provider and Q-PR-001/002 resolutions must be replaced by a genuine admitted REVISION and one CAS publication. Upstream checker.problem acceptance and downstream Q-DV blockers must remain unchanged. Old execution evidence is immutable; downstream blocked verification drafts will require trace remapping on next attempt and cannot claim accepted coverage against RETIRED identifiers.

## Quality method

New Harness skill implements source statement ownership classification and product obligation grouping, informed by INCOSE/IREB and the Spec Kit requirements-quality versus implementation-test distinction. New semantic gate checks explicit machine-addressable review dispositions, not whether a model's judgment is true. This review was independently performed against all accepted product sources.

The command `experiments/runs/harness-requirements-revision-v1/execute.py` ran through the pinned Harness Consumer Pack in GitHub Actions, returned a real REVISION **ACCEPTED**, and atomically produced an identical checked-in publication via CAS. Acceptance evidence/candidate were captured verbatim from the run. New revision: `sha256:8f5dc04d1b76ce6c347b63c796935465b84db72bb1b3623969c90ae7a89af2f5`; parent: `sha256:f38832e09ce67f6713d26e1a06ab04d1af786d5cbd148e6e702181201c938334`. First-slice Product CURRENT; Domain/Verification BLOCKED, existing Questions intact.

## Boundaries

Only bounded Checker first-slice Product Requirements revised; neither Domain nor Verification artifacts have been accepted. No code generation or device operations.
