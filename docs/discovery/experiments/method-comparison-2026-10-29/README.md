# Requirements Discovery method comparison — preregistered pilot

**Status:** DRAFT EXPERIMENT PLAN / NOT EXECUTED. **Date:** 2026-10-29. **Primary objective:** evaluate methods for *discovering necessary owner questions* and *justifying interview termination*, **not** implement Checker, approve its candidate OpenSpec or demonstrate cross-task generalization.

**Planning branch:** `experiment/iterative-discovery-protocol`, Draft PR #48. Plan is stored here for audit only; **do not give this branch or PR to a blind participant**. Owner-facing participants get only the isolated input packet. Planning this comparison does not modify accepted Q/A/D or the original discovery process.

## 1. Arms and hypotheses

| Arm | Mechanism | Native source / fidelity note |
| --- | --- | --- |
| A — Grill Me | Tree of decisions and prerequisite-ready frontier, with owner confirmation | Matt Pocock's [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) + [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md); skill blobs `df69d9936880cd3314c28858c6c52f48db23b856`, `3947ff9c4ad980d14fc07fccbf659d47c114e81d` |
| B — Spec Kit Clarify | Ambiguity/coverage taxonomy, impact × uncertainty, at most five questions **per command invocation** | GitHub [Spec Kit clarify](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md), source blob `f48d8bd703d7eb3fe4eadf2d3d283ca508e6bb80` |
| C — Combined candidate | Goal/scenario/data/evidence-state coverage scan → dependency frontier → Example Mapping/counterexamples → explicit completeness gate | **Our unvalidated composite proposal**; not a verbatim execution of all third-party frameworks |

**Hypotheses (pre-specified, not results):** H1, C finds more *material, owner-actionable* unknowns than A at similar owner attention; H2, B flags more uncovered *categories* than A; H3, the combined completion gate produces fewer unsupported `complete` claims; H4, the extra coverage checks may incur unacceptable noise/time. Null outcomes and ties are permissible.

**OpenSpec Explore is NOT an arm:** it is exploratory conversation and does not prescribe a complete coverage questionnaire; downstream specification generation is deliberately excluded.

## 2. Exactly equal task input; no spoilers

- Source is [original owner brief](../../../scenario/owner-problem-brief.md) with Git blob **`0061b6f982c015785b59cad4b1b8c9fb95478617`**. Copy frozen text from [inputs/checker-brief.md](inputs/checker-brief.md) **verbatim**. The full prior ledger/rounds/spec/Completeness Review/semantic audits MUST NOT be shared with participants.
- B requires a Spec Kit feature spec; [inputs/spec-kit-neutral-seed.md](inputs/spec-kit-neutral-seed.md) is a **neutral wrapper around exactly the same original brief**, not a previously refined specification. Record this input-format asymmetry: it is necessary for B and could affect results.
- For native tools, install all arms in separate **clean workspaces**. No old `AGENTS.md`, issue history, PRs, spec drafts, project files or corpus retrieval. With ChatGPT-only prompt emulation, record `PROMPT_EMULATION`; never present it as native skill execution.
- Start **three fresh temporary/memory-isolated chats** where possible; turn off memory and project/history connections for participants. A *new normal chat with explicit “ignore history” instruction is not proven blind*. For the strictest test, use separate workspace with no GitHub connector/web access to the original repo. If isolation cannot be guaranteed, record `BLINDING_UNVERIFIED` and downgrade any comparison claim.
- The owner's prior knowledge cannot be erased; this is a **known single-owner carryover bias**. Capture order of runs and whether earlier answers affected later ones. For confirmatory evidence, repeat with a different case/owner and randomized order; one Checker case remains only a pilot.
- Each arm uses the same model/build/effort, language, tool budget where possible; record skill/command revision, actual execution mode, available tools, active owner time, token usage if observable (otherwise `UNKNOWN`).
- **No participants may read planning `README.md`, [evaluation](EVALUATION.md), historical Checker ledger, old PR #48, earlier chats or outputs of rival arms.** Give only the relevant exact entry prompt and input bytes.

## 3. Two-phase test, with gates

### Phase P0 — independent question discovery (no owner answers)

1. Open fresh isolated participant session with the same brief. Invoke the assigned **native** method, or label explicit emulation.
2. Ask it to find questions; capture the **first published askable frontier** verbatim, its dependencies/reasons, uncertainty classifications and claimed stopping/continuation criteria. Do not answer questions yet.
3. Commit or save this P0 artifact, **timestamp and method/version**, before showing the owner or running another arm. Evaluator receives a redacted version with arm names removed.
4. Preserve natural method behavior: A may output a frontier of many questions; B asks **one question at a time** and allows at most **five per invocation**; C may group independent issues. **Do not force a uniform number of generated questions.** Normalize scoring at `first 5` and `per owner minute` where comparable; report number/order, not just counts.

### Phase P1 — adaptive interview, strictly after P0 freeze

1. The same owner answers only published owner-decision questions; agent verifies facts independently from the supplied source, separates engineering choices from owner meaning, and never fills in substantive owner choices on its own.
2. Within a common budget of **45 minutes of owner-active interaction per arm** (not cumulative agent waiting), allow each method's native number of rounds; B may repeat `/speckit.clarify` sessions as needed (**five per invocation is not a total-discovery limit**). If timing is infeasible or interrupted, mark `TIME_UNVERIFIED` and do not compare cost-adjusted outcomes.
3. After each owner response, require a short normalized interpretation and explicit confirmation before treating it as accepted. This is a **common safety/measurement wrapper** for all arms, and may deviate from native defaults; disclose this in the run record.
4. On each new question, capture its origin: initial ambiguity, prior answer dependency, negative example, entity-state boundary, contradiction, or speculation. If the owner cannot decide, mark `OPEN` or `DEFERRED`, **not** silently answered.
5. Stop if the method independently asserts sufficient discovery, the owner stops, or the common budget is reached. Record **which** stop trigger applied and the exact unfinished questions; a budget stop is `CENSORED`, not `COMPLETE`.
6. Save final normalized owner answers, proposed decisions, evidence, open issues, owner corrections and a method-specific **reason why no more questions are necessary** (or explicit inability to claim completeness).

### Evaluation gate — after all arms finish

1. Remove method labels and distinctive prompt references from outputs; save frozen anonymized records for one or preferably **two reviewers**.
2. Before reading any outputs, reviewer establishes an independent rubric from the original brief and general requirements-analysis categories — **not** a list of the nine historical Checker questions as a target. The broad rubric below is preregistered.
3. Reviewer scores *material owner decision opportunities* separately from engineering, source facts and deferred scope; require concrete impact/example for each claimed omission. Count false assumptions, duplicates, owner corrections, missed dependencies, coverage and stop quality.
4. Only **after** blind primary scoring, compare with previous Q-001..Q-009, D-001..D-012 and prior Completeness Review as a **secondary retrospective benchmark**. Q-009 must not become the privileged single golden question.
5. Do not declare winner if execution modes, model/skill versions, available sources, owner answer distributions or time budgets differ materially. Report `INCONCLUSIVE` and causal limits, not a falsely precise score.

## 4. Required controlled outputs and storage

- [RUN_PROMPTS.md](RUN_PROMPTS.md): launcher / prompts A, B, C, exact output capture rules.
- [RUN_RECORD_TEMPLATE.md](RUN_RECORD_TEMPLATE.md): method-independent per-run records; **copy it into an isolated run workspace only after redacting other arms' names/identities**.
- [EVALUATION.md](EVALUATION.md): preregistered scoring, source evidence authority, stop tests, blinding checklist.
- [inputs/checker-brief.md](inputs/checker-brief.md): **only common user-visible task statement**; hashes and past answers are not embedded in this packet.
- [inputs/spec-kit-neutral-seed.md](inputs/spec-kit-neutral-seed.md): wrapper required by native B.
- Store completed raw transcripts in **private** separated run folders or local workspace. If repository is public, publish only consented, redacted records. Do not save model-visible gold questions or historical answers to any run workspace.
- The planning branch may hold this **preregistration** only. Create run branches or workspaces **later**, only after isolation is verified. Do not create an empty run branch from the contaminated pilot branch and call it independent.

## 5. What would count as success?

**Valid pilot data** = frozen P0 for all three arms + comparable P1 conditions (or explicitly marked noncomparable) + blind evaluation with documented reasons + no implementation of Checker. **Method improvement evidence** = new materially useful, previously missed *owner-choice* issues (not larger counts), controlled false-question burden, and a justified stop decision. **General method validated** requires replication on another problem and preferably a different owner; one Checker pilot cannot prove it.

**Pre-registration / change-control:** Once the first participant starts, freeze these criteria. Any rubric change is versioned, justified and evaluated as a separate exploratory analysis; never silently modify definitions after seeing answers.
