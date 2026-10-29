# Checker Query — candidate specification delta (NOT owner-accepted)


## ADDED Requirements

### Requirement: Validated one-shot query
The Checker SHALL accept one directed TCP/UDP query with required source/destination single-host IPv4 addresses and optional source/destination ports. Each port can be a numeric value (0..65535) or unrestricted `any`; an absent port means `any`, which removes that port filter. Neither real reachability nor a global access verdict is computed.
#### Scenario: Valid input
- **WHEN** the operator submits one valid document containing two single-host IPv4 addresses, TCP or UDP, and either concrete or unrestricted port selections
- **THEN** the application evaluates only this directed query against provided synthetic evidence

#### Scenario: Invalid or unsupported input
- **WHEN** a required IP or protocol is missing, an address is a subnet rather than one host, a supplied numeric port is out of range, or a required query field is invalid
- **THEN** the application rejects the request rather than silently approximating its meaning

#### Scenario: Any source port
- **WHEN** source port is blank or any and the saved ACL has rules restricting the source port differently
- **THEN** those source-port restrictions do not exclude otherwise matching rules

#### Scenario: Any destination port
- **WHEN** destination port is blank or any and saved ACL rules restrict different destination ports
- **THEN** those destination-port restrictions do not exclude otherwise matching rules

#### Scenario: Directed query
- **WHEN** the operator requests traffic from one source to one destination
- **THEN** the result contains no automatically checked reverse-only rules or stateful return-path decision; reversing addresses and ports requires a separate request

### Requirement: Complete stored-rule matching
The Checker SHALL select all saved ACL rules that match the query's five dimensions, treating query port `any` as unconstrained. It SHALL retain rule order and original extra ACL conditions as display-only evidence, without evaluating those extra conditions. Required unknown matching fields cannot silently be treated as matches.
#### Scenario: Multiple matching actions
- **WHEN** a snapshot contains both permit and deny rules matching the same flow
- **THEN** the returned evidence contains both original rules and actions in snapshot order

#### Scenario: Predicate boundaries
- **WHEN** an address is outside a CIDR or a port is outside an inclusive interval
- **THEN** the rule does not match

#### Scenario: Additional conditions preserved
- **WHEN** a rule matches the five query dimensions but contains an established condition or schedule
- **THEN** the original rule and extra condition are displayed without claiming to have evaluated that condition

#### Scenario: Unsupported matching field
- **WHEN** a required stored matching field is unknown or malformed
- **THEN** it is rejected explicitly as a missing matching capability instead of silently treated as opaque display data or as a match

### Requirement: Relevance is a separate provided input
The synthetic prototype SHALL consume provided relevant devices and ACL bindings, display one named ACL per device with all applicable placements, and retain a relevant device without ACL. The approved route/interface relevance policy remains a separate provider contract, not implemented by consuming provided evidence.
#### Scenario: Duplicate relevance
- **WHEN** the relevance source repeats the same device/ACL pair
- **THEN** exactly one output group is produced for that pair in first-seen order

#### Scenario: Missing required snapshot
- **WHEN** a relevant named ACL has no previously successful saved snapshot
- **THEN** the proposed local query fails instead of inventing NO_MATCH; this is an unapproved engineering boundary requiring independent review

#### Scenario: Multiple placements of one ACL
- **WHEN** one ACL on one FW is relevant via inbound-interface and global bindings
- **THEN** one rule group includes both placements without duplicating the matching rows

#### Scenario: Relevant device without ACL
- **WHEN** a firewall is relevant but no ACL is attached to its applicable bindings
- **THEN** the device remains visible without an ACL name, and no ACL rules or implicit deny are fabricated

### Requirement: Preserved observation and presentation
The Checker SHALL report each relevant device, named ACL, matching and unmatched saved ACL rules, applicable placements, original rule fields/actions and per-ACL last-successful snapshot date without inferring a permit/deny verdict. A named ACL with no matches is distinct from a device without an ACL.
#### Scenario: No stored match
- **WHEN** a relevant ACL has no matching stored rules
- **THEN** the group is reported as NO_MATCH with an empty rules list, not a deny verdict

#### Scenario: Structured report
- **WHEN** the operator requests JSON output
- **THEN** success has the v1 envelope with groups in relevance order and rules in snapshot order

#### Scenario: Per-ACL last-success date
- **WHEN** two ACLs have different last-successful snapshot dates and one has a later failed refresh attempt
- **THEN** each ACL displays its own last-successful date, not the timestamp of an unsuccessful attempt

### Requirement: Failure atomicity and input isolation
The proposed local Checker SHALL not contact live firewalls, alter input snapshots or publish partial successes for invalid mandatory matching data. Opaque extra ACL conditions are preserved rather than rejected solely for being uninterpreted. Refresh-error logging and retention of last successful snapshots are an external collector contract, not an implemented MVP feature.
#### Scenario: Invalid snapshot input
- **WHEN** a relevant snapshot is absent or malformed, or a required matching field cannot be interpreted (not merely an opaque additional condition)
- **THEN** the CLI returns nonzero, writes diagnostic stderr, and does not publish successful stdout

#### Scenario: Local-only execution
- **WHEN** the query is executed with synthetic input
- **THEN** no network connection or device mutation is performed
