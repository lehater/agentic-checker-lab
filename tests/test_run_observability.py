"""Regression for truthful CoderMind timings and Codex JSONL accounting."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/analyze_run.py"
PLAN = ROOT / "tests/fixtures/observability/old-plan-excerpt.txt"
CODEX = ROOT / "tests/fixtures/observability/synthetic-codex-events.jsonl"


def probe(*args):
    return subprocess.run([sys.executable, str(SCRIPT), "--run-id", "fixture", *args],
                          capture_output=True, text=True, check=False)


class RunObservabilityTest(unittest.TestCase):
    def test_actual_historical_stage_timings_keep_token_usage_unknown(self):
        result = probe("--plan-log", str(PLAN))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        timing = report["coder_mind_plans"][0]
        self.assertEqual(timing["total_seconds"], 1039.6)
        self.assertEqual(timing["stage_seconds"]["interfaces"], 640.3)
        self.assertEqual(timing["structured_llm_success_lines"], 2)
        self.assertEqual(report["llm"]["usage_status"], "UNKNOWN")
        self.assertIsNone(report["llm"]["input_tokens"])
        self.assertIsNone(report["llm"]["cost_usd"])

    def test_synthetic_usage_without_expected_calls_is_partial(self):
        result = probe("--codex-jsonl", str(CODEX))
        self.assertEqual(result.returncode, 0, result.stderr)
        usage = json.loads(result.stdout)["llm"]
        self.assertEqual(usage["observed_completed_turns"], 2)
        self.assertEqual(usage["usage_status"], "PARTIAL")
        self.assertEqual(usage["input_tokens"], 150)
        self.assertEqual(usage["cached_input_tokens"], 50)
        self.assertEqual(usage["output_tokens"], 50)
        self.assertEqual(usage["total_input_plus_output_tokens"], 200)

    def test_complete_only_with_declared_expectation(self):
        result = probe("--codex-jsonl", str(CODEX), "--expected-turns", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["llm"]["usage_status"],
                         "COMPLETE_WITH_DECLARED_EXPECTATION")
        partial = probe("--codex-jsonl", str(CODEX), "--expected-turns", "3")
        self.assertEqual(json.loads(partial.stdout)["llm"]["usage_status"], "PARTIAL")

    def test_bad_jsonl_fails_instead_of_ignoring_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text("{bad}\n", encoding="utf-8")
            result = probe("--codex-jsonl", str(path))
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid JSONL", result.stderr)

    def test_absent_sources_rejected(self):
        result = probe()
        self.assertEqual(result.returncode, 2)

    def test_trajectory_observation_does_not_invent_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trajectory.json"
            path.write_text(json.dumps({"steps": [{"llm_interactions": [
                {"success": True, "duration_seconds": 1.5},
                {"success": False, "duration_seconds": 2.0}
            ]}]}), encoding="utf-8")
            result = probe("--trajectory", str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["trajectory"]["trajectory_recorded_interactions"], 2)
            self.assertEqual(report["trajectory"]["trajectory_llm_duration_seconds"], 3.5)
            self.assertIsNone(report["llm"]["output_tokens"])


if __name__ == "__main__":
    unittest.main()
