# Architecture guard — requirement-led validation

**Status: proposed PR #29.** The executable invariant engine is [tools/check_architecture.py](../../tools/check_architecture.py); it loads [architecture-contract.json](architecture-contract.json) and has **no built-in Checker-specific function names**.

## Source of architecture truth

[Engineering Policy](policy.md) establishes AR-01..AR-05. The project architecture contract declares:
- relative package path and import prefix;
- layers and their directory roots (different names can be used by another project);
- permitted dependency directions between layers;
- whether one named layer directory may nest beneath another;
- optional explicit symbol ownership for post-codegen checks;
- optional *exact accepted RPG feature IDs* for pre-codegen responsibility checks.

The existing checker mapping of check() to application and matches() to domain comes from this project's accepted design proposal. It is **data in a reviewable contract**, not a special-case rule in the validator. If those choices change, review the contract alongside the design.

## Checks (from repository root)

Use the fixture for a negative test:
    python3 tools/check_architecture.py --skeleton tests/fixtures/architecture/legacy-cmind-skeleton.json
    # expects exit 1: invalid nested layer and feature ownership

Use a CoderMind skeleton when present:
    python3 tools/check_architecture.py --skeleton /path/to/skeleton.json --json

After codegen, on a real generated source tree:
    python3 tools/check_architecture.py --source-root /path/to/src/acl_checker --json

Test all declared invariants:
    python3 -m unittest discover -s tests -p test_architecture_policy.py -v

The historical fixture is a **minimal exact path/feature witness** from [the unmerged PR #27](https://github.com/lehater/agentic-checker-lab/pull/27), not a new full model-driven run. Test coverage is primarily AR-01..AR-05, including numerous potential failures unknown to the historical run. The nested-path check alone is insufficient to prove use-case ownership; the optional feature responsibility map catches mismatched plan features where their IDs are declared.

## Limits

- Imports can be indirect/dynamic, and AST cannot prove that a function's implementation obeys SOLID/KISS/YAGNI.
- Only imports between declared first-party layers and directly resolvable Python module cycles are checked.
- The checker does not prove OpenSpec has been accepted, that actual CoderMind is blocked at the intended step, or that independent product behavior tests pass.
- Do not weaken rules or rewrite accepted contracts automatically to make failing generated artifacts pass.
