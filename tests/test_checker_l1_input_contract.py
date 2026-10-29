"""Public L1 input grammar regression checks, NOT held-out acceptance cases.

No Checker implementation, routing, matcher, collector or real device is run.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from tools.validate_checker_l1_input import validate_payload, _unique_keys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/evaluation/checker-v1-input.schema.json"


def valid_case():
    return {
        "schema_version": 1,
        "flow": {
            "src_ip": "192.0.2.15", "dst_ip": "198.51.100.8",
            "protocol": "tcp", "dst_port": 443,
        },
        "firewalls": [
            {"id": "fw-a", "acls": [
                {"id": "WEB_IN", "placements": [
                    {"kind": "global"},
                    {"kind": "interface", "name": "outside", "direction": "ingress"},
                ]},
            ]},
            {"id": "fw-b", "acls": []},
        ],
        "snapshots": [{
            "device_id": "fw-a", "acl_id": "WEB_IN",
            "last_success_at": "2026-10-29T08:00:00Z",
            "rules": [{
                "action": "permit", "src_ip": "192.0.2.0/24",
                "dst_ip": "198.51.100.8", "protocol": "tcp",
                "src_port": {"min": 40000, "max": 65535},
                "dst_port": 443,
                "extra": {"time_range": "office_hours"},
            }]
        }],
    }


class CheckerL1InputTests(unittest.TestCase):
    def test_public_schema_has_same_required_top_level_fields(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(set(schema["required"]),
                         {"schema_version", "flow", "firewalls", "snapshots"})
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["$defs"]), {"firewall", "acl", "snapshot", "rule"})

    def test_minimal_valid_synthetic_input(self):
        validate_payload(valid_case())

    def test_explicit_any_and_duplicate_acl_placement_allowed(self):
        data = valid_case()
        data["flow"]["src_port"] = "any"
        data["firewalls"][0]["acls"].append({
            "id": "WEB_IN", "placements": [{"kind": "global"}]})
        validate_payload(data)

    def test_empty_relevance_is_valid(self):
        data = valid_case()
        data["firewalls"], data["snapshots"] = [], []
        validate_payload(data)

    def test_valid_empty_snapshot_is_not_missing(self):
        data = valid_case()
        data["snapshots"][0]["rules"] = []
        validate_payload(data)

    def check_invalid(self, change):
        data = valid_case()
        change(data)
        with self.assertRaises(ValueError):
            validate_payload(data)

    def test_missing_snapshot_not_silently_empty(self):
        self.check_invalid(lambda d: d["snapshots"].clear())

    def test_duplicate_snapshot_id_rejected(self):
        self.check_invalid(lambda d: d["snapshots"].append(
            copy.deepcopy(d["snapshots"][0])))

    def test_duplicate_firewall_id_rejected(self):
        self.check_invalid(lambda d: d["firewalls"].append(
            copy.deepcopy(d["firewalls"][0])))

    def test_boolean_port_is_not_integer_port(self):
        self.check_invalid(lambda d: d["flow"].update(src_port=True))

    def test_range_order_and_limits(self):
        self.check_invalid(lambda d: d["snapshots"][0]["rules"][0]
                           .update(src_port={"min": 65535, "max": 80}))
        self.check_invalid(lambda d: d["flow"].update(dst_port=65536))

    def test_noncanonical_network_rejected(self):
        self.check_invalid(lambda d: d["snapshots"][0]["rules"][0]
                           .update(src_ip="192.0.2.15/24"))

    def test_ipv6_outside_small_prototype(self):
        self.check_invalid(lambda d: d["flow"].update(src_ip="2001:db8::1"))

    def test_unknown_mandatory_field_not_opaque_extra(self):
        self.check_invalid(lambda d: d["snapshots"][0]["rules"][0]
                           .update(time_range="office_hours"))

    def test_invalid_placement_rejected(self):
        self.check_invalid(lambda d: d["firewalls"][0]["acls"][0]["placements"]
                           .append({"kind": "interface", "name": "inside"}))

    def test_invalid_timestamp_rejected(self):
        self.check_invalid(lambda d: d["snapshots"][0]
                           .update(last_success_at="yesterday"))

    def test_unknown_snapshot_identity_rejected(self):
        self.check_invalid(lambda d: d["snapshots"][0]
                           .update(acl_id="NOT_RELEVANT"))

    def test_duplicate_json_keys_rejected_before_validation(self):
        with self.assertRaises(ValueError):
            json.loads('{"flow": 1, "flow": 2}', object_pairs_hook=_unique_keys)


if __name__ == "__main__":
    unittest.main()
