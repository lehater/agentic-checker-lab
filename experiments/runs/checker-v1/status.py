"""Derive scope-specific status from the single published snapshot."""
import copy
import json
from pathlib import Path
import sys
import yaml

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
PIN = json.loads((ROOT / '.harness/harness-binding.json').read_text())['source']['revision']
PACK = Path.home() / '.cache/harness/v1' / PIN
sys.path.insert(0, str(PACK / 'src'))
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.project_frontier import compose_project_frontier
from harness.application.project_publication import read_project_publication


def load(path):
    return yaml.safe_load(Path(path).read_text())


target = 'CHECKER-CODEGEN-INPUT' if '--codegen-input' in sys.argv else 'CHECKER-PROTOTYPE'
prefix = 'codegen-' if '--codegen-input' in sys.argv else ''
graph = load(ROOT / '.harness/engineering-graph.yaml')
state = read_project_publication(ROOT / '.harness/project-publication.yaml', graph=graph)['state']
overlay = copy.deepcopy(load(ROOT / '.harness/coverage-overlay.yaml'))
overlay['consumer'] = target
coverage = evaluate_with_repository_policy(graph=graph, realization=state['core_model'], consumer=target,
    scope='CHECKER-PROTOTYPE', semantic_evaluations=state['semantic_evaluations'], project_overlay=overlay)
args = dict(graph=graph, model=state['core_model'], target=target, lifecycle=state['lifecycle'],
    decision_contracts=load(PACK / 'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml'),
    decision_policy=load(ROOT / '.harness/decision-policy.yaml'))
closure = evaluate_semantic_closure(**args, skill_registry=load(PACK / 'skills/artifact-skill-registry-v0.yaml'),
    semantic_evaluations=state['semantic_evaluations'],
    knowledge_contracts=load(PACK / 'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml'))
roadmap = derive_decision_roadmap(**args, decision_failures=state['decision_failures'])
frontier = compose_project_frontier(target=target, decision_roadmap=roadmap,
                                  semantic_closure=closure, engineering_coverage=coverage)
for name, value in [('coverage', coverage), ('closure', closure), ('roadmap', roadmap), ('frontier', frontier)]:
    (RUN / (prefix + name + '.json')).write_text(json.dumps(value, indent=2) + '\n')
print(target, 'Coverage:', coverage['completion_ready'], 'Closure:', closure['status'],
      'Roadmap:', roadmap['frontier_status'], 'Frontier:', frontier['status'])
if '--require-complete' in sys.argv:
    assert coverage['completion_ready'] and closure['status'] == 'COMPLETE' and roadmap['frontier_status'] == 'COMPLETE'
