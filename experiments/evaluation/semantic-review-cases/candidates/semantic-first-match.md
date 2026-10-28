# Candidate: matching behavior drift with valid layers

Status: PROPOSED test candidate.

1. Domain matches one ACL rule according to the accepted IPv4, protocol and port predicates.
2. Application loops over relevant ACL snapshots but returns immediately after finding the first matching stored rule.
3. All files and imports follow declared domain/application/adapter dependencies.
4. CLI prints that one rule and infers a global Permit or Deny verdict from its action.
5. Requirement says report **all** stored matching rules and do not compute an end-to-end verdict.
