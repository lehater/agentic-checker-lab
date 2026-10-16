# Scoped CoderMind execution instructions — Checker prototype

This workspace is an isolated implementation/planning workspace for the accepted
Harness contracts transferred into `docs/requirements.md`. That file contains the
canonical requirements/domain/interface/components/test contracts and independent
expected examples. Treat all generated feature/RPG/type/interface/task artifacts
as derived candidates. They cannot introduce new semantics or defer already
specified semantics. Read the relevant accepted contract before each planning
or coding task. Produce the requested structured output schema.

Required contract preservation during EVERY stage:
- Input JSON: version=1; flow has source, destination, protocol, source_port,
  destination_port. Both ports are REQUIRED integers 0..65535, never booleans.
- Rules have id, source, destination, protocol, source_ports, destination_ports,
  action. Address predicates are IPv4 hosts or canonical CIDR. Each rule port
  predicate is an INCLUSIVE TWO-BOUND RANGE [lower, upper], not scalar equality.
  Protocol is tcp/udp/any. Match is the conjunction of both CIDR memberships,
  protocol equal-or-any, and both inclusive port memberships. No placeholder
  predicates, None semantics, unknown-schema deferral or first-match shortcut.
- relevance is a list of device/acl pairs; snapshots contain device, acl,
  placements and ordered rules. Placements originate from snapshots. Additional
  address-indexed relevance_records input is unsupported. Deduplicate relevance
  pairs in first-seen order; include only their snapshots; missing snapshot is error.
- Public JSON is exactly {version:1,groups:[{device,acl,placements,status,rules}]}.
  Status is MATCHES or NO_MATCH, rules preserve complete original rule objects.
  No matches/device_id/acl_id/MATCH public substitutes and no universal verdict.
- Public command: python3 -m checker --input PATH [--format text|json]. Required
  --input, no default stdin. Provide the checker package and __main__ entrypoint.
  Expected errors: exit 2, empty stdout, stderr 'Checker error: <reason>'.
- Pure matches and application check(flow,relevance,snapshot); narrow injected
  source callables; validation/serialization/composition outside. Inner modules
  never import concrete outer adapters, CLI, JSON/file/network tooling.
- Read-only local synthetic data, no live network/devices, web, database,
  model-dependent runtime, global mutable caches or speculative service framework.
- Independent fixed expected cases predate code. Preserve them; fix generated
  candidates when they conflict. Tool self-validation does not override contracts.

These are execution constraints derived from already accepted contracts, not
new Product Requirements or authorization to edit canonical upstream sources.
