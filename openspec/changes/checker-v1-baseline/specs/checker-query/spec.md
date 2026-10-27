# Checker Query — candidate specification delta

## Purpose

Bounded synthetic ACL query CLI: match all stored rules for a single IPv4 flow against separately supplied relevant ACL snapshots, without querying network devices or issuing a global firewall verdict.

## ADDED Requirements

### Requirement: Validated one-shot query
The Checker SHALL accept exactly one explicitly selected local UTF-8 JSON input document containing a versioned IPv4 TCP/UDP flow with source and destination addresses and integer source and destination ports in 0..65535.

#### Scenario: Valid input
- **WHEN** the operator invokes the CLI with a valid local document and both port values
- **THEN** the application evaluates that flow against the provided synthetic evidence

#### Scenario: Invalid or unsupported input
- **WHEN** a required field is missing, an IP is invalid, a port is out of range, or a predicate is unsupported
- **THEN** the application rejects the request rather than silently approximating its meaning

### Requirement: Complete stored-rule matching
The Checker SHALL compare source/destination IPv4 addresses against exact addresses or canonical CIDR networks, protocols against tcp/udp/any, and both ports against inclusive ranges, returning every matching stored rule without a first-match shortcut.

#### Scenario: Multiple matching actions
- **WHEN** a snapshot contains both permit and deny rules matching the same flow
- **THEN** the returned evidence contains both original rules and actions in snapshot order

#### Scenario: Predicate boundaries
- **WHEN** an address is outside a CIDR or a port is outside an inclusive interval
- **THEN** the rule does not match

### Requirement: Relevance is a separate provided input
The Checker SHALL use the ordered sequence of provided device/ACL pairs as relevance evidence for one flow, deduplicate pairs by both keys preserving first occurrence, and fetch each required snapshot without attempting to infer live network topology.

#### Scenario: Duplicate relevance
- **WHEN** the relevance source repeats the same device/ACL pair
- **THEN** exactly one output group is produced for that pair in first-seen order

#### Scenario: Missing required snapshot
- **WHEN** a relevant device/ACL pair has no accessible corresponding snapshot
- **THEN** the entire query fails instead of inventing a NO_MATCH result

### Requirement: Preserved observation and presentation
The Checker SHALL report one group per unique relevant ACL, preserving device, ACL, placements, original matching rule fields, and MATCHES or NO_MATCH status, without computing a global permit/deny verdict.

#### Scenario: No stored match
- **WHEN** a relevant ACL has no matching stored rules
- **THEN** the group is reported as NO_MATCH with an empty rules list, not a deny verdict

#### Scenario: Structured report
- **WHEN** the operator requests JSON output
- **THEN** success has the v1 envelope with groups in relevance order and rules in snapshot order

### Requirement: Failure atomicity and input isolation
The Checker SHALL never query or modify live devices, mutate supplied snapshot data, or publish a partially successful report after validation, decoding, or required-snapshot failure.

#### Scenario: Invalid snapshot input
- **WHEN** a relevant snapshot is absent, malformed, or contains an unsupported field
- **THEN** the CLI returns nonzero, writes diagnostic stderr, and does not publish successful stdout

#### Scenario: Local-only execution
- **WHEN** the query is executed with synthetic input
- **THEN** no network connection or device mutation is performed
