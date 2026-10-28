#!/usr/bin/env python3
"""Require coverage of each candidate OpenSpec scenario by a proposed acceptance case.

No Checker implementation is tested; neither spec nor cases are owner-accepted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

REQ = re.compile(r"^### Requirement: (.+)$")
SCENARIO = re.compile(r"^#### Scenario: (.+)$")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def scenario_pairs(source: str) -> set[tuple[str, str]]:
    current = None
    found = set()
    for line in source.splitlines():
        if match := REQ.fullmatch(line):
            current = match.group(1)
        elif match := SCENARIO.fullmatch(line):
            if not current:
                raise ValueError("scenario lacks requirement heading")
            pair = current, match.group(1)
            if pair in found:
                raise ValueError("duplicate spec scenario: " + str(pair))
            found.add(pair)
    if not found:
        raise ValueError("spec has no scenarios")
    return found


def check_catalog(repo_root: Path, catalog_path: Path) -> dict:
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != "checker-acceptance-catalog/v1":
        raise ValueError("unsupported catalog schema")
    errors = []
    if data.get("status") != "PROPOSED_NOT_OWNER_ACCEPTED":
        errors.append("catalog cannot claim owner acceptance")
    relative = data.get("spec")
    if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("unsafe spec reference")
    spec = (repo_root / relative).resolve()
    if not spec.is_relative_to(repo_root.resolve()) or not spec.is_file():
        raise ValueError("spec not found inside repo")
    content = spec.read_bytes()
    if git_blob_sha(content) != data.get("spec_git_blob_sha"):
        errors.append("spec Git blob SHA mismatch; reconcile changed requirements")
    expected = scenario_pairs(content.decode("utf-8"))
    source = data.get("source_problem")
    if (not isinstance(source, str) or Path(source).is_absolute() or
            ".." in Path(source).parts or not (repo_root / source).is_file()):
        errors.append("source problem document not found")
    seen_ids, covered = set(), set()
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise ValueError("cases must be list")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("non-object case")
            continue
        ident = case.get("id")
        pair = (case.get("requirement"), case.get("scenario"))
        if (not isinstance(ident, str) or not re.fullmatch(r"CHK-[0-9]{3}", ident)
                or ident in seen_ids):
            errors.append("invalid or duplicate case ID " + str(ident))
        seen_ids.add(ident)
        if pair in covered:
            errors.append("duplicate scenario coverage: " + str(pair))
        covered.add(pair)
        for key in ("given", "expected"):
            if not isinstance(case.get(key), str) or len(case[key].strip()) < 15:
                errors.append(str(ident) + ": substantive " + key + " missing")
        if case.get("execution_status") != "NOT_RUN":
            errors.append(str(ident) + ": unverified runtime result claimed")
    for pair in sorted(expected - covered):
        errors.append("missing scenario coverage: " + " / ".join(pair))
    for pair in sorted(covered - expected, key=str):
        errors.append("unrecognized scenario mapping: " + str(pair))
    return {"status": "FAIL" if errors else "PASS", "spec_scenarios": len(expected),
            "case_count": len(cases), "catalog_accepted": False,
            "implementation_executed": False, "errors": errors}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--catalog", type=Path, default=Path("docs/evaluation/checker-acceptance-catalog.json"))
    args = p.parse_args()
    try:
        result = check_catalog(args.repo_root.resolve(), args.catalog)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "PASS" else 1
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
