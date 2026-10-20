#!/usr/bin/env python3
"""Materialize a hash-checked, isolated CoderMind CLI review fix (ADR-0004).

Run with the pinned CoderMind virtualenv's Python. Prints the PYTHONPATH root.
The installed base package is never modified.
"""
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / 'tooling/patches/cmind-cli-global-review.patch'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    import cmind_cli
    lock = json.loads(PATCH.with_suffix('.json').read_text())
    metadata = json.loads(distribution('cmind-cli').read_text('direct_url.json'))
    assert metadata['vcs_info']['commit_id'] == lock['base_revision']
    assert digest(PATCH) == lock['patch_sha256']
    base = Path(cmind_cli.__file__).resolve().parent
    for name, hashes in lock['files'].items():
        assert digest(base / name) == hashes['base_sha256'], f'Base changed: {name}'
    destination = Path.home() / '.cache/agentic-checker-lab/overlays' / lock['patch_sha256']
    package = destination / 'cmind_cli'
    if not package.exists():
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copytree(base, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        subprocess.run(['patch', '--batch', '--forward', '-p1', '-d', str(package),
                        '-i', str(PATCH)], check=True, stdout=subprocess.DEVNULL)
    for path in base.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        name = str(path.relative_to(base))
        expected = lock['files'].get(name, {}).get('patched_sha256', digest(path))
        assert digest(package / name) == expected, f'Overlay mismatch: {name}'
    print(destination)


if __name__ == '__main__':
    main()
