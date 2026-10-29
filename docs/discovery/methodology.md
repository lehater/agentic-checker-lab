# Evidence-Gated Requirements Discovery — methodology v0.1

**Status:** experimental working practice. Owner answers remain the only authority for owner-controlled product meaning. The active \`main\` baseline and [engineering policy](../engineering/policy.md) still apply.

## When to run

| Situation | Action |
| --- | --- |
| New feature, behavior change, unclear acceptance, competing user-visible outcomes | Run **Fast** and **Quality Gate** |
| Existing accepted Q/D records fully cover requested change | Link those records; **do not re-interview** |
| Technical refactoring, typo, mechanical repair with no change in observable behavior | Use normal engineering/change review, not full Discovery |
| High risk, many actors/states, conflicting sources, missing-data/security consequences | Trigger **Deep** after compact Quality Gate |
| Owner answer unavailable | Mark unresolved and **BLOCK**, or explicitly agree to defer; never invent acceptance |

A query must distinguish owner-visible meaning from engineering choices delegated in the source. No fixed target number of questions.

## 0. Preflight and recoverability

1. Read **main** project entrypoint, source problem statement, relevant accepted decisions, active task branch and PR, latest committed discovery checkpoint, and any already approved scope. When resuming in another chat, reconstruct from **GitHub**, not conversation memory.
2. Identify goal, out-of-scope work, user actors, requirements authority and dependency order. Mark conflicting or missing evidence; draft OpenSpec is **not** an owner decision.
3. Decide whether a new interview is necessary. If not, cite existing Q/D and proceed to the Quality Gate or normal engineering.
4. Create a task branch/Draft PR when persisting a new Discovery; use the [ledger template](templates/decision-ledger.md) in a task-specific directory. Do not write directly to main.

## 1. Fast — one bounded interview loop

1. Generate the dependency-ready **frontier** of material owner decisions. Check each candidate against prior answers and [Authority Gate](authority-gate.md); source facts, already accepted decisions and engineering details are **not owner questions**.
2. Batch independent questions, typically **3–7**. A smaller batch or **zero** is fine. For each provide Q-ID, concrete alternative behavior, why it matters, evidence and dependencies. No repetitive one-at-a-time confirmation.
3. Save prepared questions in the task branch **before asking** if a durable experiment is required, so interrupted interviews can recover the exact wording. Do not create a ceremonial round solely to satisfy a counter.
4. Owner answers in free form. Normalize Q → answer → proposed D with source and a **positive/negative example** for material meaning. Preserve negation, quantifiers, scope, error/no-data states. Clearly separate **suggestion** from owner's answer.
5. Confirm the whole normalized **batch once**. A correction is incorporated and reviewed; silence is never consent. Do not mark D as ACCEPTED until explicit confirmation.
6. Commit accepted answers and approvals with stable IDs and a checkpoint SHA; retain superseded decisions and their relationships. Continue only if a real new frontier remains.

**Stop interview** when there are no unresolved, dependency-ready owner questions; this is **not yet** permission to say that discovery is complete.

## 2. Quality Gate — required, compact and read-only

Run once after the last Fast batch and on a material requirements change. Use the [review template](templates/quality-gate.md). Scan at minimum:

- Five dimensions of **input**: required/missing/default/wildcard/invalid and direction or ordering where applicable.
- **Entity/state/cardinality**: none/one/many, identity, duplicates, visibility of empty results.
- **Result/evidence**: success/no match/missing data/stale or unavailable data/error; do not convert unknown into false.
- **Cross-rule consistency**: permissions, conflicting policies, precedence, all-vs-first match, extra constraints, time-related boundaries, and scope.
- **Scope/verification**: cited D/source for each material case; deliberately delegated engineering work and exclusions recorded separately.

For every uncovered or disputed **user-observable** branch apply Authority Gate; cite **exact** evidence for derivation or delegation. Ask the owner only about newly demonstrated material decisions, in **one deduplicated batch**. If zero genuinely new questions, do not manufacture them. Run Quality Gate again only for changed areas after an answer.

**Quality Gate output:** no critical unresolved owner choices; any contradictions and assumptions logged; at least one nontrivial negative/alternative scenario per critical rule; unresolved engineering choices listed for subsequent spec review; provenance limits explicit. A model assertion "all covered" without citations is insufficient.

## 3. Deep — opt-in, bounded challenge

Trigger only for documented reason: safety/security impact; high-value financial/operational loss; multiple interacting states/paths; contradictory authority; repeated semantic losses; materially weak Quality Gate coverage. Otherwise **SKIPPED — NO RISK TRIGGER**.

Challenge **weakly evidenced, not already-settled** combinations and metamorphic transformations. Examples: changing one parameter should change/no-change a result; duplicating a rule must not collapse distinct row occurrences; removing all relevant entities must not imply deny. Specify which unexamined class the challenge tests; repeated easy examples do not count as added coverage. Stop after a bounded set (default 3–5 novel critical challenges) or when no materially new risk remains; reason about remaining risk explicitly.

Deep does **not** automatically generate another owner interview. Apply Authority Gate to any discovered gap.

## 4. Completion, handoff and change control

Allowed statuses: \`READY_FOR_SPEC_REVIEW\`, \`NEEDS_OWNER_DECISIONS\`, \`BLOCKED_EVIDENCE\`, \`DEFERRED_WITH_SCOPE\`. A status is always accompanied by reasons; \`READY\` is **not** product specification approval.

Only claim \`READY_FOR_SPEC_REVIEW\` when:
1. Scope/goal and all critical user-visible choices are source-backed, owner-accepted or validly derived.
2. No conflicting accepted requirement or unjustified owner-choice assumption remains.
3. Required Quality Gate completed with concrete counterexamples; Deep either justified or explicitly skipped.
4. Every retained Q/D has provenance; non-owner technical obligations and explicit deferrals are visible.
5. Owner has approved normalized decisions, and checkpoint has been committed, with independent semantic review requirements disclosed.
6. Handoff maps D IDs to spec obligations/scenarios or flagged gaps; approval of spec/oracle remains a **separate** gate.

Use [handoff](templates/handoff.md). Engineering must not silently promote an interview answer, candidate spec or CI structural PASS into approved product semantics.

## Governance, efficiency and constraints

- Scope: one task, one branch, small PR. GitHub is the durable state. If writes fail, mark \`BLOCKED_EVIDENCE\`; do not claim committed status.
- Stable IDs \`Q-xxx\` and \`D-xxx\`. Corrections preserve history; major changes supersede old decisions instead of silently rewriting. Retain source and approval evidence, but avoid posting secrets, private transcripts or raw audio to a public repository.
- Measure: unique material questions, repeat/low-value questions, owner corrections, semantic loss, checkpoints, new gaps from Quality Gate/Deep, owner-active minutes where observed, and \`UNKNOWN\` when not.
- The experiment in PR #48 produced 24 reported Fast questions and zero new Standard/Deep questions. Mutation testing found some misses and unstable authority triage. **No evidence yet proves that a full separate Deep stage is worth default cost.**
- **Do not modify** project state, local-executor L1–L5 gates, independent acceptance oracle, code or \`main\` merely by applying this methodology.
