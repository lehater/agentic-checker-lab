"""Scenario-policy tests; figures are synthetic fixtures, never measured results."""
from __future__ import annotations

import copy
import unittest
from tools.compare_runs import compare


def sample():
    records = []
    for arm, times in [("direct", (100, 105)), ("rpg", (120, 130))]:
        for i, value in enumerate(times):
            records.append({
                "run_id": f"{arm}-{i}", "arm": arm,
                "spec_sha": "spec-v1", "oracle_sha": "oracle-v1",
                "budget_id": "quota-plan-1", "environment_id": "env-1",
                "model_config_sha": "model-1", "record_class": "fixture",
                "quality": "PASS", "architecture": "PASS",
                "verified_by": "independent-tests", "elapsed_seconds": value,
                "input_tokens": None, "output_tokens": None,
            })
    return {"schema": "checker-lab/run-comparison/v1", "runs": records}


class RunComparisonTests(unittest.TestCase):
    def test_synthetic_cases_never_claim_measured_win(self):
        result = compare(sample())
        self.assertEqual(result["status"], "SIMULATED_ONLY")
        self.assertIsNone(result["routing_candidate"])
        self.assertFalse(result["all_observed"])

    def test_incomplete_timing_stays_inconclusive(self):
        data = sample()
        data["runs"][0]["elapsed_seconds"] = None
        result = compare(data)
        self.assertEqual(result["status"], "INCONCLUSIVE")

    def test_quality_regression_blocks_even_if_faster(self):
        data = sample()
        data["runs"][0]["quality"] = "FAIL"
        self.assertEqual(compare(data)["status"], "NO_GO")

    def test_unknown_quality_cannot_select_winner(self):
        data = sample()
        data["runs"][0]["quality"] = "UNKNOWN"
        self.assertEqual(compare(data)["status"], "INCONCLUSIVE")

    def test_different_oracle_or_quota_not_comparable(self):
        for field in ("spec_sha", "oracle_sha", "budget_id", "environment_id"):
            data = sample()
            data["runs"][0][field] = "different"
            with self.subTest(field=field):
                result = compare(data)
                self.assertFalse(result["comparable_context"])
                self.assertIsNone(result["routing_candidate"])

    def test_reject_fake_independent_pass(self):
        data = sample()
        data["runs"][0]["verified_by"] = "not-verified"
        with self.assertRaisesRegex(ValueError, "unverified positive gate"):
            compare(data)

    def test_minimum_repetitions_enforced(self):
        data = sample()
        data["runs"].pop()
        self.assertEqual(compare(data)["status"], "INCONCLUSIVE")

    def test_observed_repetition_can_be_compared_not_certified(self):
        data = sample()
        for record in data["runs"]:
            record["record_class"] = "observed"
        result = compare(data, minimum_gain=.01)
        self.assertEqual(result["status"], "MEASURED_COMPARISON")
        self.assertEqual(result["routing_candidate"], "direct")
        self.assertEqual(result["confidence"], "NOT_STATISTICALLY_ESTABLISHED")

    def test_declared_minimum_gain_prevents_overclaim(self):
        data = sample()
        for record in data["runs"]:
            record["record_class"] = "observed"
        self.assertIsNone(compare(data, minimum_gain=.3)["routing_candidate"])

    def test_duplicate_runs_rejected(self):
        data = sample()
        data["runs"][1]["run_id"] = data["runs"][0]["run_id"]
        with self.assertRaisesRegex(ValueError, "duplicated"):
            compare(data)

    def test_negative_tokens_rejected(self):
        data = sample()
        data["runs"][0]["input_tokens"] = -1
        with self.assertRaisesRegex(ValueError, "invalid input_tokens"):
            compare(data)


if __name__ == "__main__":
    unittest.main()
