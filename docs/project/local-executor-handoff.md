# Local executor handoff — Agentic Checker Lab

**Source of truth:** main branch, AGENTS.md and docs/project/current-state.yaml. GitHub-only tooling has passed CI; NO new model-driven Checker run has been performed, no semantic AI accuracy has been established, and the candidate OpenSpec domain subset is NOT accepted.

## Preflight (isolated working branch)

    git fetch origin
    git switch main
    git pull --ff-only
    make check
    make archived-rpg-test
    python3 tools/check_requirements_trace.py
    openspec --version
    openspec validate checker-v1-baseline --strict --json --no-interactive

GitHub Actions pins @fission-ai/openspec 1.14.3 on Node.js 22. Use the same supported CLI locally before claiming comparable setup. The archived historical RPG fails the raw architecture checker **by design**; the regression test itself passes. No secrets, raw sessions, or production devices in CI.

## L1 — approve scope and freeze independent oracle (issue #32)

See the [scope comparison and pending owner decisions](l1-owner-review.md) for the observed local preflight and remaining contract/oracle questions. L1 is not complete.

- Compare docs/scenario/owner-problem-brief.md with the PROPOSED OpenSpec Checker subset. Owner explicitly accepts or rejects IPv4/CIDR/TCP/UDP/ports, JSON input and output, failure semantics. An executor cannot manufacture approval.
- Resolve open semantics; update requirements, design and docs/evaluation/checker-acceptance-catalog.json together in a PR.
- Turn all ten proposed cases CHK-001..010 into concrete immutable black-box input/expected-result fixtures; keep a truly held-out oracle inaccessible to implementation agents.
- Record approved spec, oracle and architecture hashes before any model-driven codegen. STOP on disagreements.

## L2 — real runtime integration, not simulation (issue #33)

- Record local Codex, CoderMind, OpenSpec and environment versions. Authenticate using operator-controlled login, never commit credentials.
- Intercept the actual CoderMind RPG skeleton stage BEFORE interface/codegen: run tools/check_architecture.py against the true skeleton.json. Prove invalid plans stop and corrected plans resume only after review. Bound retries.
- Capture Codex turn.completed JSONL, stage time and attempts; correlate run/task/model/config. Unknown token usage stays UNKNOWN, never zero.
- Integrate semantically grounded review per docs/engineering/semantic-review.md with limited cloud calls and independent adjudication, no automatic change to approved requirements.

## L3 — calibrate the semantic reviewer (issue #38)

- Have an independent person adjudicate the proposed labels before exposing them to any reviewer model.
- Export cases with python3 tools/export_semantic_case.py --case-id role-drift --output /tmp/role-drift.zip . The reviewer must receive ONLY the extracted case bundle; unrestricted repository access defeats hiding labels.
- Save authentic report.json and request.json per case; evaluate with python3 tools/evaluate_semantic_reviewer.py --reports-dir /path/to/reviews --require-complete .
- Record false blocks, missed violations, uncertainty, latency, model ID, prompt SHA and actually observed usage. Reserve genuinely unseen cases for final quality checks.

## L4 — direct Codex vs CoderMind controlled experiment (issue #34)

- Use exactly the same owner-accepted specifications, frozen acceptance oracle, model/config, declared budget and environment for both direct and RPG arms, with isolated worktrees.
- Both arms run the same independent acceptance + architecture checks. Only RPG additionally uses the pre-code skeleton gate. Log all failed runs, retries, interventions, wall clock, hash/version and measured tokens if available.
- Record each E2E attempt as checker-lab/run-comparison/v1: comparison_kind=process, run_id/arm, spec_sha, oracle_sha, budget_id, environment_id, model_config_sha, record_class=observed, quality, architecture, verified_by=independent-tests, elapsed_seconds, input_tokens and output_tokens (null if unavailable).
- Compare with python3 tools/compare_runs.py --input /path/to/run-records.json --minimum-per-arm 2 . Two per arm is a minimum fixture gate, NOT statistical proof; use more repetitions or paired sampling when feasible.

## L5 — optimization and model routing, then transfer test (issues #35 and #36)

- Use real stage logs to predeclare ONE narrow process change; test against frozen oracle and matched conditions.
- For model choice, comparison_kind=model permits different model configurations but still requires matched input/oracle/budget/conditions. Measure local GPU latency, correctness, cloud quota, subscription restrictions and fallback. Do not infer billing from tokens or choose a route from synthetic data.
- Implement an adaptive dispatcher only after controlled real-world evidence, and validate transferred benefit on a second independent task.

## Stop conditions and governance

Any missing owner approval, unknown model access, failed architecture/behavior gate, unbounded quota request, missing telemetry, non-comparable experiment or dubious semantic judgment -> BLOCKED/INCONCLUSIVE, not PASS. Never change main directly; make one scoped PR per task. Preserve historical closed-unmerged PR #27 as evidence, never activate Harness.

**The remaining actionable work is L1–L5, all requiring the local operator or actual model access.** The repository already contains the offline checks and experiment inputs needed to begin.
