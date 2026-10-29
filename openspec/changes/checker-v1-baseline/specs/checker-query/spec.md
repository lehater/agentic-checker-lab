# Checker Query — reconciled candidate specification delta (NOT OWNER ACCEPTED)

## ADDED Requirements

### Requirement: Validated one-shot query
The Checker SHALL accept one explicitly selected local UTF-8 versioned JSON input describing a directed IPv4 TCP/UDP flow with required source/destination IP and protocol. Each source/destination port MAY be an integer in 0..65535, the value `any`, or omitted; **omission is equivalent to `any` and does not constrain that query port dimension**. IPv4-only, JSON envelope and CLI invocation are a deliberately small *proposed engineering subset*; no real network device access is performed.

#### Scenario: Valid input
- **WHEN** the operator supplies valid IPv4 source/destination addresses, TCP or UDP, and optional port values
- **THEN** the application evaluates only the specified source-to-destination flow against provided synthetic evidence

#### Scenario: Invalid or unsupported input
- **WHEN** a mandatory IP/protocol field is missing, an address is invalid, a numeric port is out of range, or protocol is unsupported
- **THEN** the request fails explicitly rather than treating invalid input as valid empty results

#### Scenario: Omitted and wildcard query ports
- **WHEN** the source port is omitted and the destination port is 443, and a stored supported rule otherwise matches but constrains source port
- **THEN** the source-port dimension of the query does not filter that stored rule; an explicitly supplied `any` source port behaves identically

#### Scenario: No automatic reverse direction
- **WHEN** the operator requests A-to-B flow and matching rules exist only for the reverse B-to-A flow
- **THEN** reverse-flow rules are not included; checking the reverse direction requires its own query

### Requirement: Complete stored-rule matching
The Checker SHALL compare a directed flow against supported synthetic predicates over five fields and return **every original matching row occurrence** in its ACL snapshot order, without a first-match shortcut or end-to-end verdict. Supplemental saved conditions SHALL be displayed but not evaluated; unsupported mandatory matching predicate forms SHALL NOT be guessed.

#### Scenario: Multiple matching actions
- **WHEN** a snapshot contains both permit and deny rule rows matching the flow
- **THEN** all matching original row occurrences and actions are present in snapshot order, without a first-match shortcut or end-to-end decision

#### Scenario: Predicate boundaries
- **WHEN** a query address or port is inside or outside a supported canonical CIDR or inclusive port interval
- **THEN** the row matches only when all supported mandatory predicate dimensions match; unknown required predicate forms are not silently treated as matches

#### Scenario: Supplemental conditions are displayed but not evaluated
- **WHEN** a row matches the five query dimensions and also contains a saved additional time-range or other supplemental condition
- **THEN** the matched row and its extra condition are displayed without evaluating that condition as a claim of actual applicability

#### Scenario: Identical rows at different snapshot positions
- **WHEN** one ACL snapshot contains two distinct row occurrences with identical rule text at different positions, both matching a query
- **THEN** both occurrences are retained in snapshot order even if the ACL appears in multiple relevant placements

### Requirement: Relevance is separate provided evidence
The Checker SHALL consume synthetic **relevant firewall** evidence, including firewalls with no ACL, plus each ACL's relevant ingress/egress/global placements. An ACL SHALL appear once per firewall with all applicable placements, without duplication of matched rows. Firewalls SHALL NOT be merged solely because their ACL names coincide. Real route inference is outside this prototype.

#### Scenario: Duplicate relevance
- **WHEN** one relevant firewall repeats a relevant ACL binding, or one ACL has multiple distinct applicable bindings
- **THEN** the report contains one ACL group for that firewall and all distinct relevant placements, not duplicated matched rows

#### Scenario: Relevant firewall with no ACL
- **WHEN** a firewall is relevant but has no relevant ACL, or no firewalls are relevant at all
- **THEN** the result retains the firewall with an empty ACL collection or, respectively, returns an empty firewall collection, without inventing a permit/deny outcome

#### Scenario: Missing required snapshot
- **WHEN** a relevant named ACL has never had a valid successful saved snapshot
- **THEN** the **proposed engineering error contract** fails the whole query explicitly without reporting an invented `NO_MATCH` or a partially successful normal report

### Requirement: Preserved observation and presentation
The Checker SHALL report relevant firewalls, their relevant ACLs and placements, and matching rule rows as a hierarchy, keeping parents even with empty child collections. Each relevant ACL with a valid supplied snapshot SHALL expose its **own** last-successful timestamp and matching evidence. Collection, retry and preservation after later refresh failures are outside the executable synthetic L1 slice. The output SHALL NOT claim an end-to-end permit/deny verdict.

#### Scenario: No stored match
- **WHEN** a relevant named ACL has a valid complete saved snapshot with zero matching rows
- **THEN** that firewall and ACL remain in the report with an empty matched-row collection; the report does not assert that the ACL itself is empty or that access is denied

#### Scenario: Structured report
- **WHEN** there are several relevant devices, ACLs and placements, including an ACL attached more than once
- **THEN** the versioned output preserves the relevant firewall-to-ACL-to-row hierarchy, relevant placements and original matching row order, without a global verdict

#### Scenario: Per-ACL last-success provenance
- **WHEN** a synthetic input supplies two relevant ACLs with valid successful snapshots bearing different last-success timestamps
- **THEN** each ACL's corresponding timestamp and matching rows are preserved in the result; the prototype does not claim to execute or verify a later refresh attempt

### Requirement: Failure atomicity and input isolation
The Checker SHALL not access live devices or modify supplied evidence. The **proposed CLI error contract** SHALL reject malformed input, unsupported required matching predicates, corrupt saved snapshots or missing first-successful snapshots with a diagnostic and no partially successful output. This atomic failure policy remains a delegated engineering proposal pending L1 review.

#### Scenario: Invalid snapshot input
- **WHEN** a relevant snapshot is corrupt or includes an unsupported mandatory five-field matcher form, even if other ACLs have valid evidence
- **THEN** the CLI returns nonzero, reports a diagnostic to stderr, and does not publish successful or partial stdout; a supplemental display-only condition alone does not cause this failure

#### Scenario: Local-only execution
- **WHEN** the query runs with prepared synthetic snapshots and relevance inputs
- **THEN** it does not contact live devices, update persisted ACLs or perform network acquisition
