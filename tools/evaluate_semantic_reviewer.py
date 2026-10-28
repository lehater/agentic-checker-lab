#!/usr/bin/env python3
"""Score submitted semantic reviews; reject invalid/incomplete protocol evidence.

Reference labels are PROPOSED, not independently adjudicated. This script does
not call a model, cannot verify semantic truth, and does not infer missing runs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from check_semantic_review import validate_report

LABELS = Path("experiments/evaluation/semantic-review-cases/annotations.json")


def ratio(a: int, b: int) -> float | None:
    return round(a / b, 4) if b else None


def score(root: Path, reports: Path, labels_path: Path) -> dict:
    annotations = json.loads(labels_path.read_text(encoding="utf-8"))
    if annotations.get("schema") != "semantic-review-cases/v1":
        raise ValueError("invalid case annotations schema")
    cases = annotations.get("cases", [])
    if not cases:
        raise ValueError("no annotated cases")
    matrix = {name: 0 for name in [
        "true_block", "false_block", "true_pass", "false_pass",
        "abstain_on_violation", "abstain_on_valid",
        "correct_uncertainty", "missed_uncertainty"
    ]}
    results, seen = [], set()
    for case in cases:
        cid, expected = case.get("id"), case.get("expected")
        if (not isinstance(cid, str) or not cid or cid in seen or "/" in cid or
                "\\" in cid or cid in {".", ".."}):
            raise ValueError("invalid/duplicate case ID")
        seen.add(cid)
        if (not isinstance(expected, dict) or not expected or
                any(v not in {"pass", "fail", "uncertain"} for v in expected.values())):
            raise ValueError("invalid labels for " + cid)
        folder = reports / cid
        request_file, report_file = folder / "request.json", folder / "report.json"
        entry = {"case_id": cid, "status": "MISSING"}
        if request_file.is_file() and report_file.is_file():
            try:
                request = json.loads(request_file.read_text(encoding="utf-8"))
                candidates = [s.get("path") for s in request.get("sources", [])
                              if s.get("role") == "candidate"]
                if request.get("subject") != cid or candidates != [case.get("candidate")]:
                    raise ValueError("case and candidate mismatch")
                raw_report = json.loads(report_file.read_text(encoding="utf-8"))
                verdict = validate_report(root, request_file, raw_report)
                got = {item["rule_id"]: item["assessment"] for item in raw_report["coverage"]}
                if not set(expected).issubset(got):
                    raise ValueError("annotated rule missing from report")
                delta = {name: 0 for name in matrix}
                for rule, truth in expected.items():
                    observation = got[rule]
                    if truth == "fail":
                        key = {"fail": "true_block", "pass": "false_pass",
                               "uncertain": "abstain_on_violation"}[observation]
                    elif truth == "pass":
                        key = {"fail": "false_block", "pass": "true_pass",
                               "uncertain": "abstain_on_valid"}[observation]
                    else:
                        key = ("correct_uncertainty" if observation == "uncertain"
                               else "missed_uncertainty")
                    delta[key] += 1
                for k in matrix:
                    matrix[k] += delta[k]
                entry = {"case_id": cid, "status": "SCORED",
                         "annotations_scored": len(expected),
                         "review_gate": verdict["decision"]}
            except (ValueError, OSError, TypeError, KeyError) as exc:
                entry = {"case_id": cid, "status": "INVALID", "reason": str(exc)}
        elif request_file.is_file() or report_file.is_file():
            entry = {"case_id": cid, "status": "INCOMPLETE_FILES"}
        results.append(entry)
    completed = sum(c["status"] == "SCORED" for c in results)
    tp, fp, tn, fn = (matrix[k] for k in ("true_block", "false_block", "true_pass", "false_pass"))
    return {
        "schema": "semantic-review-evaluation/v1",
        "status": "PROVISIONAL_COMPLETE" if completed == len(results) else "INCOMPLETE",
        "ground_truth_status": annotations.get("status", "UNVERIFIED"),
        "cases_total": len(results), "cases_scored": completed, "cases": results,
        "confusion": matrix,
        "metrics": {
            "block_precision": ratio(tp, tp + fp),
            "block_recall_including_abstentions": ratio(tp, tp + fn + matrix["abstain_on_violation"]),
            "block_recall_excluding_abstentions": ratio(tp, tp + fn),
            "false_block_rate_excluding_abstentions": ratio(fp, fp + tn),
            "case_coverage": ratio(completed, len(results)),
        },
        "limitations": [
            "Labels are PROPOSED, not independently adjudicated.",
            "A visible repo annotation is not a genuinely hidden evaluation set.",
            "Only explicitly labeled rules are scored. Missing cases are not invented.",
            "This measures submitted judgments, not actual LLM quality without genuine model runs."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--reports-dir", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, default=LABELS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        result = score(args.repo_root.resolve(), args.reports_dir, args.annotations)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(encoded, encoding="utf-8")
        else:
            print(encoded, end="")
        return 1 if args.require_complete and result["status"] != "PROVISIONAL_COMPLETE" else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
