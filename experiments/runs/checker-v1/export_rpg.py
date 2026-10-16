"""Export real CoderMind outputs with immutable identities for semantic review."""
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import shutil
import sys

from cmind_cli._storage import workspace_data_dir

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
WORKSPACE = Path.home() / '.cache/agentic-checker-lab/runs/checker-v1/workspace'
DATA = workspace_data_dir(WORKSPACE)
DEST = RUN / ('rpg-' + sys.argv[1])
if DEST.exists():
    raise SystemExit('Export exists; choose a distinct evidence identity')
names = ['feature_spec', 'feature_build', 'feature_tree', 'skeleton', 'data_flow',
         'base_classes', 'interfaces', 'tasks', 'rpg']
for name in names:
    value = json.loads((DATA / (name + '.json')).read_text())
    if not isinstance(value, dict) or not value:
        raise SystemExit('Missing or invalid artifact: ' + name)
DEST.mkdir()
for name in names:
    shutil.copyfile(DATA / (name + '.json'), DEST / (name + '.json'))
for name in ['feature-construct.stdout', 'feature-construct.stderr', 'plan.stdout', 'plan.stderr']:
    shutil.copyfile(WORKSPACE.parent / name, DEST / name)
provenance = json.loads(distribution('cmind-cli').read_text('direct_url.json'))['vcs_info']['commit_id']
manifest = dict(status='EXPORTED_FOR_SEMANTIC_REVIEW', cmind_revision=provenance,
                workspace=str(WORKSPACE), data_directory=str(DATA),
                bridge_sha256=hashlib.sha256((RUN/'bridge.json').read_bytes()).hexdigest(),
                files={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DEST.iterdir())},
                model_cost=None, model_cost_note='No verified billing/token counters available.')
(DEST / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print('Exported', len(names), 'actual artifacts:', DEST)
