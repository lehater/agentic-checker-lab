# Tasks — proposed benchmark, no tasks completed

## 1. Accept and validate specifications
- [ ] 1.1 Review candidate domain predicates, fields, CLI and failure semantics against the owner's source problem; record decisions or unresolved questions.
- [ ] 1.2 Run official `openspec init --tools none` (only in a disposable project copy first), check supported Codex tool integration, and validate this change with a pinned OpenSpec CLI.
- [ ] 1.3 Freeze one identical input package, explicit architecture policy and independent critical oracle for both experiment arms.

## 2. Prepare evaluation gates
- [ ] 2.1 Run the archived RPG skeleton through `tools/check_architecture.py`, record FAIL; verify a corrected sketch passes.
- [ ] 2.2 Define bounded model quotas, logging/redaction, stage/time/token counters and stop-on-failure conditions.
- [ ] 2.3 Confirm the acceptance oracle is independent of generated code, with no post-hoc rewriting.

## 3. Implement comparison
- [ ] 3.1 Implement directly with Codex in an isolated branch/workspace and record immutable evidence.
- [ ] 3.2 Implement with pinned CoderMind + equivalent Codex/provider/model and the same accepted input, stopping on a failing RPG architecture check.
- [ ] 3.3 Run identical source and behavioral checks; collect elapsed time, verified tokens or UNKNOWN, retry/repair cost and manual changes.

## 4. Review
- [ ] 4.1 Publish all results and compare quality-adjusted time/cost; explicitly report inconclusive evidence.
- [ ] 4.2 Only if candidate has demonstrable value, open a bounded optimizer experiment.
