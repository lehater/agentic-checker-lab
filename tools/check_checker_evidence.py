#!/usr/bin/env python3
"""Check that recorded acceptance belongs to the checked-out Checker inputs.

Stdlib only; this checks evidence identity/accounting, not semantic authority.
Re-admission and native model execution remain explicit pinned-tool operations.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'experiments/runs/checker-v1'


def load(name):
    return json.loads((RUN / name).read_text(encoding='utf-8'))


def verify_hashes(files):
    for name, expected in files.items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise AssertionError(f'Unsafe evidence path: {name}')
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f'Acceptance evidence is stale for {name}; rerun and review affected evidence')


def main():
    completion = load('completion.json')
    assert completion['status'] == 'PASS'
    verify_hashes(completion['files_sha256'])
    verify_hashes(completion['canonical_input_sha256'])
    verify_hashes(completion['independent_source_sha256'])
    native = load('native-provenance.json')
    verify_hashes(native['source_sha256'])
    runtime = {str(p.relative_to(ROOT)) for folder in ['checker', 'src']
               for p in (ROOT / folder).rglob('*.py')}
    assert runtime == set(native['source_sha256']), 'Runtime source inventory changed'
    final = load('native-final-test.json')
    assert final['success'] and final['failed'] == final['errors'] == 0
    assert final['smoke_test']['success']
    review = load('native-global-review.json')
    assert review['success'] and review['review_interface'] == 'cli'
    lock = json.loads((ROOT / 'tooling/patches/cmind-cli-global-review.json').read_text())
    assert native['review_patch_sha256'] == lock['patch_sha256']
    assert load('cmind-review-patch-tests.json')['status'] == 'PASS'
    assert not load('native-global-review-upstream.json')['success']
    verify_hashes(native['native_replay_sha256'])
    assert load('traceability.json')['status'] == 'SOURCE_BOUND'
    for row in load('traceability.json')['traceability']:
        for node in row['rpg_nodes']:
            verify_hashes({node['locator'].split('::', 1)[0]: node['source_sha256']})
    for contract in ['TD-BEHAVIOR', 'TD-BOUNDARIES']:
        result = load(contract + '-conformance.json')
        assert result['status'] == 'ACCEPTED' and not result['findings']
        for accounting in result['coverage'].values():
            assert accounting['covered'] == accounting['required']
    assert load('verification.json')['status'] == 'PASS'
    assert load('closure.json')['status'] == 'COMPLETE'
    assert load('coverage.json')['completion_ready']
    mutations = load('mutations.json')
    assert mutations['status'] == 'PASS' and mutations['original_source_unchanged']
    assert len(mutations['results']) == 7
    assert all(row['status'] == 'DETECTED' for row in mutations['results'][1:])
    print('Checker evidence PASS: source/input identity, native validation, conformance and closure')


if __name__ == '__main__':
    main()
