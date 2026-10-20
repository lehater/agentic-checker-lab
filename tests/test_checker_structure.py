"""Independent COMP-1/ARCH-1/POL-1 verification via public function roles.

Trace: TD-BOUNDARIES / OP-BOUNDARY / OR-BOUNDARY; VC-ARCH.
Physical paths are discovered from the accepted matches/check function contracts.
"""
import ast
import copy
import importlib
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / 'tests/fixtures/scenarios.json').read_text())['base']


def source_modules():
    modules = {}
    for root in [ROOT / 'checker', ROOT / 'src/acl_checker']:
        if root.is_dir():
            for path in root.rglob('*.py'):
                parts = list(path.relative_to(ROOT).with_suffix('').parts)
                if parts[-1] == '__init__':
                    parts.pop()
                modules['.'.join(parts)] = path
    return modules


def owner(function_name, modules):
    candidates = []
    for module, path in modules.items():
        tree = ast.parse(path.read_text())
        if any(isinstance(node, ast.FunctionDef) and node.name == function_name for node in tree.body):
            candidates.append((module, path))
    if len(candidates) != 1:
        raise AssertionError(f'Expected one public {function_name} function, found {candidates}')
    return candidates[0]


class CheckerStructure(unittest.TestCase):
    def test_inward_dependencies(self):
        modules = source_modules()
        pending = [owner(name, modules)[0] for name in ['matches', 'check']]
        visited = set()
        forbidden = {'argparse', 'json', 'pathlib', 'os', 'socket', 'subprocess',
                     'urllib', 'http', 'requests', 'harness', 'cmind_cli', 'tests', 'pytest'}
        while pending:
            module = pending.pop()
            if module in visited:
                continue
            visited.add(module)
            path = modules[module]
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                imports = []
                if isinstance(node, ast.Import):
                    imports = [item.name for item in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        package = module.rsplit('.', 1)[0]
                        prefix = package.split('.')[:len(package.split('.')) - node.level + 1]
                        imported = '.'.join([*prefix, *([node.module] if node.module else [])])
                    else:
                        imported = node.module or ''
                    imports = [imported, *[imported + '.' + item.name for item in node.names]]
                for imported in imports:
                    self.assertNotIn(imported.split('.')[0], forbidden,
                                     f'Inner role depends on infrastructure: {module} -> {imported}')
                    if imported in modules:
                        segments = set(imported.split('.'))
                        self.assertFalse(segments & {'cli', 'input', 'inputs', 'adapters'},
                                         f'Inner role imports outer adapter: {module} -> {imported}')
                        pending.append(imported)
        self.assertGreaterEqual(len(visited), 2)

    def test_runtime_dependency_inventory(self):
        allowed = set(sys.stdlib_module_names) | {'src', 'checker', '__future__'}
        modules = source_modules()
        self.assertTrue(modules, 'No runtime modules')
        for module, path in modules.items():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Import):
                    imports = [name.name for name in node.names]
                elif isinstance(node, ast.ImportFrom) and not node.level:
                    imports = [node.module or '']
                else:
                    imports = []
                for imported in imports:
                    self.assertIn(imported.split('.')[0], allowed,
                                  f'Unaccepted runtime dependency: {module} -> {imported}')

    def test_source_substitution_and_immutability(self):
        modules = source_modules()
        module_name, _ = owner('check', modules)
        check = getattr(importlib.import_module(module_name), 'check')
        data = copy.deepcopy(BASE)
        before = copy.deepcopy(data)
        calls = []
        snapshots = {(s['device'], s['acl']): s for s in data['snapshots']}

        def relevance(source, destination):
            calls.append(('relevance', str(source), str(destination)))
            return data['relevance']

        def snapshot(device, acl):
            calls.append(('snapshot', device, acl))
            return snapshots[(device, acl)]

        result = check(data['flow'], relevance, snapshot)
        relevance_calls = [call for call in calls if call[0] == 'relevance']
        self.assertTrue(relevance_calls)
        self.assertEqual(set(relevance_calls), {('relevance', '10.0.0.1', '192.0.2.10')})
        # Lookup scheduling/caching is private; observable groups establish order/dedup.
        self.assertEqual({call for call in calls if call[0] == 'snapshot'}, {
            ('snapshot', 'fw-a', 'outside'), ('snapshot', 'fw-a', 'inside'),
            ('snapshot', 'fw-b', 'global')})
        self.assertEqual([(g['device'], g['acl'], g['status'], [r['id'] for r in g['rules']])
                          for g in result],
                         [('fw-a', 'outside', 'MATCHES', ['z-deny', 'a-permit']),
                          ('fw-a', 'inside', 'NO_MATCH', []), ('fw-b', 'global', 'NO_MATCH', [])])
        self.assertEqual(data, before)

        def broken_source(source, destination):
            raise RuntimeError('provider programming error')

        with self.assertRaisesRegex(RuntimeError, 'provider programming error'):
            check(data['flow'], broken_source, snapshot)


if __name__ == '__main__':
    unittest.main()
