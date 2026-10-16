import subprocess,sys,json,datetime
from pathlib import Path
r=Path(__file__).resolve().parent
name=sys.argv[1]; args=sys.argv[2:]
p=subprocess.run(args,capture_output=True,text=True)
(r/(name+'.stdout')).write_text(p.stdout)
(r/(name+'.stderr')).write_text(p.stderr)
with (r/'commands.jsonl').open('a') as f: f.write(json.dumps({'name':name,'argv':args,'cwd':str(Path.cwd()),'exit_code':p.returncode,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
print(p.stdout,end=''); print(p.stderr,end='',file=sys.stderr); print('EXIT_CODE='+str(p.returncode))
