#!/usr/bin/env python3
"""Create an immutable-input semantic review request from current repository files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--candidate", required=True)
    p.add_argument("--constraint", action="append", required=True)
    p.add_argument("--specification", action="append", default=[])
    p.add_argument("--subject", required=True)
    p.add_argument("--rules", nargs="+", default=[
        "AR-01", "AR-02", "AR-03", "SOLID-S", "SOLID-D", "KISS", "YAGNI", "SPEC-TRACE"
    ])
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    root = args.repo_root.resolve()
    sources = []
    for role, paths in [
        ("candidate", [args.candidate]),
        ("constraint", args.constraint),
        ("specification", args.specification),
    ]:
        for path in paths:
            absolute = (root / path).resolve()
            if not absolute.is_relative_to(root) or not absolute.is_file():
                p.error(f"source must be an existing repository file: {path}")
            sources.append({
                "id": f"{role}-{len(sources) + 1}",
                "role": role,
                "path": absolute.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(absolute.read_bytes()).hexdigest()
            })
    if len(args.rules) != len(set(args.rules)):
        p.error("required rules must be unique")
    result = {"schema": "semantic-review-request/v1", "subject": args.subject,
              "required_rules": args.rules, "sources": sources}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared: {args.output}")


if __name__ == "__main__":
    main()
