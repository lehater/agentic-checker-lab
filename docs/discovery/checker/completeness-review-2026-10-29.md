# Checker — Independent Requirements Completeness Review (2026-10-29)

**Status:** REVIEW FINDINGS / NOT OWNER-APPROVED; **review basis:** GitHub evidence only; **scope:** elicitation completeness, not Checker implementation or product-spec acceptance.
**Observed branch HEAD before review:** `c23d524f5ba35d95da68998b7b94ba1c6be4d31e`; Draft PR [#48](https://github.com/lehater/agentic-checker-lab/pull/48), OPEN/DRAFT, base `main` at `23fb14db473635b8ad2dfbb8121a581a9c42eafa`.
**Reproducibility:** source files below were inspected on `experiment/iterative-discovery-protocol` at that HEAD; accepted source is the existing ledger and round approval records, **not** the candidate OpenSpec. This is an independent *artifact* reading; primary oral evidence was not available and independent confirmation of voice transcription remains INCONCLUSIVE.
**Initial checks:** repository workflow [40835072570](https://github.com/lehater/agentic-checker-lab/actions/runs/40835072570) SUCCESS, strict OpenSpec workflow [40835072581](https://github.com/lehater/agentic-checker-lab/actions/runs/40835072581) SUCCESS on the above SHA; they validate **structure only**. Do not transfer those conclusions to subsequent commits without checking their CI.

## 1. Evidence and recovered state

Sources (all at observed branch HEAD unless an immutable SHA/URL is given):
- [AGENTS.md](../../../../AGENTS.md), [protocol v0.2](../protocol.md), [chat-start](../chat-start.md), [original owner brief](../../scenario/owner-problem-brief.md);
- [ledger](ledger.json): checkpoint **4**, `IN_PROGRESS`, **R-001/R-002 CLOSED**, **Q-001..Q-008 ANSWERED/APPROVED**, **D-001..D-011 ACCEPTED**, no PREPARED R-003;
- [round 001](rounds/001.md) and [round 002](rounds/002.md) with published exact questions, normalized answers, corrections and recorded approval;
- [pilot retrospective](../pilot-retrospective.md), [fresh-chat audit](https://github.com/lehater/agentic-checker-lab/pull/48#issuecomment-6490016712);
- candidate [OpenSpec](../../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md), [design](../../../openspec/changes/checker-v1-baseline/design.md), [CHK-001..018 catalog](../../evaluation/checker-acceptance-catalog.json), [D-to-spec trace](decision-trace.json), [author semantic draft](semantic-review-draft.md).

**Authority split:** D-001..011 are accepted *as recorded* in GitHub; the brief is original need; route/provider decisions, JSON/CLI schema, IPv4-only subset and error behavior in OpenSpec/CHK are proposals; CHK-001..018 are ALL `NOT_RUN`/`PROPOSED_NOT_OWNER_ACCEPTED`. The existing trace covers 11/11 D identifiers mechanically but retains four existing coverage gaps (D-002, D-003, D-006, D-008). The earlier new-chat audit established recoverability, not independently verified consent or completeness. A prior assessment that no R-003 was needed is an observation, not a proof.

## 2. Goal-to-capability and scenario completeness matrix

Legend: **A** accepted meaning; **P** candidate only; **G** semantic/coverage gap; **E** approved but delegated engineering; **F** future scope. These can coexist.

| Capability / scenario partition | Owner authority | Candidate evidence | Review |
| --- | --- | --- | --- |
| Directed TCP/UDP query with single source and target IP | D-001/009/011 | CHK-001/002/013 | A+P; IPv4-only / invalid-input choices E |
| Concrete and both `any` ports; predicate boundaries | D-004/009 | CHK-004/011/012 | A+P+G; five-dimensional cross-product incomplete |
| Matching includes all rows, both actions and snapshot order | D-004/005 | CHK-003/008 | A+P+G; repeated identical rows not explicitly tested |
| Opaque extra conditions preserved, not evaluated | D-004 | CHK-014/015 | A+P+G; unknown mandatory fields vs opaque extras |
| FW relevance under differing vs equal routed interfaces | D-002 | external seam only | A+G; route evidence absent/ambiguous and zero candidate outcome |
| Ingress/egress/global applicable ACL placements | D-003 | CHK-016 supplied placements | A+G; provider selection not tested |
| Same named ACL multi-placement and FW grouping | D-010 | CHK-005/016 | A+P+G; identity and row multiplicity |
| Relevant FW with no bound ACL | D-007 | CHK-017 | A+P |
| Bound ACL with zero matching stored rows | D-007 | CHK-007 | A+P; distinguish missing evidence |
| **No potentially relevant FW at all** | no explicit outcome in D-002/D-007 | none | **G; novel owner-visible situation** |
| ACL known but never successfully collected | explicitly delegated by Q-004 | CHK-006, fail-whole-query proposal | E+G; candidate is not approved |
| Last successful per-ACL timestamp, no history | D-006 | CHK-018 display; storage absent | A+G; real lifecycle separate |
| Collector refresh failure, log, preserve successful snapshot | D-008 | external seam, no acceptance test | A+G; actual collector F for synthetic MVP |
| Malformed/incomplete/unsupported input and atomic output | Q-004, D-004/006/008 partly | CHK-002/009 | E+G; clear evidence integrity boundary |
| No implicit deny or end-to-end verdict | D-001/004/005/007 | CHK-003/007/008 | A+P |
| Source fact provenance and independent behavior proof | accepted round records | proposed CHK catalog | G; no CHK execution/independent semantic sign-off |

**Coverage method:** goal decomposition (operator sees preserved policy evidence rather than inferred access decision); BABOK-style completeness/consistency and requirement-validation checks; rule/example/counterexample mapping; equivalence classes/negative boundaries; data availability state partition; dependencies `routing → relevant FW → placements → ACL identity → successful snapshot → rule predicate match → grouped presentation`. No quantitative completeness percentage is claimed: candidate cases are not executed and the search space is open.

## 3. Gap register

Each finding identifies the missing rule, source/accepted D, competing interpretations, a falsifying example, MVP criticality, decision authority and novelty relative to the pre-existing trace. **Priority:** P0 blocks a trustworthy thin slice or product meaning; P1 required before candidate contract/acceptance; P2 advisable documented boundary. A finding is **not** a new owner requirement.

### CR-01 — P0 · OWNER_DECISION · NEW · zero relevant FW vs no relevant ACL

- **Missing:** user-visible semantics of a *valid* relevance evaluation yielding zero FW. [Brief, Relevance/Purpose](../../scenario/owner-problem-brief.md), Q-002/D-002 (equal-interface devices excluded), Q-004/D-007 (covers **relevant FW with no ACL**, not zero FW). **Affected:** D-002, D-007, D-001.
- **Alternatives:** (A) explicit `NO_RELEVANT_FW` / “no candidate FW under this heuristic”; (B) empty groups alone; (C) a different diagnostic/representation. No existing approval selects one.
- **Counterexample:** every synthetic FW resolves both IPs to the same interface; an empty result indistinguishable from “a candidate ACL exists and has no matching rules” makes a false operational implication possible.
- **Why owner:** the *meaning communicated to the operator*, not the JSON field name, is a product choice; a single clarification is justified. **MVP:** critical if zero candidates are valid. **Predecessors:** Q-002 and Q-004 approved; new linked clarification Q-009 may be prepared after this review is safely checkpointed.

### CR-02 — P0 · ENGINEERING_DECISION · KNOWN, sharpened · named ACL with no first successful snapshot

- **Missing:** failure/result contract when relevance identifies a named ACL but stored evidence is missing. Q-004 explicitly delegates it; D-006/D-007/D-008, CHK-006 and candidate “Missing required snapshot” propose fail-all.
- **Alternatives:** fail entire query atomically; report per-ACL `UNKNOWN_DATA` while retaining other results; omit the group (unsafe without distinguishing reason). **Example:** fw-a ACL-A has valid snapshot and match; fw-b ACL-B was never collected. `NO_MATCH` for B is false, dropping B hides an expected group.
- **Authority:** engineer proposes explicit fail-closed contract and independent cases, subject to later contract/owner-scope review; **not** a new owner question merely because the proposed design is still unapproved. **MVP:** critical for truthful results when evidence can be absent.

### CR-03 — P1 · ENGINEERING_DECISION / DEFERRED_SCOPE · NEW · nonunique or unavailable route/interface evidence

- **Missing:** determinism and uncertainty state of D-002/D-003 when source/destination route is missing, one route has multiple next-hops/interfaces, or a routing domain is unspecified. Q-002's accepted “different vs same interface” presumes one resolved interface per endpoint; its answer explicitly defers exceptions.
- **Alternatives:** MVP requires one unambiguous pair in synthetic relevance input and rejects absent/ambiguous input; later provider handles multiple path candidates; silent pick/omit risks fabricated certainty.
- **Example:** source lookup returns interfaces `Gi0/1` **and** `Gi0/2`, destination `Gi0/2`; some possibilities satisfy D-002, others do not. **MVP:** important to validate the provider seam, not to build a live route engine. **Authority:** engineering subset and documented deferred route algorithms; reclassify OWNER_DECISION only if an unavoidable owner trade-off remains after a concrete proposal.

### CR-04 — P0 · ENGINEERING_DECISION · NEW/partly known · supported mandatory five-field predicate subset

- **Missing:** executable definitions and reject/skip boundary for ACL IP objects, wildcards/CIDR, port single/range, protocol and malformed mandatory values; D-004 requires five-field evaluation while the brief expressly delegates predicate subset. Candidate OpenSpec and CHK-004/009/015 are insufficient to establish supported behavior.
- **Alternatives:** narrow documented synthetic schema with deterministic matching and explicit unsupported error; treating unknown required fields as successful matches; silently dropping only unsupported rows. The latter two can misstate “all matching rules”.
- **Example:** two rows refer to a destination address group; one is parsed as `any` because object group is unknown, producing false positive, while an omitted row produces false negative. **MVP:** critical. **Authority:** engineer (document supported subset, negative equivalence classes and failure atomicity); no vendor parser required.

### CR-05 — P1 · DERIVED_REQUIREMENT · NEW · repeated identical ACL rows must survive placement deduplication

- **Missing:** distinction between *deduplicating one ACL group across bindings* (D-010) and *preserving every original matching row occurrence* (D-005). CHK-016's “one copy of each matched rule” can be read as value deduplication.
- **Alternatives:** retain separate row instances with distinct snapshot positions (follows D-005), or collapse identical rows (would discard saved evidence). **Example:** same literal `permit tcp ...` occurs on lines 2 and 5 of the same ACL, attached inbound and global; expected one ACL group with **two** ordered lines, not one. **MVP:** important. **Authority:** derived from D-005/D-010; engineer add identity/position invariant and a test, not an owner question.

### CR-06 — P1 · CONTRADICTION · NEW · candidate spec promises unmatched rule output

- **Missing:** within candidate “Preserved observation and presentation”, prose says “matching and unmatched saved ACL rules”, whereas D-005 says show **matching** rows, and the same candidate's `No stored match` scenario expects an **empty** rules list.
- **Alternatives:** show only matched rows and an empty list for no match (consistent with D-005/D-007), or include all unmatched rows (unapproved feature and contradicts current case).
- **Example:** 1 of 100 lines matches: emitting 99 nonmatching rows in the result changes its accepted semantics. **MVP:** important before OpenSpec review. **Authority:** engineering/editorial reconciliation to exact accepted decisions, then independent semantic review; do not silently change D-005.

### CR-07 — P1 · ENGINEERING_DECISION / DEFERRED_SCOPE · KNOWN · provider must select correct placement semantics

- **Missing:** D-003's ingress-interface inbound, egress-interface outbound and global binding selection; candidate consumes already selected placements and CHK-016 tests their rendering, not selection.
- **Alternatives:** explicit synthetic seam guarantees verified placement list for the prototype; define/verify a separate provider contract later; silently present all ACLs on selected FW (incorrect).
- **Example:** ACL `OUT` bound outbound on **incoming** interface, versus outbound on **outgoing** interface; only latter is applicable under D-003. **MVP:** important for a self-contained vertical slice's fixture correctness; route collector itself deferred. **Authority:** engineer specifying seam and independent fixture contract.

### CR-08 — P1 · ENGINEERING_DECISION · NEW · device/ACL identity and collision boundaries

- **Missing:** identity key for D-010 “one named ACL per FW”, duplicate provider events and distinct FW with same ACL name; CHK-005 does not test cross-FW name collision or repeated positions.
- **Alternatives:** group by stable `(FW identity, ACL identity)` (follows D-010); group only by ACL name (incorrect); split a single ACL by placement (incorrect).
- **Example:** fw-a and fw-b both have `WEB_IN`; a naive name-keyed map merges them. **MVP:** important; **authority:** engineer / derived from D-010, preserve original matching rows as CR-05.

### CR-09 — P1 · ENGINEERING_DECISION · NEW · successful snapshot atomicity and completeness

- **Missing:** what makes one ACL read a “successful snapshot” for D-006/D-008 (full ACL order, rules, identity, placements, timestamp), and how partial/invalid reads affect last success. Candidate CHK-018 tests a failed refresh timestamp but not partial-truncation integrity.
- **Alternatives:** validate complete per-ACL snapshot and atomically replace it; accept a partially read list as successful; replace only valid rows. **Example:** collector fetches 5/20 rows and times out: storing 5 with a new date creates ungrounded `NO_MATCH` for 15 unseen rows.
- **MVP:** important for fixture/data contract; real collector and persistence may be deferred, but no synthetic fixture should claim incomplete data is complete. **Authority:** engineering contract derived from D-006/D-008, not owner.

### CR-10 — P1 · DEFERRED_SCOPE · KNOWN · persistence/collector lifecycle not exercised

- **Missing:** evidence for successful update replacement, per-ACL dates, no history, failure log without overwrite from D-006/D-008. CHK-018 observes timestamps in supplied data; no functioning collector/persistence is included in synthetic MVP by the brief.
- **Alternatives:** explicitly defer real persistence/collector and test their synthetic input invariants; or add isolated fake collector contract tests without networking. **Example:** failed update 11:00 after successful 10:00 must retain rules/date 10:00; no complete collector test exists.
- **MVP:** bounded outside initial physical implementation; acceptance of full D-006/D-008 requires later independent contract tests. **Authority:** engineering scope boundary, subject to eventual scope acceptance.

### CR-11 — P2 · ENGINEERING_DECISION · NEW · IPv4-only, numeric port and invalid input boundary

- **Missing:** approved D-009 says “single IP” TCP/UDP without settling IPv4 vs IPv6, 0 vs 1 minimum port, textual `any`/blank input and normalization; candidate assumes single IPv4, `0..65535`.
- **Alternatives:** explicit IPv4-only and synthetically supported port range in first slice; dual-stack/other input validation; silent implicit restriction. **Example:** `2001:db8::1` rejected while the owner approved “single IP” generically, or port 0 treated inconsistently.
- **MVP:** low if clearly declared subset; **authority:** engineer selects minimal documented scope and checks boundaries; reopen owner scope only upon evidence that IPv6 is essential for the minimal goal. No assertion that IPv6 was rejected by owner.

### CR-12 — P1 · ENGINEERING_DECISION · NEW · result status partition and partial-error atomicity

- **Missing:** presentation must distinguish `no relevant FW` (CR-01), `relevant FW with no ACL` (D-007), `ACL with no matching rows` (D-007), `data missing` (CR-02), and `unsupported matching/invalid data` (CR-04), without inventing access verdict.
- **Alternatives:** explicit per-stage typed statuses and source provenance; reuse empty lists for unrelated states; fail-all on invalid evidence. **Example:** one named ACL has zero matches while another is inaccessible: returning two empty arrays hides unknown evidence. **MVP:** important; **authority:** engineering shape after CR-01 owner meaning, no new owner decision for every field/code.

### CR-13 — P1 · INSUFFICIENT_EVIDENCE · KNOWN · no executed independent behavior oracle

- **Missing:** acceptance catalog CHK-001..018 all `NOT_RUN` and candidate-only; existing D-to-case trace has 4 open links; CI checks source structure and schema, not semantic completeness. **Affected:** every D for verification, especially D-002/003/006/008.
- **Alternatives:** freeze and independently review cases with positive/negative boundaries before executing prototype; report structural PASS as semantic PASS (invalid). **Example:** CHK-016 passes supplied placement rendering while ingress/egress *selection* is wrong. **MVP:** critical at behavioral acceptance, not a reason to implement now. **Authority:** independent reviewer + engineer + owner for final product meaning.

### CR-14 — P1 · INSUFFICIENT_EVIDENCE · KNOWN · original owner speech cannot be independently verified

- **Missing:** primary transcript/audio of R-001/R-002 and direct independent approval evidence; round files record normalized answers and explicit approval claims, but cannot verify their transcription externally. **Affected:** D-001..011 provenance.
- **Alternatives:** mark transcript fidelity UNKNOWN and use new targeted owner semantic-review confirmations; infer correctness from repository logs (invalid). **Example:** a recorded normalization could omit a spoken qualifier without changing any structural check. **MVP:** independent semantic acceptance gate. **Authority:** owner and independent reviewer; do not retrospectively alter recorded approvals.

## 4. Example-mapping coverage to add (no owner semantics invented)

| Dimension | Positive example | Counterexample / boundary | Expected provenance |
| --- | --- | --- | --- |
| Relevance | one FW has source/destination on distinct interfaces | same interface; no FW; provider missing/ambiguous | D-002; CR-01/03 |
| Placement | inbound ingress + outbound egress + global | outbound on ingress; inbound on egress | D-003; CR-07 |
| Rule matching | 5/5 match; query port `any` | nonmatching IP/protocol/source port/destination port; unsupported mandatory matcher | D-004/009; CR-04 |
| Additional conditions | matching five fields + `established` | reject solely due to `established` | D-004 |
| Rule multiplicity | two matching identical rows at different indices | deduplicated row values or first-match truncation | D-005/010; CR-05 |
| Data | current last-success snapshot; failed refresh retains it | never-successful, corrupt, partial or unsupported snapshot | D-006/008; CR-02/09 |
| Observation | no ACL vs named ACL with 0 matches | no relevant FW / missing evidence claimed NO_MATCH | D-007; CR-01/12 |
| Direction | A→B only | reverse-only evidence shown without second request | D-011 |

## 5. Why the first two rounds missed findings; generalizable process changes

| Failure category | Observed mechanism | Preventive process invariant |
| --- | --- | --- |
| Initial problem framing | brief emphasizes relevant FW/ACL, Q-004 partitions only **ACL** availability; no explicit zero-device outcome | derive scenario-state taxonomy from every entity in pipeline, including cardinality **0/1/N** |
| Question formulation | Q-002 asks for one include/exclude example but does not vary missing or nonunique route evidence | each high-impact rule gets positive, negative, ambiguous and unavailable-evidence examples; defer truly out-of-scope algorithms explicitly |
| Clarification depth | Q-004 elicits named ACL vs no ACL and delegates never-successful snapshot, but leaves operator-facing empty-result semantics across stages | follow each “no match / no data” answer with provenance-aware distinctions; mark engineering vs owner boundaries |
| Normalization | D-005 plus D-010 each correct, but composition may lead to row-value deduplication (CR-05) | preserve identity, multiplicity and ordering as separate invariants when aggregate/group operations are introduced |
| Missing counterexamples | no identical rows, cross-FW ACL-name collision, truncated snapshot, wrong-interface ACL test | independent boundary-value and adversarial scenario matrix before declaring frontier exhausted |
| Downstream interpretation drift | candidate “matching and unmatched” contradicts D-005 and CHK empty-list scenario | semantic diff gate: accepted D text vs every candidate SHALL and THEN; flag contradictory or additional behavior, not just missing references |
| Premature stopping | “0 open Qs” after R-002 used as a practical stopping point despite no explicit independent completeness sweep | **closure gate:** objectives→capabilities→scenario states→examples→negative paths→uncertainties→authorities; zero open Qs is necessary but insufficient |
| Mechanical check limitation | latest CI green despite known D provider/storage coverage gaps and no executed oracle | separate structural CI, coverage inventory, independent semantic verification, owner acceptance, and actual execution verdicts |

**Reusable guardrails (not Checker-specific):**
1. Before ending discovery, enumerate each decision-relevant input, transformation and output, and check `absent/one/many/unknown/invalid/stale` partitions **where meaningful**. Do not mechanically generate every Cartesian product; require a concrete harmful counterexample.
2. Maintain a `coverage_register` with each uncovered case classified OWNER_DECISION / ENGINEERING_DECISION / DERIVED_REQUIREMENT / DEFERRED_SCOPE / CONTRADICTION / INSUFFICIENT_EVIDENCE and its **decision authority**, affected D and evidence.
3. Select an owner frontier only for meaningful business trade-offs after checking semantic duplicates against all historical Q texts/answers. A new question must explain why an accepted Q does **not** already settle it. Preparing fewer than 3 questions is preferable to fabricating a batch.
4. Do not equate missing evidence with negative business results. Distinguish material data availability from valid empty sets.
5. Check compositional invariants: deduplicating parent entities must not collapse valid child occurrences or discard provenance.
6. Review candidate specifications and oracle **as derivatives** of approved decisions. Explicitly label unapproved engineering choices; CI structure/trace success never proves completeness.
7. Preserve source SHA, questions and source records, owner confirmation gate, PREPARED checkpoint *before asking*, CLOSED checkpoint *after approval*, and separate verdicts `RECOVERY_OK`, `STRUCTURAL_OK`, `SEMANTIC_REVIEWED`, `OWNER_ACCEPTED`.

## 6. Proposed next frontier and continuation rules

One genuinely new OWNER_DECISION (**CR-01**). Proposed **Q-009**, linked to but not duplicating Q-002 and Q-004: “Если поиск по корректным данным не обнаружил ни одного потенциально релевантного межсетевого экрана (например, на всех проверенных FW оба адреса соответствуют одному интерфейсу), какой смысл и какой результат должен увидеть оператор? Нужно ли явно отличать этот случай от найденного FW без ACL и от ACL без совпавших правил?” Alternatives: explicit no-candidate result, empty list with explanatory context, or another owner choice. The answer concerns operator semantics, **not** output schema. Dependencies Q-002/Q-004 answered. A separate “missing/ambiguous route” owner question is **not** justified for synthetic MVP while Q-002 explicitly defers route exceptions; classify CR-03 ENGINEERING_DECISION/DEFERRED_SCOPE.

**Do not present Q-009 as an active interview item until a distinct PREPARED checkpoint has committed its exact text and the branch/checks have been verified.** Do not touch accepted Q/A/D text, declare R-003 answered, approve the candidate spec, execute Checker, merge PR #48 or change `main`. Remaining engineering and independent-review gaps are not evidence of more owner questions.

## 7. Verdict and limits

- Operational recovery of existing recorded decisions: **PASS** (GitHub-only).
- Requirement completeness: **INCOMPLETE** (CR-01 owner meaning and multiple downstream design/verification gaps); cannot claim an exhaustive search proof.
- Independent original voice/owner-fidelity check: **INCONCLUSIVE** (primary source unavailable).
- Structural baseline CI: **PASS on c23d524 only**, pending separate new-commit checks.
- Proposed spec, acceptance oracle and Checker execution: **NOT ACCEPTED / NOT_RUN**.
- Method improvement hypothesis: enforce independent completeness and semantic counterexample sweep before interview closure; validate on another **independent** problem before a general transfer claim, but do not manufacture Checker questions.
