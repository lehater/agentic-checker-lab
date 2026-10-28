"""Tests derive coverage from actual OpenSpec headings, not known historical defects."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
import unittest
from tools.check_requirements_trace import check_catalog, scenario_pairs

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/evaluation/checker-acceptance-catalog.json"


class RequirementsTraceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(CATALOG.read_text(encoding="utf-8"))

    def check_changed(self, data):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "catalog.json"
            file.write_text(json.dumps(data), encoding="utf-8")
            return check_catalog(ROOT, file)

    def test_every_proposed_scenario_has_oracle(self):
        verdict = self.check_changed(self.data)
        self.assertEqual(verdict["status"], "PASS", verdict)
        self.assertEqual(verdict["case_count"], 10)
        self.assertIs(verdict["implementation_executed"], False)

    def test_new_requirement_is_detectable(self):
        source = (ROOT / self.data["spec"]).read_text()
        self.assertEqual(len(scenario_pairs(source + "\n### Requirement: New\n#### Scenario: Missing\n")), 11)

    def test_missing_acceptance_case_fails(self):
        changed = copy.deepcopy(self.data)
        changed["cases"].pop()
        self.assertIn("missing scenario coverage", str(self.check_changed(changed)["errors"]))

    def test_duplicate_mapping_fails(self):
        changed = copy.deepcopy(self.data)
        duplicate = copy.deepcopy(changed["cases"][0])
        duplicate["id"] = "CHK-999"
        changed["cases"].append(duplicate)
        self.assertIn("duplicate scenario coverage", str(self.check_changed(changed)["errors"]))

    def test_stale_spec_revision_fails(self):
        changed = copy.deepcopy(self.data)
        changed["spec_git_blob_sha"] = "0"*40
        self.assertIn("SHA mismatch", str(self.check_changed(changed)["errors"]))

    def test_synthetic_execution_claim_fails(self):
        changed = copy.deepcopy(self.data)
        changed["cases"][0]["execution_status"] = "PASS"
        self.assertIn("unverified runtime result", str(self.check_changed(changed)["errors"]))

    def test_cannot_mark_proposed_as_accepted(self):
        changed = copy.deepcopy(self.data)
        changed["status"] = "OWNER_ACCEPTED"
        self.assertIn("cannot claim owner acceptance", str(self.check_changed(changed)["errors"]))


if __name__ == "__main__":
    unittest.main()
