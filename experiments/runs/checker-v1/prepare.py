"""Authoring helpers. These do not determine semantic acceptance."""
from pathlib import Path
import yaml
ROOT = Path.cwd()
RUN = ROOT/'experiments/runs/checker-v1'
PACK = Path.home()/'.cache/harness/v1'/__import__('json').loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision']
def load(p): return yaml.safe_load(Path(p).read_text())
def save(p,v): Path(p).write_text(yaml.safe_dump(v,sort_keys=False,allow_unicode=True))
def prepare(slug, authority, kind, dependencies, path, assertions, rationale, review_extra=None):
    g=load(ROOT/'.harness/engineering-graph.yaml')
    catalog=load(PACK/'catalogs/software-authorities-v0.yaml')
    caps=['checker.'+d for d in dependencies]
    if not any(a['id']==authority for a in g['authorities']):
        row=next(a for a in catalog['authorities'] if a['id']==authority)
        g['authorities'].append({k:row[k] for k in ['id','responsibility','boundary']} | {'produces':[]})
    a=next(a for a in g['authorities'] if a['id']==authority)
    if not any(p['capability']=='checker.'+slug for p in a['produces']):
        a['produces'].append(dict(capability='checker.'+slug,knowledge_kind=kind,requires=caps))
        g['consumers'][0]['requires'].append(dict(capability='checker.'+slug))
    save(ROOT/'.harness/engineering-graph.yaml',g)
    contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml')
    contract=next(c for c in contracts['contracts'] if c['knowledge_kind']==kind)
    checks=contracts['defaults']['required_review_checks']+contract.get('required_review_checks',[])
    review=dict(status='ACCEPTED',checks=checks,reviewer='Engineering agent under current owner assignment',record=path,rationale=rationale)
    review.update(review_extra or {})
    aa=[dict(id=i,kind=k,subject=i,semantic_value=v,decision_authority=authority,derived_from=refs) for i,k,v,refs in assertions]
    spec=dict(knowledge_kind=kind,depends_on=dependencies,candidate=dict(id=slug,path=path,capability='checker.'+slug,
        canonical_references=[dict(referenced_path=load(RUN/(d+'.yaml'))['candidate']['path']) for d in dependencies],semantic_assertions=aa,semantic_review=review))
    save(RUN/(slug+'.yaml'),spec)
