"""Reproduce pinned semantic projections and test CAS/currentness boundaries."""
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
import yaml
ROOT=Path.cwd(); RUN=Path(__file__).resolve().parent
load=lambda p:yaml.safe_load(Path(p).read_text())
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision']
PACK=Path.home()/'.cache/harness/v1'/PIN; sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication, prepare_reconciliation_publication, publish_project_publication
from harness.project_model.core import CoreError
pubpath=ROOT/'.harness/project-publication.yaml'; snapshot=pubpath.read_bytes(); logs=[]
for i in range(2):
 p=subprocess.run(['python3',str(RUN/'execute.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 assert p.returncode==0,p.stderr
 assert pubpath.read_bytes()==snapshot
 if i==0: evidence=(RUN/'evidence.json').read_bytes()
 else: assert (RUN/'evidence.json').read_bytes()==evidence
 logs.append(dict(check='replay-'+str(i+1),exit_code=p.returncode,stdout=p.stdout))
g=load(ROOT/'.harness/engineering-graph.yaml'); pub=read_project_publication(pubpath,graph=g); before=load(RUN/'publication-before.yaml'); s=pub['state']
checks={}
def rejected(name,call):
 try: call()
 except CoreError as e: checks[name]=str(e)
 else: raise AssertionError(name+' unexpectedly accepted')
 assert pubpath.read_bytes()==snapshot
rejected('stale_cas',lambda:publish_project_publication(pubpath,graph=g,publication=pub,expected_revision=before['revision']))
rejected('false_current_with_questions',lambda:prepare_reconciliation_publication(graph=g,current_publication=pub,expected_revision=pub['revision'],outcomes={'checker.verification-strategy':'CURRENT'},core_model=s['core_model'],semantic_evaluations=s['semantic_evaluations'],lifecycle=s['lifecycle'],decision_failures=s['decision_failures']))
assert s['lifecycle']==before['state']['lifecycle']
assert s['semantic_evaluations']==before['state']['semantic_evaluations']
assert s['core_model']['artifacts']==before['state']['core_model']['artifacts']
assert s['core_model']['questions'][:2]==before['state']['core_model']['questions']
assert [q['id'] for q in s['core_model']['questions'][2:]]==['Q-DV-001','Q-DV-002']
assert all(a['id']!='DOMAIN-STRATEGY' for a in g['authorities'])
assert load(RUN/'semantic-admission.yaml')['status']=='REJECTED'
assert 'lifecycle_assertion' not in load(RUN/'semantic-admission.yaml')
a=load(RUN/'verification-candidate.yaml'); reqs=load(ROOT/'.harness/knowledge/checker-requirements.yaml')['content']['requirements']
assert {r['id'] for r in reqs}=={r for c in a['content']['checks'] for r in c['verifies']}
assert len(reqs)==28 and len(load(RUN/'scenario-drafts.yaml')['scenarios'])==8
for path in ['.harness/knowledge/checker-requirements.yaml','docs/scenario/problem-framing-decision.md','docs/scenario/first-slice-product-decision.md','docs/scenario/domain-verification-delegation.md']:
 p=subprocess.run(['git','diff','--exit-code','b8779db','--',path],capture_output=True,text=True); assert p.returncode==0,p.stdout
for args in [['make','check'],['git','diff','--check'],['git','diff','--cached','--check']]:
 p=subprocess.run(args,capture_output=True,text=True); assert p.returncode==0,p.stdout+p.stderr
 logs.append(dict(argv=args,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
result=dict(status='PASS',replays_identical=True,publication_bytes_stable=True,upstream_evaluations_and_lifecycle_unchanged=True,all_28_requirements_have_disposition=True,no_fabricated_strategy_provider=True,scenario_drafts=8,negative_checks=checks,commands=logs,publication_revision=pub['revision'])
(RUN/'verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('PASS: two stable replays, strict rejection, upstream CURRENT preserved, CAS/false CURRENT rejected, all 28 dispositions, make check')
