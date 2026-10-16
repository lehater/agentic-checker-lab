"""Verify replay and critical acceptance/publication boundaries without mutations."""
import copy,hashlib,json,os,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision'];PACK=Path.home()/'.cache/harness/v1'/PIN
sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication,prepare_reconciliation_publication,publish_project_publication
from harness.project_model.engineering_graph import validate_realization
from harness.project_model.core import resolve_question,CoreError
load=lambda p:yaml.safe_load(Path(p).read_text())
pubpath=ROOT/'.harness/project-publication.yaml';snapshot=pubpath.read_bytes();commands=[]
# Replay recomputes every real input and projection, but must not republish.
for argv in [['python3',str(RUN/'execute.py')],['make','check'],['git','diff','--cached','--check'],['git','diff','--check']]:
 p=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));commands.append(dict(argv=argv,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr));assert p.returncode==0,commands[-1]
assert pubpath.read_bytes()==snapshot
first_evidence=(RUN/'evidence.json').read_bytes()
p=subprocess.run(['python3',str(RUN/'execute.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));assert p.returncode==0,p.stderr
assert (RUN/'evidence.json').read_bytes()==first_evidence;assert pubpath.read_bytes()==snapshot
g=load(ROOT/'.harness/engineering-graph.yaml');pub=read_project_publication(pubpath,graph=g);s=pub['state'];before=load(RUN/'publication-before.yaml');checks={}
def rejected(name,operation):
 try:operation()
 except CoreError as error:checks[name]=dict(result='PASS',error=str(error))
 else:raise AssertionError(name+' unexpectedly accepted')
 assert pubpath.read_bytes()==snapshot
rejected('stale_cas',lambda:publish_project_publication(pubpath,graph=g,publication=pub,expected_revision=before['revision']))
badlife=copy.deepcopy(s['lifecycle']);badlife['providers'][-1]['acceptance_id']='deliberate-negative-mismatch'
rejected('mixed_admission_lifecycle_identity',lambda:prepare_reconciliation_publication(graph=g,current_publication=pub,expected_revision=pub['revision'],outcomes={'checker.requirements':'CURRENT'},core_model=s['core_model'],semantic_evaluations=s['semantic_evaluations'],lifecycle=badlife,decision_failures=s['decision_failures']))
m=validate_realization(g,s['core_model'])
rejected('wrong_resolution_authority',lambda:resolve_question(m,'Q-PR-001','CHECKER-PROBLEM-EVIDENCE','negative-attempt','ABSENT'))
aid=s['lifecycle']['providers'][-1]['acceptance_id']
rejected('same_superseded_acceptance',lambda:resolve_question(m,'Q-PR-001','CHECKER-REQUIREMENTS',aid,aid))
for q in s['core_model']['questions']:
 assert q['resolution']==dict(artifact='CHECKER-REQUIREMENTS',acceptance_id=aid,supersedes_acceptance_id='ABSENT')
assert s['lifecycle']['providers'][0]==before['state']['lifecycle']['providers'][0]
assert s['semantic_evaluations']['semantic_evaluations'][0]==before['state']['semantic_evaluations']['semantic_evaluations'][0]
for path in ['.harness/engineering-graph.yaml','docs/scenario/problem-framing-decision.md','docs/scenario/first-slice-product-decision.md','experiments/runs/harness-requirements-v1']:
 assert subprocess.run(['git','diff','--exit-code','e2690dc','--',path],capture_output=True).returncode==0
(RUN/'verification.json').write_text(json.dumps(dict(commands=commands,second_replay=dict(argv=['python3',str(RUN/'execute.py')],exit_code=p.returncode),negative_checks=checks,question_admission_lifecycle_identities_match=True,replay_identical=True,publication_bytes_stable=True,discovery_preserved=True,publication_revision=pub['revision']),indent=2,ensure_ascii=False)+'\n')
print('PASS: replay, identities, Core resolutions, CAS, preserved Discovery, repository checks')
