# Minimal candidate: synthetic Checker

Status: PROPOSED test candidate; not a verified implementation.

1. Domain pure function matches(flow, rule) implements exactly supported IPv4 CIDR, protocol and inclusive port matching.
2. Application check(flow, relevance_provider, snapshot_provider) deduplicates device/ACL pairs, requires each relevant snapshot and returns every matching rule in stored order.
3. CLI adapter validates local JSON, composes the use case and presents text or JSON; no network access.
4. Application imports only domain. Domain imports no application, CLI, input, persistence or external APIs.
5. No database, persistent cache, CQRS, event bus, DI framework or extension framework.
6. Missing snapshot or unsupported predicate fails the entire query, without an invented permit/deny verdict.
