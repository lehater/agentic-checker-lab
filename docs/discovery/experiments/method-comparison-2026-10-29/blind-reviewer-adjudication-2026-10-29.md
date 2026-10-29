# Fast → Standard → Deep — independent reviewer result and post-unblinding adjudication

**Date:** 2026-10-29  
**Status:** EXPLORATORY / POST-UNBLINDING COMPARISON / NOT AN INDEPENDENTLY VALIDATED METHOD.  
**Scope:** evaluation of requirements elicitation and stop criterion, **not** implementation or approval of a Checker specification. No new owner interview.

## 1. Source and reported outcome

- Reviewer was supplied only the original Checker brief + normalized Fast D1–D24, with no deliberate exposure to the former [historical ledger](../../checker/ledger.json), the Standard/Deep reports or prior [post-hoc audit](posthoc-fsd-validation-2026-10-29.md). However, technical isolation could not be verified (`BLINDING_UNVERIFIED`).
- Reviewer report was delivered by the owner as `Pasted text(20261029-143940).txt` and preserved **privately** at ChatGPT Library `/Projects/Checker-Discovery/Experiments/Method-Validation-After-FSD/Blind_Reviewer_Result_2026-10-29.txt`. Do not place full transcript/reviewer text in this public planning branch without explicit permission.
- Reviewer **self-reported** `SUFFICIENT_FOR_MVP_SPEC`, `moderately high confidence`, and **0 necessary new owner questions**. It identified 10 candidate gaps G1–G10 and considered several adversarial cases, but assigned no mandatory `OWNER_GAP`.
- This is a **single reviewer on the same task**, following previous iterative analyses on the same case. It is not conclusive external validation, a statistically meaningful test, or native Spec Kit/Grill Me operation.

## 2. Primary-observation versus post-unblinding classification

The reviewer **noticed** ambiguity in G1, so this is primarily a **triage/authority-classification failure**, not simply a question discovery failure.

| Review item | Reviewer's reasoning/outcome | After comparison with historical owner-approved decisions | Adjudication |
| --- | --- | --- | --- |
| **G1 — source port omitted** | Reject missing source port **versus** treat it as wildcard `any`. Reviewer classified as `DERIVABLE` and said wildcard expands the agreed model, hence not needed for MVP | Historical **D-009** explicitly says *both* ports optional, blank defaults to `any` and removes filtering on that dimension. New Fast D12 merely lists five fields. The original brief does not explicitly mandate that ports be supplied or delegate optionality to engineering | **MISCLASSIFIED OBSERVABLE OWNER CHOICE (HIGH)**. Neither branch is derivable from the supplied Fast record. Need `OWNER_UNRESOLVED`/authority evidence; **reuse prior D-009 as an existing known answer after scoring**. Never call this a new answer elicited by Fast |
| **Reverse direction** (reviewer's additional scenario) | Reviewer considered `A→B` versus automatic `B→A`, inferred that only specified flow is checked from source/destination roles, and asked nothing | Historical **D-011** expressly records only requested direction; new Fast D8/D12/D13 suggest but do not explicitly record it | **PRESERVATION/TRACE GAP (MEDIUM)**. Could be a valid inference for narrow MVP; not proof of a new indispensable owner question. Record explicit authority or tested derived assumption rather than silent PASS |
| **Additional ACL attributes** (reviewer's scenario on TCP flags and other predicates) | Suggests unsupported predicates should be excluded from the minimal language; not a new owner choice | Historical **D-004** evaluates five flow fields, displays extra conditions without evaluating them, and does not claim full rule applicability; new Fast covers `disabled` and `time-range` but not the general rule | **POSSIBLE SEMANTIC PRESERVATION GAP (MEDIUM)**. Narrow synthetic grammar is engineer-delegated; **display-only supplemental attributes vs required matcher predicates** are separate categories. A class-level rule should be explicit before asserting complete equivalence |
| **G4 zero relevant devices** | Classified the choice of message/empty display as engineering UX | Historic **D-012** preserves entity hierarchy; zero FW yields empty FW set, without mandating a special status string | **DERIVABLE/ENGINEERING**; do not count it as a new owner question merely to inflate count |
| **No duplicated ACL but identical rows** | Did not explicitly challenge duplicated *row occurrences* with distinct positions | Historical D-005 and D-010 jointly imply retain both row occurrences while deduplicating the ACL grouping | **TEST COVERAGE GAP**, not automatically an owner question. Add one mutation/metamorphic fixture |

### Critical example G1

Input: src IP/dst IP, TCP, destination port 443, **blank source port**.  
Output A: `INVALID_QUERY`, no results.  
Output B: request is accepted; source-port filter is unconstrained; all matching rules preserved.

The two outputs have materially different user-visible results. Neither is selected by the new Fast D12, and the brief delegates **ACL predicate grammar** to engineers, not product semantics of optional query fields. Marking A as implicit or B as an unapproved extension fails the authority check. The earlier owner answer (historical D-009) resolves the question **for actual continuity only**, not retroactively for the tested Fast run.

## 3. Method failure decomposition

1. **Question discovery:** reviewer *generated* G1 and an explicit reverse-flow contrast, so nonzero relevant uncertainty was surfaced despite `0 new owner questions` at closure.
2. **Question triage:** reviewer rejected G1 as supposedly derivable without a source/decision that entails its preferred branch. The stop gate accepted an unsupported choice.
3. **Semantic preservation:** Fast D1–D24 omitted at least one previously decided observable behavior (D-009). Standard and Deep did not flag it. Reviewer saw but failed to escalate it.
4. **Coverage completeness:** repeating many previously resolved counterexamples can look convincing without evaluating *unsettled* high-impact dimensions.
5. **Evidence/independence:** raw Fast P1 Q/A absent; reviewer `BLINDING_UNVERIFIED`; only one Checker domain and one owner with prior knowledge; no measured owner-active time/tokens. Do not claim measured comparative efficiency or a statistically validated improvement.

**Conclusion:** `REVIEWER_P0_COMPLETE / SELF_REPORTED_SUFFICIENT / STOP_GATE_FALSE_NEGATIVE_FOR_KNOWN_OWNER_SEMANTICS / METHOD_NOT_VALIDATED`. The historical decision is available, so **no repeat owner questioning is necessary** for the known port case. This result does **not** imply that Checker cannot proceed to engineering; it implies that the *proposed method's completion claim is too strong.*

## 4. Required correction to the next experimental protocol (candidate only)

**Cross-cutting rule, Fast/Standard/Deep:** when the analysis finds two plausible, materially different **user-observable behaviors** within MVP:

1. Identify exact source/decision evidence supporting each claimed choice; if neither is authorized, do **not** classify as `DERIVED`.
2. To classify as `ENGINEERING`, cite an explicit scope delegation that actually covers the choice. A generic “developer chooses minimal language/format” does **not** transfer authority over required-versus-optional user input semantics.
3. Classify `DEFERRED` only with explicit MVP boundary and its operational consequences. An exclusion must not silently change the core goal.
4. If consequential and genuinely unresolved, classify as `OWNER_GAP`. Ask it **once in a later batch**, never through repetitive single-question rounds.
5. A `DERIVED` label requires an auditable implication (source facts or approved decisions + concrete counterexample that would falsify it). A possibility, default preference or engineering recommendation is *not* a derivation.
6. Reviewer evaluates **separate counts**: generated candidate gaps, correctly classified gaps, wrongly downgraded owner gaps, owner questions sent, false positives, and owner time. Never award a completion gate just because question count is zero.

**Standard matrix requirement:** explicitly cross dimension × omission/wildcard/value × match/no-match/rejection, and direction × requested/reverse behavior. Classifications must cite source authority, not just note `covered`.

**Deep novelty requirement:** include tests drawn from *uncovered or weakly evidenced* classes plus metamorphic changes, not only five high-confidence already resolved cases; report `NO_NEW_COVERAGE` if none are new.

**Stop criterion:** no critical unresolved authority gaps **plus** justified coverage of user-observable branches **plus** noncircular challenge against weakly evidenced classes **plus** explicit provenance/confirmation limits. Otherwise say `SUFFICIENT_WITH_KNOWN_GAPS` or `UNVERIFIED`, not categorical `DISCOVERY_COMPLETE`.

## 5. Small next controlled test (not run)

1. Freeze a **reference requirement fixture** (original brief + previously accepted meanings) with an evaluation key **never accessible to test agents**.
2. Create blinded variants: remove (a) optional-port/default behavior, (b) explicit one-way-only behavior, (c) supplemental-condition non-evaluation policy. Include an unmodified control. Supply each to isolated evaluator in randomized order.
3. Demand issue-level output `source / alternative observable behaviors / classification / authority citation / materiality / skip reason` rather than only a conclusion or total question count. **Do not feed historical D labels or the seeded gap list to participants.**
4. Compare detection and *correct authority classification* separately; count false positives and time cost. Validate on a second non-Checker domain before any claim of general applicability.

**No modifications** to historical accepted ledger D-001..012, new Fast D1..D24, candidate Checker OpenSpec, CHK cases, implementation or main branch. This note remains experimental in Draft PR #48.
