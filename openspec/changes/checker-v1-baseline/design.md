# Design — Checker v1 experimental baseline (PROPOSED)

## Context

The owner's brief requires all matching stored ACL rules in the full provided relevant firewall → ACL → rule hierarchy. Historical PR #27 is informative evidence, not executable input for a fair new evaluation. OpenSpec validation and owner approval are still pending.

**Proposed concrete CLI/JSON example (not accepted):** [Checker v1 contract proposal](../../../docs/evaluation/checker-v1-contract-proposal.md). This contract is for consolidated owner/engineering review and is not an independent oracle.

## Goals and non-goals

Goals: a small read-only CLI; deterministic outcome; narrow domain rules; replaceable relevance/snapshot provider in the application; stable external failure semantics; independent tests.

Non-goals: firewall reachability verdict, real devices, routing/topology algorithm, packet simulation, persistence, HTTP/UI, vendor ACL parser, cache, queue, event bus, DI framework, future-feature scaffolding.

## Decisions

1. **Domain:** pure IPv4/predicate logic in `domain`; no outer imports. No orchestration, CLI or source lookup within domain.
2. **Application:** `check()` consumes a synthetic provider of relevant firewalls, including firewalls with zero ACL, and distinct ACL placements; it deduplicates ACL groups by (firewall, ACL identity) while preserving identical stored row occurrences and builds the full hierarchy. Narrow injected callables remain sufficient. Avoid unnecessary class hierarchies.
3. **Outer adapters:** `input` validates local documents, optional source/destination ports as integers or `any`, and defaults omitted ports to unconstrained. `cli` parses options and serializes results, including per-ACL last-success timestamps and display-only supplemental rule conditions. Concrete in-memory synthetic providers may live in adapters; dependency direction is inward.
4. **Architecture gate:** evaluate proposed RPG `skeleton.json` *before* interface/task/codegen; check generated Python structure and imports after codegen. Fail on any `domain/application/check.py` and domain→application dependency.
5. **Verification:** proposed independent pre-code scenarios cover wildcard/omitted ports, one-way direction, all matches, permit+deny, identical row occurrences, CIDR/port boundaries, supplemental attributes, zero ACL/zero FW hierarchy, per-ACL timestamps (not a running collector), missing/corrupt snapshots, and immutability. **These are not yet a frozen independent oracle.** Same approved frozen inputs must be used for both later implementation arms.
6. **Efficiency:** compare time-to-verified-result, retries and verified token usage (or UNKNOWN) under the same declared quota. Do not optimize token count alone.

## Alternatives

A direct CLI with all logic in one file is simpler physically but couples matching with I/O and makes independent source substitution harder. Class-heavy multi-layer abstractions add overhead without a current need. Small modules and injected callable ports satisfy inward dependencies and KISS.

## Risks and open decisions

- IPv4-only subset, concrete JSON/CLI envelope, fail-atomic contract, supported predicate grammar and provider shape are **proposed engineer-delegated decisions, not accepted owner choices**. Missing first successful snapshot is not NO_MATCH; optional port semantics and hierarchy are from recorded D-009/D-012, which still require L1 spec-level reconciliation and review.
- Source-level gate cannot prove SOLID/KISS/YAGNI semantically; design review remains required.
- OpenSpec CLI 1.14.3 strict validation has passed in GitHub Actions; local setup and Codex/OpenSpec workflow integration have not been executed.
- The collector's failed-refresh preservation invariant from historic D-008 is **not executable in this synthetic-only slice**. Verify snapshot provenance in L1 and defer collector behavior to a separate future test without implying it was validated.
- Independent oracles must be frozen and separately reviewed before codegen; the updated CHK-001..016 cases are only **PROPOSED_NOT_OWNER_ACCEPTED / NOT_RUN**, visible and not held out. The independent held-out oracle must be kept inaccessible to implementation agents.
