#!/usr/bin/env python3
"""Prepare a self-contained semantic-review case, without gold annotations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ANNOTATIONS = "experiments/evaluation/semantic-review-cases/annotations.json"
RUBRIC = ["AR-01", "AR-02", "AR-03", "SOLID-S", "SOLID-D", "KISS", "YAGNI", "SPEC-TRACE"]
SOURCES = [
    ("constraint", "docs/engineering/policy.md"),
    ("constraint", "docs/engineering/architecture-contract.json"),
    ("specification", "docs/scenario/owner-problem-brief.md"),
]
EXTRA = [
    "docs/engineering/semantic-review-prompt.md",
    "docs/engineering/semantic-review-rubric.md",
    "docs/engineering/semantic-review.md",
]


def read_source(root: Path, relative: str) -> bytes:
    file = (root / relative).resolve()
    if not file.is_relative_to(root.resolve()) or not file.is_file():
        raise ValueError("invalid/outside source: " + relative)
    return file.read_bytes()


def export_case(root: Path, case_id: str, output: Path) -> dict:
    labels = json.loads(read_source(root, ANNOTATIONS))
    if labels.get("schema") != "semantic-review-cases/v1":
        raise ValueError("unsupported annotations schema")
    matches = [case for case in labels["cases"] if case.get("id") == case_id]
    if len(matches) != 1:
        raise ValueError("unknown or duplicated case ID")
    inputs = [("candidate", matches[0]["candidate"]), *SOURCES]
    files, sources = {}, []
    for role, path in inputs:
        payload = read_source(root, path)
        files[path] = payload
        sources.append({"id": f"{role}-{len(sources) + 1}", "role": role,
                        "path": path, "sha256": hashlib.sha256(payload).hexdigest()})
    for path in EXTRA:
        files[path] = read_source(root, path)
    request = {"schema": "semantic-review-request/v1", "subject": case_id,
               "required_rules": RUBRIC, "sources": sources}
    request_bytes = (json.dumps(request, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    files["request.json"] = request_bytes
    files["README.txt"] = (
        "Evaluate only the candidate against supplied requirements and constraints.\n"
        "Read docs/engineering/semantic-review-prompt.md and return report.json.\n"
        "This archive deliberately excludes gold labels and annotations.\n"
    ).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w") as archive:
        for path in sorted(files):
            info = ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, files[path])
    return {"case": case_id, "archive": str(output), "sources": len(sources),
            "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
            "gold_labels_included": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(export_case(args.repo_root.resolve(), args.case_id, args.output),
                         ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("export error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
