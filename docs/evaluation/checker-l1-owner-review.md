# Checker L1 — approved synthetic scope; technical and oracle gates remain

**Approval outcome (2026-10-29): `APPROVED_SCOPE_AND_SEMANTICS`.** After the full package was explicitly presented in this ChatGPT conversation, the owner answered: **«Да, утверждаю, продолжай.»** This records acceptance of the **synthetic L1 scope and observable meaning in this review packet**, including the explicitly deferred implementation coverage and permission for the engineer to finalize the proposed JSON/CLI contract within this scope. It is **not** approval of unpublished technical changes, a hidden oracle, or execution of code-generation models. The underlying original chat message is not independently linkable from GitHub; this documentation records the approval claim and its context.

**Review revision:** Draft [PR #51](https://github.com/lehater/agentic-checker-lab/pull/51); [candidate OpenSpec](../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md); [proposed concrete CLI/JSON contract](checker-v1-contract-proposal.md); [proposed CHK catalog](checker-acceptance-catalog.json), **16 items, all NOT_RUN**.

## 1. Evidence and limits

- [Original owner brief](../scenario/owner-problem-brief.md), blob `0061b6f982c015785b59cad4b1b8c9fb95478617`.
- The [historical Q/D ledger](https://github.com/lehater/agentic-checker-lab/blob/experiment/iterative-discovery-protocol/docs/discovery/checker/ledger.json) in separate unmerged [Draft PR #48](https://github.com/lehater/agentic-checker-lab/pull/48), blob `6e25f5249416579d27462e2f54b26925339ee251`. The experiment records explicit owner approval of Q-001..Q-009 and D-001..D-012. This is **approval evidence of normalized meaning**, not acceptance of PR #51. Raw microphone recordings have not been independently verified.
- [L1 issue #32](https://github.com/lehater/agentic-checker-lab/issues/32) still demands approved product scope, coherent CLI contract, independent oracle custody and local tool preflight. Passing structural CI does not discharge those gates.

## 2. Decision-by-decision coverage in the *proposed* synthetic MVP

| Historic D | Accepted meaning as recorded | Candidate L1 disposition | Evidence / gap |
| --- | --- | --- | --- |
| **D-001** | Directed TCP/UDP five-field lookup, not real reachability | **COVERED_IN_PROPOSAL** | Validated query + local-only; IPv4-only is engineer-selected test scope |
| **D-002** | FW relevance from routes to src/dst on different interfaces; equal interfaces exclude | **DEFERRED_ACTUAL_COMPUTATION** | L1 consumes preselected relevant FW; does **not** test route inference. Future provider must preserve this criterion |
| **D-003** | Applicable ingress, egress and global ACL | **DEFERRED_ACTUAL_SELECTION** | L1 consumes preselected ACL and placement facts; does **not** independently determine which attachments apply |
| **D-004** | Five-field match; supplemental conditions displayed, not checked | **COVERED_IN_PROPOSAL** | Complete stored-rule matching / supplemental condition scenario; distinct mandatory matching vs opaque extra fields |
| **D-005** | All matches incl permit/deny in stored ACL order; no first-match/global verdict | **COVERED_IN_PROPOSAL** | Multiple actions and identical row occurrence scenarios; original row indices preserved |
| **D-006** | Only latest successful snapshot per ACL, its own date, no history | **PARTIAL** | L1 accepts one complete synthetic snapshot per relevant ACL and outputs date; it does **not** implement long-lived storage/history |
| **D-007** | Relevant FW without ACL retained; named ACL with zero matches retained | **COVERED_IN_PROPOSAL** | Zero-ACL FW and valid zero-match cases; no deny inference |
| **D-008** | Failed collection logged, prior successful snapshot/date unchanged, no user alert about past failure | **DEFERRED_COLLECTOR** | L1 has no running collector/refresher or log event. It must not claim this behavior tested. Pre-supplied snapshot timestamp is only a proxy for saved state |
| **D-009** | Required single IPs and TCP/UDP; source/dest ports numeric or `any`; omitted defaults `any` | **COVERED_IN_PROPOSAL** | Optional/wildcard query ports; IPv4 grammar an engineer scope proposal |
| **D-010** | One named ACL group per FW with all relevant placements, not duplicate rows | **COVERED_IN_PROPOSAL** | Group per (FW, ACL), placements preserved, row identity from position |
| **D-011** | Original direction only; reverse requires new query | **COVERED_IN_PROPOSAL** | Explicit no-automatic-reverse scenario |
| **D-012** | FW → ACL/placements → matching rows, parents survive empty children | **COVERED_IN_PROPOSAL** | Full hierarchy, no FW, no ACL, zero match |

**Interpretation:** `COVERED_IN_PROPOSAL` means stated and traceable, **not implemented, tested or approved**. `DEFERRED` requires owner acceptance of the limited synthetic MVP scope, not a retroactive claim that the owner's long-term requirement was cancelled.

## 3. Proposed bounded implementation contract

- **Data source:** local versioned JSON for a single directed query, supplied relevance FW→ACL and complete snapshots; never polls real firewalls.
- **Flow:** IPv4 src/dst IP required; TCP/UDP required; each port integer 0–65535, explicit `any` or omitted=`any`.
- **Matching:** saved ACL mandatory predicates over source/destination IP, protocol and two ports; exact IP/CIDR, tcp/udp/any, integers/inclusive ranges/any. Opaque `extra` conditions are shown but not interpreted.
- **Output:** all relevant FW (even without ACL), each relevant ACL (even without matches), all distinct attachment facts, matching rule occurrences in snapshot order with action and opaque extra data, individual last-success timestamp. No global permit/deny or real connectivity conclusion.
- **Error/missing evidence:** proposed fail-atomic for invalid mandatory inputs or missing/corrupt relevant snapshots; **never** silently turn unknown evidence into zero matches. Exit and stderr are engineering wire details, subject to review.
- **Excluded from this first implementation:** real route-table/ingress-egress ACL selection, collection/refresh/logging, long-term snapshot history, vendor parsing, distributed storage, live connectivity check.

The [contract proposal](checker-v1-contract-proposal.md) now **proposes explicit engineering rules** for duplicate identities, unexpected fields, ordering, mandatory matcher validation, error shape and port types. They remain reviewable proposed choices (not owner-confirmed universal product requirements). A [draft JSON Schema](checker-v1-input.schema.json) and [public no-dependency input linter](../../tools/validate_checker_l1_input.py) now exist with [open negative tests](../../tests/test_checker_l1_input_contract.py). They are **engineering-authored contract checks, not an independently authored or held-out acceptance oracle**. The schema does not by itself express cross-object identity, canonical IPv4 CIDR or port-range ordering; the linter checks those. No executable Checker behavior has been tested.

## 4. Approval request — one package, not renewed interrogation

**Approved scope and observable semantics:** The owner explicitly approved this consolidated Checker L1 package on 2026-10-29 by replying «Да, утверждаю, продолжай.» to the stated review request. The approval covers the synthetic MVP boundary, preservation of historically recorded D-001..D-012 semantics, explicit implementation deferrals for D-002/D-003/D-006/D-008, and engineering finalization of the documented minimal JSON/CLI/error contract. It does not make implementation coverage of deferred work complete.

**Recorded decision:** `APPROVED_SCOPE_AND_SEMANTICS`. This was an explicit response to the review package, **not** inferred from a generic continuation or CI result. **Acceptance does not imply authorization to codegen** before independent oracle and operator preflight. If later engineering changes materially alter the approved observable behavior, return the changed meaning for review.

## 5. After approval, not before

1. Engineer finalizes typed schema and negative validation tests within approved scope; records final spec SHA.
2. Independent oracle custodian **separately** authors and seals held-out black-box inputs/expected outputs, records SHA, and keeps them **inaccessible to implementation agents**. Public CHK-001..016 are **ideas only**, not hidden oracle; do not publish secret fixtures or labels in this public PR.
3. Independent semantic review reconciles changed spec and fixtures with the approved D evidence. Freeze versioned spec + oracle hashes.
4. Local operator verifies toolchain/OpenSpec/Codex and authorized quota. Only after these gates may the separately bounded code/model experiment begin.

**Current status:** `OWNER_SCOPE_SEMANTICS_APPROVED / ENGINEERING_CONTRACT_HARDENING / INDEPENDENT_ORACLE_NOT_FROZEN / LOCAL_PREFLIGHT_NOT_VERIFIED`. The OpenSpec remains a reviewed **candidate** until typed grammar, independent semantic review and approval evidence are reconciled on the final revision.
