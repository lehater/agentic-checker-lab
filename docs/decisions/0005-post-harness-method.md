# ADR-0005 — Spec-first research without Harness

Status: PROPOSED FOR MAIN (owner direction given 2026-10-28).

## Context

The old Harness workflow imposes unproven overhead. A complete historical Checker candidate and RPG traces exist in [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27), including semantic drift, expensive planning and an undetected layer violation. User wants Clean Architecture, SOLID, KISS, YAGNI and efficient local/cloud routing, not local-first token minimization.

## Decision

Retire Harness from current instructions. Preserve its artifacts/history and PR #27; do not mechanically merge a historical Harness-bound workflow. Use accepted specifications (OpenSpec integration to be validated), direct Codex as baseline and CoderMind as an optional realization tool. Gate architecture before/after codegen; collect telemetry before optimizing; compare outcomes under equal inputs and resource budgets. AI Lab owns only shared infrastructure if justified by a real consumer.

## Consequences

- New project docs no longer require the Harness API.
- Historical Make targets and test fixtures remain until an independently tested cleanup, avoiding destructive broad changes.
- OpenSpec/CoderMind/model router are **not** considered installed, integrated or verified from this ADR alone.
- No expensive model calls or main branch merges by documentation change.
