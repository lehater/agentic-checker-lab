#!/usr/bin/env python3
"""Replay exported CoderMind tests against repository source in a temporary tree.

Optional development check: run with a Python environment containing the packages
in experiments/runs/checker-v1/native-replay/requirements-dev.lock.
The independent stdlib acceptance gate remains `make check`.
"""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'experiments/runs/checker-v1/native-replay'


def main():
    with tempfile.TemporaryDirectory(prefix='checker-native-replay-') as directory:
        workspace = Path(directory)
        for name in ['checker', 'src']:
            shutil.copytree(ROOT / name, workspace / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for name in ['tests', 'examples', 'main.py']:
            source = SNAPSHOT / name
            if source.is_dir():
                shutil.copytree(source, workspace / name)
            else:
                shutil.copyfile(source, workspace / name)
        return subprocess.run([sys.executable, '-m', 'pytest', '-q', '--timeout=60'],
                              cwd=workspace).returncode


if __name__ == '__main__':
    raise SystemExit(main())
