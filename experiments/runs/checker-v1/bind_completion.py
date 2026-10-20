"""Hash-bind already reviewed evidence; never admit or decide semantic authority.

Run after actual acceptance/native/conformance/verify operations, from repo root.
Requires PyYAML for reading the existing Harness evidence, not for product/CI.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import yaml

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    paths = set()
    independent = {}
    for contract in ['TD-BEHAVIOR', 'TD-BOUNDARIES']:
        evidence = yaml.safe_load((RUN / (contract + '-evidence.yaml')).read_text())
        assert all(e['status'] == 'PASSED' for e in evidence['executables'])
        for name, sha in evidence['test_source_sha256'].items():
            assert digest(ROOT / name) == sha, f'Execution is stale for {name}'
            independent[name] = sha
    slugs = ['problem', 'requirements', 'domain', 'verification', 'scenarios',
             'architecture', 'interface', 'policy', 'components',
             'technical-verification', 'tests', 'implementation']
    for slug in slugs:
        spec = yaml.safe_load((RUN / (slug + '.yaml')).read_text())
        evidence = yaml.safe_load((RUN / (slug + '-evidence.yaml')).read_text())
        path = ROOT / spec['candidate']['path']
        assert evidence['status'] == 'ACCEPTED'
        assert digest(path) == evidence['content_sha256'], f'Admission content changed: {path}'
        paths.add(path)
        for suffix in ['.yaml', '-admission.yaml', '-evidence.yaml']:
            paths.add(RUN / (slug + suffix))
    for folder in ['.harness', 'checker', 'src', 'tests', 'tooling/patches']:
        paths.update(p for p in (ROOT / folder).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'
                     and not p.name.endswith('.lock'))
    paths.update([ROOT / 'Makefile', ROOT / '.github/workflows/repository.yml',
                  ROOT / 'tooling/versions.yaml', ROOT / 'examples/checker-input.json'])
    paths.update((ROOT / 'tools').glob('*checker*.py'))
    paths.update((ROOT / 'tools').glob('*cmind_cli_review.py'))
    paths.update((ROOT / 'docs/decisions').glob('000[234]*.md'))
    paths.update(RUN.glob('*.json'))
    paths.update(RUN.glob('TD-*.yaml'))
    paths.update(RUN.glob('*.py'))
    paths.update((RUN / 'rpg-realized').glob('*'))
    paths.add(ROOT / 'docs/checker/realization-plan.md')
    paths.discard(RUN / 'completion.json')
    paths.discard(RUN / 'clean-checkout.json')
    bridge = json.loads((RUN / 'bridge.json').read_text())
    result = dict(status='PASS', scope='Synthetic Checker implementation evidence; no production or comparative claim',
                  canonical_input_sha256=bridge['inputs'], independent_source_sha256=independent,
                  files_sha256={str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)})
    (RUN / 'completion.json').write_text(json.dumps(result, indent=2) + '\n')
    subprocess.run([sys.executable, str(ROOT / 'tools/check_checker_evidence.py')], check=True)


if __name__ == '__main__':
    main()
