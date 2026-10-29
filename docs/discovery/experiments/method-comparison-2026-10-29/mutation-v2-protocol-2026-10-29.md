# Discovery Authority Gate v2 — Cross-domain Mutation Pilot

**Date:** 2026-10-29. **Status:** PREREGISTERED / CASES NOT YET RUN / EVALUATOR IDENTITIES HIDDEN. This is a methodology experiment, **not** approval or implementation of either product.

## Hypotheses

H1: An evidence-based authority gate distinguishes an unresolved business-observable choice from an explicitly delegated engineering choice.
H2: The gate detects a direct contradiction between requirements without silently prioritizing either one.
H3: The gate does not manufacture owner questions merely because working requirements lack a verbatim approval transcript.

## Test structure

- Four isolated single-file evaluator cases from **two domains**: the historic, approved Checker requirements and a **fictional** small shared-meeting-room booking product. The latter is an intentionally synthetic test fixture, **not** a claim about any real user's requirements.
- Each domain has one unmodified control and one case with **one local semantic mutation**. Mutations cover a **removed product rule** and a **directly conflicting rule**; each is judged separately. There is no assumed prevalence of flaws in a real product.
- All cases have their **own complete brief, numbered requirements and identical evaluator instructions**. No evaluator may see any other case or public protocol, historical accepted Checker ledger, mutation answer key or previous experimental reports.
- The **Checker baseline** is the historic accepted D-001..D-012, used here solely as a frozen gold reference; it does **not** overwrite or merge the separate Fast D1..D24 experiment. The meeting-room baseline is a fictional, explicitly stated reference, not owner-confirmed history.
- Mutation file IDs are opaque. The hidden operator key, file digests and variant mapping are kept in a **private workspace outside the public GitHub repo**, and are revealed **only after four reviewer outputs are recorded**.
- Four separate Temporary Unpersonalized Chats, one per file. Model/effort should be the same if possible. No connectors, GitHub, web, memory, cross-case references. Where isolation cannot be technically proved, mark `BLINDING_UNVERIFIED`.
- **Zero additional owner interviews**: evaluators report candidate issues, not ask the product owner to resolve them.

## Required evaluator output

A) Coverage review, especially user-visible boundaries and negative cases.  
B) No more than **six** candidate issues. Every candidate must include (i) exact requirement source, (ii) concrete scenario, (iii) **two observably different outcomes**, (iv) classification `OWNER_UNRESOLVED | SOURCE_CONTRADICTION | ENGINEERING_DELEGATED | DERIVED_FROM_SOURCE | OUT_OF_SCOPE | EVIDENCE_ONLY | NEEDS_PROOF`, (v) explanation of why a source settles or does not settle it, and (vi) owner-question relevance.  
C) One stop verdict `SUFFICIENT | INSUFFICIENT | SUFFICIENT_WITH_KNOWN_GAPS` with justification. Do not infer existence of a planted defect from this request.

**Authority gates**: `DERIVED` needs an entailment that rules out alternative behavior, and `ENGINEERING` requires an applicable explicit delegation. Contradictory normative requirements cannot be reconciled by preference or assumed publication order. Lack of raw approval transcript must be marked separately, not treated as a new functional question.

## Preregistered scoring

Compare outputs against the private answer key only after all four are frozen.

- `TARGET_DETECTED`: exact seeded behavioral gap/contradiction described with competing outcomes (not just generic uncertainty and not just an `INSUFFICIENT` verdict).
- `TARGET_TRIAGED`: unresolved business-observable policy correctly recognized as owner authority, or source contradiction recognized as such; `NEEDS_PROOF` with precise evidence is partial, not full.
- `TARGET_MISCLASSIFIED`: target discovered but incorrectly asserted `DERIVED`, inapplicably `ENGINEERING`, or safely `OUT_OF_SCOPE`.
- `TARGET_MISSED`: target behavior not discussed.
- `CONTROL_SPURIOUS_OWNER`: proposed owner issue where the control directly determines behavior, engineering delegation is explicit, or source cited does not support proposed alternative. Other plausible open cases receive `REVIEW_REQUIRED`, not automatic false-positive labels.
- Record `stop correctness` separately, along with issue counts and any unverified provenance; do **not** equate an `INSUFFICIENT` stop with detection of the hidden target.

**Before scoring**, verify package manifest, individual SHA-256 hashes, one mutation per variant, identical prompt and independent case isolation. If materials differ more than stated, mark `INVALID_CASE`. This is a small descriptive pilot (two changed cases), **not** a statistical estimate; do not infer superiority over native alternative frameworks or general deployment readiness.

## Operations / boundaries

1. Freeze this plan; prepare all cases, operator-only key and manifest.
2. Review one input per temporary chat. Copy responses verbatim to an operator-only workspace. **No feedback to other evaluators.**
3. After four outputs, decode case roles and score against private key and this rubric. Flag any ambiguity in mutation ground truth.
4. If evidence suggests success, replicate with new undisclosed mutations, new reviewers/models and another non-Checker domain before any claim of validated method.

Never modify main, historical Checker ledger, Fast D1..D24, product OpenSpec, code, oracle or GitHub issue statuses because of these review outputs. Keep Draft PR #48 Draft.
