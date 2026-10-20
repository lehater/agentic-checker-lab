"""Check immutable accepted inputs used by the isolated CoderMind run."""
import hashlib
import json
from pathlib import Path

ROOT = Path.cwd()
RUN = ROOT / 'experiments/runs/checker-v1'
manifest = json.loads((RUN / 'bridge.json').read_text())


def require_hash(data, expected):
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(f'Input changed: {actual} != {expected}')


for relative, digest in manifest['inputs'].items():
    require_hash((ROOT / relative).read_bytes(), digest)
workspace = Path.home() / '.cache/agentic-checker-lab/runs/checker-v1/workspace'
transferred = (workspace / 'docs/requirements.md').read_bytes()
require_hash(transferred, manifest['transferred_sha256'])
context = json.loads((RUN / 'context-bridge.json').read_text())
require_hash((workspace / 'AGENTS.md').read_bytes(), context['context_instruction_sha256'])
require_hash((RUN / 'cmind-AGENTS.md').read_bytes(), context['context_instruction_sha256'])
try:
    require_hash(transferred + b'\nUse first match only.\n', manifest['transferred_sha256'])
except ValueError:
    negative = 'PASS: changed input cannot reuse accepted transfer identity'
else:
    raise AssertionError('Changed input accepted')
result = dict(status='PASS', accepted_source_bytes_unchanged=True,
              transferred_bytes_unchanged=True, negative_check=negative,
              limitation='Hash binding proves input identity, not correctness of generated semantics.')
(RUN / 'bridge-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: accepted-source and transfer hashes; changed-input identity rejected')
