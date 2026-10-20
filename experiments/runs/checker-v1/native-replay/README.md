# Native CoderMind verification snapshot

These files are generated verification/example evidence, not accepted product
requirements and not the independent acceptance oracle. Original relative paths
under `tests/`, `examples/` and `main.py` are preserved. Source identity and exact
file checksums are in `../native-provenance.json`.

`tools/replay_checker_native_tests.py` reconstructs a temporary workspace with
these files and the current repository's `checker/` + `src/`, then runs pytest.
The recorded environment uses Python 3.12 and packages from requirements-dev.lock:

```bash
python3.12 -m venv /tmp/checker-native-qa
/tmp/checker-native-qa/bin/python -m pip install -r experiments/runs/checker-v1/native-replay/requirements-dev.lock
/tmp/checker-native-qa/bin/python tools/replay_checker_native_tests.py
```

This optional development check requires pytest; the product runtime and default
independent gate `make check` use only the standard library. No CoderMind or model
call is needed to replay the exported tests. Two runpy warnings from the generated
entrypoint tests result from repeated module execution in one interpreter; the
independent CLI tests execute fresh processes.
