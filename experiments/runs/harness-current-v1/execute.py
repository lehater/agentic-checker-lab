"""Reproduce strict admission and atomic publication using the pinned Consumer API.
Run from repository root. Existing publication is verified, never overwritten on replay.
"""
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
import yaml
ROOT=Path.cwd(); RUN=Path(__file__).resolve().parent
PACK=Path.home()/'.cache/harness/v1/442db854c3a736a5e500b4a41664b80981b0d94c'
sys.path.insert(0,str(PACK/'src'))
def load(p): return yaml.safe_load(Path(p).read_text())
def save(name,value): (RUN/name).write_text(yaml.safe_dump(value,sort_keys=False,allow_unicode=True))
def command(name,args):
 p=subprocess.run(args,capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=str(PACK/'src'),PYTHONDONTWRITEBYTECODE='1'))
 (RUN/(name+'.stdout')).write_text(p.stdout); (RUN/(name+'.stderr')).write_text(p.stderr)
 with (RUN/'commands.jsonl').open('a') as f: f.write(json.dumps(dict(name=name,argv=args,cwd=str(ROOT),exit_code=p.returncode))+'\n')
 if p.returncode: raise RuntimeError(name+': '+p.stderr)
 return p.stdout
command('sync',['python3','.harness/harnessw.py','sync'])
command('validate-pack',[sys.executable,'-m','harness.application.consumer_pack','validate-pack',str(PACK),'--revision',PACK.name])
for category,key in [('operation','project-bootstrap-reconcile'),('artifact','problem-evidence'),('operation','project-engineering-status')]:
 args=[sys.executable,'-m','harness.application.skill_router',category,'--root',str(PACK)]
 args+=['--knowledge-kind',key] if category=='artifact' else ['--surface','consumer','--operation',key]
 route=json.loads(command('route-'+key,args))
 # Preserve exact instructions used; loaded in contract-before-skill order.
 for path in [*route['instruction_contracts'],route['skill']]:
  (RUN/('instruction-'+path.replace('/','__')+'.txt')).write_text((PACK/path).read_text())
from harness.project_model.engineering_graph import validate_realization
from harness.application.semantic_admission import admit_artifact,derive_acceptance_policy_fingerprints
from harness.application.project_publication import build_project_publication,prepare_capability_transition,publish_project_publication,read_project_publication
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
from harness.application.project_frontier import compose_project_frontier
old=load(ROOT/'experiments/runs/harness-intake-v1/engineering-graph-candidate.yaml')
g=copy.deepcopy(old);g.update(id='CHECKER-PROBLEM',default_subject='CHECKER-PROBLEM')
g['authorities']=g['authorities'][:1]
a=g['authorities'][0];a['responsibility']='Project-owned Discovery problem evidence under PDEC-CHECKER-002, TASK-004 only.';a['boundary']['public_contract']='Provide checker.problem; no downstream product or design authority.'
g['consumers']=[dict(id='CHECKER-PROBLEM-ADMISSION',purpose='TASK-004 Discovery admission only; not an implementation Consumer.',requires=[dict(capability='checker.problem')])]
graph_path=ROOT/'.harness/engineering-graph.yaml'
if graph_path.exists(): assert load(graph_path)==g
else: graph_path.write_text(yaml.safe_dump(g,sort_keys=False))
model=dict(artifacts=[],questions=[])
save('core-before.yaml',model)
command('target-before',[sys.executable,'-m','harness.project_model.engineering_graph','evaluate',str(graph_path),'CHECKER-PROBLEM-ADMISSION',str(RUN/'core-before.yaml')])
statements=[('actor','Оператор'),('need','Объяснимо исследовать сетевой поток'),('outcome','Релевантные места применения политики, подходящие сохранённые ACL-правила в порядке обработки и достоверность источников'),('verdict-boundary','Нет обязанности формировать единый универсальный Permit/Deny; отсутствие совпадения не означает автоматически DENY/ALLOW'),('scope-boundary','Offline/fixture-only, IP/protocol/matching, completeness/freshness, live diagnostics, UI/API, architecture и oracle не приняты')]
candidate=dict(id='CHECKER-PROBLEM-EVIDENCE',path='docs/scenario/problem-framing-decision.md',capability='checker.problem',canonical_references=[],semantic_assertions=[dict(id='problem-'+k,kind='problem-'+k,subject='Checker',semantic_value=v,decision_authority='DISCOVERY',derived_from=[]) for k,v in statements],semantic_review=dict(status='ACCEPTED',checks=['source-discipline','authority-boundary','no-invention','evidence-not-solution'],reviewer='Acting engineering agent, delegated by PDEC-CHECKER-002; not an independent human signature',record='experiments/runs/harness-current-v1/semantic-review.md'))
# Root Discovery decisions are original assertions under delegated DISCOVERY.
# PDEC/fixtures are cited review evidence, never fictitious canonical prerequisites.
sources=dict(semantic_assertions=[])
save('candidate.yaml',candidate);save('sources.yaml',sources)
registry=load(PACK/'skills/artifact-skill-registry-v0.yaml');contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml'); decisions=load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml')
acceptance='task-004-checker-problem-'+hashlib.sha256(json.dumps(candidate,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:20]
evaluation=admit_artifact(graph=g,model=model,skill_registry=registry,knowledge_contracts=contracts,decision_contracts=decisions,capability='checker.problem',sources=sources,candidate=candidate,acceptance_id=acceptance)
save('semantic-admission.yaml',evaluation)
assert evaluation['status']=='ACCEPTED',evaluation
sem=dict(version=1,kind='harness-semantic-evaluation-set',semantic_evaluations=[],derivation_evaluations=[])
life=dict(version=1,kind='harness-capability-lifecycle',providers=[])
baseline=build_project_publication(graph=g,core_model=model,semantic_evaluations=sem,lifecycle=life)
save('publication-baseline.yaml',baseline)
publication_path=ROOT/'.harness/project-publication.yaml'
if not publication_path.exists(): publish_project_publication(publication_path,graph=g,publication=baseline,expected_revision=None)
model['artifacts']=[dict(id=candidate['id'],path=candidate['path'],authority='DISCOVERY',provides=['checker.problem'],depends_on=[])]
sem['semantic_evaluations']=[evaluation];life['providers']=[evaluation['lifecycle_assertion']]
next_pub=prepare_capability_transition(graph=g,current_publication=baseline,expected_revision=baseline['revision'],capability='checker.problem',outcome='CURRENT',core_model=model,semantic_evaluations=sem,lifecycle=life)
current=read_project_publication(publication_path,graph=g)
if current['revision']!=next_pub['revision']: publish_project_publication(publication_path,graph=g,publication=next_pub,expected_revision=baseline['revision'])
pub=read_project_publication(publication_path,graph=g);assert pub==next_pub
# All following projections consume exactly the read-back published snapshot.
s=pub['state'];model=s['core_model'];life=s['lifecycle'];sem=s['semantic_evaluations'];target='CHECKER-PROBLEM-ADMISSION'
policy=derive_acceptance_policy_fingerprints(graph=g,knowledge_contracts=contracts,decision_contracts=decisions)
states=lifecycle_states(g,validate_realization(g,model),life,current_acceptance_policy_fingerprints=policy);save('lifecycle-status.yaml',states);assert states['checker.problem']['state']=='CURRENT'
roadmap=derive_decision_roadmap(graph=g,model=model,target=target,lifecycle=life,decision_contracts=decisions,decision_policy=None,decision_failures=s['decision_failures']);save('decision-roadmap.yaml',roadmap)
closure=evaluate_semantic_closure(graph=g,model=model,target=target,skill_registry=registry,semantic_evaluations=sem,lifecycle=life,knowledge_contracts=contracts,decision_contracts=decisions);save('semantic-closure.yaml',closure)
coverage=evaluate_with_repository_policy(graph=g,realization=model,consumer=target,scope='CHECKER-PROBLEM',semantic_evaluations=sem);save('engineering-coverage.yaml',coverage)
frontier=compose_project_frontier(target=target,decision_roadmap=roadmap,semantic_closure=closure,engineering_coverage=coverage);save('project-frontier.yaml',frontier)
save('outcome.yaml',dict(status='CURRENT',publication_revision=pub['revision'],acceptance_id=acceptance,scope=target,model_metadata=None,tokens=None,cost=None))
print(yaml.safe_dump(dict(status='CURRENT',revision=pub['revision'],lifecycle=states),sort_keys=False))

# Reconcile the full catalog without adopting downstream topology or applicability.
from harness.reference_model.project_status import bootstrap_registry,validate_registry,status
catalog=load(PACK/'catalogs/software-authorities-v0.yaml')
registry_path=ROOT/'.harness/authority-assessments.yaml'
assessments=bootstrap_registry(catalog,existing=load(registry_path) if registry_path.exists() else None,core=model)
assert not validate_registry(catalog,assessments)
registry_path.write_text(yaml.safe_dump(assessments,sort_keys=False))
save('project-engineering-status.yaml',status(catalog,assessments,model))
# Boundary checks: stale CAS and mixed acceptance identity must fail closed.
from harness.project_model.core import CoreError
before=publication_path.read_bytes()
try:
 publish_project_publication(publication_path,graph=g,publication=next_pub,expected_revision=baseline['revision'])
except CoreError as error:
 save('stale-cas-check.yaml',dict(result='PASS',error=str(error)))
else: raise AssertionError('stale CAS accepted')
assert publication_path.read_bytes()==before
bad_lifecycle=copy.deepcopy(life);bad_lifecycle['providers'][0]['acceptance_id']='deliberate-mismatch-for-negative-check'
try:
 prepare_capability_transition(graph=g,current_publication=pub,expected_revision=pub['revision'],capability='checker.problem',outcome='CURRENT',core_model=model,semantic_evaluations=sem,lifecycle=bad_lifecycle)
except CoreError as error:
 save('mixed-identity-check.yaml',dict(result='PASS',error=str(error)))
else: raise AssertionError('mixed acceptance identity accepted')
assert publication_path.read_bytes()==before
