import sys,json,yaml
from pathlib import Path
r=Path.cwd();p=Path.home()/'.cache/harness/v1'/json.loads((r/'.harness/harness-binding.json').read_text())['source']['revision'];sys.path.insert(0,str(p/'src'))
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
g=yaml.safe_load((r/'.harness/engineering-graph.yaml').read_text());s=yaml.safe_load((r/'.harness/project-publication.yaml').read_text())['state']
c=evaluate_with_repository_policy(graph=g,realization=s['core_model'],consumer='CHECKER-PROTOTYPE',scope='CHECKER-PROTOTYPE',semantic_evaluations=s['semantic_evaluations'],project_overlay=yaml.safe_load((r/'.harness/coverage-overlay.yaml').read_text()))
(r/'experiments/runs/checker-v1/coverage.json').write_text(json.dumps(c,indent=2))
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.project_frontier import compose_project_frontier
load=lambda f:yaml.safe_load(Path(f).read_text())
policy=load(r/'.harness/decision-policy.yaml')
args=dict(graph=g,model=s['core_model'],target='CHECKER-PROTOTYPE',lifecycle=s['lifecycle'],decision_contracts=load(p/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml'),decision_policy=policy)
closure=evaluate_semantic_closure(**args,skill_registry=load(p/'skills/artifact-skill-registry-v0.yaml'),semantic_evaluations=s['semantic_evaluations'],knowledge_contracts=load(p/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml'))
road=derive_decision_roadmap(**args,decision_failures=s['decision_failures'])
front=compose_project_frontier(target='CHECKER-PROTOTYPE',decision_roadmap=road,semantic_closure=closure,engineering_coverage=c)
for name,value in [('closure',closure),('roadmap',road),('frontier',front)]:
 (r/('experiments/runs/checker-v1/'+name+'.json')).write_text(json.dumps(value,indent=2))
print('Coverage:',c['completion_ready'],'Closure:',closure['status'],'Roadmap:',road['frontier_status'],'Frontier:',front['status'])
if '--require-complete' in sys.argv:
 assert c['completion_ready'] and closure['status']=='COMPLETE' and road['frontier_status']=='COMPLETE'

