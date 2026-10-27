# Architecture guard — first executable regression

Status: proposed in tooling PR; **not a replacement for semantic design review**.

The historical Checker candidate in [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27) was generated from RPG skeleton `experiments/runs/checker-v1/rpg-context-1/skeleton.json` with an invalid file placement: `src/acl_checker/domain/application/check.py`. Its function `check()` imported `src.acl_checker.application.types`, reversing the declared inward dependency. Existing independent structural tests did not reject the location.

`tools/check_architecture.py` provides two independently selectable checks:

```sh
python3 tools/check_architecture.py --skeleton tests/fixtures/architecture/legacy-cmind-skeleton.json
# expected: FAIL (regression; exit 1)
python3 tools/check_architecture.py --source-root src/acl_checker --json
# only when a real Checker source package is present
python3 -m unittest discover -s tests -p test_architecture_policy.py -v
```

- Pre-codegen: validate all known skeleton file placements; **do not** start expensive interface/codegen stages if the architecture fails.
- Post-codegen: parse Python imports and role placement; detect prohibited inward-layer imports and direct module cycles.
- The regression fixture is a minimal path witness, linked to the immutable historical RPG, not a fake full-run artifact.
- This is Checker-specific and deliberately small: `domain`, `application` and outer adapters, plus ownership of `check()` and `matches()`. Extend only when a real supported consumer requires it.
- SOLID, KISS and YAGNI remain review obligations; the guard cannot infer whether a class is justified from file structure.
- These tests need only Python stdlib, run in GitHub Actions with no model calls. Real CoderMind integration/run and live model usage are not claimed.

Next implementation: invoke the guard at an actual CoderMind pause point, then prove a rejected plan is repaired and regenerated without violating frozen contracts.
