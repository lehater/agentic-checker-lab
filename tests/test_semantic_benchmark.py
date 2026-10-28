"""No-model tests for label-free exports and independently scored review results."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

REPO = Path(__file__).resolve().parents[1]
EXPORT = REPO / "tools/export_semantic_case.py"
SCORE = REPO / "tools/evaluate_semantic_reviewer.py"


def invoke(*arguments):
    return subprocess.run([sys.executable, *map(str, arguments)], cwd=REPO,
                          capture_output=True, text=True, check=False)


class OfflineSemanticBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.zipfile = self.root / "case.zip"
        self.reports = self.root / "reports"
        self.export = invoke(EXPORT, "--case-id", "role-drift", "--output", self.zipfile)
        self.assertEqual(self.export.returncode, 0, self.export.stderr)
        with ZipFile(self.zipfile) as zipfile:
            self.archive_names = zipfile.namelist()
            self.request_bytes = zipfile.read("request.json")
            self.req = json.loads(self.request_bytes)

    def test_bundle_excludes_all_gold_annotations_and_other_cases(self):
        self.assertTrue(self.zipfile.is_file())
        self.assertFalse(any("annotations" in name for name in self.archive_names))
        self.assertFalse(any("semantic-first-match" in name for name in self.archive_names))
        self.assertIn("docs/engineering/policy.md", self.archive_names)
        self.assertIn("docs/scenario/owner-problem-brief.md", self.archive_names)
        self.assertIn("docs/engineering/semantic-review-prompt.md", self.archive_names)
        self.assertEqual(self.req["subject"], "role-drift")
        self.assertEqual(len(self.req["sources"]), 4)

    def test_bundle_inputs_match_versioned_sources(self):
        with ZipFile(self.zipfile) as archive:
            for source in self.req["sources"]:
                content = archive.read(source["path"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), source["sha256"])
                self.assertEqual(content, (REPO / source["path"]).read_bytes())

    def test_deterministic_export_bytes(self):
        next_path = self.root / "repeat.zip"
        run = invoke(EXPORT, "--case-id", "role-drift", "--output", next_path)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.zipfile.read_bytes(), next_path.read_bytes())

    def test_absent_case_rejected(self):
        run = invoke(EXPORT, "--case-id", "nonexistent", "--output", self.root / "bad.zip")
        self.assertEqual(run.returncode, 2)

    def _quote(self, source_id, needle):
        source = next(x for x in self.req["sources"] if x["id"] == source_id)
        lines = (REPO / source["path"]).read_text(encoding="utf-8").splitlines()
        index = next(i for i, line in enumerate(lines, 1) if needle in line)
        return {"source_id": source_id, "start_line": index,
                "end_line": index, "quote": needle}

    def _submit_report(self, tamper=False):
        case_dir = self.reports / "role-drift"
        case_dir.mkdir(parents=True)
        (case_dir / "request.json").write_bytes(self.request_bytes)
        cand = self._quote("candidate-1", "application orchestration")
        policy = self._quote("constraint-2", "AR-01")
        citation = [cand, policy]
        coverage = []
        findings = []
        for rule in self.req["required_rules"]:
            assessment = "fail" if rule in ("AR-01", "AR-03") else "uncertain"
            coverage.append({"rule_id": rule, "assessment": assessment,
                             "rationale": "Fixture-only protocol test; no model inference.",
                             "citations": citation})
            if assessment == "fail":
                findings.append({
                    "id": "fixture-" + rule, "rule_id": rule,
                    "severity": "BLOCKER",
                    "claim": "Orchestration resides in domain, not application",
                    "reasoning": "Candidate conflicts with the declared role separation.",
                    "minimal_fix": "Move the orchestration responsibility into application.",
                    "citations": citation
                })
        report = {
            "schema": "semantic-review-report/v1",
            "request_sha256": hashlib.sha256(self.request_bytes).hexdigest(),
            "reviewer": {"kind": "fixture", "identifier": "handwritten-score-test"},
            "coverage": coverage, "findings": findings,
        }
        if tamper:
            report["request_sha256"] = "0" * 64
        (case_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False),
                                               encoding="utf-8")

    def test_missing_reports_never_counted_as_results(self):
        run = invoke(SCORE, "--reports-dir", self.reports)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["cases_scored"], 0)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertIsNone(result["metrics"]["block_precision"])
        strict = invoke(SCORE, "--reports-dir", self.reports, "--require-complete")
        self.assertEqual(strict.returncode, 1)

    def test_handwritten_valid_report_scores_only_labeled_rules(self):
        self._submit_report()
        run = invoke(SCORE, "--reports-dir", self.reports)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["cases_scored"], 1)
        self.assertEqual(result["confusion"]["true_block"], 2)
        self.assertEqual(result["confusion"]["false_block"], 0)
        self.assertEqual(result["metrics"]["block_recall_including_abstentions"], 1)
        self.assertTrue(result["ground_truth_status"].startswith("PROPOSED"))
        self.assertEqual(invoke(SCORE, "--reports-dir", self.reports,
                                "--require-complete").returncode, 1)

    def test_invalid_report_does_not_contribute_metrics(self):
        self._submit_report(tamper=True)
        run = invoke(SCORE, "--reports-dir", self.reports)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        entry = next(x for x in result["cases"] if x["case_id"] == "role-drift")
        self.assertEqual(entry["status"], "INVALID")
        self.assertEqual(result["cases_scored"], 0)
        self.assertEqual(result["confusion"]["true_block"], 0)
        self.assertIsNone(result["metrics"]["block_precision"])


if __name__ == "__main__":
    unittest.main()
