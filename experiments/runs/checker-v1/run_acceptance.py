"""Execute independent test contracts and record real evidence, never infer PASS."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import yaml

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
contracts = {
    'TD-BEHAVIOR': ['test_checker_acceptance.CheckerAcceptance.test_precode_scenarios'],
    'TD-BOUNDARIES': [
        'test_checker_acceptance.CheckerAcceptance.test_text_report',
        'test_checker_acceptance.CheckerAcceptance.test_strict_boundary',
        'test_checker_acceptance.CheckerAcceptance.test_duplicate_snapshot_and_rule_rejected',
        'test_checker_acceptance.CheckerAcceptance.test_missing_and_empty_inputs',
        'test_checker_structure.CheckerStructure.test_inward_dependencies',
        'test_checker_structure.CheckerStructure.test_source_substitution_and_immutability',
    ],
}
design = yaml.safe_load((ROOT / '.harness/knowledge/tests.yaml').read_text())
overall = True
for contract_id, tests in contracts.items():
    executions = []
    commands = []
    for index, locator in enumerate(tests):
        result = subprocess.run([sys.executable, '-m', 'unittest', '-v', locator], cwd=ROOT/'tests',
                                capture_output=True, text=True,
                                env=__import__('os').environ | {'PYTHONPATH': str(ROOT)})
        # cwd=tests allows direct locators; acceptance itself always executes from ROOT.
        evidence_id = contract_id + '-' + str(index + 1)
        executions.append(dict(id=evidence_id, test='tests/' + locator, status='PASSED' if result.returncode == 0 else 'FAILED'))
        commands.append(dict(test=locator, exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr))
        overall = overall and result.returncode == 0
    contract = next(t for t in design['content']['tests'] if t['id'] == contract_id)
    ids = [t['id'] for t in executions]
    bindings = [dict(id=contract_id+'-'+o['id'], obligation=o['id'], evidence=ids)
                for kind in ['operation_obligations', 'oracle_obligations'] for o in contract[kind]]
    evidence = dict(version=1, kind='harness-test-realization-evidence', test_contract=contract_id,
                    executables=executions, bindings=bindings,
                    test_source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                        for p in (ROOT/'tests').glob('test_checker*.py')})
    (RUN/(contract_id+'-execution.json')).write_text(json.dumps(commands, indent=2)+'\n')
    (RUN/(contract_id+'-evidence.yaml')).write_text(yaml.safe_dump(evidence, sort_keys=False))
    print(contract_id, 'PASSED' if all(e['status']=='PASSED' for e in executions) else 'FAILED')
raise SystemExit(0 if overall else 1)
