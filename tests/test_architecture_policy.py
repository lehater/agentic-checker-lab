"""Architecture gate regression, independent of unmerged Checker PR #27."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_architecture.py"
FIXTURE = ROOT / "tests/fixtures/architecture/legacy-cmind-skeleton.json"


def run_guard(*args: str) -> tuple[int, dict]:
    proc = subprocess.run([sys.executable, str(SCRIPT), "--json", *args],
                          capture_output=True, text=True, check=False)
    return proc.returncode, json.loads(proc.stdout)


class ArchitecturePolicyTest(unittest.TestCase):
    def test_real_historical_rpg_path_rejected_before_codegen(self):
        rc, report = run_guard("--skeleton", str(FIXTURE))
        self.assertEqual(rc, 1)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("domain/application/check.py" in e for e in report["violations"]))

    def test_corrected_rpg_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "skeleton.json"
            p.write_text(json.dumps({"root": {"type": "directory", "children": [
                {"type": "file", "path": "src/acl_checker/application/check.py"},
                {"type": "file", "path": "src/acl_checker/domain/matching.py"},
                {"type": "file", "path": "src/acl_checker/cli/main.py"}
            ]}}), encoding="utf-8")
            rc, result = run_guard("--skeleton", str(p))
            self.assertEqual(rc, 0, result)
            self.assertEqual(result["checked"]["skeleton_files"], 3)

    def test_real_historical_reverse_import_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "src/acl_checker"
            path = package / "domain/application/check.py"
            path.parent.mkdir(parents=True)
            path.write_text("from src.acl_checker.application.types import Snapshot\n\n"
                            "def check(): pass\n", encoding="utf-8")
            rc, report = run_guard("--source-root", str(package))
            self.assertEqual(rc, 1)
            self.assertTrue(any("domain -> application" in e for e in report["violations"]))
            self.assertTrue(any("check()" in e for e in report["violations"]))

    def test_inward_imports_are_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "src/acl_checker"
            domain = package / "domain/matching.py"
            app = package / "application/check.py"
            domain.parent.mkdir(parents=True)
            app.parent.mkdir(parents=True)
            domain.write_text("def matches(flow, rule): return True\n", encoding="utf-8")
            app.write_text("from src.acl_checker.domain.matching import matches\n\n"
                           "def check(flow): return matches(flow, {})\n", encoding="utf-8")
            rc, report = run_guard("--source-root", str(package))
            self.assertEqual(rc, 0, report)
            self.assertEqual(report["checked"]["source_modules"], 2)

    def test_reverse_application_to_cli_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "src/acl_checker"
            app = package / "application/check.py"
            app.parent.mkdir(parents=True)
            app.write_text("from src.acl_checker.cli.main import main\n", encoding="utf-8")
            rc, report = run_guard("--source-root", str(package))
            self.assertEqual(rc, 1)
            self.assertTrue(any("application -> cli" in e for e in report["violations"]))

    def test_no_silent_empty_skeleton_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "empty.json"
            p.write_text('{"root":{"type":"directory","children":[]}}', encoding="utf-8")
            rc, report = run_guard("--skeleton", str(p))
            self.assertEqual(rc, 1)
            self.assertTrue(any("no file paths" in e for e in report["violations"]))


if __name__ == "__main__":
    unittest.main()
