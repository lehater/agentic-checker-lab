# Data Model — ACL Snapshot Checker

**Источник потребности:** [spec.md](spec.md); **технические решения:** [research.md](research.md).

## 1. FlowQuery
`source_ip`, `destination_ip`: literal IPv4 host addresses. `protocol`: one of `tcp`, `udp`. `source_port` and `destination_port`: integers 0..65535. All five fields required.

## 2. RelevantACL
Pair `(device_id, acl_id)`: nonempty stable strings. Relevance is an **input assumption** provided by another mechanism, not evidence of a real network path. Unique pairs retain input order.

## 3. ACLSnapshot
Unique key `(device_id, acl_id)` matching one relevant pair (extra snapshots allowed but not consumed). Contains:
- `placements`: zero or more descriptors of where ACL is bound, either an interface binding (interface + in/out direction) or a global binding; these are display metadata only.
- `rules`: ordered list, possibly empty. Array order **is** authoritative original snapshot order.

For every relevant pair exactly one snapshot must exist (provisional assumption A-03).

## 4. ACLRule
Fields: `rule_id` (unique nonempty within snapshot), `action` (`permit` or `deny`), `source`, `destination`, `protocol`, `source_ports`, `destination_ports`.
- source/destination are `any`, one IPv4 address, or canonical/non-canonical IPv4 CIDR accepted by the IP network parser.
- protocol: `tcp`, `udp`, `any`.
- port selectors: `{min:int,max:int}`, inclusive; each endpoint 0..65535 and min<=max.
- For a FlowQuery of tcp/udp, even `protocol:any` rules must satisfy both port ranges. This is the **declared synthetic semantics**, not a claim about vendor ACLs.
- Action records observation; it neither stops scanning nor determines end-to-end accessibility.

## 5. Match / Report
Match: `rule_id`, `action`, `ordinal` (1-based source snapshot position).
Report: `flow`, `devices` groups (with `device_id`; ACL groups contain `acl_id`, `placements`, `matches`), `summary.matched_rule_count`. 
- Device order is first encountered among relevant pairs; ACL order is first encountered per device.
- Empty relevant ACLs are retained with `matches: []`.
- An empty relevant list gives `devices: []` and count zero.
- No `verdict`, `effective_action`, `implicit_deny` or predicted network path.

## 6. Validity and failure states
Reject malformed dataset, IPv6, unsupported protocol/predicate, duplicate snapshot key, duplicate relevant key, ambiguous rule IDs or missing snapshot. Errors are distinct from valid zero matches and do not return a partial success report.

## 7. Main relationships
```text
FlowQuery (1)
RelevantACL (*) --key--> ACLSnapshot (1)
ACLSnapshot (1) --ordered--> ACLRule (*)
ACLSnapshot (1) --metadata--> Placement (*)
MatchReport (1) --groups--> RelevantACL (*) --matches--> ACLRule (*)
```
