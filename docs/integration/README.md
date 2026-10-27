# Integration: accepted design → optional RPG / CoderMind

**Current direction: experimental, not E2E verified.** Harness is not used in new engineering flows. Historical bridge proposals remain accessible in the repository history and [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27).

## Authority

- Accepted requirements, domain semantics, architecture, interfaces and independent acceptance oracles: versioned specification/ADR. OpenSpec is the intended specification/change manager; actual CLI integration remains unverified.
- CoderMind/RPG: derived file skeleton, function/interface relationships, implementation tasks and code. It proposes—not approves—architectural choices.
- Architecture guard: rejects layer placement/dependency violations from RPG before codegen and checks source after codegen.
- Independent tests: final executable acceptance; model-generated tests do not replace them.
- Telemetry: descriptive evidence only, never authority over product requirements.

## Minimum input/output contracts

Input: exact source revision, requirement/design references, selected architectural constraints, allowed implementation freedoms, expected behavior and negative cases.

Output: immutable RPG snapshot with source/provenance, mapped implementation nodes, proposed deviations and unresolved choices, files/functions, model-call timing and usage when measured.

A candidate must not silently change accepted CLI, packet matching, status semantics, target scope or source-of-truth. An architecture/semantic failure yields **BLOCKED_REPAIR** before codegen.

## Non-goals

No new generic graph language, mirrored Harness capability engine, required central orchestration service or mandatory model-driven CI. Keep integration versioned and replaceable.
