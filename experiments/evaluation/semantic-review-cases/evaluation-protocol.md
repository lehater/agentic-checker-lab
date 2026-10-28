# Offline semantic reviewer benchmark

This is a label-free input exporter plus an offline scoring program, **not** an LLM runner.

## Export a case without labels

From the repository root, execute:

    python3 tools/export_semantic_case.py --case-id role-drift --output /tmp/role-drift.zip

The ZIP contains only the selected candidate, owner brief, policy, architecture contract, reviewer prompt/rubric, and a source-hashed request.json. It **excludes** annotations and other candidate files. The same case exports byte-identically.

**Important:** the archive is not a true holdout if the reviewing model can browse the original repository, which contains the proposed labels.

## Evaluate independently obtained outputs

A reviewer gets only an extracted case archive and returns report.json in the semantic-review-report/v1 schema. Keep its original request.json unchanged in a folder:

    /tmp/reviews/role-drift/request.json
    /tmp/reviews/role-drift/report.json

Then run:

    python3 tools/evaluate_semantic_reviewer.py --reports-dir /tmp/reviews --require-complete

The scorer first checks the real request source SHA-256 against this repository, the exact case ID and candidate path, and the complete semantic-review protocol. Only explicitly annotated rules are evaluated. Invalid, partial or missing submissions do not contribute to the confusion matrix; optional --require-complete causes exit 1 until every case is valid.

Metrics show: true/false blockers, true/false passes, abstentions, precision, recall (with/without abstentions), false-block rate, and evaluated case coverage. Undefined denominators produce null, never a fabricated 100%.

## Acceptance restrictions

The existing annotations are still **PROPOSED**, not independently reviewed, and must not be called ground truth yet. An independent adjudicator must verify positive, negative and uncertain labels before any valid method comparison. Only actual model outputs with pinned model versions, bounded call budgets and usage traces can establish performance. Synthetic test reports demonstrate software plumbing, not semantic AI quality.

The evaluator must never revise the annotations to agree with observed model outputs. Tune prompt and use a separate unseen set for final evaluation; do not use the same public six cases as a true blind benchmark.
