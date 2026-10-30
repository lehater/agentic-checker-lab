"""Public L1 input grammar regression checks, NOT held-out acceptance cases.

No Checker implementation, routing, matcher, collector or real device is run.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from tools.validate_checker_l1_input import (validate_payload, parse_document,
                                             canonical_utc_text, _unique_keys)
from decimal import Decimal

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

    def test_named_relevant_acl_requires_a_placement(self):
        self.check_invalid(lambda d: d["firewalls"][0]["acls"][0]
                           .update(placements=[]))

    def test_invalid_placement_rejected(self):
        self.check_invalid(lambda d: d["firewalls"][0]["acls"][0]["placements"]
                           .append({"kind": "interface", "name": "inside"}))

    def test_invalid_timestamp_rejected(self):
        self.check_invalid(lambda d: d["snapshots"][0]
                           .update(last_success_at="yesterday"))

    def test_utc_z_and_plus_zero_offset_accepted(self):
        for suffix in ("Z", "+00:00"):
            with self.subTest(suffix=suffix):
                data = valid_case()
                data["snapshots"][0]["last_success_at"] = "2026-10-29T08:00:00" + suffix
                validate_payload(data)

    def test_non_utc_timestamp_offset_rejected(self):
        self.check_invalid(lambda d: d["snapshots"][0]
                           .update(last_success_at="2026-10-29T09:00:00+01:00"))

    def test_nested_nonfinite_extra_rejected(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=str(bad)):
                self.check_invalid(lambda d: d["snapshots"][0]["rules"][0]
                                   .update(extra={"nested": [{"x": bad}]}))

    def test_strict_json_decoder_rejects_nonstandard_constants(self):
        for bad in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=bad):
                document = json.dumps(valid_case()).replace(
                    '"office_hours"', bad, 1)
                with self.assertRaises(ValueError):
                    parse_document(document)

    def test_json_exponent_overflow_rejected_in_extra(self):
        text = json.dumps(valid_case()).replace('"office_hours"', "1e400", 1)
        parsed = parse_document(text)
        with self.assertRaises(ValueError):
            validate_payload(parsed)

    def test_fractional_utc_normalization_is_lexically_lossless(self):
        raw = "2026-10-29T08:00:00.12345678901234567890+00:00"
        self.assertEqual(canonical_utc_text(raw),
                         "2026-10-29T08:00:00.12345678901234567890Z")
        self.assertEqual(canonical_utc_text(raw[:-6] + "Z"), raw[:-6] + "Z")

    def test_precise_extra_number_does_not_pass_through_float(self):
        source = "0.1234567890123456789012345"
        text = json.dumps(valid_case()).replace('"office_hours"', source, 1)
        decoded = parse_document(text)
        validate_payload(decoded)
        value = decoded["snapshots"][0]["rules"][0]["extra"]["time_range"]
        self.assertIsInstance(value, Decimal)
        self.assertEqual(str(value), source)
        # Candidate output rule: emit the exact decimal numeric token, not a quoted string.
        reparsed = parse_document('{"number":' + str(value) + '}')
        self.assertEqual(reparsed["number"], value)

    def test_decimal_magnitude_subset_and_in_memory_float(self):
        good = json.dumps(valid_case()).replace('"office_hours"', "1e308", 1)
        validate_payload(parse_document(good))
        self.check_invalid(lambda d: d["snapshots"][0]["rules"][0]
                           .update(extra={"rounded": 0.1234567890123456789012345}))

    def test_numeric_lexeme_that_schema_can_treat_as_integer_is_rejected(self):
        data = json.dumps(valid_case()).replace('"dst_port": 443', '"dst_port": 443.0', 1)
        with self.assertRaises(ValueError):
            validate_payload(parse_document(data))

    def test_unknown_snapshot_identity_rejected(self):
        self.check_invalid(lambda d: d["snapshots"][0]
                           .update(acl_id="NOT_RELEVANT"))

    def test_duplicate_json_keys_rejected_before_validation(self):
        with self.assertRaises(ValueError):
            json.loads('{"flow": 1, "flow": 2}', object_pairs_hook=_unique_keys)


if __name__ == "__main__":
    unittest.main()
