# Engineering Policy — Clean Architecture, SOLID, KISS, YAGNI

**Owner-directed baseline for all new Checker implementation and design proposals.** These are **constraints and review questions**, not a guarantee that an LLM can independently certify design quality.

## Architecture rules (hard gates where mechanically checkable)

1. Domain holds entities/value objects and pure business rules. It must not depend on application, infrastructure, CLI, input/file adapters or external services.
2. Application owns use-case orchestration and inward-facing source ports; application can depend on domain but not on CLI, input/file or concrete infrastructure adapters.
3. Outer adapters (CLI, input, infrastructure) depend inward; wiring/composition stays at the outer boundary.
4. A nested `domain/application` package is forbidden. A public `check()` use case belongs in application, while rule predicate `matches()` belongs in domain. Repository design can choose functions or types as warranted.
5. RPG skeleton and interface graphs must pass applicable checks **before** codegen. Source imports/roles must pass after codegen. Tests must reject historic example: `src/acl_checker/domain/application/check.py` importing `src.acl_checker.application.types`.
6. Schema/structural checks alone do not prove semantic correctness; human or independent evaluation reviews ownership and observable behavior.

## SOLID (review; do not mechanically count classes)

- **S**: cohesion—each module/function has a clear responsibility; use case coordination is not business-rule implementation.
- **O**: extend through existing well-defined ports where change is required, not speculative interfaces.
- **L**: substitutes preserve observable contracts and failure semantics.
- **I**: consumer ports are as narrow as present consumers require.
- **D**: higher-level policy does not import concrete outer implementation; use simple callables when sufficient.

## KISS and YAGNI (default deny speculative complexity)

- **KISS**: choose the simplest design that demonstrably meets requirements and known constraints; justify every extra layer, abstraction and cross-component hop.
- **YAGNI**: no feature, generalization, cache, DB, event bus, UI, adapter or future-compatibility framework without a current requirement, verified risk, or operational need.
- A component without explicit requirement/architecture/testing/operational rationale is `YAGNI_REVIEW`, not an automatic deletion. Exception needs a short rationale and decision owner.
- Avoid fake simplicity that violates required security, correctness, independently replaceable sources or error handling.

## Verification protocol

- **Deterministic:** scan path roles and Python imports/known cycles, validate RPG file placements, run independent behavior tests and diff submitted artifacts. Use stdlib by default.
- **Semantic review:** ownership, SRP, abstraction value, hypothetical features and hidden duplication. Record finding, evidence, suggested minimal repair and adjudication; do not silently rewrite approved design.
- **Budget:** fail early on architecture errors; no unbounded repair loop. An optimizer proposes one change at a time and re-runs frozen checks.
- **Pass conditions:** architecture pass AND independent critical behavior pass, plus explicitly dispositioned review warnings; never report quality as verified from syntax alone.

Historical CoderMind/Codex/Checker evidence in PR #27 is a regression target, not authority to mutate the specification.
