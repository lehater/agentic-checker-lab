# Archived full RPG — actual pre-codegen gate evidence

The fixture at tests/fixtures/architecture/checker-v1-archived-skeleton.json is the original, **byte-identical** 2026 Checker RPG skeleton from [unmerged PR #27](https://github.com/lehater/agentic-checker-lab/blob/c7f794099e925a31c381aef53ff2927ae28f09aa/experiments/runs/checker-v1/rpg-context-1/skeleton.json). Its Git blob SHA is a6201115f9597f809aed60a83483bcb713e6acbc. The original contains the incorrect nested domain/application/check.py and an accompanying nested __init__.py.

The standard deterministic architecture tool reads the **complete** archived skeleton, evaluating its 14 files under the declared src/acl_checker package. The other seven files (tests, entrypoints and scaffolding) are outside the Checker package contract and are not reported as architecture-validated. A test then performs a controlled path correction, placing the actual use-case file under application and removing the redundant nested directory. The corrected skeleton passes the declared structural checks. This is a regression comparison for AR-01..03, not new CoderMind reasoning or product correctness.

Run:

    python3 tools/check_architecture.py --skeleton tests/fixtures/architecture/checker-v1-archived-skeleton.json --json
    # expected FAIL, exit 1

    python3 -m unittest discover -s tests -p test_archived_rpg_gate.py -v
    # expected test PASS, demonstrating correct blocking and positive control

**Still not integrated:** the live CoderMind process is not suspended at a genuine skeleton checkpoint and cannot be claimed blocked before expensive interface design. This fixture makes its proposed gate objectively testable in GitHub CI, using the exact prior failure rather than just a manually simplified path.
