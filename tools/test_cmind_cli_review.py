#!/usr/bin/env python3
"""Regression of actual patched guards; model/test execution replaced, not guards."""
from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
lock = json.loads((ROOT / 'tooling/patches/cmind-cli-global-review.json').read_text())
overlay = Path.home() / '.cache/agentic-checker-lab/overlays' / lock['patch_sha256']
sys.path.insert(0, str(overlay / 'cmind_cli/core_pack/scripts'))
from code_gen import global_review as review


def exercise(interface='visual', *, pytest_pass=True, stub=False, unresolved=False, pages=0):
    section = dict(verified=['CLI behavior'], fixed=[], failed=[], not_tested=[])
    checklist = dict(functional=section, pages_inspected=pages, screenshots_taken=0)
    if unresolved:
        section['not_tested'] = ['unverified required feature']
    tests = SimpleNamespace(success=pytest_pass, passed=197 if pytest_pass else 196,
                            failed=0 if pytest_pass else 1, errors=0, output='test result')
    with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
        workspace = Path(directory)
        stack.enter_context(patch.multiple(review,
            resolve_test_backend=lambda **kw: SimpleNamespace(name='python'),
            ensure_deps_installed=lambda *a, **kw: None,
            run_project_tests=lambda *a, **kw: tests,
            _save_stage_result=lambda *a, **kw: None,
            _build_review_prompt=lambda *a, **kw: 'Verify project',
            _build_review_retry_context=lambda *a, **kw: 'retry',
            _cleanup_background_processes=lambda *a, **kw: None,
            dispatch_sub_agent=lambda *a, **kw: ('REVIEW_RESULT: DONE', None),
            _extract_review_checklist=lambda *a, **kw: checklist))
        stack.enter_context(patch('smoke_test._find_source_files', return_value=[workspace / 'stub.py']))
        stack.enter_context(patch('code_gen.static_checks.static_completeness_check',
                                  return_value=['STUB: missing body'] if stub else []))
        kwargs = {} if interface == 'default' else {'interface_kind': interface}
        return review.global_review(repo_path=workspace, max_iterations=1, **kwargs)


checks = {
    'cli_without_visuals': exercise('cli')['success'],
    'visual_without_visuals_rejected': not exercise('visual')['success'],
    'default_without_visuals_rejected': not exercise('default')['success'],
    'visual_with_inspection': exercise('visual', pages=1)['success'],
    'cli_failed_tests_rejected': not exercise('cli', pytest_pass=False)['success'],
    'cli_stubs_rejected': not exercise('cli', stub=True)['success'],
    'cli_unresolved_feature_rejected': not exercise('cli', unresolved=True)['success'],
}
try:
    exercise('unknown')
except ValueError:
    checks['unknown_scope_rejected'] = True
else:
    checks['unknown_scope_rejected'] = False
assert all(checks.values()), checks
print(json.dumps(dict(status='PASS', patch_sha256=lock['patch_sha256'], model_calls=0,
                      scope='Tool regression with external providers replaced', checks=checks), indent=2))
