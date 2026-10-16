"""Pinned Consumer execution. Run from repo root; safe replay validates terminal snapshot.
Supported intent rows are reviewed individually; incomplete artifact is NOT a provider.
"""
import copy,hashlib,json,os,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
PIN=json.loads((ROOT/'.harness/harness-binding.json').read_text())['source']['revision'];PACK=Path.home()/'.cache/harness/v1'/PIN
logs=[]
def cmd(argv):
 p=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=str(PACK/'src'),PYTHONDONTWRITEBYTECODE='1'))
 logs.append(dict(argv=argv,cwd=str(ROOT),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
 assert p.returncode==0,logs[-1]
 return p.stdout
def load(p):return yaml.safe_load(Path(p).read_text())
def save(path,value):Path(path).write_text(yaml.safe_dump(value,sort_keys=False,allow_unicode=True))
cmd(['python3','.harness/harnessw.py','sync']);cmd([sys.executable,'-m','harness.application.consumer_pack','validate-pack',str(PACK),'--revision',PIN])
instructions={}
for category,key in [('operation','project-bootstrap-reconcile'),('artifact','product-requirements'),('operation','project-engineering-status')]:
 args=[sys.executable,'-m','harness.application.skill_router',category,'--root',str(PACK)]
 args+=['--knowledge-kind',key] if category=='artifact' else ['--surface','consumer','--operation',key]
 route=json.loads(cmd(args))
 for rel in [*route['instruction_contracts'],route['skill']]:instructions[rel]=hashlib.sha256((PACK/rel).read_bytes()).hexdigest()
sys.path.insert(0,str(PACK/'src'))
from harness.application.project_publication import read_project_publication,prepare_reconciliation_publication,publish_project_publication
from harness.application.semantic_admission import admit_artifact,derive_acceptance_policy_fingerprints
from harness.project_model.engineering_graph import validate_realization
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.application.decision_pipeline import derive_decision_roadmap
from harness.application.semantic_closure import evaluate_semantic_closure
from harness.coverage.engineering_coverage import evaluate_with_repository_policy
from harness.application.project_frontier import compose_project_frontier
from harness.reference_model.project_status import bootstrap_registry,validate_registry,status
# Frozen original accepted publication is retained as one historical execution input.
baseline_path=RUN/'publication-before.yaml';pubpath=ROOT/'.harness/project-publication.yaml';graphpath=ROOT/'.harness/engineering-graph.yaml'
g=load(graphpath)
if not baseline_path.exists():save(baseline_path,read_project_publication(pubpath,graph=g))
baseline=load(baseline_path)
catalog=load(PACK/'catalogs/software-authorities-v0.yaml')
if not any(a['id']=='PRODUCT-REQUIREMENTS' for a in g['authorities']):
 a=copy.deepcopy(next(a for a in catalog['authorities'] if a['id']=='PRODUCT-REQUIREMENTS'))
 a={k:a[k] for k in ['id','responsibility','boundary']}
 a['produces']=[dict(capability='checker.requirements',knowledge_kind='product-requirements',requires=['checker.problem'])];g['authorities'].append(a)
 g['consumers'].append(dict(id='CHECKER-REQUIREMENTS-ADMISSION',purpose='PDEC-CHECKER-003 bounded requirements admission; not complete product implementation scope.',requires=[dict(capability='checker.requirements')]))
 save(graphpath,g)
model=copy.deepcopy(baseline['state']['core_model']);life=baseline['state']['lifecycle'];sem=copy.deepcopy(baseline['state']['semantic_evaluations'])
contracts=load(PACK/'spec/semantic-acceptance/knowledge-kind-contracts-v1.yaml');decisions=load(PACK/'spec/decision-governance/knowledge-kind-decision-contracts-v1.yaml');skills=load(PACK/'skills/artifact-skill-registry-v0.yaml')
policies=derive_acceptance_policy_fingerprints(graph=g,knowledge_contracts=contracts,decision_contracts=decisions)
states=lifecycle_states(g,validate_realization(g,model),life,current_acceptance_policy_fingerprints=policies);assert states['checker.problem']['state']=='CURRENT'
before_roadmap=derive_decision_roadmap(graph=g,model=model,target='CHECKER-REQUIREMENTS-ADMISSION',lifecycle=life,decision_contracts=decisions,decision_policy=None,decision_failures=baseline['state']['decision_failures'])
assert any(x.get('capability')=='checker.requirements' for x in before_roadmap['ready'])
rows=[
 ('001','Показывать оператору релевантные места применения политики для исследуемого сетевого потока.','outcome','Для потока и независимо установленного релевантного placement проверить, что результат представляет этот placement; критерий выбора поддерживаемых потоков/placements ожидает Q-PR-001.'),
 ('002','Показывать оператору подходящие сохранённые ACL-правила для исследуемого сетевого потока.','outcome','При известных подходящих сохранённых правилах результат содержит сведения о правилах; критерий подходящего правила и полноты набора ожидает Q-PR-001.'),
 ('003','Сохранять порядок обработки показываемых подходящих ACL-правил.','outcome','Для двух показываемых правил с установленным порядком обработки результат сохраняет этот порядок; общий порядок между разными policy contexts не придумывается.'),
 ('004','Предоставлять оператору сведения о достоверности источников используемых свидетельств.','outcome','Результат позволяет оценить достоверность источников; конкретное значение достоверности и поведение при неизвестных данных требуют Q-PR-002.'),
 ('005','Формирование единого универсального Permit/Deny не является обязательным результатом Checker.','verdict-boundary','Отсутствие универсального verdict само по себе не является провалом приёмки; специфичная интерпретация не запрещена и не становится обязательной.'),
 ('006','Не превращать отсутствие совпадающего правила само по себе в DENY или ALLOW.','verdict-boundary','При одном лишь отсутствии совпадения результат не утверждает DENY/ALLOW на этом основании; формат no-match output этим требованием не задаётся.'),
 ('007','Не выводить общесистемный эффективный verdict из одного лишь факта наличия подходящего правила.','verdict-boundary','Наличие подходящего Permit или Deny правила само по себе не представлено как доказанный общесистемный эффективный verdict.')]
requirements=[]
for suffix,statement,source,criterion in rows:
 requirements.append(dict(id='REQ-CHECKER-'+suffix,statement=statement,status='ACCEPTED',source_refs=['checker.problem#problem-'+source,'docs/scenario/problem-framing-decision.md'],acceptance_criteria=[criterion]))
artifact=dict(version=1,kind='harness-knowledge-artifact',artifact='CHECKER-REQUIREMENTS',title='Checker — source-supported intent subset, incomplete requirements candidate',schema='product-requirements/v1',disposition='CANDIDATE_BLOCKED_NOT_CORE_PROVIDER',status_semantics='Row ACCEPTED denotes individually reviewed normative intent under PDEC-003; the entire artifact has REJECTED semantic review and is not admitted or published as canonical product knowledge.',content=dict(purpose='Объяснимое исследование сетевого потока оператором в рамках PDEC-CHECKER-001; набор недостаточен для завершённой product acceptance.',requirements=requirements,non_goals=['Универсальный Permit/Deny не обязателен; это не запрет любой специфичной интерпретации.','Этот кандидат не принимает offline-only, автоматический route discovery, live diagnostics, UI/API, конкретный tuple, matching algorithm, architecture или runtime.']))
artifact_path=RUN/'requirements-candidate.yaml';save(artifact_path,artifact)
cmd([sys.executable,'-m','harness.workspace.workspace','validate-artifact',str(artifact_path)])
# Source assertions mirror actual accepted prerequisite atoms; no historical artifacts
# or delegation records are forged into canonical semantic prerequisites.
previous=load(ROOT/'experiments/runs/harness-current-v1/candidate.yaml')
sources=dict(semantic_assertions=[dict(x,source_artifact='CHECKER-PROBLEM-EVIDENCE') for x in previous['semantic_assertions']])
candidate=dict(id='CHECKER-REQUIREMENTS',path=str(artifact_path.relative_to(ROOT)),capability='checker.requirements',canonical_references=[dict(referenced_path='docs/scenario/problem-framing-decision.md')],semantic_assertions=[dict(id=r['id'],kind='product-requirement',subject=r['id'],semantic_value=r['statement'],decision_authority='PRODUCT-REQUIREMENTS',derived_from=['problem-'+row[2]]) for r,row in zip(requirements,rows)],semantic_review=dict(status='REJECTED',checks=['source-discipline','authority-boundary','no-invention','observable-product-level','no-downstream-design-promotion'],reason='Supported intent subset reviewed, but no accepted supported traffic/placement/match scope or observable credibility/partial-evidence acceptance policy. Q-PR-001 and Q-PR-002 prevent complete requirements acceptance.',reviewer='Acting engineering agent delegated by PDEC-CHECKER-003',record='experiments/runs/harness-requirements-v1/review.md'))
save(RUN/'sources.yaml',sources);save(RUN/'admission-candidate.yaml',candidate)
attempt='task-004-requirements-attempt-'+hashlib.sha256(json.dumps(candidate,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:20]
evaluation=admit_artifact(graph=g,model=model,skill_registry=skills,knowledge_contracts=contracts,decision_contracts=decisions,capability='checker.requirements',sources=sources,candidate=candidate,acceptance_id=attempt,lifecycle=life)
save(RUN/'semantic-admission.yaml',evaluation)
assert evaluation['status']=='REJECTED';assert 'lifecycle_assertion' not in evaluation
questions=[dict(id='Q-PR-001',authority='PRODUCT-REQUIREMENTS',text='Какой минимальный наблюдаемый scope первого Checker принимается: какие потоки и policy contexts поддерживаются, какие сведения считаются входом/обязательным результатом и по каким продуктовым условиям placements/правила считаются релевантными/подходящими? Необходима граница, не выбор алгоритма, интерфейса или архитектуры.',blocks_capabilities=['checker.requirements'],blocks=[],answer_from=[]),dict(id='Q-PR-002',authority='PRODUCT-REQUIREMENTS',text='Как оператор должен различать надёжные, неизвестные, неполные или устаревшие свидетельства и какой результат считается допустимым при отсутствующих/недостоверных источниках в scope Q-PR-001? Определить наблюдаемые условия приёмки без придуманных порогов freshness и без универсального verdict.',blocks_capabilities=['checker.requirements'],blocks=[],answer_from=[])]
model['questions'].extend(questions)
# Rejection belongs to the rejected attempt, not to a canonical provider. Keep it
# in run evidence; publish actual Core blockers together with unchanged acceptance.
next_pub=prepare_reconciliation_publication(graph=g,current_publication=baseline,expected_revision=baseline['revision'],outcomes={'checker.problem':'CURRENT','checker.requirements':'BLOCKED'},core_model=model,semantic_evaluations=sem,lifecycle=life,decision_failures=baseline['state']['decision_failures'])
current=read_project_publication(pubpath,graph=g)
if current['revision']!=next_pub['revision']:publish_project_publication(pubpath,graph=g,publication=next_pub,expected_revision=baseline['revision'])
readback=read_project_publication(pubpath,graph=g);assert readback==next_pub
s=readback['state'];model=s['core_model'];life=s['lifecycle'];sem=s['semantic_evaluations']
states=lifecycle_states(g,validate_realization(g,model),life,current_acceptance_policy_fingerprints=policies);assert states['checker.problem']['state']=='CURRENT'
assert s['lifecycle']==baseline['state']['lifecycle'];assert s['semantic_evaluations']==baseline['state']['semantic_evaluations'];assert s['core_model']['artifacts']==baseline['state']['core_model']['artifacts']
# Registry applicability remains separate from producer delegation.
registry_path=ROOT/'.harness/authority-assessments.yaml';registry=load(registry_path)
for item in registry['assessments']:
 if item['authority_id']=='PRODUCT-REQUIREMENTS':item.update(applicability='UNRESOLVED',evidence=['docs/scenario/product-requirements-delegation.md','core:question:Q-PR-001','core:question:Q-PR-002'],rationale='Delegated production with unresolved product scope/acceptance questions; no canonical requirements provider yet.',depends_on_evidence=['Q-PR-001','Q-PR-002'],reopening_conditions=['Questions resolved via admitted product provider'])
registry=bootstrap_registry(catalog,existing=registry,core=model);assert not validate_registry(catalog,registry);save(registry_path,registry)
target='CHECKER-REQUIREMENTS-ADMISSION'
road=derive_decision_roadmap(graph=g,model=model,target=target,lifecycle=life,decision_contracts=decisions,decision_policy=None,decision_failures=s['decision_failures'])
closure=evaluate_semantic_closure(graph=g,model=model,target=target,skill_registry=skills,semantic_evaluations=sem,lifecycle=life,knowledge_contracts=contracts,decision_contracts=decisions)
overlay=dict(subject_inventory=dict(state='QUESTION',question='Q-PR-001',rationale='Q-REC-002 refined into actual Product Core Questions; accepted atomic product scope remains incomplete.'))
coverage=evaluate_with_repository_policy(graph=g,realization=model,consumer=target,scope='CHECKER-REQUIREMENTS',semantic_evaluations=sem,project_overlay=overlay)
front=compose_project_frontier(target=target,decision_roadmap=road,semantic_closure=closure,engineering_coverage=coverage)
assert any(x.get('capability')=='checker.requirements' for x in road['blocked'])
paths=['AGENTS.md','.harness/harness-binding.json','docs/scenario/problem-framing-decision.md','docs/scenario/discovery-authority-delegation.md','docs/scenario/product-requirements-delegation.md','docs/scenario/checker-scope-reconciliation.yaml','tooling/fixtures/checker-intake/sssr-scn-006.md','tooling/fixtures/checker-intake/product-access-as-is.md']
result=dict(status='BLOCKED',pin=PIN,commands=logs,instruction_hashes=instructions,source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},admission_attempt_id=attempt,accepted_requirements_provider=False,publication_revision=readback['revision'],parent_revision=readback['parent_revision'],lifecycle=states,questions=questions,authority_status=status(catalog,registry,model),decision_roadmap_before=before_roadmap,decision_roadmap=road,semantic_closure=closure,coverage={k:coverage[k] for k in ['consumer','scope','completion_ready','activated_count','work_item_count','summary','subject_obligation_rows']},project_frontier=front,model_metadata=None,tokens=None,cost=None)
(RUN/'evidence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(status='BLOCKED',publication=readback['revision'],states=states),ensure_ascii=False))
