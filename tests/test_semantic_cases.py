"""Basic integrity checks for proposed requirement-led semantic evaluation cases."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "experiments/evaluation/semantic-review-cases/annotations.json"
ALLOWED = {"AR-01", "AR-02", "AR-03", "SOLID-S", "SOLID-D", "KISS", "YAGNI", "SPEC-TRACE"}


class SemanticCaseIntegrity(unittest.TestCase):
    def test_cases_have_unique_ids_existing_inputs_and_valid_labels(self):
        obj = json.loads(FILE.read_text(encoding="utf-8"))
        self.assertEqual(obj["schema"], "semantic-review-cases/v1")
        self.assertTrue(obj["status"].startswith("PROPOSED"))
        seen = set()
        outcomes = set()
        rules = set()
        for case in obj["cases"]:
            self.assertNotIn(case["id"], seen)
            seen.add(case["id"])
            path = ROOT / case["candidate"]
            self.assertTrue(path.is_file(), case["candidate"])
            self.assertTrue(path.read_text(encoding="utf-8").strip())
            self.assertTrue(case["expected"])
            self.assertTrue(set(case["expected"]).issubset(ALLOWED))
            self.assertTrue(all(v in {"pass", "fail", "uncertain"} for v in case["expected"].values()))
            outcomes.update(case["expected"].values())
            rules.update(case["expected"].keys())
        self.assertGreaterEqual(len(seen), 5)
        self.assertEqual(outcomes, {"pass", "fail", "uncertain"})
        self.assertIn("SPEC-TRACE", rules)
        self.assertIn("YAGNI", rules)


if __name__ == "__main__":
    unittest.main()
