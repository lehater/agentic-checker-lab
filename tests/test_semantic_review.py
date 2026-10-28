"""Offline semantic-report protocol and adversarial-source regression tests."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
PREPARE = REPO / "tools/prepare_semantic_review.py"
CHECK = REPO / "tools/check_semantic_review.py"
CANDIDATE = "tests/fixtures/semantic-review/historical-rpg-excerpt.json"
POLICY = "docs/engineering/policy.md"
CONTRACT = "docs/engineering/architecture-contract.json"


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], cwd=REPO,
                          capture_output=True, text=True, check=False)


class SemanticReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.request = self.folder / "request.json"
        self.report_file = self.folder / "report.json"
        self.prep = run(PREPARE, "--repo-root", REPO, "--candidate", CANDIDATE,
                        "--constraint", POLICY, "--constraint", CONTRACT,
                        "--subject", "checker-historical-rpg", "--output", self.request)
        self.assertEqual(self.prep.returncode, 0, self.prep.stderr)
        self.req = json.loads(self.request.read_text(encoding="utf-8"))
        self.citation = self.quote("candidate-1", "domain/application/check.py")
        self.report = {
            "schema": "semantic-review-report/v1",
            "request_sha256": hashlib.sha256(self.request.read_bytes()).hexdigest(),
            "reviewer": {"kind": "fixture", "identifier": "handwritten contract test (not AI)"},
            "coverage": [
                {"rule_id": name, "assessment": "uncertain",
                 "rationale": "Independent reviewer has not established compliance.",
                 "citations": [self.citation]}
                for name in self.req["required_rules"]
            ],
            "findings": [],
        }

    def quote(self, source_id, needle):
        source = next(s for s in self.req["sources"] if s["id"] == source_id)
        lines = (REPO / source["path"]).read_text(encoding="utf-8").splitlines()
        lineno = next(n for n, line in enumerate(lines, 1) if needle in line)
        return {"source_id": source_id, "start_line": lineno,
                "end_line": lineno, "quote": needle}

    def verify(self):
        self.report_file.write_text(json.dumps(self.report, ensure_ascii=False), encoding="utf-8")
        p = run(CHECK, "--repo-root", REPO, "--request", self.request,
                "--report", self.report_file)
        return p.returncode, json.loads(p.stdout)

    def test_incomplete_semantic_evidence_escalates_not_passes(self):
        status, out = self.verify()
        self.assertEqual(status, 0, out)
        self.assertEqual(out["decision"], "ESCALATE")
        self.assertIs(out["semantic_truth_verified"], False)

    def test_all_pass_is_still_human_review_required(self):
        for r in self.report["coverage"]:
            r["assessment"] = "pass"
        status, out = self.verify()
        self.assertEqual(status, 0, out)
        self.assertEqual(out["decision"], "HUMAN_REVIEW_REQUIRED")
        self.assertIs(out["semantic_truth_verified"], False)

    def test_historical_misplacement_is_one_explicit_failure_witness(self):
        entry = next(r for r in self.report["coverage"] if r["rule_id"] == "AR-03")
        entry["assessment"] = "fail"
        self.report["findings"] = [{
            "id": "finding-1", "rule_id": "AR-03", "severity": "BLOCKER",
            "claim": "Use-case orchestration is placed in domain/application",
            "reasoning": "Assigned implementation feature and proposed package violate the layer role",
            "minimal_fix": "Place use-case orchestration in the application layer; preserve matching in domain",
            "citations": [self.citation]
        }]
        status, out = self.verify()
        self.assertEqual(status, 0, out)
        self.assertEqual(out["decision"], "BLOCK")
        self.assertIs(out["semantic_truth_verified"], False)

    def test_missing_rule_coverage_fails_closed(self):
        self.report["coverage"].pop()
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("missing coverage", result["error"])

    def test_duplicate_rule_coverage_fails_closed(self):
        self.report["coverage"].append(self.report["coverage"][0])
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("repeated", result["error"])

    def test_fabricated_quote_fails_closed(self):
        self.report["coverage"][0]["citations"] = [{
            **self.citation, "quote": "line that does not exist in the archived design"}]
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("quote not present", result["error"])

    def test_out_of_range_citation_fails_closed(self):
        self.report["coverage"][0]["citations"] = [{
            **self.citation, "end_line": 9999}]
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("citation range", result["error"])

    def test_wrong_source_id_fails_closed(self):
        self.report["coverage"][0]["citations"] = [{
            **self.citation, "source_id": "not-in-request"}]
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("unknown source id", result["error"])

    def test_stale_request_hash_fails_closed(self):
        self.report["request_sha256"] = "0" * 64
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("stale request", result["error"])

    def test_source_digest_change_detected(self):
        self.req["sources"][0]["sha256"] = "f" * 64
        self.request.write_text(json.dumps(self.req), encoding="utf-8")
        self.report["request_sha256"] = hashlib.sha256(self.request.read_bytes()).hexdigest()
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("stale or modified source", result["error"])

    def test_fail_assessment_needs_matching_finding(self):
        self.report["coverage"][0]["assessment"] = "fail"
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("without finding", result["error"])

    def test_path_escape_is_invalid_even_with_digest(self):
        self.req["sources"][0]["path"] = "../etc/passwd"
        self.request.write_text(json.dumps(self.req), encoding="utf-8")
        self.report["request_sha256"] = hashlib.sha256(self.request.read_bytes()).hexdigest()
        status, result = self.verify()
        self.assertEqual(status, 1, result)
        self.assertIn("path must be relative", result["error"])

    def test_prepare_rejects_external_files(self):
        p = run(PREPARE, "--repo-root", REPO, "--candidate", "../etc/passwd",
                "--constraint", POLICY, "--subject", "x", "--output", self.request)
        self.assertNotEqual(p.returncode, 0)

    def test_sources_are_pinned_to_real_revisions(self):
        self.assertEqual(self.req["schema"], "semantic-review-request/v1")
        self.assertEqual(len(self.req["sources"]), 3)
        for source in self.req["sources"]:
            contents = (REPO / source["path"]).read_bytes()
            self.assertEqual(source["sha256"], hashlib.sha256(contents).hexdigest())


if __name__ == "__main__":
    unittest.main()
