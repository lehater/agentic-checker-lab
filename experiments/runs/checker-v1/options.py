"""Bind authored pre-choice options to a real Harness request; no candidate input."""
import sys
from prepare import *
sys.path.insert(0,str(PACK/'src'))
from harness.application.decision_explorer_request import build_decision_explorer_request
from harness.decision.decision_governance import decision_contract_index, axis_policies
from harness.project_model.engineering_graph import validate_realization
from harness.application.authority_context import build_authority_context

slug, authority, kind = sys.argv[1:4]
deps=sys.argv[4:]
g=load(ROOT/'.harness/engineering-graph.yaml')
cat=load(PACK/'catalogs/software-authorities-v0.yaml')
if not any(a['id']==authority for a in g['authorities']):
    row=next(a for a in cat['authorities'] if a['id']==authority)
    g['authorities'].append({k:row[k] for k in ['id','responsibility','boundary']}|dict(produces=[]))
a=next(a for a in g['authorities'] if a['id']==authority)
if not any(p['capability']=='checker.'+slug for p in a['produces']):
    a['produces'].append(dict(capability='checker.'+slug,knowledge_kind=kind,requires=['checker.'+d for d in deps]))
    g['consumers'][0]['requires'].append(dict(capability='checker.'+slug))
save(ROOT/'.harness/engineering-graph.yaml',g)
pub=load(ROOT/'.harness/project-publication.yaml'); model=pub['state']['core_model']
model['authorities']=[dict(id=a['id']) for a in g['authorities']]
model=validate_realization(g,model)
contract=decision_contract_index(load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml'))[kind]
policy=load(ROOT/'.harness/decision-policy.yaml')
context=build_authority_context(g,model,authority,['checker.'+slug])
baseline={p['capability']:p['acceptance_id'] for p in pub['state']['lifecycle']['providers'] if p['capability'] in ['checker.'+d for d in deps]}
req=build_decision_explorer_request(capability='checker.'+slug,knowledge_kind=kind,authority=authority,authority_context=context,contract=contract,axis_policies=axis_policies(contract,policy),prerequisite_baseline=baseline,model=model)
save(RUN/(slug+'-request.yaml'),req)
# Options content is authored separately before any candidate.
evidence=load(RUN/(slug+'-options-input.yaml'))
evidence.update(version=1,kind='harness-decision-exploration',capability='checker.'+slug,knowledge_kind=kind,explorer_request_id=req['request_id'])
save(RUN/(slug+'-options.yaml'),evidence)
print(req['request_id'])
