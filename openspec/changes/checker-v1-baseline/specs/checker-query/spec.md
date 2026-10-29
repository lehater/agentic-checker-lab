# Checker Query — reconciled candidate specification delta (NOT OWNER ACCEPTED)

This is an **engineering proposal** for L1, NOT an approval or implementation. The original [owner brief](../../../../../docs/scenario/owner-problem-brief.md) is the product starting point. The unmerged [historical discovery ledger](https://github.com/lehater/agentic-checker-lab/blob/experiment/iterative-discovery-protocol/docs/discovery/checker/ledger.json) records normalized D-001..D-012 as owner-confirmed; these meanings are evidence to reconcile and are **not automatically accepted as this OpenSpec**. A separate L1 owner/spec review and independently held-out acceptance review are still required.

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
The Checker SHALL compare the directed query against source/destination IPv4 exact-address or canonical CIDR predicates, tcp/udp/any protocol predicates and inclusive numeric port ranges, returning **all matching original row occurrences** in each ACL's snapshot order without a first-match shortcut. Permit and deny are *reported facts*, not an effective-path verdict. A valid supported predicate required for matching SHALL be distinguished from supplemental stored conditions that are preserved as uninterpreted evidence.

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
The Checker SHALL consume a synthetic **list of relevant firewall identities**, each with zero or more relevant ACL identities and their relevant ingress/egress/global placement facts. Device relevance and ACL attachment selection are **already supplied** for this thin slice, not inferred from live routing. An ACL SHALL appear once per device with all relevant placements; repeated provider references SHALL NOT create duplicate ACL groups, while distinct devices SHALL NOT be merged just because ACL names coincide. The complete relevant-device hierarchy MUST be representable even if no ACL is bound.

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
The Checker SHALL report the **hierarchy of facts** relevant firewall → relevant ACL including relevant placements → matching stored rows, retaining parent objects even when child collections are empty. Each ACL with a successful snapshot SHALL expose its **own** last-successful snapshot timestamp and stored rows in snapshot order; an unsuccessful later refresh MUST NOT silently change that saved timestamp or content. The first slice MAY use supplied synthetic last-success snapshots rather than implementing a real collector. Presentation MAY add useful statuses but cannot turn no match into implicit deny or claim full end-to-end permit/deny.

#### Scenario: No stored match
- **WHEN** a relevant named ACL has a valid complete saved snapshot with zero matching rows
- **THEN** that firewall and ACL remain in the report with an empty matched-row collection; the report does not assert that the ACL itself is empty or that access is denied

#### Scenario: Structured report
- **WHEN** there are several relevant devices, ACLs and placements, including an ACL attached more than once
- **THEN** the versioned output preserves the relevant firewall-to-ACL-to-row hierarchy, relevant placements and original matching row order, without a global verdict

#### Scenario: Per-ACL last-success provenance
- **WHEN** two relevant ACLs were successfully snapshotted at different times and a later collection attempt for one failed
- **THEN** each ACL retains its own last-success timestamp and saved content; no past collection failure is asserted as a current matching outcome

### Requirement: Failure atomicity and input isolation
The Checker SHALL not query or modify live devices or mutate input snapshots. For the proposed one-shot CLI, a malformed input, an unsupported **required** matching predicate, corrupt saved snapshot, or missing required first-successful snapshot SHALL cause an explicit nonzero failure and diagnostic stderr with **no successful or partial stdout report**. This atomic-failure rule is an engineering proposal subject to L1 contract review; it is not a new owner-confirmed decision about every future missing-data scenario.

#### Scenario: Invalid snapshot input
- **WHEN** a relevant snapshot is corrupt or includes an unsupported mandatory five-field matcher form, even if other ACLs have valid evidence
- **THEN** the CLI returns nonzero, reports a diagnostic to stderr, and does not publish successful or partial stdout; a supplemental display-only condition alone does not cause this failure

#### Scenario: Local-only execution
- **WHEN** the query runs with prepared synthetic snapshots and relevance inputs
- **THEN** it does not contact live devices, update persisted ACLs or perform network acquisition
