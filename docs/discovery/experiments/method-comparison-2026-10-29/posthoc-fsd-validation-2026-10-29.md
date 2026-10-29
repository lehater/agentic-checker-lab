# Post-hoc audit of Fast → Standard → Deep on Checker (2026-10-29)

**Status:** EXPLORATORY / POST-HOC / NOT BLIND / NOT METHOD VALIDATED. This assesses the *quality of elicitation*, **not** Checker implementation or candidate OpenSpec. The owner is **not** being asked to repeat previously answered questions.

## 1. Provenance and methodological separation

- Common original [owner brief](../../../scenario/owner-problem-brief.md), Git blob `0061b6f982c015785b59cad4b1b8c9fb95478617`.
- New **Fast**: Matt Pocock Grill Me `PROMPT_EMULATION`; P0 first frontier had five questions; P1 **self-reported** 24 owner questions / 24 answers / five rounds, 24 numbered decisions D1–D24, `DISCOVERY_COMPLETE`. The user supplied a final summary and normalized D texts, **not complete, verbatim P1 Q/A or timestamps**. Stored privately in ChatGPT Library at `/Projects/Checker-Discovery/Experiments/A-GrillMe-Fast/P1_handoff.md`, not published here.
- New **Standard**: took those Fast decisions as input; classified eight findings R01–R08, no additional owner questions; user supplied `STANDARD_REVIEW_COMPLETE_NO_NEW_OWNER_QUESTIONS`.
- New **Deep**: took Fast and Standard; reported 12 scenario rows, five adversarial cases (A1–A5), ten findings DP-F01–F10, zero new owner questions, and `DEEP_P0_REVIEW_COMPLETE_NO_NEW_OWNER_QUESTIONS`. Deep acknowledged `BLINDING_UNVERIFIED`. Private source: `/Projects/Checker-Discovery/Experiments/Deep-After-Standard/Deep_P0_review.txt`.
- **Historical benchmark** (opened only for this retrospective): accepted [D-001..D-012](../../checker/ledger.json), three earlier rounds, plus [completeness audit](../../checker/completeness-review-2026-10-29.md) and [semantic boundary audit](../../checker/semantic-boundaries-review-2026-10-29.md). This historical material is *not* proof that the new run was wrong; it supplies specific counterexamples to any completeness claim.

### Experimental protocol deviation

The [pre-registered A/B/C comparison](README.md) was **not completed as planned**. A/Grill Me proceeded to P1; B/Spec Kit and C/combined P1 were interrupted because single-question and repeated review interactions imposed unacceptable owner burden. The shared P1 prompt had also required confirmation after every response, confounding native method usability. Later **Fast → Standard → Deep** is a *different, sequential* intervention with its own outcome; it must not be reported as the original three-arm comparison or as a controlled win for any particular framework. All runs were explicit `PROMPT_EMULATION`, not real skill/command execution.

## 2. Audit method

The pre-existing [EVALUATION.md](EVALUATION.md) defines M1–M9, material owner-gap criteria, burden, stop correctness, preservation and evidence rules. **Do not pretend that this review is a blind execution of that rubric.** Current evaluator has seen the historical benchmark and earlier method discussions (`PRIOR_EXPOSURE`), and only normalized P1 outcomes—not a complete source dialogue—are available. A genuine primary blind score is **NOT PERFORMED**.

For this post-hoc comparison, an omission is marked:
- `UNRECORDED_OWNER_MEANING`: earlier owner-confirmed observable behavior with no explicit equivalent in Fast D1–D24.
- `POSSIBLE_SEMANTIC_GAP`: potential user-visible choice; meaning requires a concrete counterexample and domain-authority review.
- `DERIVABLE_OR_ENGINEERING`: a consequence of already accepted rules or explicitly delegated engineering scope; **do not force a question**.
- `EVIDENCE_GAP`: inability to prove what happened, not by itself a new requirement.

A historical decision may be reused as a **known answer** without requiring the owner to repeat it, but *must not* be silently credited to the new Fast as an elicited or preserved decision.

## 3. Post-hoc differences: what the stop gates failed to flag

| ID | Historical reference | New Fast / Standard / Deep evidence | Adjudication and practical counterexample |
| --- | --- | --- | --- |
| **H-01** | Historic **D-009**: both ports optional and default empty/`any`; when set to `any`, the corresponding port dimension is *not filtered* | New Fast **D12** merely lists source/destination ports among five fields; **D22/D24** choose TCP/UDP and reject unsupported protocols. No explicit default or wildcard query semantics. Standard R01 labels port representation engineering; Deep DP-F05 does likewise | **UNRECORDED_OWNER_MEANING; HIGH.** Query omits source port: reject as malformed vs treat as `any` lead to different matches and different UI behavior. Concrete prior owner decision existed. Reuse it as prior evidence, not as a new Fast discovery |
| **H-02** | Historic **D-011**: only requested flow direction; reverse direction requires a separate query | New Fast **D8/D12/D13** imply a directed flow by source/destination roles but do **not** explicitly settle automatic reverse-direction evaluation. Standard/Deep did not test this alternative | **UNRECORDED_OWNER_MEANING; MEDIUM.** One-way A→B query could return ACL observations for A→B alone or automatically include B→A. Existing historic answer is known; do not re-ask. The original brief suggests directionality, so inference may be correct, but it is not a clearly persisted owner decision in this run |
| **H-03** | Historic **D-004**: all additional ACL conditions (e.g. `established`, schedule) are displayed but **not interpreted/evaluated**; matcher uses five fields; a match is not a full applicability verdict | New Fast **D5/D11/D12** explicitly preserve `disabled`, `time-range` and other attributes, and say time-range is not evaluated, but they don't establish an *all-other-conditions* non-evaluation policy. Standard/Deep treated the generalized issue as resolved | **POSSIBLE_SEMANTIC_GAP; MEDIUM.** A saved rule with an extra `established` condition: include based on five fields while displaying the attribute, or exclude because current-state matching cannot prove established? Engineering chooses supported syntax; only the scope of claimed rule applicability needs an explicit semantic statement. Prior decision exists but is not preserved as such |
| **H-04** | Historic **D-012**: hierarchy retains relevant FW, ACL and rows even when any child set is empty; **zero relevant FW** means empty FW set | New Fast **D4/D10/D13** cover FW with no ACL, no ACL matches, missing snapshot and device exclusion; no standalone `zero relevant FW` example. Deep scenario row 2 discusses non-relevant/unknown devices, not zero-set output | **DERIVABLE_OR_TEST_GAP, not automatically new owner question.** Require an explicit zero-relevant-FW fixture and a result that does not suggest deny. In the original brief/accepted model an empty set follows from no relevant entities; no new UI status is automatically mandated |
| **H-05** | Historic D-005/D-010 and completeness CR-05: retain distinct identical matching row **occurrences** while deduplicating ACL **groups** across bindings | New Fast all matches in source order; Deep tests overlapping rules with different actions but not two identical rows with distinct saved positions | **DERIVABLE_OR_TEST_GAP.** Add a metamorphic example: duplicate an identical row at a new saved position; result row count increases by one, ACL group count stays one. No owner interview needed |

**Materiality statement:** H-01 is a clear owner-visible unpreserved decision. H-02 is a relevant explicit directional semantics gap, though arguably inferable. H-03 needs carefully bounded semantic review, not a fabricated new decision. H-04/H-05 are better expressed as tests/invariants, not owner questions. These classifications are a **post-hoc analytic judgment**, not an independent reviewer or new user approval.

### Why five Deep counterexamples were inadequate

Deep A1–A5 all chose pairs already explicitly solved by its supplied D1–D24: permit/deny multiplicity, repeated ACL placements, three kinds of empty/missing result, global ACL after relevance, unsupported protocol. **Five resolved checks demonstrate consistency of familiar scenarios, not discovery of missing requirements.** No challenge forced a search for uncovered *query-port defaults*, *reverse direction*, *non-time additional ACL attributes*, or *duplicate identical row occurrences*. The stop gate did not compare claim coverage against a bounded dimension × state × interaction matrix or deliberately challenge the least evidenced classes.

## 4. What the evidence supports

| Observation | Supported conclusion | Unsupported claim |
| --- | --- | --- |
| Fast had 24 reported questions over five rounds; owner reported explicit overall confirmation | Batch interview produced a sufficiently coherent owner-accepted *reported* result for this pilot | Every literal question/response or approval transition is independently verified; comparative efficiency is measured |
| Standard classified R01–R08 and did not re-ask accepted decisions | Deduplication and engineering-vs-owner scope separation were applied | Standard increased semantic recall or verified all critical missing classes |
| Deep found 0 new owner questions and resolved 5 tested counterexamples | Known scenario meanings are mostly internally consistent in tested cases | Deep proved no significant omission remained |
| Prior accepted D-009/D-011/D-004 reveal unrecorded or less explicit meanings | The **new three-step stop decision was overconfident** relative to available evidence | A broader product implementation is blocked; or all remaining gaps require new owner interview |
| Separate B/C P1 were stopped for UX burden | One-question-per-turn and repeated confirmations were poorly suited to this owner's workflow | Original native Spec Kit/combined method is intrinsically ineffective |

**M1/M2:** not computable for P1 without verbatim questions and an independent reviewer; the P0 frontiers exist but do not establish P1 recall. **M3:** a numeric 0–18 blind score would be misleading; not assigned. **M4/M7:** full assumption/correction history missing. **M5:** subjective excessive owner burden reported for B/C, no measured minutes or counts. **M6:** methodological stop **not validated**; H-01/H-02 demonstrate missed explicit historical semantics, so a strict unqualified `COMPLETE` claim is unsound. **M8:** time/tokens unknown. **M9:** observed three-step mechanics, not proven native-skill fidelity. **General verdict:** `OPERATIONAL_FSD_PILOT_COMPLETE / INDEPENDENT_METHOD_VALIDATION_NOT_PERFORMED`.

## 5. Proposed next iteration — change candidate, not yet validated

Preserve **a single batch interview interface** across all depths. An internal analyser may be sequential, but the owner should receive only a **deduplicated, dependency-ready bundle** (suggested maximum 3–7 owner-actionable questions), with one final normalized confirmation per batch—not confirmation after every answer. An already answered question may be reopened only with an explicit conflicting source and a concrete, consequential distinction. No artificial minimum number of questions.

**Fast / Rapid elicitation:** brief → goal & choice tree → independently answerable frontier → owner batch → one approval → durable D record. Keep question-to-decision provenance and change/supersession, not just a final consolidated summary.

**Standard / Coverage audit:** using *frozen Fast results*, perform mandatory **dimension × value/state × outcome** checks before declaring no questions. For Checker at minimum: source/destination IP, proto, src/dst port defaults/wildcards, direction/reversal, zero/one/many candidate FW, ACL placements, snapshots missing/present, extra matching vs display-only conditions, matching row multiplicity. Mark each cell `SOURCE`, `APPROVED`, `DERIVED`, `ENGINEERING`, `DEFERRED`, or `UNRESOLVED` and cite the exact D or source line; `DERIVED` requires a falsifiable example. A category that says “covered” without evidence is a *claim*, not a passing gate. Batch only unresolved high-impact OWNER issues.

**Deep / Adversarial challenge:** generate **at least one novel candidate counterexample for each critical uncovered/equivocal class**, including **metamorphic** tests (changing one dimension should change/keep the output in a predictable way) and alternative interpretations. Require *negative proof* explaining why each proposed counterexample is inapplicable, delegated or already answered, with precise evidence. Count how many distinct previously unexamined issue classes were checked; `0 novel classes` → **`DEEP_NO_NEW_COVERAGE`**, not proof of exhaustive completeness. A critical open class blocks an unqualified `DISCOVERY_COMPLETE` claim even if no model-produced questions remain.

**Stop gate:** `no critical unresolved owner choice` AND `all mandatory coverage cells have cited authority or explicit documented deferral` AND `novel challenge pass has been performed` AND `owner-confirmed meaning preserved` AND `evidence limitations reported`. Deep is optional based on risk, but a minimal **Standard coverage/termination audit** is mandatory to claim requirements readiness. Without primary Q/A, downgrade independent-consent verification.

**Operational burden metric:** record owner-active minutes (only when observable), questions sent vs uniquely useful, duplicated/rephrased/rejected proposals, clarification iterations and owner corrections. Stop B/C sessions as `ABORTED_OWNER_BURDEN`, not “Discovery failed” or "the underlying original frameworks failed."

## 6. Smallest credible next test (no owner re-interview)

1. Freeze this report and propose a **new blind reviewer packet** containing *only* the common original brief plus the new **Fast D1–D24**, no historical D-001..012, no R01–R08, no Deep or this report.
2. In a fresh, genuinely isolated session, require reviewer to find the **three most consequential unresolved or insufficiently documented observable behaviors**, with concrete input/expected-output alternatives and exact evidence checks; separate OWNER vs ENGINEERING. Do not tell them to look for ports or reverse direction.
3. Freeze reviewer output **before** exposing historic ledger; compare it against this post-hoc report and old decisions. Record missing/new true discoveries and false positives, not simply counts.
4. For a stronger mechanism test, seed known synthetic omissions into cloned requirements (a `mutation challenge`) and measure blinded detection, then replicate on at least one **different domain** and preferably with a different owner/model. Current case alone cannot validate generality.
5. Do not change approved D1–D24, historical D-001..012, candidate OpenSpec, tests/oracle or Checker code during method audit. No main merge. A blind evaluator must not access PR #48 or this report.

**Decision:** further *owner* questioning is not justified by the audit; further *method validation* is justified. A new chat is useful only for the independent reviewer packet, not for another Fast/Standard/Deep owner interview.
