# Preregistered blinded evaluation: requirements question discovery

**Status:** proposed scoring protocol, **freeze before first run**; no pre-filled scores. Evaluator should have no knowledge of which anonymous transcript corresponds to A/B/C. If the evaluator already saw historic Checker D/Q, disclose `PRIOR_EXPOSURE` and avoid strong claims of independent blinding.

## Primary outcome and source limits

**Primary unit is a unique MATERIAL OWNER-DECISION GAP, not an interrogative sentence.** Candidate issue is material only if (a) not explicitly settled by the shared source or previous owner answer in **that run**, (b) feasible to turn into a scenario/rule, (c) affects a business-observable result or acceptance criterion within agreed small-MVP scope, and (d) cannot responsibly be chosen by engineering alone. A duplicate paraphrase counts once; an implementation preference does not count as an owner gap.

**Reviewer's rulebook is derived first from the frozen original brief and general requirements methods**, with no historical Checker question list visible during primary scoring. Historical ledger is a *secondary* benchmark revealed afterward. Do not reward rote recall of known Q-009 or known D numbers.

## Independently audited coverage taxonomy (not a golden list)

| Domain | Prompt to evaluator |
| --- | --- |
| Goals / outcome | What user decision or operation does the system support, and what is explicitly not a verdict? |
| Flow / boundaries | Are directionality, input dimensions, valid/invalid and optional values addressed when material? |
| Relevance / selection | Are device relevance, non-relevance, boundary states and provenance of relevance distinguished? |
| Entities / identity | Are FW, ACL, attachments, rule rows, multiplicity, order and identity composable without loss? |
| Snapshots / evidence | Are valid empty, unknown, missing, stale-but-valid and malformed evidence distinguished as needed? |
| Matching / predicates | Are five-field matching, wildcard behavior, unknown mandatory matching fields and opaque extras examined? |
| Result observations | Can positive, negative and empty nested outcomes be explained without fabricating permit/deny? |
| Dependencies / exclusions | Are synthetic MVP limits, delegated engineering contracts and live-network non-goals correctly scoped? |
| Verification / unknowns | Are critical examples and negative cases checkable, and unresolved assumptions explicit? |

**Ratings per category:** `0=not examined`; `1=mentioned but ambiguous or without testable consequences`; `2=examined with meaningful positive/negative or boundary example and a correct owner-vs-engineering classification`. Nine categories, **0–18** descriptive coverage points. Do not interpret this number alone as question-elicitation quality.

## Primary per-run metrics and rubrics

| Metric | Computation / interpretation |
| --- | --- |
| **M1 — validated owner-gap yield (primary)** | Count distinct material owner-decision gaps actually raised by the method and confirmed as material by blinded reviewer; record `raised / material / in-scope / answered`. More is not always better; false positives and false negatives separately |
| **M2 — first-frontier precision** | Material owner-choice questions / unique owner-choice questions in frozen P0; 0/0 = N/A. Native Spec Kit P0 produces **one** visible question; report native asymmetry |
| **M3 — evidence-based coverage** | 0–18 above, **with examples and source citations**. A named category without actual examination is at most 1 |
| **M4 — unsupported assumption burden** | Count owner-meaning claims invented without source or confirmation; count absent/unknown evidence treated as negative result separately |
| **M5 — unnecessary owner burden** | Count duplicates, source-fact questions, low-impact preference questions, engineering choices sent to owner; compute ratio per validated material issue |
| **M6 — stop correctness** | `0` premature unsupported complete; `1` stops with named unresolved critical gaps or budget exhaustion clearly disclosed; `2` reasoned coverage+counterexample audit, no reviewer-identified open critical owner issue in scope; `N/A` no stop decision |
| **M7 — semantic preservation** | Count contradicted or silently strengthened approved owner answers, lost negations and reviewer-reported corrections |
| **M8 — efficiency** | Validated owner gaps per **measured active owner minute**; questions and agent tokens counted separately. If active minutes/tokens not captured, `UNKNOWN`, not 0 |
| **M9 — method-specific discipline** | Did A respect prerequisites / whole frontier, B the official 5-per-call/taxonomy/clarification logs, C cover scan + negative examples + separate closure? Failures require concrete transcript references |

**No weighted single-number leaderboard by default.** Present an evidence matrix, precision–coverage trade-offs and confidence. A candidate approach can discover more real gaps and still be worse if it consumes disproportionate owner attention. Use `first-five` only for comparable P1 prefixes, not to force A/C to copy B's session cap.

## Issue-level adjudication sheet (copy per distinct issue)

```text
anonymous_run:
issue_id:
actual question (verbatim):
source phrase and why it is not already settled:
business consequence / concrete positive-negative example:
scope: IN_MVP | DEFERRED | OUT_OF_SCOPE | UNKNOWN
authority: OWNER | ENGINEERING | SOURCE_FACT | JOINT | UNKNOWN
reviewer verdict: MATERIAL_OWNER_GAP | VALID_ENGINEERING_NOTE | DUPLICATE | TRIVIAL | UNGROUNDED | NEEDS_OWNER_VALIDATION
correction/semantic loss:
independent reviewer evidence:
confidence: HIGH | MEDIUM | LOW
```

**Disagreement policy:** two reviewers independently score the same anonymous candidate issues, then reconcile with quotes and examples. If no second reviewer, record `SINGLE_REVIEWER` and no claim of reliable independent validation. Unknown owner semantics remain `NEEDS_OWNER_VALIDATION`; neither AI evaluator nor historical snapshot can choose them.

## Termination challenge (evaluate after P1)

Ask a blinded evaluator to propose the **single most consequential still-unasked owner question**, if any, while being restricted to the same brief and the arm's approved answers. For each claimed omission require a concrete scenario and proof it is *not* in owner-approved/deferred content. Then test whether the method's final stop rationale already explicitly handled it. Avoid grading based only on “empty frontier” or the observed count of questions. A reviewer may find no material issue; that is not an absolute completeness proof.

## Fairness / contamination gates

- Same frozen task text and same model/effort, same access to external knowledge? If not, note comparison `CONFOUNDED`.
- Native method artifacts and versions inspected, or all labelled `PROMPT_EMULATION`; **do not compare native results to prompted imitation as a causal method test without noting confounder**.
- Spec Kit's blank spec shell has no decisions beyond brief. Verify it did not ingest candidate OpenSpec/history via a copied repository.
- Input history, memory, connected GitHub and competitor outputs hidden from agent; any leaked Q/D or result invalidates strict-blind status.
- Owner's repeat exposure is logged. Randomize run order in later replication.
- P0 frozen prior to P1 and before viewing rival outputs.
- Budget stop reported as `CENSORED`, not `COMPLETE`.
- Original Checker historical ledger remains unavailable until **after** independent primary scoring.
- No secret prompts, hidden oracle or participant transcripts in a public test branch without consent.

## Verdict report

Deliver: input/spec hashes and runtime versions; anonymous raw issue count; M1..M9 with citations to transcripts; reviewer disagreements; which method falsely declared complete; source/skill discrepancies; limitations; secondary post-unblinding historical contrast; recommendation for which *mechanisms*, if any, warrant another trial.

**Interpretation:** This is one-domain exploratory pilot. Statistical confidence and generalized reliability are **not** established. “C has more questions than A” is not sufficient evidence of method superiority.
