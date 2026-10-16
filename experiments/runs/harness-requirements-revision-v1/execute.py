"""Revise admitted Checker Product Requirements against pinned Harness semantic contract.

Uses a real REVISION admission and atomic publication. Never manually assigns
ACCEPTED evaluation, lifecycle, fingerprints or publication revision.
"""
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
import yaml

ROOT=Path.cwd()
RUN=Path(__file__).resolve().parent
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision']
PACK=Path.home()/'.cache/harness/v1'/PIN
def load(path): return yaml.safe_load(Path(path).read_text(encoding='utf-8'))
def save(path,data): Path(path).write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def command(args):
    e=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(PACK/'src'))
    result=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,env=e)
    if result.returncode: raise RuntimeError(' '.join(args)+'\n'+result.stdout+'\n'+result.stderr)
    return result.stdout

command(['python3','.harness/harnessw.py','sync'])
command(['python3','-m','harness.application.consumer_pack','validate-pack',str(PACK),'--revision',PIN])
sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication,prepare_reconciliation_publication,publish_project_publication
from harness.application.semantic_admission import admit_artifact,derive_acceptance_policy_fingerprints
from harness.project_model.core import resolve_question
from harness.project_model.engineering_graph import validate_realization
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.semantic_closure import evaluate_semantic_closure

graph=load(ROOT/'.harness/engineering-graph.yaml')
pubpath=ROOT/'.harness/project-publication.yaml'
before=load(RUN/'publication-before.yaml')
assert before['revision']=='sha256:8f5dc04d1b76ce6c347b63c796935465b84db72bb1b3623969c90ae7a89af2f5'
data=load(ROOT/'.harness/knowledge/checker-requirements.yaml')
all_reqs=data['content']['requirements']
active=[x for x in all_reqs if x['status']=='ACCEPTED']
retired=[x for x in all_reqs if x['status']=='RETIRED']
assert len(active)==13 and len(retired)==0 and len(all_reqs)==13
active_ids={x['id'] for x in active}
expected={f'REQ-CHECKER-{i:03d}' for i in [1,2,3,6,7,12,13,14,25,29,30,31,32]}
assert active_ids==expected
for row in all_reqs: assert row['source_refs']

# Reviewer-owned classification. An independently testable field is not an independent normative obligation.
OBLIGATIONS={
 '001':('PRODUCT_BEHAVIOR','relevant-placements','Observable set of relevant provided placements'),
 '002':('PRODUCT_BEHAVIOR','matching-rules','Observable matched-rule result, predicates remain Q-DV-002'),
 '003':('PRODUCT_BEHAVIOR','within-context-order','Distinct observable ordering constraint'),
 '006':('PRODUCT_CONSTRAINT','no-universal-verdict-from-absence','Negative interpretation constraint for no matching rule'),
 '007':('PRODUCT_CONSTRAINT','no-universal-verdict-from-presence','Negative interpretation constraint for matching rule'),
 '012':('PRODUCT_BEHAVIOR','provided-policy-contexts','Distinct accepted input source boundary'),
 '013':('PRODUCT_BEHAVIOR','provided-acl-snapshots','Distinct accepted policy evidence input'),
 '014':('PRODUCT_BEHAVIOR','rule-context-attribution','Distinct visible attribution of a rule to a policy context'),
 '025':('PRODUCT_CONSTRAINT','founded-freshness','Distinct rule for describing stale vs unknown source'),
 '029':('PRODUCT_BEHAVIOR','network-flow-input','One input contract; addresses/protocol/both ports are fields not separate requirements'),
 '030':('PRODUCT_BEHAVIOR','source-metadata','One source credibility contract with known and unknown facets'),
 '031':('PRODUCT_BEHAVIOR','partial-explanation','Conditional observable restrictions on a partial result, not mandatory partial return'),
 '032':('PRODUCT_BEHAVIOR','evidence-state-distinction','One three-way evidence state distinction, not separate test cases'),
}
assert {rid[-3:] for rid in active_ids}==set(OBLIGATIONS)
classifications=[
 dict(assertion=row['id'],role=OBLIGATIONS[row['id'][-3:]][0],
      obligation=OBLIGATIONS[row['id'][-3:]][1],
      rationale=OBLIGATIONS[row['id'][-3:]][2])
 for row in active
]
PRODUCT='PRODUCT_REQUIREMENT'
CONSTRAINT='PRODUCT_CONSTRAINT'
SOURCE_DISPOSITIONS=[
 ('problem-placements',PRODUCT,['001'],'Operator observes provided relevant placements'),
 ('problem-matching',PRODUCT,['002'],'Operator observes matching stored ACL rules'),
 ('problem-order',PRODUCT,['003'],'Operator sees known intra-context order'),
 ('problem-credibility',PRODUCT,['030'],'Known/unknown evidence credibility in one result contract'),
 ('problem-not-required-verdict','NON_GOAL',[],'No mandatory universal effective verdict'),
 ('problem-absence-verdict',CONSTRAINT,['006'],'No invented DENY/ALLOW on absence alone'),
 ('problem-presence-verdict',CONSTRAINT,['007'],'No invented overall effective verdict on presence alone'),
 ('PDEC004-flow-fields',PRODUCT,['029'],'One IPv4 TCP/UDP 5-tuple input contract'),
 ('PDEC004-provided-contexts',PRODUCT,['012'],'Contexts provided as inputs, not discovered'),
 ('PDEC004-stored-snapshots',PRODUCT,['013'],'Stored snapshots provided as source facts'),
 ('PDEC004-rule-context',PRODUCT,['014'],'Each result rule retains attributable context'),
 ('PDEC004-metadata',PRODUCT,['030'],'One origin/date/completeness result contract'),
 ('PDEC004-partial-explanation',PRODUCT,['031'],'One conditional partial explanation obligation'),
 ('PDEC004-evidence-states',PRODUCT,['032'],'Complete no-match/missing/unknown must be distinguishable'),
 ('PDEC004-staleness',CONSTRAINT,['025'],'Staleness requires established grounds; unknown date not fresh'),
 ('PDEC004-independent-test-examples','VERIFICATION_OBLIGATION',[],'Requires independent expected test oracle, owned by Verification Design, not Product'),
 ('PDEC004-TTL','ACCEPTANCE_CRITERION',[],'Do not invent source freshness threshold; captured by REQ-025 criteria'),
 ('PDEC004-future-exclusions','NON_GOAL',[],'No IPv6, ICMP, route discovery, NAT or live access in first slice'),
 ('PDEC004-interface-decisions','DOWNSTREAM_DECISION',[],'No CLI/API/runtime/architecture selection'),
]
source_dispositions=[dict(source=s,disposition=d,assertions=[f'REQ-CHECKER-{i}' for i in ids],rationale=reason) for s,d,ids,reason in SOURCE_DISPOSITIONS]
review=dict(
 status='ACCEPTED',
 checks=['source-discipline','authority-boundary','no-invention','observable-product-level',
         'no-downstream-design-promotion','product-requirement-boundary-review'],
 requirement_classifications=classifications,source_dispositions=source_dispositions,
 reviewer='Independent semantic audit of owner decisions + corrected Harness contract',
 record='experiments/runs/harness-requirements-revision-v1/README.md'
)
sources=load(ROOT/'experiments/runs/harness-requirements-v1/sources.yaml')
candidate=dict(
 id='CHECKER-REQUIREMENTS',path='.harness/knowledge/checker-requirements.yaml',
 capability='checker.requirements',
 canonical_references=[dict(referenced_path='docs/scenario/problem-framing-decision.md')],
 semantic_assertions=[
  dict(id=x['id'],kind='product-requirement',subject=x['id'],semantic_value=x['statement'],
       decision_authority='PRODUCT-REQUIREMENTS',
       derived_from=(
         ['problem-outcome'] if x['id'] in ['REQ-CHECKER-001','REQ-CHECKER-002','REQ-CHECKER-003']
         else ['problem-verdict-boundary'] if x['id'] in ['REQ-CHECKER-006','REQ-CHECKER-007']
         else []
       ),source_refs=x['source_refs']) for x in active
 ],
 semantic_review=review)
save(RUN/'admission-candidate.yaml',candidate)
command([sys.executable,'-m','harness.workspace.workspace','validate-artifact','.harness/knowledge/checker-requirements.yaml'])
contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml')
decision_contracts=load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml')
skills=load(PACK/'skills/artifact-skill-registry-v0.yaml')
new_identity='task-004-requirements-revised-'+hashlib.sha256(
 json.dumps(dict(artifact=data,candidate=candidate,decision_sha=digest(ROOT/'docs/scenario/first-slice-product-decision.md')),
 sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:24]
state=before['state'];model=copy.deepcopy(state['core_model'])
oldlife=next(p for p in state['lifecycle']['providers'] if p['capability']=='checker.requirements')
oldid=oldlife['acceptance_id']
assert oldid=='task-004-requirements-revised-508d09a81929c4b2257bb8fa'
for qid in ['Q-PR-001','Q-PR-002']:
 q=next(q for q in model['questions'] if q['id']==qid)
 assert q['resolution']['acceptance_id']==oldid
 model=resolve_question(validate_realization(graph,model),qid,'CHECKER-REQUIREMENTS',new_identity,oldid)
model={k:model[k] for k in ['artifacts','questions']}
ev=admit_artifact(graph=graph,model=model,skill_registry=skills,knowledge_contracts=contracts,
 decision_contracts=decision_contracts,capability='checker.requirements',
 sources=sources,candidate=candidate,acceptance_id=new_identity,
 lifecycle=state['lifecycle'],decision_request_mode='REVISION')
save(RUN/'semantic-admission.yaml',ev)
if ev['status']!='ACCEPTED':raise RuntimeError('Semantic admission rejected: '+str(ev['findings']))
sem=copy.deepcopy(state['semantic_evaluations']);life=copy.deepcopy(state['lifecycle'])
for i,e in enumerate(sem['semantic_evaluations']):
 if e['capability']=='checker.requirements':sem['semantic_evaluations'][i]=ev;break
else:raise AssertionError('missing previous evaluation')
for i,p in enumerate(life['providers']):
 if p['capability']=='checker.requirements':life['providers'][i]=ev['lifecycle_assertion'];break
else:raise AssertionError('missing previous provider')
result=prepare_reconciliation_publication(graph=graph,current_publication=before,
 expected_revision=before['revision'],outcomes={
  'checker.problem':'CURRENT','checker.requirements':'CURRENT',
  'checker.domain-use-case':'BLOCKED','checker.verification-strategy':'BLOCKED'},
 core_model=model,semantic_evaluations=sem,lifecycle=life,
 decision_failures=state['decision_failures'])
current=read_project_publication(pubpath,graph=graph)
if current['revision']==before['revision']:
 publish_project_publication(pubpath,graph=graph,publication=result,expected_revision=before['revision'])
else:
 assert current==result,'unrecognized current publication revision'
published=read_project_publication(pubpath,graph=graph)
assert published==result
assert published['state']['semantic_evaluations']['semantic_evaluations'][0]==state['semantic_evaluations']['semantic_evaluations'][0]
assert published['state']['lifecycle']['providers'][0]==state['lifecycle']['providers'][0]
assert published['state']['core_model']['artifacts']==state['core_model']['artifacts']
assert published['state']['core_model']['questions'][2:]==state['core_model']['questions'][2:]
policy=derive_acceptance_policy_fingerprints(graph=graph,knowledge_contracts=contracts,
 decision_contracts=decision_contracts)
states=lifecycle_states(graph,validate_realization(graph,published['state']['core_model']),
 published['state']['lifecycle'],current_acceptance_policy_fingerprints=policy)
assert states['checker.problem']['state']=='CURRENT'
assert states['checker.requirements']['state']=='CURRENT',states['checker.requirements']
road=derive_decision_roadmap(graph=graph,model=published['state']['core_model'],
 target='CHECKER-DOMAIN-VERIFICATION-ADMISSION',lifecycle=published['state']['lifecycle'],
 decision_contracts=decision_contracts,decision_policy=None,
 decision_failures=published['state']['decision_failures'])
assert {x['capability'] for x in road['blocked']} >= {'checker.domain-use-case','checker.verification-strategy'}
print(json.dumps(dict(status='CURRENT',revision=published['revision'],acceptance_id=new_identity,
 active=len(active),removed_historical_rows_from_active_state=True,downstream='BLOCKED'),ensure_ascii=False))
