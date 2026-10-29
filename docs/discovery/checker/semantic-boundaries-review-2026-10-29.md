# Checker — Semantic Boundaries Review: snapshot evidence and matching

**Date:** 2026-10-29. **Status:** INDEPENDENT ARTIFACT-LEVEL ANALYSIS / PROPOSALS ONLY; **NOT** owner approval, accepted OpenSpec, independent transcript verification, frozen oracle, or behavioral test execution.

**Reproducible review baseline:** `experiment/iterative-discovery-protocol` at `1f0d9ecaf1de0b203b564ecc12e24d673f593e70`; Draft [PR #48](https://github.com/lehater/agentic-checker-lab/pull/48) OPEN/DRAFT. The branch records R-001..R-003 CLOSED, checkpoint 6, Q-001..009 APPROVED, D-001..012 ACCEPTED, zero prepared rounds. No accepted Q/A/D is modified by this report.

## 1. Source authority, scope, and method

1. **Approved source as recorded:** [ledger](ledger.json), [round 001](rounds/001.md), [round 002](rounds/002.md), [round 003](rounds/003.md), plus [original problem brief](../../scenario/owner-problem-brief.md). These support decisions *as recorded*, not independent verification of original microphone audio.
2. **Unaccepted derivatives:** [candidate query OpenSpec](../../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md), [candidate design](../../../openspec/changes/checker-v1-baseline/design.md), [CHK catalog](../../evaluation/checker-acceptance-catalog.json), [candidate trace](decision-trace.json), [earlier completeness review](completeness-review-2026-10-29.md) and [author semantic draft](semantic-review-draft.md). The 18 CHK cases are `NOT_RUN` / `PROPOSED_NOT_OWNER_ACCEPTED`.
3. **Procedure:** derive invariants from accepted D; partition each stage into present / absent / empty / invalid / stale evidence; test positive, negative and boundary counterexamples; check proposed OpenSpec and CHK against accepted meanings; assign decision authority and **do not** call an engineering choice an owner requirement.
4. **Gate:** [protocol](../protocol.md) requires independent semantic review and owner approval of scope and critical examples before discovery completion. This artifact is an additional cross-check by an assistant of repo artifacts, **not** an independent external reviewer sign-off or a complete formal proof.

## 2. Material observations and provisional disposition

| ID | Priority / kind | Result / source decisions | Disposition and authority |
| --- | --- | --- | --- |
| SB-01 | **P0 ENGINEERING_DECISION** | Named, relevant ACL with no first successful snapshot is not equivalent to a complete snapshot with zero matches; Q-004, D-006/007/008/012; candidate CHK-006 | Recommend explicit fail-atomic for the synthetic v1 **as proposal**; engineer owns error contract and fixture; independent reviewer verifies |
| SB-02 | **P0 ENGINEERING_DECISION** | Support for five matching predicates/accepted data forms not fully defined; D-004/009; brief delegates vendor/predicate subset | Specify minimal explicit synthetic schema, reject unsupported mandatory predicate, isolate opaque extras; engineer + reviewer |
| SB-03 | **P1 CONTRADICTION** | Candidate “Preserved observation and presentation” promises **“matching and unmatched saved ACL rules”** while D-005/012 and its own No stored match case require **matching rows only** | Reconcile *candidate* wording to D-005/012; no owner decision change; reviewer verifies |
| SB-04 | **P1 ENGINEERING_DECISION** | Invalid/incomplete snapshot vs failed refresh vs missing initial snapshot have different evidence semantics; D-006/008; candidate CHK-009/018 | Define valid complete snapshot invariant and provider validation; collector persistence itself can be deferred |
| SB-05 | **P1 DERIVED_REQUIREMENT** | Group dedupe D-010 cannot dedupe same-text rule occurrences D-005; candidate CHK-016 “one copy of each matched rule” may be misread | Deduplicate ACL identity/placements only; preserve every matching row position, including equal-text rows |
| SB-06 | **P1 ENGINEERING_DECISION** | A mandatory five-field predicate vs uninterpreted auxiliary condition can be confused; D-004 vs candidate CHK-009/014/015 | Data contract must tag which fields decide matching; preserve extra conditions without evaluating them |
| SB-07 | **P1 DERIVED_REQUIREMENT** | A valid result keeps all relevant FW and ACL even when children are empty; D-007/010/012; candidate CHK-007/017 separate | Test whole parent/child hierarchy, zero FW, no ACL, zero rules and zero matches |
| SB-08 | **P1 ENGINEERING_DECISION / DEFERRED_SCOPE** | Real route-interface inference and ACL selection not proven by synthetic supplied relevance; D-002/003 | State provider preconditions explicitly; do not claim synthetic rendering verifies routing |
| SB-09 | **P1 INSUFFICIENT_EVIDENCE** | Mechanical 12/12 trace entries but D-002/003/006/008/012 gaps remain; no behavior execution, no primary audio | Preserve `VALID_WITH_OPEN_GAPS`; do not claim complete discovery/semantic verification |
| SB-10 | **P2 ENGINEERING_DECISION** | IPv4-only, TCP/UDP grammar, port range including 0, ordering across FW/ACL and JSON envelope are not all owner-accepted; D-009 and candidate design | Document deliberate prototype subset/outer-layer behavior; do not invent owner choices |

**Novelty vs [Completeness Review](completeness-review-2026-10-29.md):** SB-01..10 largely **deepen CR-02/04/05/06/07/08/09/10/11/12/13** rather than claiming ten newly discovered owner issues. The materially new deliverable is an evidence-state and five-field coverage matrix with concrete acceptance fixtures. CR-01 was addressed by approved Q-009/D-012; no additional owner-only frontier is justified.

## 3. Evidence-state matrix (snapshot contract)

**Key rule:** An empty set is a *valid observed result*, while an unavailable or untrusted snapshot is *absence of evidence*. Both can be represented by an empty array accidentally; that must not change their meaning. D-012 governs **valid query result content**; it does not already decide the error/partial-output contract for invalid mandatory evidence.

| Case | Relevance and ACL | Snapshot state | Entailed owner semantics | Proposed engineering handling |
| --- | --- | --- | --- | --- |
| ES-01 | No relevant FW | N/A | Empty FW collection (D-012) | Return successful empty collection (do not invent mandatory UI status) |
| ES-02 | FW relevant; no relevant ACL | N/A | Preserve FW, zero ACL children (D-007/012) | Successful query, `ACLs=[]` semantically; schema is not approved |
| ES-03 | Named relevant ACL | Valid successful snapshot, **zero stored rules** | Preserve FW/ACL, zero matched rules (D-007/012) | Success with ACL and empty match collection |
| ES-04 | Named relevant ACL | Valid successful snapshot, rules exist but none match | Preserve FW/ACL, zero matched rules (D-007/012) | Same *match count* as ES-03; **do not infer ACL itself is empty** |
| ES-05 | Named relevant ACL | **Never successfully captured** | No proof of `NO_MATCH`; Q-004 explicitly delegated (D-006/008/012) | **Candidate:** fail entire request, no successful partial output. Alternative: typed per-ACL unavailable fact; not yet selected as accepted contract |
| ES-06 | Named relevant ACL | Last success at 10:00; later refresh failed at 11:00 | Use saved 10:00 content/date; collector logs failure, query does not report past failure (D-006/008) | Test old content + unchanged timestamp + collector boundary separately; do not invent a stale/failed badge |
| ES-07 | Named relevant ACL | Partial/invalid candidate read and prior valid snapshot exists | D-006/008 require preservation on **failed** read; criteria for success not specified | Validate completeness before replacing; continue with last success and its timestamp |
| ES-08 | Named relevant ACL | Invalid existing stored matching fields or corrupt saved evidence | Cannot safely assert correct set of matching rows (D-004/005) | Proposed fail-atomic input validation, independently tested; original D do not mandate particular stderr/exit code |
| ES-09 | Two relevant ACLs | ACL-A valid, ACL-B never successful | ACL-A may have proven matches; ACL-B lacks evidence | Candidate global failure, or explicitly signalled partial result with B unknown; **never** convert B to zero matches |
| ES-10 | One FW with two ACLs | Each successful at different time | Each ACL carries its own last-successful date (D-006) | Check timestamps per ACL, not derived from FW refresh or query time |

**Engineering recommendation for minimal vertical slice:** model a provider result for each required named ACL as **(a) valid complete saved snapshot with last-success timestamp, or (b) unavailable/invalid evidence**. An empty valid snapshot is (a), not (b). Validate all mandatory evidence before publishing successful output; fail atomically on (b). Keep genuine collector/storage work deferred (the brief explicitly permits synthetic data); this proposal does not add a requirement for real polling, long-term persistence, network connection or partial-success UI. Check that the provider never labels a partial capture as a complete successful snapshot.

**Reasoning about D-012:** a failure response from an unsuccessful query is not an approved successful result with suppressed FW/ACL children. Conversely, if engineering later chooses per-ACL unknown status with successful partial results, that is a separate product-contract candidate requiring consistency review, not an automatic conclusion from D-012.

## 4. Five-field matching: independent equivalence and boundary analysis

**Approved meaning:** D-001/004/009/011 select a directed source-IP, destination-IP, TCP/UDP protocol, source-port and destination-port query. A **numeric** port limits matching; a blank/any query port removes just that dimension. Every matching saved rule is output in snapshot order, regardless of permit/deny or earlier matching rows (D-005); auxiliary conditions remain displayed but are not evaluated (D-004).

**Engineering subset hypothesis for synthetic v1, NOT owner accepted:** single IPv4 host query addresses, TCP/UDP, port fields absent/any or integer within an explicitly chosen valid range, saved rule IP matcher as host/CIDR/any, port matcher as singleton/inclusive range/any, protocol matcher with explicit supported values. The original brief delegates the subset, including actual ACL wildcard grammar, object-groups and vendor syntax. Query numeric-port 0 boundary, IPv6 and protocol superclasses are **scope decisions** requiring explicit documentation, not tacit owner rejections.

For the next table, use one **canonical base rule**: `permit tcp 10.0.0.5/32:50000 → 192.0.2.10/32:443`. Base query is `10.0.0.5:50000 → 192.0.2.10:443 tcp`, expected match. The arrow denotes source/destination, not an actual packet trace.

| Fixture | Variation (other dimensions unchanged) | Expected *if selected subset is approved* | Why / D |
| --- | --- | --- | --- |
| MF-01 | Base query vs base rule | MATCH | all five match; D-004 |
| MF-02 | source IP `10.0.0.6` | NO_MATCH | source IP independent negative |
| MF-03 | destination IP `192.0.2.11` | NO_MATCH | destination IP independent negative |
| MF-04 | protocol UDP vs TCP rule | NO_MATCH | protocol independent negative |
| MF-05 | source port 49999 vs exact 50000 | NO_MATCH | source-port independent negative |
| MF-06 | destination port 444 vs exact 443 | NO_MATCH | destination-port independent negative |
| MF-07 | source query port blank/any vs rule src 50000 | MATCH | query any bypasses only source-port filter, D-009 |
| MF-08 | destination query port blank/any vs rule dst 443 | MATCH | bypasses only destination-port filter, D-009 |
| MF-09 | both query ports blank/any vs exact-port rule | MATCH | combined default, not numeric 65535 |
| MF-10 | source query port any; destination IP mismatch | NO_MATCH | any must **not** bypass IP dimension |
| MF-11 | destination query port any; protocol mismatch | NO_MATCH | any must **not** bypass protocol |
| MF-12 | CIDR src `10.0.0.0/24`, host 10.0.0.0 and 10.0.0.255, outside 10.0.1.0 | inside/inside/outside according to **selected host/CIDR semantics** | IP boundary; candidate CHK-004 insufficient to settle network/broadcast semantics |
| MF-13 | destination inclusive interval `443..445`, queries 442/443/445/446 | NO/MATCH/MATCH/NO | inclusive port boundary; proposed |
| MF-14 | two physically distinct identical matching lines at positions 2 and 5 | 2 returned lines, order 2 then 5 | D-005; dedup ACL group is not row dedup |
| MF-15 | matching deny line before matching permit | **both** returned in original order | D-005, no first-match verdict |
| MF-16 | matching rule with `established` or schedule | MATCH and preserve extra condition *verbatim as stored* | D-004; no applicability claim |
| MF-17 | unsupported **mandatory** destination matcher; matching known rule also exists | Explicit unsupported-data outcome, not pretend complete result | Proposed error contract CHK-009/015; exact error shape engineering |
| MF-18 | rule has only uninterpreted **auxiliary** condition and five supported fields | MATCH and include extra condition | D-004; must not be rejected just for auxiliary condition |
| MF-19 | a rule matches source/destination **reversed**, but not query direction | NO_MATCH | D-011; do not autoinvert |
| MF-20 | relevant named ACL with no matching rows plus other FW with matching ACL | Both FW/ACL parents retained; only matching rows below second ACL | D-007/012 |
| MF-21 | named ACL present on one FW with two relevant placements | One ACL group, both placements; rules once per stored occurrence | D-010/005 |
| MF-22 | same ACL name on **two different FW** | Two distinct ACL groups within respective FW | D-012/010; group key includes FW identity |

**Important semantic distinction:** “all matches” is **all rows matching the supported five-field predicates in the saved snapshot**, not a proof of end-to-end packet access and not all ACL rows. If the implementation silently discards unsupported mandatory rows and continues returning only the supported ones as complete, that claim is unsafe.

### Five-field truth contract (proposed precise rule)

For valid query `Q` and a saved rule `R` whose five mandatory predicates have supported representations:

`match(R,Q) = srcIP_R(Q.srcIP) AND dstIP_R(Q.dstIP) AND protocol_R(Q.proto) AND (Q.sport == any OR sport_R(Q.sport)) AND (Q.dport == any OR dport_R(Q.dport))`

Here `X_R(value)` means **the rule's supported predicate includes the supplied query value**, not “evaluate every vendor condition”. Numeric/host range inclusivity comes from the selected engineering subset. For unsupported mandatory predicates, `match` is **not a false value or an assumed true value**: the operation invokes the separately defined unsupported-evidence policy. Opaque auxiliary conditions do not enter this conjunction.

This formula is an explanatory **engineering candidate**, not a new accepted owner D.

## 5. Semantic trace evaluation against all 12 accepted decisions

| Accepted decisions | Evidence in current candidate OpenSpec/CHK | Gaps or hazards |
| --- | --- | --- |
| D-001/011 | CHK-001/013; directed-only semantics | no executed tests; IPv4-only is candidate subset |
| D-002/003 | CHK-005/016 consume externally supplied relevance/placements | no route-based interface inference or ingress/egress/global selection contract test |
| D-004 | CHK-004/009/014/015 | unsupported mandatory vs opaque auxiliary boundary; full independent five-dimensional negatives absent |
| D-005 | CHK-003/008 | no duplicate-identical-row fixture; candidate wording about “unmatched saved ACL rules” contradicts D-005/012 |
| D-006/008 | CHK-018 shows timestamps; no collector tests | valid snapshot completeness, atomic refresh/retention, failure logging and history deferred |
| D-007 | CHK-007/017 | valid zero match vs never-successful unknown must be distinct |
| D-009 | CHK-001/002/011/012 | both-any combined, independently nonmatching other dimensions and numerical boundaries under-tested |
| D-010 | CHK-005/016 | preserve multiple placements without deduping equal-text rows or conflating two FW with same ACL name |
| D-012 | CHK-007/016/017, open gap in trace | no zero FW or composite hierarchy case; UI status codes not owner-mandated |

**Trace validation does not imply semantic pass:** `decision-trace.json` currently contains 12 D entries and 5 explicitly open gaps (D-002/003/006/008/012). Rows without trace gaps may still have material counterexample deficiencies: this report expands the review **without altering the machine trace or frozen candidate CHK**. That distinction is essential; 12/12 links and 18/18 candidate scenario references are only structural completeness.

## 6. Proposed minimal engineer-ready contract (not yet accepted)

- **Input:** exactly one synthetically supplied directed query plus a trusted relevance/placement fixture and saved ACL snapshots. Relevance fixture explicitly contains all relevant FW, including those with no ACL; ACL identity is scoped by FW; snapshot includes ordered rule occurrences and last successful timestamp per ACL.
- **Required capabilities:** validate a small five-field predicate vocabulary; evaluate every supported saved row; preserve matching row multiplicity/order, actions, opaque extra conditions, placements and parent-level zero cardinality.
- **Evidence contract:** one relevant named ACL has either one complete successful stored snapshot or is unavailable/error; empty valid snapshot is distinguishable. Recommendation: reject the *whole query* before reporting success if any mandatory evidence is missing/malformed.
- **Outputs:** logical `FW → ACL(+placements) → matching rows`; empty child collections are facts, not negative access verdicts. Physical JSON/CLI shape, error channel and status labels remain design proposals.
- **Deferred seams:** live polling, routing tables, actual device interface selection, vendor parsing, persistent last-success replacement and collector logging. Document/verify the **boundary contracts** separately; do not claim that a mocked value proves their actual algorithm.
- **Verification before product acceptance:** independent reviewer approves revised candidate spec/fixtures without consulting implementation; freeze positive/negative cases for data absence, five-field independence, both-any behavior and hierarchical multiplicity; then execute and inspect outcomes. Nothing in this report authorizes Checker codegen.

## 7. Process lessons and next allowed step

**Why two earlier rounds missed the edges:** Q-004 asked about three ACL states but did not force a complete evidence-state partition; Q-003 asked about extra conditions but not unsupported mandatory predicates; D-005 and D-010 were checked independently rather than compositionally. The subsequent completeness review found the zero-FW case; D-012 resolved owner meaning but did not replace the need for engineering contract verification.

**Reusable invariants for iterative discovery (proposal):**

1. For each stage, classify **zero valid results**, **unknown/missing evidence**, **stale-but-valid evidence**, **malformed evidence** separately, and test two differently shaped states that could accidentally serialize alike.
2. For every rule with `n` independent filter dimensions, obtain a positive case, **one independent negative per dimension**, wildcard bypass cases and a wildcard-with-other-mismatch guard. Add boundary tests for the chosen predicate vocabulary.
3. For grouping and deduplication, assert **parent identity**, **child multiplicity**, **preserved order** and **provenance** across all hierarchies.
4. For proposed source adapters, distinguish “fixture says it is relevant” from “real routing algorithm correctly inferred it”.
5. After decision trace validation, compare candidate MUST/SHALL clauses to **approved** source meaning, including unwanted additional behavior; independent human review is still necessary.
6. Do not ask the owner about engineer-chosen serializations, predicate subsets, or failure channels until a concrete owner-impacting trade-off survives engineering analysis.

**Next allowed action:** separately propose a minimal `synthetic query + evidence provider + predicate grammar + error contract` specification for review and an **independent acceptance matrix**. Resolve SB-01/SB-02/SB-03 before candidate OpenSpec approval. Do **not** create R-004 without a novel owner-choice dependency, alter Q/A/D, execute Checker, or merge PR #48.

**Verdicts:** artifact semantic boundary audit **PERFORMED (limited)**; original owner-voice fidelity **INCONCLUSIVE**; behavioral oracle **NOT_RUN**, candidate OpenSpec **NOT_ACCEPTED**, generalized methodology completeness **NOT VERIFIED**.
