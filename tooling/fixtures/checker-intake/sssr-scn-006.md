# SCN-006 — Reconstructed requirements: check specific traffic

Status: core historical business semantics `author-confirmed`; Legacy routing/policy/live-check pipeline `verified` where preserved.

## Purpose

Given one concrete host-to-host traffic tuple, present the administrator with the relevant firewall/path facts, the stored ACL rules covering that traffic in evaluation order, contextual evidence, and—where supported—the result returned by a live vendor diagnostic. The checker itself does not synthesize a cross-vendor allow/deny conclusion.

## Requirements

### REQ-034 — Check one concrete traffic tuple
Status: `author-confirmed`; input shape `verified`

The system must support diagnostic checking of a concrete traffic tuple consisting historically of:

- source host IP;
- destination host IP;
- protocol;
- source port where applicable;
- destination port where applicable.

The preserved Legacy implementation is IPv4 host-to-host. Address-family/range support is a future design decision rather than a reconstructed historical requirement.

Provenance: `author`, `legacy-code`.

### REQ-035 — Determine all relevant firewall placements using shared candidate semantics
Status: `author-confirmed`; reuse `verified`

The traffic checker must identify every firewall placement relevant to the tuple using the same routing/correction candidate concept reconstructed in `SCN-002`, rather than inventing a separate path-selection algorithm.

The result should preserve enough placement context to explain the path, including logical firewall identity and relevant ingress/egress or policy-placement information where available.

Provenance: `author`, `legacy-code`, `legacy-db`.

### REQ-036 — Show all stored policy rules covering the tuple in policy order
Status: `author-confirmed`; matcher/order `verified`

For each relevant firewall/policy placement, the checker must be able to show all stored ACL/policy rules whose normalized semantics cover the supplied traffic tuple.

The result must preserve policy evaluation order and include both permitting and denying rules. Historically the operator used this ordered evidence to understand the configured policy rather than receiving only a single opaque allow/deny value.

Relevant rule information includes, as applicable:

- firewall and ACL/policy identity;
- rule order/number;
- action;
- protocol/service;
- source/destination ranges;
- source/destination ports;
- policy context/zones;
- hit count;
- snapshot/update time.

Provenance: `author`, `legacy-code`, `legacy-db`.

### REQ-037 — Preserve no-match as an evidence fact
Status: `author-confirmed correction`

If a firewall/enforcement attachment is relevant but no stored rule covers the tuple, the checker must present that fact without converting it into an application-level allow/deny verdict.

The operator may interpret absence of a matching rule using their knowledge of the concrete firewall/policy model.

The stored snapshot remains last-known evidence rather than guaranteed live state.

Provenance: `author`.

### REQ-038 — Provide diagnostic context without changing candidate/policy semantics
Status: observed; business usefulness implicit in UI

The checker may enrich the result with contextual information useful to the operator, historically including:

- matching historical requests;
- source address description/group/owner/site/administrator;
- destination address description/group/owner/site/administrator.

Such context is presented alongside the result but must not silently redefine firewall relevance, policy matching, or produce a synthesized verdict.

Provenance: `legacy-code`.

### REQ-039 — Support stronger live behavioral verification where a device provides it
Status: `author-confirmed`; Cisco mechanism `verified`

Where the firewall/vendor provides a reliable behavioral simulation/diagnostic, the checker should be able to execute it against the concrete traffic tuple and show its result separately from stored-policy analysis.

Historically Cisco ASA `packet-tracer` was considered a highly trustworthy, effectively authoritative check of how that firewall would process the supplied tuple and could return allow/drop plus diagnostic reason/details.

The requirement is the ability to present live behavioral evidence where supported. Cisco `packet-tracer` returns its own action/reason facts; the application does not generalize that vendor-specific mechanism into the universal definition of traffic verdict.

Provenance: `author`, `legacy-code`.

### REQ-040 — Preserve evidence source and freshness distinctions
Status: `author-confirmed` As-Is basis; evidence layers `verified`

The checker combines evidence with different confidence/freshness characteristics:

- relevant-device discovery from routing/correction data;
- stored-policy matching from the last successful normalized ACL snapshot;
- optional live-device behavioral verification.

Stored routing/policy evidence historically operated best effort and did not guarantee live truth. The result must retain sufficient provenance/timing information for an operator to distinguish stored facts from live device-returned facts.

The exact To-Be confidence/warning/blocking policy is deferred to requirements audit.

Provenance: `author`, related `SCN-002` and `SCN-004`, `legacy-code`.

## Rules / operating semantics

### RULE-018 — Routing relevance and access permission are separate
Status: `author-confirmed`

A firewall can be relevant to the traffic path without containing a rule that permits the traffic.

Conceptually:

`relevant firewall != matching rule != permit`.

### RULE-019 — Matching rule order is semantically significant
Status: `author-confirmed`; output order `verified`

When multiple stored rules cover the tuple, the checker must preserve their ACL/policy order because ordered firewall policy evaluation affects which rule is effective.

Legacy showed all covering permit/deny rules rather than discarding later/earlier matches during presentation.

### RULE-020 — No explicit match remains an uninterpreted checker fact
Status: `author-confirmed correction`

A relevant enforcement context with no matching stored rule is reported as "no matching configured rule found".

The checker does not infer implicit deny, effective rule, or blocking point. Policy-processing interpretation remains with the operator or with an explicit vendor diagnostic such as packet-tracer where available.

### RULE-021 — Source port was technically modeled but historically low-significance
Status: `author-confirmed` historical practice; implementation `verified`

The checker technically carries source port through stored-policy matching and live checks. In historical operations, requested/configured ACL access normally did not constrain source port, so the value was commonly an arbitrary/high ephemeral port such as `65535`.

Future implementations should not erase source-port semantics if a supported policy genuinely constrains them, but should not overstate their importance based on the Legacy UI field alone.

### RULE-022 — Stored analysis and live verification are distinct evidence layers
Status: `author-confirmed`

Stored ACL matching explains what the application's last-known normalized model says. Live device diagnostics, where available, test current device behavior more directly.

Legacy Cisco ASA packet-tracer supplied a stronger live-device fact than indirect stored/model evidence. No historical generic disagreement-resolution workflow is reconstructed; a future implementation should expose evidence sources separately rather than silently synthesize a verdict.

## Shared dependency on SCN-002

SCN-006 consumes the relevant-firewall candidate semantics reconstructed in `SCN-002`, including its historical limitations around local routing knowledge, correction/enrichment factors, NAT representations and best-effort evidence.

Do not duplicate or fork that candidate model solely for the checker.

## Shared dependency on SCN-004

Stored ACL matching consumes the last-known successful normalized policy snapshot from `SCN-004`. Snapshot timestamp/freshness remains relevant to interpretation.

## Historical implementation not promoted to business requirement

- literal SQL procedures `FindFirewallMain` / `FindACLMatch`;
- Django page/table layout;
- Cisco ASA command syntax;
- sentinel port values used for ICMP;
- fixed vendor-specific permission checks.

## To-Be audit notes

Future requirements audit should decide:

- whether source port should normally be explicit, inferred or defaulted;
- how to represent freshness, completeness and confidence for routing and ACL snapshots;
- how live verification can be generalized across vendors;
- how evidence from stored/model sources and optional live behavior should be presented without inventing a universal verdict.
