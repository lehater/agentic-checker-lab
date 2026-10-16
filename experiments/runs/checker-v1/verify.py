"""Read-only admission/currentness verification and negative CAS checks."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import yaml

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
PIN = json.loads((ROOT / '.harness/harness-binding.json').read_text())['source']['revision']
PACK = Path.home() / '.cache/harness/v1' / PIN
sys.path.insert(0, str(PACK / 'src'))
from harness.application.project_publication import read_project_publication, publish_project_publication
from harness.application.semantic_admission import derive_acceptance_policy_fingerprints
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.project_model.engineering_graph import validate_realization
from harness.project_model.core import CoreError


def load(path):
    return yaml.safe_load(Path(path).read_text())


graph = load(ROOT / '.harness/engineering-graph.yaml')
path = ROOT / '.harness/project-publication.yaml'
original = path.read_bytes()
pub = read_project_publication(path, graph=graph)
state = pub['state']
model = validate_realization(graph, state['core_model'])
policy = derive_acceptance_policy_fingerprints(
    graph=graph, knowledge_contracts=load(PACK / 'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml'),
    decision_contracts=load(PACK / 'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml'),
    decision_policy=load(ROOT / '.harness/decision-policy.yaml'))
states = lifecycle_states(graph, model, state['lifecycle'], current_acceptance_policy_fingerprints=policy)
assert all(row['state'] == 'CURRENT' for row in states.values()), states
for name in ['requirements', 'verification', 'technical-verification', 'tests']:
    document = load(ROOT / '.harness/knowledge' / (name + '.yaml'))
    from harness.workspace.workspace import validate_knowledge_document
    validate_knowledge_document(document)
negatives = {}
for name, publication, revision in [
    ('stale-CAS', pub, 'sha256:' + '0' * 64),
    ('false-acceptance-identity', copy.deepcopy(pub), pub['revision'])
]:
    if name == 'false-acceptance-identity':
        publication['state']['lifecycle']['providers'][0]['acceptance_id'] = 'invented'
    try:
        publish_project_publication(path, graph=graph, publication=publication, expected_revision=revision)
    except CoreError as error:
        negatives[name] = str(error)
    else:
        raise AssertionError(name + ' unexpectedly accepted')
    assert path.read_bytes() == original
scenarios = load(ROOT / 'docs/checker/scenarios.yaml')
exported = json.loads((ROOT / 'tests/fixtures/scenarios.json').read_text())
assert exported['cases'] == scenarios['cases']
assert exported['base'] == dict(scenarios['base'], version=1)
subprocess.run([sys.executable, str(RUN / 'status.py')], check=True)
result = dict(status='PASS', pin=PIN, publication_revision=pub['revision'], currentness=states,
              negative_checks=negatives, fixed_expected_cases_unchanged=True)
(RUN / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: currentness, schema, stale CAS/false identity rejection, fixed pre-code expected cases')
