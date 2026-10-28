# Candidate Checker requirements trace and independent acceptance ideas

Five requirements and ten WHEN/THEN scenarios are defined in the proposed OpenSpec Checker baseline. The [acceptance catalog](checker-acceptance-catalog.json) links every scenario to a concrete, independently authored scenario description with expected behavior.

Each case has a stable CHK-NNN identifier, the exact requirement and scenario heading, and nontrivial given/expected descriptions. CI checks complete traceability and the Git blob hash of the spec. A changed requirement or missing test idea fails until explicitly reconciled.

Run:
    python3 tools/check_requirements_trace.py
    python3 -m unittest discover -s tests -p test_requirements_trace.py -v

IMPORTANT: Catalog status is PROPOSED_NOT_OWNER_ACCEPTED; every case is NOT_RUN. CI PASS only proves traceability/completeness, not correctness of expected results, implementation or accepted requirements.

Before a real A/B experiment the local executor and owner must approve the predicate/CLI subset, convert these ideas to black-box executable tests with frozen expected outcomes, and run the same independent oracle against direct Codex and Codex+CoderMind candidates. Never rewrite an expected result to match generated output.
