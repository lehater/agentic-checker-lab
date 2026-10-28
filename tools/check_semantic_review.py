#!/usr/bin/env python3
"""Offline semantic-review protocol verifier. No inference and no semantic approval."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

IDENTIFIER = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.:-]*$")
DIGEST = re.compile(r"^[a-f0-9]{64}$")
ASSESS = {"pass", "fail", "uncertain"}
SEVERITY = {"BLOCKER", "WARNING", "INFO"}


class InvalidReview(ValueError):
    pass


def check(condition, message):
    if not condition:
        raise InvalidReview(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def source_path(root, value):
    check(isinstance(value, str) and bool(value.strip()), "source path required")
    rel = Path(value)
    check(not rel.is_absolute() and ".." not in rel.parts, "source path must be relative and not escape root")
    absolute = (root / rel).resolve()
    check(absolute.is_relative_to(root.resolve()) and absolute.is_file(), "source missing or outside repository")
    return absolute


def validate_request(root, request):
    check(request.get("schema") == "semantic-review-request/v1", "invalid request schema")
    check(isinstance(request.get("subject"), str) and request["subject"].strip(), "subject required")
    sources = request.get("sources")
    check(isinstance(sources, list) and len(sources) >= 2, "at least two source documents required")
    index, roles = {}, {}
    for source in sources:
        check(isinstance(source, dict), "invalid source")
        sid, role, digest = source.get("id"), source.get("role"), source.get("sha256")
        check(isinstance(sid, str) and bool(IDENTIFIER.fullmatch(sid)) and sid not in index,
              "invalid/duplicate source id")
        check(role in {"candidate", "constraint", "specification"}, "invalid source role")
        check(isinstance(digest, str) and bool(DIGEST.fullmatch(digest)), "source sha256 required")
        contents = source_path(root, source.get("path")).read_bytes()
        check(sha256(contents) == digest, f"stale or modified source {sid}")
        index[sid] = contents.decode("utf-8").splitlines()
        roles[sid] = role
    check("candidate" in roles.values() and bool(set(roles.values()) & {"constraint", "specification"}),
          "candidate and accepted rules/spec source required")
    rules = request.get("required_rules")
    check(isinstance(rules, list) and len(rules) > 0 and
          all(isinstance(x, str) and IDENTIFIER.fullmatch(x) for x in rules) and
          len(rules) == len(set(rules)), "required_rules must be nonempty unique IDs")
    return index, rules, roles


def citations_valid(citations, index, roles, where):
    check(isinstance(citations, list) and bool(citations), f"{where}: citations required")
    for c in citations:
        check(isinstance(c, dict), f"{where}: invalid citation")
        sid, start, end, quote = c.get("source_id"), c.get("start_line"), c.get("end_line"), c.get("quote")
        check(sid in index, f"{where}: unknown source id")
        check(type(start) is int and type(end) is int and 1 <= start <= end <= len(index[sid])
              and end - start < 12, f"{where}: invalid citation range")
        excerpt = "\n".join(index[sid][start-1:end])
        check(isinstance(quote, str) and bool(quote.strip()) and quote in excerpt,
              f"{where}: quote not present at cited source lines")
    cited_roles = {roles[c["source_id"]] for c in citations}
    check("candidate" in cited_roles and bool(cited_roles & {"constraint", "specification"}),
          f"{where}: require both candidate and requirement/design source evidence")


def validate_report(root, request_file, report):
    raw = request_file.read_bytes()
    request = json.loads(raw)
    check(isinstance(request, dict), "request must be an object")
    index, rules, roles = validate_request(root, request)
    check(report.get("schema") == "semantic-review-report/v1", "invalid report schema")
    check(report.get("request_sha256") == sha256(raw), "stale request hash")
    reviewer = report.get("reviewer")
    check(isinstance(reviewer, dict) and reviewer.get("kind") in {"model", "human", "fixture"} and
          isinstance(reviewer.get("identifier"), str) and reviewer["identifier"].strip(),
          "reviewer provenance missing")
    coverage = report.get("coverage")
    check(isinstance(coverage, list), "coverage missing")
    found = {}
    for item in coverage:
        check(isinstance(item, dict), "invalid coverage item")
        rid = item.get("rule_id")
        check(rid in rules and rid not in found, f"unknown or repeated coverage: {rid}")
        check(item.get("assessment") in ASSESS, f"{rid}: unknown assessment")
        check(isinstance(item.get("rationale"), str) and item["rationale"].strip(),
              f"{rid}: rationale required")
        citations_valid(item.get("citations"), index, roles, f"coverage {rid}")
        found[rid] = item
    check(set(found) == set(rules), "missing coverage: " + ",".join(sorted(set(rules)-set(found))))
    findings = report.get("findings")
    check(isinstance(findings, list), "findings missing")
    seen, failed = set(), set()
    blocker = False
    for finding in findings:
        check(isinstance(finding, dict), "invalid finding")
        fid, rid = finding.get("id"), finding.get("rule_id")
        check(isinstance(fid, str) and bool(IDENTIFIER.fullmatch(fid)) and fid not in seen,
              "invalid or duplicated finding ID")
        seen.add(fid)
        check(rid in found, "finding references unknown rule")
        check(finding.get("severity") in SEVERITY, "finding severity invalid")
        check(found[rid]["assessment"] != "pass", "finding contradicts PASS assessment")
        for key in ("claim", "reasoning", "minimal_fix"):
            check(isinstance(finding.get(key), str) and finding[key].strip(), f"finding {key} required")
        citations_valid(finding.get("citations"), index, roles, f"finding {fid}")
        if finding["severity"] == "BLOCKER":
            blocker = True
        failed.add(rid)
    check(not ({rid for rid in found if found[rid]["assessment"] == "fail"} - failed),
          "FAIL assessment without finding")
    if blocker or any(v["assessment"] == "fail" for v in found.values()):
        decision = "BLOCK"
    elif any(v["assessment"] == "uncertain" for v in found.values()):
        decision = "ESCALATE"
    else:
        decision = "HUMAN_REVIEW_REQUIRED"
    return {"protocol_status": "VALID", "decision": decision,
            "semantic_truth_verified": False, "rule_count": len(rules),
            "finding_count": len(findings),
            "note": "Exact source grounding and coverage verified, not semantic correctness."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--request", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    args = p.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        check(isinstance(report, dict), "report must be an object")
        result = validate_report(args.repo_root.resolve(), args.request, report)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(json.dumps({"protocol_status": "INVALID", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
