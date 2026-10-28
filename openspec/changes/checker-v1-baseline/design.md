# Design — Checker v1 experimental baseline (PROPOSED)

## Context

The owner's brief requires all matching stored ACL rules across externally identified relevant device/ACL pairs. Historical PR #27 is informative evidence, not executable input for a fair new evaluation. OpenSpec validation and owner approval are still pending.

## Goals and non-goals

Goals: a small read-only CLI; deterministic outcome; narrow domain rules; replaceable relevance/snapshot provider in the application; stable external failure semantics; independent tests.

Non-goals: firewall reachability verdict, real devices, routing/topology algorithm, packet simulation, persistence, HTTP/UI, vendor ACL parser, cache, queue, event bus, DI framework, future-feature scaffolding.

## Decisions

1. **Domain:** pure IPv4/predicate logic in `domain`; no outer imports. No orchestration, CLI or source lookup within domain.
2. **Application:** `check()` coordinates relevance, deduplication and required snapshots through narrow injected callables; invokes domain matching and builds report groups. Avoid unnecessary class hierarchies.
3. **Outer adapters:** `input` validates local documents, `cli` parses options and serializes results. Concrete in-memory synthetic providers may live in adapters; dependency direction is inward.
4. **Architecture gate:** evaluate proposed RPG `skeleton.json` *before* interface/task/codegen; check generated Python structure and imports after codegen. Fail on any `domain/application/check.py` and domain→application dependency.
5. **Verification:** independent pre-code scenarios include all matches, permit+deny preserved, CIDR/port boundaries, missing snapshots, unsupported predicates, empty relevance, immutability. Same frozen input for direct Codex and CoderMind arms.
6. **Efficiency:** compare time-to-verified-result, retries and verified token usage (or UNKNOWN) under the same declared quota. Do not optimize token count alone.

## Alternatives

A direct CLI with all logic in one file is simpler physically but couples matching with I/O and makes independent source substitution harder. Class-heavy multi-layer abstractions add overhead without a current need. Small modules and injected callable ports satisfy inward dependencies and KISS.

## Risks and open decisions

- Selected synthetic predicate subset, CLI schema, failure codes and source-provider semantics are candidate decisions based on previous PR, **not owner-approved**.
- Source-level gate cannot prove SOLID/KISS/YAGNI semantically; design review remains required.
- OpenSpec CLI 1.14.3 strict validation has passed in GitHub Actions; local setup and Codex/OpenSpec workflow integration have not been executed.
- Independent oracles must be frozen and separately reviewed before codegen; historical oracle cases are visible to the old generated candidate and are not automatically held out.
