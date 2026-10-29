# Run record — create a separate copy for each blinded participant

**DO NOT PREFILL METHOD ID in evaluator-facing copy.** Operator stores arm mapping offline until primary scoring closes. Questions must be preserved verbatim, including recommendations that may bias owner answers.

```yaml
run_id: "unassigned"
anonymous_evaluation_id: "unassigned"
arm_private_to_operator: "A|B|C"
start_date: "UNKNOWN"
source_brief_git_blob: "0061b6f982c015785b59cad4b1b8c9fb95478617"
spec_seed_used: false
model: "UNKNOWN"
model_effort: "UNKNOWN"
execution_mode: "NATIVE_SKILL|NATIVE_COMMAND|PROMPT_EMULATION|UNKNOWN"
skill_command_revision: "UNKNOWN"
workspace_isolated: "UNVERIFIED"
memory_disabled_or_temporary_chat: "UNVERIFIED"
connected_sources_disabled: "UNVERIFIED"
prior_owner_exposure: "KNOWN_POSSIBLE"
owner_active_minutes: "UNKNOWN"
elapsed_minutes: "UNKNOWN"
tokens_input: "UNKNOWN"
tokens_output: "UNKNOWN"
p0_frozen_at: "UNKNOWN"
p0_artifact_checksum: "UNKNOWN"
p1_budget_exhausted: false
stopping_trigger: "METHOD_COMPLETE|OWNER_STOP|BUDGET_CENSORED|BLOCKED|UNKNOWN"
method_complete_claim: false
questions_published: 0
owner_questions_answered: 0
approved_normalized_decisions: 0
unresolved_owner_questions: 0
```

## Phase P0 — published verbatim frontier (frozen before owner answers)

Paste exact published question(s), recommendations, ordering, prerequisites, and method's initial reasoning; if the native tool publishes one question at a time, keep only the first question here. Do not fabricate its hidden queue.

## Phase P1 — answer/approval log

For **each** owner-facing question:

```text
Q-local-ID / round / timestamp:
verbatim question:
why asked / source evidence / predecessor:
owner answer verbatim or consented short quotation:
agent normalized meaning:
owner explicitly approved? YES / NO / PARTIAL:
new dependency discovered:
status: ACCEPTED / OPEN / DEFERRED / CORRECTED
alternative(s) rejected or unconfirmed:
```

## Final state and stop rationale

- Approved meaning list: ...
- Open owner decisions: ...
- Delegated engineering decisions: ...
- Explicitly deferred scope: ...
- Important positive example: ...
- Important negative/counterexample: ...
- Reason no further owner questions are needed (or unknown): ...
- Why this was not mere absence of model-generated questions: ...
- Tools/skill failures, forced assumptions, deviations: ...
- Links or filenames of redacted evidence: ...

## Evaluator use only (do not show participant)

- Anonymized question ID mapping, reviewer judgments, reviewer disagreements.
- Primary blind rubric results from EVALUATION.md.
- Post-unblind comparison with prior Checker ledger: separately labelled SECONDARY.
