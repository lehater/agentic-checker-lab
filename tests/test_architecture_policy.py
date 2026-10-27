"""Requirement-led architecture tests; historical defect is only one witness."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_architecture.py"
POLICY = ROOT / "docs/engineering/architecture-contract.json"
OLD = ROOT / "tests/fixtures/architecture/legacy-cmind-skeleton.json"


def run_guard(*args: str, contract=POLICY):
    r = subprocess.run([sys.executable, str(SCRIPT), "--contract", str(contract), "--json", *args],
                       capture_output=True, text=True, check=False)
    return r.returncode, json.loads(r.stdout) if r.stdout else {"stderr": r.stderr}


def skeleton(tmp: Path, *files):
    target = tmp / "skeleton.json"
    target.write_text(json.dumps({"root": {"type": "directory", "children": [
        {"type": "file", "path": path, "feature_paths": features} for path, features in files
    ]}}, ensure_ascii=False), encoding="utf-8")
    return target


def src(tmp: Path, files: dict[str, str]) -> Path:
    root = tmp / "src/acl_checker"
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


class ArchitectureContractTests(unittest.TestCase):
    def assert_failed_rule(self, report, text):
        self.assertEqual(report["status"], "FAIL", report)
        self.assertTrue(any(text in e for e in report["violations"]), report)

    def test_ar01_accepted_layer_paths_pass(self):
        with tempfile.TemporaryDirectory() as d:
            temp = Path(d)
            path = skeleton(temp, ("src/acl_checker/domain/model.py", []),
                            ("src/acl_checker/application/usecase.py", []),
                            ("src/acl_checker/cli/main.py", []))
            code, report = run_guard("--skeleton", str(path))
            self.assertEqual(code, 0, report)
            self.assertEqual(report["checked"]["skeleton_files"], 3)

    def test_ar02_any_nested_layer_root_is_rejected(self):
        for wrong in ("domain/application/work.py", "domain/cli/io.py",
                      "application/adapters/service.py", "input/domain/reverse.py"):
            with self.subTest(wrong=wrong), tempfile.TemporaryDirectory() as d:
                p = skeleton(Path(d), ("src/acl_checker/" + wrong, []))
                code, report = run_guard("--skeleton", str(p))
                self.assertEqual(code, 1)
                self.assert_failed_rule(report, "nested layer root")

    def test_ar03_direction_matrix_on_absolute_and_relative_imports(self):
        cases = [
            ("domain/rules.py", "from src.acl_checker.application.core import usecase\n",
             "domain -> application"),
            ("domain/model.py", "from src.acl_checker.input.json_data import load\n",
             "domain -> adapters"),
            ("application/usecase.py", "from src.acl_checker.cli.main import run\n",
             "application -> adapters"),
            ("domain/nested/rules.py", "from ...application.service import do\n",
             "domain -> application"),
        ]
        for rel, code, violation in cases:
            with self.subTest(rel=rel), tempfile.TemporaryDirectory() as d:
                root = src(Path(d), {rel: code})
                status, report = run_guard("--source-root", str(root))
                self.assertEqual(status, 1, report)
                self.assert_failed_rule(report, violation)

    def test_ar04_inward_imports_and_standard_helpers_are_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            root = src(Path(d), {
                "domain/rules.py": "import ipaddress\ndef helper(): return True\n",
                "application/runner.py": "from src.acl_checker.domain.rules import helper\n",
                "cli/main.py": "from src.acl_checker.application.runner import helper\n",
            })
            code, report = run_guard("--source-root", str(root))
            self.assertEqual(code, 0, report)

    def test_ar05_declared_symbol_responsibilities_without_engine_hardcoding(self):
        for name, rel in [("check", "domain/anything.py"), ("matches", "application/other.py")]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                root = src(Path(d), {rel: f"def {name}(): pass\n"})
                code, report = run_guard("--source-root", str(root))
                self.assertEqual(code, 1, report)
                self.assert_failed_rule(report, f"{name} belongs in")

    def test_ar06_declared_feature_responsibility_before_codegen(self):
        with tempfile.TemporaryDirectory() as d:
            p = skeleton(Path(d), ("src/acl_checker/domain/evidence.py", [
                "Исследование совпадений ACL/investigation execution/check traffic evidence"]))
            code, report = run_guard("--skeleton", str(p))
            self.assertEqual(code, 1)
            self.assert_failed_rule(report, "belongs in application")

    def test_ar07_indirect_module_import_cycle_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = src(Path(d), {
                "application/a.py": "from src.acl_checker.application.b import f\n",
                "application/b.py": "from src.acl_checker.application.c import f\n",
                "application/c.py": "from src.acl_checker.application.a import f\n",
            })
            code, report = run_guard("--source-root", str(root))
            self.assertEqual(code, 1)
            self.assert_failed_rule(report, "module import cycle")

    def test_ar08_no_false_pass_on_empty_or_unrelated_input(self):
        for paths in [[], [("unrelated/foo.py", [])]]:
            with self.subTest(paths=paths), tempfile.TemporaryDirectory() as d:
                p = skeleton(Path(d), *paths)
                status, report = run_guard("--skeleton", str(p))
                self.assertEqual(status, 1)
                self.assert_failed_rule(report, "no files matching")

    def test_ar09_invalid_policy_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            src_root = src(tmp, {"domain/model.py": "pass\n"})
            config = tmp / "policy.json"
            policy = json.loads(POLICY.read_text())
            policy["allowed_dependencies"].pop("application")
            config.write_text(json.dumps(policy), encoding="utf-8")
            status, report = run_guard("--source-root", str(src_root), contract=config)
            self.assertEqual(status, 1)
            self.assert_failed_rule(report, "invalid contract")

    def test_ar10_engine_is_reusable_for_other_package_and_role_names(self):
        with tempfile.TemporaryDirectory() as d:
            temp = Path(d)
            alternate = {
                "schema": "architecture-contract/v1", "package_path": "lib/shop",
                "module_prefix": "lib.shop",
                "layers": {"core": ["kernel"], "service": ["workflow"], "edge": ["http"]},
                "allowed_dependencies": {
                    "core": ["core"], "service": ["core", "service"],
                    "edge": ["core", "service", "edge"]
                },
                "symbol_owners": {"purchase": "service"},
                "feature_owners": {"checkout": "service"},
                "disallow_nested_layer_roots": True,
            }
            contract = temp / "arch.json"
            contract.write_text(json.dumps(alternate), encoding="utf-8")
            p = skeleton(temp, ("lib/shop/kernel/main.py", ["checkout"]))
            status, report = run_guard("--skeleton", str(p), contract=contract)
            self.assertEqual(status, 1, report)
            self.assert_failed_rule(report, "belongs in service")
            p = skeleton(temp, ("lib/shop/workflow/purchase.py", ["checkout"]))
            status, report = run_guard("--skeleton", str(p), contract=contract)
            self.assertEqual(status, 0, report)
            root = temp / "lib/shop"
            (root / "kernel").mkdir(parents=True)
            (root / "kernel/main.py").write_text("def purchase(): pass\n", encoding="utf-8")
            status, report = run_guard("--source-root", str(root), contract=contract)
            self.assertEqual(status, 1)
            self.assert_failed_rule(report, "purchase belongs in service")

    def test_historical_cmind_path_stays_as_regression_witness(self):
        code, report = run_guard("--skeleton", str(OLD))
        self.assertEqual(code, 1, report)
        self.assert_failed_rule(report, "nested layer root")


if __name__ == "__main__":
    unittest.main()
