# Checker synthetic v1 — proposed wire/CLI contract (NOT ACCEPTED)

**Status: ENGINEERING PROPOSAL ONLY.** This document makes the current proposed [Checker OpenSpec](../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) concrete enough for owner/spec review and future independent executable acceptance tests. It does **not** replace the original owner need, historically recorded D-001..D-012, or the held-out oracle. No runtime exists or was tested by this document.

## Proposed one-shot CLI

```sh
checker check --input /path/to/case.json
```

The CLI reads **one UTF-8 JSON document** from the explicitly given local path. It does not read live firewalls or issue network requests. On success, it emits **one** JSON document to stdout and exits `0`. On invalid input, missing/invalid mandatory evidence or unsupported mandatory matching syntax, it emits a diagnostic to **stderr**, exits nonzero and emits **no successful or partial stdout**. Specific exit codes and final field names require engineering/spec review, and may change before acceptance. Do not treat this draft as an approved contract.

**Draft typed input grammar:** [JSON Schema](checker-v1-input.schema.json). **Open engineering regression check:** [stdlib validator](../../tools/validate_checker_l1_input.py), with [negative tests](../../tests/test_checker_l1_input_contract.py). The schema covers types, allowed keys and field shape; the validator additionally checks cross-object snapshot identity, canonical IPv4 CIDR, UTC timestamps, range ordering and nonempty IDs. These public checks are **not held-out acceptance** and do not implement matching or relevance.

## Example input

```json
{
  "schema_version": 1,
  "flow": {
    "src_ip": "192.0.2.15",
    "dst_ip": "198.51.100.8",
    "protocol": "tcp",
    "dst_port": 443
  },
  "firewalls": [
    {
      "id": "fw-a",
      "acls": [
        {
          "id": "WEB_IN",
          "placements": [
            {"kind": "interface", "name": "outside", "direction": "ingress"},
            {"kind": "global"}
          ]
        }
      ]
    },
    {"id": "fw-b", "acls": []}
  ],
  "snapshots": [
    {
      "device_id": "fw-a",
      "acl_id": "WEB_IN",
      "last_success_at": "2026-10-29T08:00:00Z",
      "rules": [
        {
          "action": "permit",
          "src_ip": "192.0.2.0/24",
          "dst_ip": "198.51.100.8",
          "protocol": "tcp",
          "src_port": {"min": 40000, "max": 65535},
          "dst_port": 443,
          "extra": {"time_range": "office_hours"}
        },
        {
          "action": "deny",
          "src_ip": "192.0.2.0/24",
          "dst_ip": "198.51.100.8",
          "protocol": "tcp",
          "src_port": "any",
          "dst_port": 443,
          "extra": {"note": "not a full applicability verdict"}
        }
      ]
    }
  ]
}
```

**Meaning:** `flow.src_port` is intentionally **omitted**, which is the same as explicit `"any"` and therefore **does not filter** source ports. Both stored rows match the other four supported fields, so both appear in the result even if their actions disagree. The `time_range` note is displayed but not evaluated; neither rule constitutes a conclusive end-to-end permit/deny verdict. FW `fw-b` is relevant even without ACL; it remains present.

The `firewalls` input is **already selected relevance evidence**; the prototype does not calculate the routes or choose interface placements. A real provider must eventually honor the separately agreed relevance and ingress/egress/global rules.

## Example successful output (proposed)

```json
{
  "schema_version": 1,
  "firewalls": [
    {
      "id": "fw-a",
      "acls": [
        {
          "id": "WEB_IN",
          "placements": [
            {"kind": "interface", "name": "outside", "direction": "ingress"},
            {"kind": "global"}
          ],
          "last_success_at": "2026-10-29T08:00:00Z",
          "matched_rules": [
            {
              "snapshot_index": 0,
              "rule": {
                "action": "permit",
                "src_ip": "192.0.2.0/24",
                "dst_ip": "198.51.100.8",
                "protocol": "tcp",
                "src_port": {"min": 40000, "max": 65535},
                "dst_port": 443,
                "extra": {"time_range": "office_hours"}
              }
            },
            {
              "snapshot_index": 1,
              "rule": {
                "action": "deny",
                "src_ip": "192.0.2.0/24",
                "dst_ip": "198.51.100.8",
                "protocol": "tcp",
                "src_port": "any",
                "dst_port": 443,
                "extra": {"note": "not a full applicability verdict"}
              }
            }
          ]
        }
      ]
    },
    {"id": "fw-b", "acls": []}
  ]
}
```

For **zero relevant FW**, the result contains `"firewalls":[]`. For a relevant ACL with a **valid** last-successful snapshot but zero matched rules, keep the FW and ACL with `matched_rules:[]` and preserve the ACL timestamp. Do not emit a special `NO_MATCH` status unless later approved as a display/format choice. No implicit deny or global verdict is synthesized.

**Occurrence identity:** `snapshot_index` is the zero-based position of the original rule occurrence, not a hash of rule text. Two matching equal-text rule occurrences at different positions must appear twice, while one ACL group is not duplicated across placements.

## Proposed minimal typed validation and error boundaries

| Data aspect | Proposed v1 subset and handling |
| --- | --- |
| Query IPs | Required exact IPv4 addresses, no wildcard, no missing input |
| Query protocol | Required `tcp` or `udp`; unsupported protocols fail validation |
| Query source/destination ports | Each may be a single integer 0..65535, explicit `"any"`, or **omitted** meaning `"any"`; no implicit default to an arbitrary concrete port |
| Saved rule IP predicate | Exact IPv4 or canonical IPv4 CIDR, including `/0` when represented canonically |
| Saved rule protocol predicate | `tcp`, `udp`, `any` |
| Saved rule port predicate | Single integer, `"any"`, or object `{"min":N,"max":M}` with `0 <= N <= M <= 65535` (inclusive) |
| Saved rule row | Position = array index; original `action`, all supported matcher fields and opaque `extra` retained; no first-match behavior |
| ACL identity | Group by `(firewall.id, acl.id)` even when same ACL name exists on different firewalls |
| Relevant placements | Ingress/egress interface or global placement facts preselected by the fixture; repeated exact placement references do not duplicate ACL groups |
| ACL snapshot | Each **relevant named ACL** must have exactly one complete saved snapshot with `last_success_at` RFC3339 UTC timestamp; different ACL timestamps allowed |
| No first successful snapshot | **Proposed** fail-atomic diagnostic, not valid empty match; owner has not approved this error wire contract |
| Corrupt or unsupported mandatory match fields | **Proposed** fail-atomic diagnostic, never silently drop an unknown required predicate |
| Supplemental conditions | Arbitrary JSON-safe `extra` object is **display-only**, never a matching predicate or a reason to claim full applicability |
| Refresh failure | Actual collector/refresh is outside L1: do not claim failed-refresh preservation was executed; future collector tests must verify preserving the last successful snapshot and timestamp |
| Identity and duplicates | Firewall IDs uniquely identify an FW in one input; repeated firewall objects or duplicate snapshots keyed by `(device_id, acl_id)` are invalid. Repeated ACL references within a firewall are coalesced by ACL name, aggregating distinct placement facts without duplicating row occurrences |
| Unexpected data | Extra arbitrary saved attributes are allowed **only** inside row `extra` objects. Unrecognized top-level, flow, firewall, ACL, snapshot and required rule-matcher keys are **proposed validation failures**, rather than silently guessed new semantics |
| Integrity and order | Every relevant ACL needs exactly one valid corresponding snapshot, with an RFC3339 UTC last-success timestamp and a `rules` array (possibly empty). Extra snapshots for nonexistent identities are invalid. Preserve input firewall/ACL first-occurrence order and distinct placement first-occurrence order as engineering presentation choices; preserve original stored row-array order as owner meaning |
| Error diagnostics | Invalid JSON/field types/duplicate IDs/missing snapshot/unsupported mandatory predicates produce nonzero exit and a nonempty stderr diagnostic, without any successful stdout document. Exact diagnostic wording and nonzero code numbers are not specified |
| Data type boundaries | Boolean values must not be treated as integer ports; reject out-of-range values, reversed intervals and noncanonical CIDR where the grammar demands canonical networks. Required ACL action is `permit` or `deny`; `extra` if present is an opaque JSON object |

**Engineering proposal for review:** The concrete example is now accompanied by a draft JSON Schema, but its supported field grammar, duplicate policy, error shape and ordering are now explicitly bounded for independent fixture design. The owner is being asked to approve the **observable MVP scope in one package**, not to decide JSON field names, exception strings or implementation classes individually.

## Examples to freeze with independent acceptance later

- Omitted vs explicit `any` ports with otherwise equal flow and data.
- Reversed flow must require a new query.
- FW with no ACL, ACL with valid snapshot and zero matches, and no relevant FW.
- One ACL with multiple placements and two distinct equal-text matching row occurrences.
- Supplemental `time_range` retained without checking its truth, and unknown **mandatory** matcher rejected.
- Two different last-success timestamps in synthetic snapshots; a separate future collector acceptance test must cover failed refresh without overwriting saved evidence.
- Relevant named ACL with no initial successful snapshot: explicit error, not inferred deny/no-match.

**Approval gate:** Review revised OpenSpec, this proposed contract and black-box cases **as one package**. After owner acceptance, the independent oracle custodian must prepare and freeze held-out inputs/expected results inaccessible to implementation agents; existing CHK cases are public proposals marked `NOT_RUN`. Neither passing structural CI nor this example authorizes code generation.
