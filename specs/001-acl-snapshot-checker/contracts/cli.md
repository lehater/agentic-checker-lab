# CLI / Result Contract — ACL Snapshot Checker

**Design status:** Proposed interface determined during Spec Kit planning. It is not an owner-provided requirement.

## Invocation
```bash
python -m acl_checker FIXTURE.json
```
One required positional dataset path; one flow query per run. Offline; no network.

- exit `0`: valid dataset, prints exactly one JSON report to stdout (including zero matches).
- exit `2`: invalid/unreadable fixture, unsupported predicate or missing relevant snapshot; diagnostic on stderr; no partial success report on stdout.
- exit `1`: unexpected internal error; diagnostic on stderr, no success report.

## Input
One UTF-8 JSON file validated against [dataset.schema.json](dataset.schema.json) plus semantic rules of [data-model.md](../data-model.md). No implicit device discovery.

### Example
```json
{
  "flow": {"source_ip":"198.51.100.10","destination_ip":"203.0.113.5","protocol":"tcp","source_port":55000,"destination_port":443},
  "relevant_acls": [{"device_id":"fw-a","acl_id":"outside-in"}],
  "snapshots": [{
    "device_id":"fw-a", "acl_id":"outside-in",
    "placements": [{"kind":"interface","interface":"eth0","direction":"in"}],
    "rules": [
      {"rule_id":"R10","action":"deny","source":"198.51.100.0/24","destination":"203.0.113.5","protocol":"tcp","source_ports":{"min":0,"max":65535},"destination_ports":{"min":443,"max":443}},
      {"rule_id":"R20","action":"permit","source":"any","destination":"any","protocol":"tcp","source_ports":{"min":0,"max":65535},"destination_ports":{"min":443,"max":443}}
    ]
  }]
}
```

## Output
For the example above, stdout is a JSON object *equivalent to*:
```json
{
  "flow":{"source_ip":"198.51.100.10","destination_ip":"203.0.113.5","protocol":"tcp","source_port":55000,"destination_port":443},
  "devices":[{
    "device_id":"fw-a",
    "acls":[{
      "acl_id":"outside-in",
      "placements":[{"kind":"interface","interface":"eth0","direction":"in"}],
      "matches":[
        {"rule_id":"R10","action":"deny","ordinal":1},
        {"rule_id":"R20","action":"permit","ordinal":2}
      ]
    }]
  }],
  "summary":{"matched_rule_count":2}
}
```

Properties:
1. Every relevant ACL has its own group, including groups with zero matches.
2. Rule `ordinal` is 1-based from the input snapshot; iteration and groups preserve input/relevance order.
3. `permit` / `deny` are raw rule actions, not conclusions; no global verdict field appears.
4. All output fields are part of the contract; unknown extra top-level conclusion fields should be rejected by consumer validation.
5. Emit valid JSON even when no pairs or matches are found.
