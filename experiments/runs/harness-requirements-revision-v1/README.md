# Checker Product Requirements — active first slice

**Canonical:** `.harness/knowledge/checker-requirements.yaml`, 13 accepted requirements. No inactive requirement records. Git commits contain prior versions.

**Scope:** accepted owner decisions [PDEC-CHECKER-001](../../../docs/scenario/problem-framing-decision.md) and [PDEC-CHECKER-004](../../../docs/scenario/first-slice-product-decision.md); product authority under PDEC-CHECKER-003. The reviewed obligations cover input flow, supplied contexts and snapshots, ACL rule results/order, evidence provenance, uncertainty and verdict limitations. Verification examples/oracle are owned by Verification Design, not Product Requirements.

**Validation:** the pinned Harness Consumer Pack, explicit semantic classifications, schema validation, actual REVISION admission and atomic Project Publication are exercised by `execute.py`; the repository CI checks replay equality of checked-in publication, admission and candidate.

**Open:** `Q-DV-001` accepted Strategic Domain ownership and `Q-DV-002` matching predicates/independent oracle. Both downstream capabilities remain BLOCKED. No accepted domain, architecture, runtime, implementation or complete product coverage is claimed.

Use [current Project Publication](../../../.harness/project-publication.yaml) for live status, not old reports.
