"""Bind accepted requirements to real reviewed RPG nodes and independent contracts."""
import hashlib
import json
from pathlib import Path
import sys
import yaml

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
graph_path = Path(sys.argv[1]) if len(sys.argv) > 1 else RUN / 'rpg-context-1/rpg.json'
graph = json.loads(graph_path.read_text())
features = {}


def visit(node):
    if node.get('node_type') == 'feature':
        features.setdefault(node['name'], []).append(node)
    for child in node.get('children', []):
        visit(child)


visit(graph['root'])
selection = {
    'REQ-CHECKER-101': ['validate flow addresses', 'validate flow protocol', 'validate flow ports',
                        'parse invocation options'],
    'REQ-CHECKER-102': ['retrieve relevant pairs', 'deduplicate relevant pairs', 'retrieve relevant snapshot',
                        'reject missing snapshot', 'validate snapshot structure', 'validate placement entries'],
    'REQ-CHECKER-103': ['evaluate stored rule match', 'collect matching evidence', 'build evidence group',
                        'render json report', 'render text groups'],
    'REQ-CHECKER-104': ['determine evidence status', 'reject missing snapshot', 'emit request diagnostic',
                        'describe saved evidence scope'],
}
requirements = yaml.safe_load((ROOT / '.harness/knowledge/requirements.yaml').read_text())
assert {r['id'] for r in requirements['content']['requirements']} == set(selection)
trace = []
for requirement, names in selection.items():
    nodes = []
    for name in names:
        if len(features.get(name, [])) != 1:
            raise AssertionError(f'Missing/ambiguous real RPG feature: {name}')
        node = features[name][0]
        locator = node.get('meta', {}).get('path')
        assert locator, node['id']
        relative = Path(locator.split('::', 1)[0])
        assert not relative.is_absolute() and '..' not in relative.parts, relative
        assert relative.suffix == '.py' and relative.parts[0] in {'src', 'checker', 'tests'}, relative
        path = ROOT / relative
        if '--require-source' in sys.argv:
            assert path.is_file(), path
        nodes.append(dict(id=node['id'], feature=name, locator=locator,
                          source_sha256=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None))
    trace.append(dict(requirement=requirement, canonical_artifact='.harness/knowledge/requirements.yaml',
                      capability='checker.requirements', design_capabilities=['checker.domain', 'checker.interface', 'checker.components'],
                      rpg_nodes=nodes, test_contracts=['TD-BEHAVIOR', 'TD-BOUNDARIES'],
                      independent_oracle='docs/checker/scenarios.yaml'))
result = dict(status='SOURCE_BOUND' if '--require-source' in sys.argv else 'PLANNED_SOURCE_BINDINGS',
              rpg_snapshot=str(graph_path.relative_to(ROOT)) if graph_path.is_relative_to(ROOT) else str(graph_path),
              rpg_sha256=hashlib.sha256(graph_path.read_bytes()).hexdigest(), traceability=trace,
              limitation='Traceability is not proof of executable behavior; acceptance/conformance evidence is separate.')
(RUN / 'traceability.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
print('Bound all four requirements to actual RPG IDs and independent test contracts.')
