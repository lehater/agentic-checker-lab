# Checker Query — candidate specification delta (NOT owner-accepted)

> This is a PROPOSED engineering specification. Only the explicit D-001–D-011 decisions in the discovery ledger are owner-approved. No live collection, independent semantic sign-off, or executed acceptance cases are implied.

## ADDED Requirements

### Requirement: Validated one-shot query
The Checker SHALL accept one explicitly selected local UTF-8 JSON document representing one directed TCP/UDP query with required single host IPv4 source and destination addresses (not subnets). Each port may be a concrete integer in 0..65535 or unrestricted `any`: absent, blank UI fields are interpreted as `any` and are the default for both ports; `any` imposes no filter on that query port. The exact JSON wildcard encoding and local CLI form are PROPOSED engineering choices, not approved owner semantics. The Checker SHALL not claim a real-access or aggregated permit/deny verdict.

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
The Checker SHALL compare request host IP addresses against the stored supported exact host or CIDR matchers, protocols against tcp/udp/any, and concrete query ports against stored inclusive ranges; a query port `any` SHALL not constrain selection on that dimension. It SHALL return every selected rule in snapshot order, without a first-match shortcut. Additional ACL conditions outside the five query fields (such as established and scheduling) SHALL be preserved in the original displayed rule without evaluation. A required unsupported five-field matcher is distinct from an opaque extra ACL condition; the former SHALL not be silently guessed as a match.

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
For the initial synthetic query slice, the Checker SHALL accept separately provided relevance evidence describing devices, named ACL bindings, and possibly a relevant device with no ACL. It SHALL deduplicate each named ACL per device while retaining all relevant interface-direction or global placements. The external provider's approved route-based relevance policy (different routing interfaces to source/destination; inbound ACL on ingress, outbound on egress, global ACLs) is NOT implemented by merely supplying synthetic pairs. A provider contract remains required.

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
The Checker SHALL report each relevant device and one group per named ACL on that device, preserving all relevant placements, original matching rule fields and actions, and the date of each ACL's last successfully obtained snapshot. A relevant device without an attached ACL is reported without an ACL name. A named ACL with no matching stored rules has an empty rules list, not an absent ACL or deny verdict. The MVP consumes stored synthetic snapshots; actual collection and history management are separate scope.

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
The proposed local query SHALL neither access live firewalls nor alter supplied stored snapshots, nor publish a partial successful result after malformed or undecodable mandatory input. It SHALL distinguish an unsupported required matching field from a preserved opaque additional ACL condition. Separately, the approved collector-stage behavior is to log a failed refresh and retain the previously successful ACL snapshot and its date; the MVP does not claim to implement collection.

#### Scenario: Invalid snapshot input
- **WHEN** a relevant snapshot is absent or malformed, or a required matching field cannot be interpreted (not merely an opaque additional condition)
- **THEN** the CLI returns nonzero, writes diagnostic stderr, and does not publish successful stdout

#### Scenario: Local-only execution
- **WHEN** the query is executed with synthetic input
- **THEN** no network connection or device mutation is performed
