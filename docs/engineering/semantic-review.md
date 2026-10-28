# Semantic Engineering Validator (protocol v1)

Status: offline input preparation and report verification **implemented**. Actual model calls, semantic accuracy and CoderMind E2E integration are **NOT VERIFIED**.

The purpose is to evaluate new architecture problems against **requirements**, not a list of historical bugs. See [rubric](semantic-review-rubric.md), [review prompt](semantic-review-prompt.md), [Engineering Policy](policy.md) and [architecture contract](architecture-contract.json).

Workflow: deterministic architecture guard first; if it fails, **block before model calls**. Otherwise prepare a bounded, SHA-256 pinned source bundle, ask one external/human reviewer to evaluate the required rules, mechanically validate citations/coverage and independently adjudicate the conclusions. No models are used by CI.

## Prepare request

```sh
python3 tools/prepare_semantic_review.py \
  --candidate tests/fixtures/semantic-review/historical-rpg-excerpt.json \
  --constraint docs/engineering/policy.md \
  --constraint docs/engineering/architecture-contract.json \
  --specification openspec/changes/checker-v1-baseline/design.md \
  --subject checker-v1-plan --output /tmp/review-request.json
```

The reviewer receives the request and the exact source documents. The response JSON is saved separately:

```sh
python3 tools/check_semantic_review.py --request /tmp/review-request.json \
  --report /tmp/review-response.json --repo-root .
```

## Contract and safety

Request fields: schema=semantic-review-request/v1, subject, required_rules, sources containing id/role/path/sha256. Report: schema=semantic-review-report/v1, request_sha256, reviewer {kind, identifier}, coverage (one item per rule: rule_id, assessment, rationale, citations), findings (id, rule_id, severity, claim, reasoning, minimal_fix, citations).

Each citation points to a provided source_id and exact text from 1-based inclusive start_line/end_line (up to 12 lines). Missing citations, source digest mismatch, incomplete coverage, inconsistent FAIL/PASS states and invalid paths **invalidate** the report.

A structurally verified response never says that the semantic claims are true. Results: BLOCK (violations), ESCALATE (insufficient evidence), or HUMAN_REVIEW_REQUIRED (no reported violations). The model cannot approve or merge.

A handwritten regression fixture uses the authentic path and feature in historical [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27), but is **not** a model response or evidence of model detection. Meaningful later calibration requires independently judged good/bad design examples with held-out negatives and false-positive measurement.

Generated code/product behavior and semantic architectural compliance require **separate** independent tests. This validator checks reporting provenance, not implementation.
