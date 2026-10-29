# Evidence-Gated Requirements Discovery v0.1

**Status: PROPOSED until this PR is reviewed and merged.** Then this document defines an **experimental working practice**, not a proven universal framework. It does not accept product requirements or override current L1 gates.

Purpose: discover and preserve *material owner decisions* before specification while minimizing unnecessary questions and loss of meaning across chats.

## Start here

- [Methodology: when and how](methodology.md)
- [Authority Gate: who can decide](authority-gate.md)
- [Quick start / new-chat recovery](usage.md)
- Templates: [question batch](templates/question-batch.md), [decision ledger](templates/decision-ledger.md), [quality review](templates/quality-gate.md), [handoff](templates/handoff.md)

Process in one line: **Fast interview → compact Quality Gate → optional risk-triggered Deep → reviewed handoff to specification**.

Use a separate task branch and Draft PR for each active discovery. Approved product answers stay in that task's Q/D ledger, never in these example templates. Existing historical Checker decisions from PR #48 are **not automatically accepted in main** and must not be copied into current implementation authority without explicit project review.

Evidence basis: historical [iterative discovery experiment](https://github.com/lehater/agentic-checker-lab/pull/48), including Grill Me, Spec Kit emulations and mutation v1/v2. Small experiments exposed missing meaning and authority-triage errors; **effectiveness is not yet independently established**. Do not claim the method has been validated just because it is in main.

Out of scope: deciding product meaning for the owner, generating an accepted OpenSpec, automatic production code changes, or bypassing security / engineering review.
