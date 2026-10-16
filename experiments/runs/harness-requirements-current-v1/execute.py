"""Continue the existing candidate and atomically admit first-slice requirements.
Run from repository root. Only staged Core.resolve_question transitions are used;
no published blocker is removed until ACCEPTED admission and terminal validation.
"""
import copy,hashlib,json,os,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision'];PACK=Path.home()/'.cache/harness/v1'/PIN
logs=[];instructions={}
def load(p):return yaml.safe_load(Path(p).read_text())
def save(p,v):Path(p).write_text(yaml.safe_dump(v,sort_keys=False,allow_unicode=True))
def command(argv):
 p=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=str(PACK/'src'),PYTHONDONTWRITEBYTECODE='1'))
 logs.append(dict(argv=argv,cwd=str(ROOT),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr));assert p.returncode==0,logs[-1]
 return p.stdout
command(['python3','.harness/harnessw.py','sync']);command([sys.executable,'-m','harness.application.consumer_pack','validate-pack',str(PACK),'--revision',PIN])
for category,key in [('operation','project-bootstrap-reconcile'),('artifact','product-requirements'),('operation','project-engineering-status')]:
 argv=[sys.executable,'-m','harness.application.skill_router',category,'--root',str(PACK)]
 argv+=['--knowledge-kind',key] if category=='artifact' else ['--surface','consumer','--operation',key]
 route=json.loads(command(argv))
 for rel in [*route['instruction_contracts'],route['skill']]:instructions[rel]=hashlib.sha256((PACK/rel).read_bytes()).hexdigest()
sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication,prepare_reconciliation_publication,publish_project_publication
from harness.application.semantic_admission import admit_artifact,derive_acceptance_policy_fingerprints
from harness.project_model.core import resolve_question,CoreError
from harness.project_model.engineering_graph import validate_realization
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
from harness.application.project_frontier import compose_project_frontier
from harness.reference_model.project_status import bootstrap_registry,validate_registry,status
pubpath=ROOT/'.harness/project-publication.yaml';g=load(ROOT/'.harness/engineering-graph.yaml')
# Preserve baseline once, without relying on mutable historic execution scripts.
beforepath=RUN/'publication-before.yaml'
if not beforepath.exists():save(beforepath,read_project_publication(pubpath,graph=g))
before=load(beforepath);s=before['state'];model=copy.deepcopy(s['core_model'])
contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml');decisions=load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml');skills=load(PACK/'skills/artifact-skill-registry-v0.yaml')
policy=derive_acceptance_policy_fingerprints(graph=g,knowledge_contracts=contracts,decision_contracts=decisions)
assert lifecycle_states(g,validate_realization(g,model),s['lifecycle'],current_acceptance_policy_fingerprints=policy)['checker.problem']['state']=='CURRENT'
artifactpath=ROOT/'.harness/knowledge/checker-requirements.yaml';artifact=load(artifactpath);requirements=artifact['content']['requirements']
command([sys.executable,'-m','harness.workspace.workspace','validate-artifact',str(artifactpath)])
old=load(ROOT/'experiments/runs/harness-requirements-v1/requirements-candidate.yaml')['content']['requirements']
assert [r['id'] for r in requirements[:7]]==[r['id'] for r in old]
assert [r['statement'] for r in requirements[:7]]==[r['statement'] for r in old]
assert len({r['id'] for r in requirements})==len(requirements)==28
# Strict derived canonical provenance uses ONLY the real CURRENT prerequisite.
previous_sources=load(ROOT/'experiments/runs/harness-requirements-v1/sources.yaml')
sources=copy.deepcopy(previous_sources)
assert all(x['source_artifact']=='CHECKER-PROBLEM-EVIDENCE' for x in sources['semantic_assertions'])
assertions=[]
for i,r in enumerate(requirements):
 assertions.append(dict(id=r['id'],kind='product-requirement',subject=r['id'],semantic_value=r['statement'],decision_authority='PRODUCT-REQUIREMENTS',derived_from=(['problem-outcome'] if i<4 else ['problem-verdict-boundary']) if i<7 else [],source_refs=r['source_refs']))
# New accepted product decisions are original PRODUCT-REQUIREMENTS assertions
# grounded in PDEC-004; PDEC is not forged into another canonical prerequisite.
candidate=dict(id='CHECKER-REQUIREMENTS',path=str(artifactpath.relative_to(ROOT)),capability='checker.requirements',canonical_references=[dict(referenced_path='docs/scenario/problem-framing-decision.md')],semantic_assertions=assertions,semantic_review=dict(status='ACCEPTED',checks=['source-discipline','authority-boundary','no-invention','observable-product-level','no-downstream-design-promotion'],reviewer='Acting engineering agent delegated by PDEC-CHECKER-003',record='experiments/runs/harness-requirements-current-v1/review.md'))
# Identity also binds actual source content, acceptance criteria, non-goals and review.
identity_payload=dict(candidate=candidate,artifact=artifact,decision_sha256=hashlib.sha256((ROOT/'docs/scenario/first-slice-product-decision.md').read_bytes()).hexdigest(),review_sha256=hashlib.sha256((RUN/'review.md').read_bytes()).hexdigest())
acceptance='task-004-requirements-'+hashlib.sha256(json.dumps(identity_payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:24]
save(RUN/'admission-candidate.yaml',candidate)
# This is a proposed in-memory transition, NOT an accepted/persisted provider yet.
model['artifacts'].append(dict(id='CHECKER-REQUIREMENTS',path=candidate['path'],authority='PRODUCT-REQUIREMENTS',provides=['checker.requirements'],depends_on=['CHECKER-PROBLEM-EVIDENCE']))
original_questions=copy.deepcopy(model['questions'])
for qid in ['Q-PR-001','Q-PR-002']:
 model=resolve_question(validate_realization(g,model),qid,'CHECKER-REQUIREMENTS',acceptance,'ABSENT')
# validate_realization supplies technical graph rows; store only native Core components.
model={k:model[k] for k in ['artifacts','questions']}
assert len(model['questions'])==len(original_questions)==2
for q,oldq in zip(model['questions'],original_questions):assert {k:v for k,v in q.items() if k!='resolution'}==oldq
save(RUN/'staged-core.yaml',model)
pre_admission_publication=pubpath.read_bytes()
evaluation=admit_artifact(graph=g,model=model,skill_registry=skills,knowledge_contracts=contracts,decision_contracts=decisions,capability='checker.requirements',sources=sources,candidate=candidate,acceptance_id=acceptance,lifecycle=s['lifecycle'])
save(RUN/'semantic-admission.yaml',evaluation)
assert evaluation['status']=='ACCEPTED',evaluation
assert pubpath.read_bytes()==pre_admission_publication
sem=copy.deepcopy(s['semantic_evaluations']);sem['semantic_evaluations'].append(evaluation)
life=copy.deepcopy(s['lifecycle']);life['providers'].append(evaluation['lifecycle_assertion'])
next_pub=prepare_reconciliation_publication(graph=g,current_publication=before,expected_revision=before['revision'],outcomes={'checker.problem':'CURRENT','checker.requirements':'CURRENT'},core_model=model,semantic_evaluations=sem,lifecycle=life,decision_failures=s['decision_failures'])
current=read_project_publication(pubpath,graph=g)
if current['revision']!=next_pub['revision']:publish_project_publication(pubpath,graph=g,publication=next_pub,expected_revision=before['revision'])
pub=read_project_publication(pubpath,graph=g);assert pub==next_pub
s=pub['state'];model=s['core_model'];life=s['lifecycle'];sem=s['semantic_evaluations']
assert s['lifecycle']['providers'][0]==before['state']['lifecycle']['providers'][0]
assert s['semantic_evaluations']['semantic_evaluations'][0]==before['state']['semantic_evaluations']['semantic_evaluations'][0]
states=lifecycle_states(g,validate_realization(g,model),life,current_acceptance_policy_fingerprints=policy)
assert all(states[c]['state']=='CURRENT' for c in ['checker.problem','checker.requirements'])
for q in model['questions']:assert q['resolution']==dict(artifact='CHECKER-REQUIREMENTS',acceptance_id=acceptance,supersedes_acceptance_id='ABSENT')
# Applicability is justified by the now accepted canonical provider, not delegation alone.
catalog=load(PACK/'catalogs/software-authorities-v0.yaml');regpath=ROOT/'.harness/authority-assessments.yaml';registry=load(regpath)
for row in registry['assessments']:
 if row['authority_id']=='PRODUCT-REQUIREMENTS':
  row.update(applicability='REQUIRED',evidence=['core:authority:PRODUCT-REQUIREMENTS','docs/scenario/product-requirements-delegation.md'],rationale='Accepted first-slice product requirements provider owned by PRODUCT-REQUIREMENTS; Q-PR-001/002 resolved with matching accepted identity.',depends_on_evidence=['core:authority:PRODUCT-REQUIREMENTS'],reopening_conditions=['canonical ownership/evidence changes','product scope changes'])
registry=bootstrap_registry(catalog,existing=registry,core=model);assert not validate_registry(catalog,registry);save(regpath,registry)
target='CHECKER-REQUIREMENTS-ADMISSION'
road=derive_decision_roadmap(graph=g,model=model,target=target,lifecycle=life,decision_contracts=decisions,decision_policy=None,decision_failures=s['decision_failures'])
closure=evaluate_semantic_closure(graph=g,model=model,target=target,skill_registry=skills,semantic_evaluations=sem,lifecycle=life,knowledge_contracts=contracts,decision_contracts=decisions)
coverage=evaluate_with_repository_policy(graph=g,realization=model,consumer=target,scope='CHECKER-FIRST-SLICE',semantic_evaluations=sem,project_overlay=dict(subject_inventory=dict(state='REQUIRED',rationale='First-slice requirements are accepted, but subject-obligation classification is not yet adopted; technical admission closure does not prove full Checker coverage.')))
front=compose_project_frontier(target=target,decision_roadmap=road,semantic_closure=closure,engineering_coverage=coverage)
assert road['frontier_status']=='COMPLETE';assert closure['status']=='COMPLETE'
paths=['AGENTS.md','.harness/harness-binding.json','.harness/engineering-graph.yaml','docs/scenario/product-requirements-delegation.md','docs/scenario/first-slice-product-decision.md','docs/scenario/problem-framing-decision.md',str(artifactpath.relative_to(ROOT)),'experiments/runs/harness-requirements-v1/requirements-candidate.yaml','experiments/runs/harness-requirements-v1/review.md','experiments/runs/harness-requirements-v1/semantic-admission.yaml','experiments/runs/harness-requirements-v1/sources.yaml','experiments/runs/harness-requirements-current-v1/review.md']
result=dict(status='CURRENT',pin=PIN,commands=logs,instruction_sha256=instructions,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},acceptance_id=acceptance,publication_revision=pub['revision'],parent_revision=pub['parent_revision'],lifecycle=states,question_resolutions=model['questions'],requirements=[r['id'] for r in requirements],authority_status=status(catalog,registry,model),decision_roadmap=road,semantic_closure=closure,coverage={k:coverage[k] for k in ['consumer','scope','completion_ready','activated_count','work_item_count','summary','subject_obligation_rows']},project_frontier=front,model_metadata=None,tokens=None,cost=None)
(RUN/'evidence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(status='CURRENT',revision=pub['revision'],acceptance_id=acceptance,lifecycle=states),ensure_ascii=False))
