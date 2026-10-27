# Engineering Policy — Clean Architecture, SOLID, KISS, YAGNI

**Owner-directed design constraints** for the Checker experiment. A structural validator checks only explicitly declared rules; it cannot prove architectural quality by itself.

## General engineering requirements

- **AR-01 (layers):** Domain contains pure business rules, Application coordinates use cases, outer adapters handle I/O and composition. The accepted design owns the actual mapping of packages, responsibilities and entry points.
- **AR-02 (dependencies):** Dependencies obey the allowed inward direction; no inner layer imports its outer adapters or orchestration. Detect dependency cycles that can be established from source imports.
- **AR-03 (ownership):** Responsibilities belong to their declared layer regardless of file or function naming. RPG feature ownership is checked at plan time where stable feature IDs are available; source symbol ownership is checked after codegen.
- **AR-04 (no silent pass):** Missing/invalid architecture contracts, an empty relevant skeleton or an absent source directory fail instead of being reported as compliant.
- **AR-05 (independent verification):** Architecture policy, accepted product requirements and behavior are verified separately. Valid Python imports do not guarantee correct use-case boundaries or product semantics.

The **machine-readable project contract** is [architecture-contract.json](architecture-contract.json). It selects package roots, layer dependency rules and **project-specific** responsibility mappings. The validator contains no hard-coded Checker symbols or filenames. Contract changes require architecture review; do not make invalid output pass by relaxing rules.

## SOLID (semantic review)

- **S:** modules and functions have coherent responsibilities.
- **O:** introduce extension seams only for actual variation, not hypothetical APIs.
- **L:** substitution preserves behavior, invariants and errors.
- **I:** consumer-facing ports remain minimal.
- **D:** high-level policy depends on inward contracts, not concrete adapters; small callable ports are often sufficient.

## KISS / YAGNI (semantic review)

- **KISS:** choose the least complicated solution that satisfies accepted requirements and verified constraints.
- **YAGNI:** do not add features, abstractions, caches, persistence, UI, microservices, frameworks or compatibility layers without current justification.
- Report unsupported/extra parts as YAGNI_REVIEW with evidence and proposed alternatives; do not auto-delete components based on model opinion.
- Avoid using these principles as a pretext for omitting required security, correctness, tests or error handling.

## Verification approach

**Tests primarily derive from requirements AR-01..AR-05**, with positive and negative matrices, alternative module/package names, import directions, ownership contracts and fail-closed behavior. A **single historical witness** based on [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27) ensures an observed bad RPG still fails. Do not add one test per incidental failure unless it exposes a new invariant or a gap in existing coverage.

Pre-codegen: check the CoderMind skeleton, its paths and declared feature responsibilities. Post-codegen: check Python imports, cycles and declared symbol roles, plus independent product acceptance tests. Semantic SOLID/KISS/YAGNI review remains a separate human/LLM-assisted assessment.

No new model call, native CoderMind gate or production Checker architecture validation is implied by static unit-test PASS.
