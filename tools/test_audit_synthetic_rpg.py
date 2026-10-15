#!/usr/bin/env python3
"""Check the Makefile audit target emits *only* JSON on stdout."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class AuditMakeTargetTest(unittest.TestCase):
    def test_json_stdout_without_recipe_echo(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for name in ("feature_spec", "feature_build", "feature_tree", "skeleton"):
                (folder / f"{name}.json").write_text("{}\n", encoding="utf-8")
            fixture = {
                "repo_name": "word-count-lab",
                "root": {
                    "id": "root", "name": "word-count-lab", "node_type": "repo",
                    "children": [{"id": "feature1", "name": "count", "node_type": "feature", "children": []}],
                },
                "edges": [{"src": "root", "dst": "feature1", "relation": "references"}],
            }
            (folder / "rpg.json").write_text(json.dumps(fixture), encoding="utf-8")
            result = subprocess.run(
                ["make", "cmind-rpg-audit", f"RPG_AUDIT_DIR={folder}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "STRUCTURE_PASS_SEMANTICS_UNREVIEWED")
            self.assertEqual(payload["repo_name"], "word-count-lab")
            self.assertEqual(payload["node_count"], 2)
            self.assertEqual(payload["edge_count"], 1)

if __name__ == "__main__":
    unittest.main()
