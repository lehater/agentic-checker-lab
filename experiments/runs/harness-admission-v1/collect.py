import subprocess,json,hashlib,sys,datetime,shutil
from pathlib import Path
r=Path(__file__).resolve().parent; root=Path.cwd(); sha='442db854c3a736a5e500b4a41664b80981b0d94c'; pack=Path.home()/'.cache/harness/v1'/sha
def run(name,args):
 p=subprocess.run(args,capture_output=True,text=True); (r/(name+'.stdout')).write_text(p.stdout); (r/(name+'.stderr')).write_text(p.stderr)
 with (r/'commands.jsonl').open('a') as f:f.write(json.dumps(dict(name=name,argv=args,cwd=str(root),exit_code=p.returncode))+'\n')
 return p
run('head',['git','rev-parse','HEAD']);run('status-before',['git','status','--short']);run('cli-version',['codex','--version'])
env=['env','PYTHONDONTWRITEBYTECODE=1','PYTHONPATH='+str(pack/'src'),sys.executable]
run('validate-pack',env+['-m','harness.application.consumer_pack','validate-pack',str(pack),'--revision',sha,'--consumer-api','v1'])
files=[Path('AGENTS.md'),Path('.harness/harness-binding.json'),*Path('docs/project').glob('*'),Path('docs/scenario/problem-framing-decision.md'),Path('docs/research/task-004-problem-semantic-admission.md'),Path('docs/research/task-004-harness-agent-review.md'),*Path('tooling/fixtures/checker-intake').rglob('*'),*Path('experiments/runs/harness-intake-v1').rglob('*')]
manifest={str(p):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'git_blob':subprocess.run(['git','hash-object',str(p)],capture_output=True,text=True).stdout.strip()} for p in files if p.is_file()}
(r/'source-hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
contracts=['spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml','spec/semantic-acceptance/artifact-semantic-acceptance-v1.yaml','src/harness/application/semantic_admission.py','docs/design/project-publication-v0.md','spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml']
run('pinned-contract-inspection',['cat',*[str(pack/p) for p in contracts]])
# Archive reviewed historical outputs as one inspection transcript, without promoting them.
run('intake-output-inspection',['cat',*[str(p) for p in sorted(Path('experiments/runs/harness-intake-v1').glob('*.stdout'))]])
run('authority-evidence',['rg','-n','DISCOVERY|Authority|review|делег|назнач|приёмк','docs/project','docs/scenario/problem-framing-decision.md','docs/research/task-004-problem-semantic-admission.md'])
run('canonical-path-inventory',['git','ls-files','.harness','*core*','*publication*','*authority*','*engineering-graph*'])
