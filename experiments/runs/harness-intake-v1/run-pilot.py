import os, sys, json, subprocess, pathlib, hashlib
R=pathlib.Path(__file__).resolve().parent
P=pathlib.Path.home()/'.cache/harness/v1/442db854c3a736a5e500b4a41664b80981b0d94c'
V=pathlib.Path.home()/'.cache/agentic-checker-lab/venvs/harness-smoke/bin/python'
env=dict(os.environ,PYTHONPATH=f'{P}/src:{P}',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R))
def run(name,args):
 c=[str(V),*args]; p=subprocess.run(c,cwd=P,env=env,text=True,capture_output=True)
 (R/(name+'.stdout')).write_text(p.stdout); (R/(name+'.stderr')).write_text(p.stderr)
 with (R/'commands.jsonl').open('a') as f:f.write(json.dumps(dict(name=name,argv=c,cwd=str(P),env_overrides={k:env[k] for k in ['PYTHONPATH','PYTHONDONTWRITEBYTECODE','TMPDIR']},exit_code=p.returncode))+'\n')
 print(name,p.returncode,p.stdout[:1800],p.stderr[:500])
 return p
if __name__=='__main__':
 run('validate-binding',['-m','harness.application.consumer_pack','validate-binding',str(R.parents[2]/'.harness/harness-binding.json')])
 run('validate-pack',['-m','harness.application.consumer_pack','validate-pack',str(P),'--revision',P.name])
 run('versions',['-c','import sys,yaml,platform; print(sys.version); print("PyYAML",yaml.__version__); print(platform.platform())'])
 run('bootstrap-route',['-m','harness.application.skill_router','operation','--surface','consumer','--operation','project-bootstrap-reconcile','--root',str(P)])
 import yaml
 kinds=[('DISCOVERY','problem-evidence','problem',[]),('PRODUCT-REQUIREMENTS','product-requirements','requirements',['problem']),('SYSTEM-ARCHITECTURE','system-architecture','architecture',['requirements']),('VERIFICATION-DESIGN','verification-strategy','verification',['requirements','architecture']),('IMPLEMENTATION-DESIGN','implementation-design','implementation',['architecture','verification'])]
 graph=dict(version=1,kind='harness-engineering-graph',id='CHECKER-DISCOVERY-CANDIDATE',default_subject='CHECKER-OFFLINE-CANDIDATE',authorities=[],consumers=[dict(id='CHECKER-IMPLEMENTATION',purpose='Candidate implementation need; discovery only, no coding authorization.',requires=[dict(capability='checker.implementation')])])
 for owner,kind,cap,deps in kinds:
  graph['authorities'].append(dict(id=owner,responsibility=f'Candidate ownership of Checker {kind}; not accepted delegation.',boundary=dict(semantic_cohesion=f'One class of {kind} knowledge.',independent_change=f'{kind} knowledge has its own revision boundary.',public_contract=f'Expose checker.{cap} to downstream engineering; candidate only.'),produces=[dict(capability='checker.'+cap,knowledge_kind=kind,requires=['checker.'+d for d in deps])]))
 (R/'engineering-graph-candidate.yaml').write_text(yaml.safe_dump(graph,sort_keys=False)); (R/'core-candidate.yaml').write_text('artifacts: []\nquestions: []\n')
 g=str(R/'engineering-graph-candidate.yaml'); m=str(R/'core-candidate.yaml'); target='CHECKER-IMPLEMENTATION'
 run('graph-validation',['-m','harness.project_model.engineering_graph','validate',g])
 run('profile',['-m','harness.project_model.engineering_graph','profile',g,target])
 run('target-evaluation',['-m','harness.project_model.engineering_graph','evaluate',g,target,m])
 run('agent-routing',['-m','harness.application.agent_router',g,target,m])
 run('engineering-coverage',['-m','harness.coverage.engineering_coverage',g,m,target,'--scope','CHECKER-OFFLINE-CANDIDATE'])
