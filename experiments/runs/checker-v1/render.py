"""Disposable deterministic managed-artifact projections; publication remains truth."""
import json
from pathlib import Path
import sys
import yaml

ROOT = Path.cwd()
PIN = json.loads((ROOT / '.harness/harness-binding.json').read_text())['source']['revision']
sys.path.insert(0, str(Path.home() / '.cache/harness/v1' / PIN / 'src'))
from harness.workspace.workspace import SCHEMA_RENDERERS, validate_knowledge_document

output = ROOT / 'docs/generated/checker'
output.mkdir(parents=True, exist_ok=True)
for path in sorted((ROOT / '.harness/knowledge').glob('*.yaml')):
    document = yaml.safe_load(path.read_text())
    validate_knowledge_document(document)
    (output / (path.stem + '.md')).write_text(SCHEMA_RENDERERS[document['schema']](document))
print('Rendered managed requirements, verification and tests without duplicate Core graphs.')
