# Checker — preliminary semantic reconciliation (not independent approval)

**2026-10-29. Status: AUTHOR REVIEW ONLY.** Authority: owner-approved D-001..D-011 in `docs/discovery/checker/ledger.json`; new OpenSpec and CHK cases are PROPOSED and NOT_RUN. This review was prepared by the authoring assistant and cannot satisfy the independent-review gate or verify absent raw voice evidence.

| D | Proposed alignment | Verification example or counterexample |
|---|---|---|
| D-001, D-011 | One directed host IPv4 TCP/UDP query; no access verdict | CHK-001 and CHK-013; reverse-only rules must not appear |
| D-004 | Five query dimensions distinct from opaque extra rule conditions | CHK-014 and CHK-015; an `established` condition alone is NOT an unsupported matching error |
| D-005 | All matching permit and deny rules, in stored order | CHK-003; no first-match truncation |
| D-007 | Named ACL with zero matches versus relevant device with no ACL | CHK-007 and CHK-017; neither means implicit deny |
| D-009 | Both ports blank/`any` by default and act as unrestricted query dimensions | CHK-011 and CHK-012; never replace blank port with 65535 |
| D-010 | One group per FW/ACL, all relevant placements | CHK-016; no duplicate rule groups |
| D-006 (partial) | Per-ACL last-success date displayed | CHK-018; failed refresh cannot update the date |

## Remaining deferred engineering boundaries

- **D-002:** Real route/interface relevance criteria (different interfaces to source and destination, exclude same interface) are NOT verified by synthetic provided relevance data.
- **D-003:** The external provider must select inbound, outbound and global ACL bindings; the current proposal only shows supplied bindings.
- **D-006:** Actual last-successful snapshot storage replacement and no-version-history are still outside the local query.
- **D-008:** Collector failed-read logging and nonoverwrite need an independent external adapter contract/test. Query decode failures are a distinct stage.
- **No first successful snapshot:** Candidate fail-closed query behavior is an ENGINEERING PROPOSAL, not confirmed owner meaning.
- **Schema and oracle:** The local JSON representation, IPv4-only subset and independent acceptance oracle remain proposed. CHK is NOT_RUN.

The trace check must report `VALID_WITH_OPEN_GAPS`, not semantic PASS. Independent review must verify all 11 D meanings against these proposals, rejected counterexamples, and decide whether the external seams are explicitly deferred or covered by a separate accepted contract. No Checker implementation or merge is authorized.
