"""Pinned Consumer reconciliation. Replay derives the same atomic BLOCKED snapshot."""
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
import yaml
ROOT=Path.cwd(); RUN=Path(__file__).resolve().parent
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision']
PACK=Path.home()/'.cache/harness/v1'/PIN
sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication, prepare_reconciliation_publication, publish_project_publication
from harness.application.semantic_admission import admit_artifact, derive_acceptance_policy_fingerprints
from harness.project_model.engineering_graph import validate_realization
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
from harness.application.project_frontier import compose_project_frontier
from harness.reference_model.project_status import bootstrap_registry, validate_registry, status

def load(p): return yaml.safe_load(Path(p).read_text())
def save(p,v): Path(p).write_text(yaml.safe_dump(v,sort_keys=False,allow_unicode=True))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
logs=[]; instructions={}
def command(args):
 p=subprocess.run(args,capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=str(PACK/'src'),PYTHONDONTWRITEBYTECODE='1'))
 logs.append(dict(argv=args,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
 assert p.returncode==0,logs[-1]
 return p.stdout
command(['python3','.harness/harnessw.py','sync'])
command(['python3','-m','harness.application.consumer_pack','validate-pack',str(PACK),'--revision',PIN])
for category,key in [('operation','project-bootstrap-reconcile'),('artifact','domain-use-case'),('artifact','verification-strategy'),('artifact','acceptance-scenarios'),('operation','project-engineering-status')]:
 args=['python3','-m','harness.application.skill_router',category,'--root',str(PACK)]
 args+=['--knowledge-kind',key] if category=='artifact' else ['--surface','consumer','--operation',key]
 route=json.loads(command(args))
 for rel in [*route['instruction_contracts'],route['skill']]: instructions[rel]=digest(PACK/rel)
gpath=ROOT/'.harness/engineering-graph.yaml'; pubpath=ROOT/'.harness/project-publication.yaml'
g=load(gpath); baseline_path=RUN/'publication-before.yaml'
if not baseline_path.exists(): save(baseline_path,read_project_publication(pubpath,graph=g))
before=load(baseline_path); s=before['state']; model=copy.deepcopy(s['core_model'])
catalog=load(PACK/'catalogs/software-authorities-v0.yaml')
for aid,cap,kind in [('DOMAIN-USE-CASE-DESIGN','checker.domain-use-case','domain-use-case'),('VERIFICATION-DESIGN','checker.verification-strategy','verification-strategy')]:
 if not any(a['id']==aid for a in g['authorities']):
  a=copy.deepcopy(next(a for a in catalog['authorities'] if a['id']==aid)); a={k:a[k] for k in ['id','responsibility','boundary']}
  a['produces']=[dict(capability=cap,knowledge_kind=kind,requires=['checker.requirements'])]; g['authorities'].append(a)
target='CHECKER-DOMAIN-VERIFICATION-ADMISSION'
if not any(c['id']==target for c in g['consumers']):
 g['consumers'].append(dict(id=target,purpose='PDEC-CHECKER-005 first-slice design admission only; not implementation scope.',requires=[dict(capability=c) for c in ['checker.domain-use-case','checker.verification-strategy']]))
save(gpath,g)
contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml'); decisions=load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml'); skills=load(PACK/'skills/artifact-skill-registry-v0.yaml')
policy=derive_acceptance_policy_fingerprints(graph=g,knowledge_contracts=contracts,decision_contracts=decisions)
states=lifecycle_states(g,validate_realization(g,model),s['lifecycle'],current_acceptance_policy_fingerprints=policy)
assert all(states[c]['state']=='CURRENT' for c in ['checker.problem','checker.requirements'])
road_before=derive_decision_roadmap(graph=g,model=model,target=target,lifecycle=s['lifecycle'],decision_contracts=decisions,decision_policy=None,decision_failures=s['decision_failures'])
assert any(x.get('capability')=='checker.verification-strategy' for x in road_before['ready'])
questions=[dict(id='Q-DV-001',authority='DOMAIN-USE-CASE-DESIGN',text='Владелец проекта: обеспечьте accepted Strategic Domain ownership для first slice PDEC-004 через надлежащий DOMAIN-STRATEGY процесс. Какой принятый provider закрепляет эту ответственность? PDEC-005 и Product Requirements не заменяют обязательный input domain-use-case skill.',blocks_capabilities=['checker.domain-use-case'],blocks=[],answer_from=[]),dict(id='Q-DV-002',authority='DOMAIN-USE-CASE-DESIGN',text='После установления Strategic ownership: примите минимальные поддерживаемые ACL facts и match/non-match predicates для IPv4 TCP/UDP source/destination и обоих портов, роль порядка при выборе показываемых правил и границу unknown/unsupported facts. Нужны независимо размеченные положительные/отрицательные примеры с основанием из контракта. Syntax/masks, implicit deny, first-match и action priority не заданы и не могут выбираться тестом или legacy SQL.',blocks_capabilities=['checker.domain-use-case','checker.verification-strategy'],blocks=[],answer_from=[])]
# Review full verification scope independently of missing Domain production ownership.
artifactpath=RUN/'verification-candidate.yaml'; artifact=load(artifactpath)
command(['python3','-m','harness.workspace.workspace','validate-artifact',str(artifactpath.relative_to(ROOT))])
reqs=load(ROOT/'.harness/knowledge/checker-requirements.yaml')['content']['requirements']
assert {r['id'] for r in reqs}=={r for c in artifact['content']['checks'] for r in c['verifies']}
assert len(reqs)==28
sources=dict(semantic_assertions=[dict(a,source_artifact='CHECKER-REQUIREMENTS') for a in load(ROOT/'experiments/runs/harness-requirements-current-v1/admission-candidate.yaml')['semantic_assertions']])
candidate=dict(id='CHECKER-VERIFICATION',path=str(artifactpath.relative_to(ROOT)),capability='checker.verification-strategy',canonical_references=[dict(referenced_path='.harness/knowledge/checker-requirements.yaml')],semantic_assertions=[dict(id=c['id'],kind='verification-check',subject=c['id'],semantic_value=c['objective'],decision_authority='VERIFICATION-DESIGN',derived_from=c['verifies']) for c in artifact['content']['checks']],semantic_review=dict(status='REJECTED',checks=['source-discipline','authority-boundary','no-invention','verification-not-semantic-owner'],reason='Full first-slice strategy lacks accepted matching predicates and independently justified match/non-match oracle. VC-DV-MATCH BLOCKED; VC-DV-ORDER CONDITIONAL. Q-DV-002. Metadata work does not establish the whole capability.',reviewer='Engineering agent delegated by PDEC-CHECKER-005',record=str((RUN/'review.md').relative_to(ROOT))))
save(RUN/'admission-candidate.yaml',candidate)
identity=dict(candidate=candidate,artifact=artifact,review_sha256=digest(RUN/'review.md'))
attempt='checker-verification-attempt-'+hashlib.sha256(json.dumps(identity,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:24]
ev=admit_artifact(graph=g,model=model,skill_registry=skills,knowledge_contracts=contracts,decision_contracts=decisions,capability='checker.verification-strategy',sources=sources,candidate=candidate,acceptance_id=attempt,lifecycle=s['lifecycle'])
save(RUN/'semantic-admission.yaml',ev)
assert ev['status']=='REJECTED' and 'lifecycle_assertion' not in ev
model['questions'].extend(questions)
outcomes={'checker.problem':'CURRENT','checker.requirements':'CURRENT','checker.domain-use-case':'BLOCKED','checker.verification-strategy':'BLOCKED'}
nextpub=prepare_reconciliation_publication(graph=g,current_publication=before,expected_revision=before['revision'],outcomes=outcomes,core_model=model,semantic_evaluations=s['semantic_evaluations'],lifecycle=s['lifecycle'],decision_failures=s['decision_failures'])
current=read_project_publication(pubpath,graph=g)
if current['revision']!=nextpub['revision']: publish_project_publication(pubpath,graph=g,publication=nextpub,expected_revision=before['revision'])
pub=read_project_publication(pubpath,graph=g); assert pub==nextpub
assert pub['state']['lifecycle']==s['lifecycle'] and pub['state']['semantic_evaluations']==s['semantic_evaluations']
assert pub['state']['core_model']['artifacts']==s['core_model']['artifacts']
registry_path=ROOT/'.harness/authority-assessments.yaml'; registry=load(registry_path)
for row in registry['assessments']:
 if row['authority_id'] in ['DOMAIN-USE-CASE-DESIGN','VERIFICATION-DESIGN']:
  q='Q-DV-001' if row['authority_id']=='DOMAIN-USE-CASE-DESIGN' else 'Q-DV-002'
  row.update(applicability='UNRESOLVED',evidence=['docs/scenario/domain-verification-delegation.md','core:question:'+q],rationale='Scoped delegated work has real prerequisite/semantic blockers; no accepted provider.',depends_on_evidence=[q],reopening_conditions=['Accepted ownership/matching contracts and genuine admission'])
registry=bootstrap_registry(catalog,existing=registry,core=model); assert not validate_registry(catalog,registry); save(registry_path,registry)
road=derive_decision_roadmap(graph=g,model=model,target=target,lifecycle=s['lifecycle'],decision_contracts=decisions,decision_policy=None,decision_failures=s['decision_failures'])
closure=evaluate_semantic_closure(graph=g,model=model,target=target,skill_registry=skills,semantic_evaluations=s['semantic_evaluations'],lifecycle=s['lifecycle'],knowledge_contracts=contracts,decision_contracts=decisions)
coverage=evaluate_with_repository_policy(graph=g,realization=model,consumer=target,scope='CHECKER-FIRST-SLICE',semantic_evaluations=s['semantic_evaluations'],project_overlay=dict(subject_inventory=dict(state='REQUIRED',rationale='Full subject inventory remains unaccepted; this task adds only two scoped contracts.')))
front=compose_project_frontier(target=target,decision_roadmap=road,semantic_closure=closure,engineering_coverage=coverage)
assert {x.get('capability') for x in road['blocked']} >= {'checker.domain-use-case','checker.verification-strategy'}
states=lifecycle_states(g,validate_realization(g,model),s['lifecycle'],current_acceptance_policy_fingerprints=policy)
assert all(states[c]['state']=='CURRENT' for c in ['checker.problem','checker.requirements'])
paths=['AGENTS.md','.harness/harness-binding.json','.harness/engineering-graph.yaml','.harness/knowledge/checker-requirements.yaml','docs/scenario/problem-framing-decision.md','docs/scenario/first-slice-product-decision.md','docs/scenario/domain-verification-delegation.md','docs/decisions/0004-checker-domain-verification-boundary.md']+[str(p.relative_to(ROOT)) for p in RUN.glob('*') if p.name in ['execute.py','review.md','domain-contract.md','verification-candidate.yaml','scenario-drafts.yaml']]
evidence=dict(outcomes=outcomes,publication_revision=pub['revision'],parent_revision=pub['parent_revision'],pin=PIN,commands=logs,instructions=instructions,source_sha256={p:digest(ROOT/p) for p in sorted(paths)},domain_admission='NOT_ATTEMPTED_MISSING_REQUIRED_STRATEGIC_OWNERSHIP',verification_admission=ev['status'],acceptance_scenarios='NOT_RUN_NO_ACCEPTED_STRATEGY',questions=questions,lifecycle=states,decision_roadmap=road,semantic_closure=closure,engineering_coverage={k:coverage[k] for k in ['status','completion_ready','activated_count','work_item_count','summary','subject_obligation_rows']},project_frontier=front,authority_status=[r for r in status(catalog,registry,model)['rows'] if r['authority'] in ['DISCOVERY','PRODUCT-REQUIREMENTS','DOMAIN-USE-CASE-DESIGN','VERIFICATION-DESIGN']])
(RUN/'evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(outcomes=outcomes,revision=pub['revision']),ensure_ascii=False))
