"""Meaningful predicate/order mutations in temporary source copies only."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
sys.path.insert(0, str(ROOT / 'tests'))
from test_checker_structure import owner, source_modules

SCENARIOS = json.loads((ROOT / 'tests/fixtures/scenarios.json').read_text())
CASES = [c for c in SCENARIOS['cases'] if c['id'] in {'SC-ALL', 'SC-UDP', 'SC-SOURCE-OUTSIDE', 'SC-DPORT-LOW', 'SC-DPORT-HIGH'}]
modules = source_modules()
_, matching = owner('matches', modules)
_, collection = owner('collect_matching_evidence', modules)
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [matching, collection]}


def observe(workspace):
    outcomes = []
    for case in CASES:
        data = copy.deepcopy(SCENARIOS['base'])
        for key, value in case.get('changes', {}).items():
            parent, name = key.split('.')
            data[parent][name] = value
        request = workspace / 'input.json'
        request.write_text(json.dumps(data))
        process = subprocess.run([sys.executable, '-m', 'checker', '--input', str(request), '--format', 'json'],
                                 cwd=workspace, capture_output=True, text=True, timeout=15)
        if process.returncode:
            raise AssertionError('Mutant failed to execute, not a semantic detection: ' + process.stderr)
        report = json.loads(process.stdout)
        actual = [r['id'] for group in report['groups'] for r in group['rules']]
        expected = case.get('expected_rule_ids')
        if expected is None:
            expected = [i for g in case['expected_groups'] for i in g['rules']]
        outcomes.append(dict(case=case['id'], expected=expected, actual=actual, matches=actual == expected))
    return outcomes


def mutate(path, name, kind):
    tree = ast.parse(path.read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    if kind in {'always_true', 'always_false'}:
        function.body = [ast.Return(ast.Constant(kind == 'always_true'))]
    elif kind == 'exclusive_ports':
        changed = 0
        for node in ast.walk(function):
            if isinstance(node, ast.Compare):
                for index, operator in enumerate(node.ops):
                    if isinstance(operator, ast.LtE):
                        node.ops[index] = ast.Lt()
                        changed += 1
        assert changed, 'No inclusive comparisons found for this mutation'
    else:
        changed = 0
        for node in ast.walk(function):
            if isinstance(node, ast.Return) and node.value is not None:
                original = node.value
                if kind == 'first_only':
                    node.value = ast.Subscript(value=original, slice=ast.Slice(upper=ast.Constant(1)), ctx=ast.Load())
                elif kind == 'sort_by_id':
                    key = ast.Lambda(args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='rule')], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
                                     body=ast.Subscript(value=ast.Name(id='rule', ctx=ast.Load()), slice=ast.Constant('id'), ctx=ast.Load()))
                    node.value = ast.Call(func=ast.Name(id='sorted', ctx=ast.Load()), args=[original], keywords=[ast.keyword(arg='key', value=key)])
                elif kind == 'permit_only':
                    condition = ast.Compare(left=ast.Subscript(value=ast.Name(id='rule', ctx=ast.Load()), slice=ast.Constant('action'), ctx=ast.Load()),
                                            ops=[ast.Eq()], comparators=[ast.Constant('permit')])
                    node.value = ast.ListComp(elt=ast.Name(id='rule', ctx=ast.Load()), generators=[ast.comprehension(
                        target=ast.Name(id='rule', ctx=ast.Store()), iter=original, ifs=[condition], is_async=0)])
                else:
                    raise ValueError(kind)
                changed += 1
        assert changed, 'No return found for collection mutation'
    tree = ast.fix_missing_locations(tree)
    compile(tree, str(path), 'exec')
    path.write_text(ast.unparse(tree) + '\n')


results = []
for kind in ['baseline', 'always_true', 'always_false', 'exclusive_ports', 'first_only', 'sort_by_id', 'permit_only']:
    with tempfile.TemporaryDirectory(prefix='checker-mutation-') as directory:
        workspace = Path(directory)
        for name in ['checker', 'src']:
            shutil.copytree(ROOT / name, workspace / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        if kind != 'baseline':
            target = matching if kind in {'always_true', 'always_false', 'exclusive_ports'} else collection
            mutate(workspace / target.relative_to(ROOT), 'matches' if target == matching else 'collect_matching_evidence', kind)
        cases = observe(workspace)
        all_match = all(case['matches'] for case in cases)
        assert all_match if kind == 'baseline' else not all_match, (kind, cases)
        results.append(dict(mutation=kind, status='PASS' if kind == 'baseline' else 'DETECTED', cases=cases))
for relative, digest in before.items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
(RUN / 'mutations.json').write_text(json.dumps(dict(status='PASS', original_source_unchanged=True, results=results), indent=2)+'\n')
print('PASS: baseline and six semantic mutants; original source unchanged')
