# Proposal: Checker v1 controlled benchmark

## Why

Checker Lab needs one identical accepted specification for evaluating direct Codex against optional Microsoft CoderMind/RPG. The earlier CoderMind implementation in [historical PR #27](https://github.com/lehater/agentic-checker-lab/pull/27) exposed architecture drift, long planning and incomplete token accounting. A fresh benchmark must not rely on its generated code as product truth.

## What Changes

- Propose a bounded one-shot CLI Checker on **synthetic local inputs**, derived from the owner's original brief.
- Define the supported IPv4 TCP/UDP subset, exact observable output and negative cases.
- Require Clean Architecture, SOLID, KISS and YAGNI while allowing straightforward functions/callables.
- Freeze independent tests and model/tool budgets **before** running either implementation arm.

## Impact

Product implementation is not introduced in this proposal. OpenSpec strict structural validation is VERIFIED in GitHub Actions run 40605882242 using pinned CLI 1.14.3. Product acceptance, local installation, Codex/CoderMind integration and code generation remain NOT_VERIFIED. The selected IPv4/CIDR/port subset and JSON shape are **candidate engineering decisions** based on historical PR #27, not pre-approved facts inferred from the owner's original brief.

## Evidence

- Source: `docs/scenario/owner-problem-brief.md` in main.
- Historical candidate and pre-code tests: [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27).
- Current engineering constraints: `docs/engineering/policy.md`.
