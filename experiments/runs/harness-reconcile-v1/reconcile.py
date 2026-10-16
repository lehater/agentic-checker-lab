"""Read-only pinned Harness reconciliation; run from repository root.
Writes only one essential evidence bundle; never admits or republishes knowledge.
"""
import copy,hashlib,json,os,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision']
PACK=Path.home()/'.cache/harness/v1'/PIN
commands=[];instructions={}
def command(argv):
 p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=str(PACK/'src'),PYTHONDONTWRITEBYTECODE='1'))
 commands.append(dict(argv=argv,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
 if p.returncode: raise RuntimeError(commands[-1])
 return p.stdout
command(['python3','.harness/harnessw.py','sync'])
command([sys.executable,'-m','harness.application.consumer_pack','validate-pack',str(PACK),'--revision',PIN])
for category,key in [('operation','project-bootstrap-reconcile'),('operation','project-engineering-status'),('artifact','product-requirements')]:
 argv=[sys.executable,'-m','harness.application.skill_router',category,'--root',str(PACK)]
 argv+=['--knowledge-kind',key] if category=='artifact' else ['--surface','consumer','--operation',key]
 route=json.loads(command(argv))
 for rel in [*route['instruction_contracts'],route['skill']]:
  text=(PACK/rel).read_text();instructions[rel]=hashlib.sha256(text.encode()).hexdigest()
 # Product skill is inspected solely to identify its preconditions; never executed.
sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication
from harness.application.semantic_admission import derive_acceptance_policy_fingerprints
from harness.project_model.engineering_graph import validate_realization
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.reference_model.project_status import bootstrap_registry,validate_registry,status
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.application.project_frontier import compose_project_frontier
load=lambda p:yaml.safe_load(Path(p).read_text())
pubpath=ROOT/'.harness/project-publication.yaml';original=pubpath.read_bytes()
g=load(ROOT/'.harness/engineering-graph.yaml');pub=read_project_publication(pubpath,graph=g);s=pub['state'];m=s['core_model'];life=s['lifecycle'];sem=s['semantic_evaluations']
contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml');decisions=load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml');skills=load(PACK/'skills/artifact-skill-registry-v0.yaml')
policies=derive_acceptance_policy_fingerprints(graph=g,knowledge_contracts=contracts,decision_contracts=decisions)
states=lifecycle_states(g,validate_realization(g,m),life,current_acceptance_policy_fingerprints=policies)
assert states['checker.problem']['state']=='CURRENT'
catalog=load(PACK/'catalogs/software-authorities-v0.yaml');assessments=load(ROOT/'.harness/authority-assessments.yaml')
reconciled=bootstrap_registry(catalog,existing=assessments,core=m)
assert not validate_registry(catalog,reconciled)
assert reconciled==assessments # Preserve accepted REQUIRED and all 22 UNASSESSED.
target='CHECKER-PROBLEM-ADMISSION'
road=derive_decision_roadmap(graph=g,model=m,target=target,lifecycle=life,decision_contracts=decisions,decision_policy=None,decision_failures=s['decision_failures'])
closure=evaluate_semantic_closure(graph=g,model=m,target=target,skill_registry=skills,semantic_evaluations=sem,lifecycle=life,knowledge_contracts=contracts,decision_contracts=decisions)
before=evaluate_with_repository_policy(graph=g,realization=m,consumer=target,scope='CHECKER-PROBLEM',semantic_evaluations=sem)
# A project document id alone cannot stand in for a published Core Question.
from harness.project_model.core import CoreError
invalid_overlay=copy.deepcopy(load(ROOT/'.harness/coverage-reconciliation.yaml'))
invalid_overlay['subject_inventory'].update(state='QUESTION',question='Q-REC-002')
try:
 evaluate_with_repository_policy(graph=g,realization=m,consumer=target,scope='CHECKER-PROBLEM',semantic_evaluations=sem,project_overlay=invalid_overlay)
except CoreError as error:
 question_boundary=dict(status='EXPECTED_REJECTION',error=str(error))
 assert str(error)=='unknown question: Q-REC-002'
else: raise AssertionError('An unpublished Core Question unexpectedly accepted')
after=evaluate_with_repository_policy(graph=g,realization=m,consumer=target,scope='CHECKER-PROBLEM',semantic_evaluations=sem,project_overlay=load(ROOT/'.harness/coverage-reconciliation.yaml'))
front=compose_project_frontier(target=target,decision_roadmap=road,semantic_closure=closure,engineering_coverage=after)
assert before['work_item_count']==16
assert len(front['next_actions'])+len(front['blocked'])>0
assert pubpath.read_bytes()==original
paths=['.harness/harness-binding.json','.harness/engineering-graph.yaml','.harness/project-publication.yaml','.harness/authority-assessments.yaml','.harness/coverage-reconciliation.yaml','docs/scenario/checker-scope-reconciliation.yaml','docs/scenario/problem-framing-decision.md','docs/scenario/discovery-authority-delegation.md','docs/project/strategy.md','docs/project/roadmap.md','experiments/runs/harness-current-v1/project-frontier.yaml']
dispositions=load(ROOT/'docs/scenario/checker-scope-reconciliation.yaml')['frontier_dispositions']
assert {x['concern'] for x in dispositions}=={x['concern'] for x in before['work_items']}
assert len(dispositions)==16
assert not any(x['applicability']=='NOT_APPLICABLE' for x in reconciled['assessments'])
def compact_coverage(value):
 keys=['kind','consumer','scope','completion_ready','activated_count','remaining_work_count','work_item_count','summary','subject_obligation_rows']
 return {k:value[k] for k in keys}
result=dict(pin=PIN,commands=commands,instructions_sha256=instructions,sources_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},publication_revision=pub['revision'],publication_unchanged=True,question_boundary=question_boundary,lifecycle=states,authority_status=status(catalog,reconciled,m),decision_roadmap=road,semantic_closure=closure,coverage_before=compact_coverage(before),coverage_after=compact_coverage(after),frontier_after=front,product_frontier=dict(status='UNAVAILABLE',reason='No accepted product Consumer/production contract or product delegation; technical frontier must not be relabeled as product frontier.',next_authority='PRODUCT-REQUIREMENTS',proposed_capability='checker.requirements',owner_gate='Q-REC-001'))
(RUN/'evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(lifecycle=states,coverage_before=before['work_item_count'],coverage_after=after['work_item_count'],frontier_status=front['status'],publication_unchanged=True),ensure_ascii=False))
