# Mutation-testing Discovery closure and decision authority — protocol v1

**Date:** 2026-10-29. **Status:** PREREGISTERED EXPLORATORY TEST / NOT RUN. **Purpose:** independently test whether an auditor detects *missing product meaning* and correctly classifies its decision authority before declaring Discovery complete. **Not** a Checker implementation test or an authorization to change approved product decisions.

## 1. Why this test

The sequential Fast → Standard → Deep pilot and one isolated reviewer all concluded that no new owner questions were necessary. Yet the reviewer independently generated an example contrasting a missing port with a wildcard and then downgraded the choice as supposedly `DERIVED` without sufficient source authority. Historical owner-approved behavior explicitly resolved that observable choice.

The current hypothesis is that **authority triage and unsupported derivation**, not simply generating more candidate questions, is the critical gap. Compare issue discovery and authority classification as **separate outcomes**.

Historical evidence: [post-hoc FSD audit](posthoc-fsd-validation-2026-10-29.md), [reviewer adjudication](blind-reviewer-adjudication-2026-10-29.md). The full historical approved ledger and original owner brief are only the *operator's* reference; evaluators must not browse them or previous experiments.

## 2. Controlled materials

- Four blinded input variants of a **single bounded Checker requirements set**: three with one semantically meaningful clause neutralized or removed each, one unchanged control.
- Each variant contains the **exact original owner problem brief**, byte-identical to Git blob `0061b6f982c015785b59cad4b1b8c9fb95478617`, and twelve same-position, source-derived statements. The historic D numbers are not shown; `R01..R12` are only local labels. Mutation changes remove or neutralize *one product meaning*, not the surrounding technical scope.
- All four variants have the **same independent-review prompt**. Their identifiers do not convey which is the control or which meaning changed.
- Variant files and the answer key are kept **outside this public repository** until testing concludes. The operator-only answer key must be stored separately from the files sent to evaluators. Do not publish the mapping or share a folder containing it with a model.
- **Caveat:** the twelve normalized statements and test variants are **synthetic audit fixtures**. A mutated document is *not* new owner-approved semantics and is never an authoritative replacement for the original ledger.

## 3. Execution protocol

1. Record the frozen SHA-256 of each input file **before** starting any run, and store operator key in a private location.
2. Use a **new independent Temporary Unpersonalized Chat per case**, with no memory, repository access, web search, external skills, competitor results or prior Checker conversations. If this cannot be established, explicitly classify `BLINDING_UNVERIFIED`.
3. The operator attaches **exactly one case file** and sends only: `Проведи независимую проверку по файлу. Выдай один итоговый отчёт и остановись.`
4. The evaluator must **not interview the owner**. It may produce up to six significant candidate uncertainties, each with concrete input, two different user-observable outcomes, classification (`OWNER_GAP / ENGINEERING_DELEGATED / DERIVED_FROM_SOURCE / OUT_OF_SCOPE / NOT_ENOUGH_EVIDENCE`), source citation and a proposed stop verdict.
5. Preserve the evaluator's full response **verbatim** with case ID. Freeze **all four** before opening the operator key, after which post-unblinding scoring can start. Do not give later evaluators feedback from earlier results.
6. Record observable tool/model/effort version when available. Do not invent tokens or time; use `UNKNOWN`.
7. Do not change this rubric or any case material after seeing outcomes. Any revision receives a **new** version and test ID.

No acceptance or rejection decision is to be made by Checker owners as part of this test. It is designed to add **zero owner interview burden**.

## 4. Preregistered evaluation, including negative controls

**Issue detection (recall)** and **decision-authority classification (precision)** are scored separately for each known mutation:
- `DETECTED`: evaluator explicitly describes the materially different outcomes corresponding to the omitted clause, regardless of whether it asks an owner question.
- `CORRECTLY_TRIAGED`: evaluator reports `OWNER_GAP` or `NOT_ENOUGH_EVIDENCE` with a concrete unresolved owner-visible distinction and acknowledges lack of a source-supported resolution, **not** a fabricated `DERIVED`.
- `MISCLASSIFIED`: detects the two outcomes but calls one derivable/engineering solely by assumption or by delegations that do not apply.
- `MISSED`: does not mention the target distinction or only makes vague unsupported claims.
- `SOURCE_SUPPORTED_DERIVATION`: a documented, falsifiable derivation from the **input as supplied**, with exact citation, must be considered by human adjudication before labelling a finding a false negative.

For the **unchanged control**, calculate unsupported `OWNER_GAP` proposals and correctly recognized delegated/open technical scope. Not every new question on an unchanged case is automatically a false positive: reviewers must judge against the actual supplied source and a concrete observable example.

Report **per-case** outcomes, `mutated_cases_detected / mutated_cases_total`, `correctly_triaged / detected`, unsupported owner-question proposals in control, and audit notes. Avoid a weighted winner score or spurious statistical precision.

**Adjudication rule:** the grading analyst has prior exposure to historical meanings, so this first pass is **not independent or fully blind**. A second reviewer of frozen outputs and, later, tests on a different task are needed for generalizable method claims. Pay attention to borderline cases in which a narrow user-observable implication genuinely can be inferred from the remaining statements.

## 5. Completion and next decision

Stop the experiment after the four outputs are frozen and scored. If the candidate gate repeatedly downgrades unresolved owner-visible choices, revise the **authority-classification rule**; if it never surfaces those choices, revise **coverage generation**. If both are adequate but false positives rise, tighten triage and risk prioritization. Then retest with fresh hidden cases, and only later replicate on another domain.

**Not permitted:** modifying approved D-001..D-012, new Fast D1..D24, OpenSpec candidate, acceptance oracle, Checker code, `main`, or merging Draft PR #48 based solely on these test results. A successful structural CI check is not evidence of elicitation quality.

**Current status:** four variants **prepared and statically checked**, evaluator results **none**, scoring **not performed**.
