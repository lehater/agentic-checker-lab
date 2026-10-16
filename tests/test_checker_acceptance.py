"""Independent public oracle: expectations were committed before RPG/code.

Run: python3 -m unittest discover -s tests -v
Trace: TD-BEHAVIOR/OP-SCENARIOS/OR-SCENARIOS, TD-BOUNDARIES/OP-BOUNDARY/OR-BOUNDARY.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = json.loads((ROOT / 'tests/fixtures/scenarios.json').read_text())


def invoke(data, output='json', raw=None):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'input.json'
        path.write_text(json.dumps(data) if raw is None else raw)
        before = path.read_bytes()
        result = subprocess.run([sys.executable, '-m', 'checker', '--input', str(path),
                                '--format', output], cwd=ROOT, capture_output=True, text=True)
        if path.read_bytes() != before:
            raise AssertionError('CLI changed the supplied snapshot file')
        return result


class CheckerAcceptance(unittest.TestCase):
    def assert_error(self, result):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertIn('Checker error:', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_precode_scenarios(self):
        for case in SCENARIOS['cases']:
            with self.subTest(case=case['id']):
                data = copy.deepcopy(SCENARIOS['base'])
                for key, value in case.get('changes', {}).items():
                    parent, name = key.split('.')
                    data[parent][name] = value
                if 'remove_snapshot' in case:
                    missing = case['remove_snapshot']
                    data['snapshots'] = [s for s in data['snapshots']
                                         if (s['device'], s['acl']) != (missing['device'], missing['acl'])]
                if 'add_rule_field' in case:
                    data['snapshots'][0]['rules'][0].update(case['add_rule_field'])
                original = copy.deepcopy(data)
                result = invoke(data)
                self.assertEqual(data, original)
                if case.get('expected_error'):
                    self.assert_error(result)
                    continue
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                report = json.loads(result.stdout)
                self.assertEqual(set(report), {'version', 'groups'})
                self.assertEqual(report['version'], 1)
                groups = report['groups']
                self.assertEqual([(g['device'], g['acl']) for g in groups],
                                 [('fw-a', 'outside'), ('fw-a', 'inside'), ('fw-b', 'global')])
                ids = [r['id'] for g in groups for r in g['rules']]
                if 'expected_rule_ids' in case:
                    self.assertEqual(ids, case['expected_rule_ids'])
                for index, group in enumerate(groups):
                    self.assertEqual(set(group), {'device', 'acl', 'placements', 'status', 'rules'})
                    snapshot = next(s for s in data['snapshots']
                                    if (s['device'], s['acl']) == (group['device'], group['acl']))
                    self.assertEqual(group['placements'], snapshot['placements'])
                    for rule in group['rules']:
                        self.assertIn(rule, snapshot['rules'])
                    self.assertEqual(group['status'], 'MATCHES' if group['rules'] else 'NO_MATCH')
                    if 'expected_groups' in case:
                        expected = case['expected_groups'][index]
                        self.assertEqual([r['id'] for r in group['rules']], expected['rules'])
                        self.assertEqual([r['action'] for r in group['rules']], expected['actions'])
                        self.assertEqual(group['status'], expected['status'])

    def test_text_report(self):
        result = invoke(SCENARIOS['base'], 'text')
        self.assertEqual(result.returncode, 0, result.stderr)
        for text in ['fw-a', 'outside', 'inside', 'fw-b', 'global', 'MATCHES', 'NO_MATCH',
                     'z-deny', 'a-permit', 'deny', 'permit', 'wan0', '50000', '443',
                     'source', 'destination', 'protocol', 'source_ports', 'destination_ports']:
            self.assertIn(text, result.stdout)
        self.assertLess(result.stdout.index('z-deny'), result.stdout.index('a-permit'))

    def test_strict_boundary(self):
        changes = [
            ('version', 2), ('version', True), ('flow.source_port', True),
            ('flow.destination_port', -1), ('flow.protocol', 'icmp'),
            ('flow.source', 'not-an-ip'), ('flow.extra', 'unsupported'),
            ('snapshots.0.rules.0.source', '10.0.0.1/24'),
            ('snapshots.0.rules.0.source_ports', [5, 4]),
            ('snapshots.0.rules.0.destination_ports', [0, 65536]),
            ('snapshots.0.rules.0.action', 'maybe'),
            ('snapshots.0.rules.0.source_ports', [True, 50000]),
            ('snapshots.2.placements.0.global', 1),
            ('snapshots.0.rules.0.protocol', 'icmp'),
            ('snapshots.0.placements.0.direction', 'sideways'),
            ('snapshots.0.placements.0.extra', True),
            ('relevance.0.device', ''), ('relevance.0.acl', 7),
        ]
        for key, value in changes:
            with self.subTest(field=key, value=value):
                data = copy.deepcopy(SCENARIOS['base'])
                parent = data
                parts = key.split('.')
                for part in parts[:-1]:
                    parent = parent[int(part)] if isinstance(parent, list) else parent[part]
                parent[parts[-1]] = value
                self.assert_error(invoke(data))
        for raw in ['{broken', '[]', 'null']:
            with self.subTest(raw=raw):
                self.assert_error(invoke(None, raw=raw))

    def test_duplicate_snapshot_and_rule_rejected(self):
        data = copy.deepcopy(SCENARIOS['base'])
        data['snapshots'].append(copy.deepcopy(data['snapshots'][0]))
        self.assert_error(invoke(data))
        data = copy.deepcopy(SCENARIOS['base'])
        data['snapshots'][0]['rules'].append(copy.deepcopy(data['snapshots'][0]['rules'][0]))
        self.assert_error(invoke(data))

    def test_same_rule_id_in_distinct_acls(self):
        data = copy.deepcopy(SCENARIOS['base'])
        data['flow']['protocol'] = 'udp'
        data['snapshots'][2]['rules'][0]['id'] = 'a-permit'
        result = invoke(data)
        self.assertEqual(result.returncode, 0, result.stderr)
        groups = json.loads(result.stdout)['groups']
        self.assertEqual([(g['device'], g['acl'], [r['id'] for r in g['rules']]) for g in groups],
                         [('fw-a', 'outside', ['a-permit']), ('fw-a', 'inside', []),
                          ('fw-b', 'global', ['a-permit'])])

    def test_help_and_required_input(self):
        help_result = subprocess.run([sys.executable, '-m', 'checker', '--help'], cwd=ROOT,
                                     capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=10)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn('--input', help_result.stdout)
        self.assertIn('IPv4', help_result.stdout)
        missing = subprocess.run([sys.executable, '-m', 'checker'], cwd=ROOT,
                                 capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=10)
        self.assertEqual(missing.returncode, 2, missing.stderr)
        self.assertEqual(missing.stdout, '')

    def test_missing_and_empty_inputs(self):
        data = copy.deepcopy(SCENARIOS['base'])
        del data['flow']['source_port']
        self.assert_error(invoke(data))
        result = subprocess.run([sys.executable, '-m', 'checker', '--input', '/nonexistent/checker.json'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assert_error(result)
        data = copy.deepcopy(SCENARIOS['base'])
        data['relevance'] = []
        result = invoke(data)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'version': 1, 'groups': []})
        self.assertIn('Нет релевантных ACL', invoke(data, 'text').stdout)


if __name__ == '__main__':
    unittest.main()
