#!/usr/bin/env python3
"""Validate explicit, UNREVIEWED decision-to-candidate-requirement-to-CHK trace.

This verifies referential integrity and visibility of gaps only. It cannot
establish semantic equivalence, owner acceptance, or executed test results.
"""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs/discovery/checker/decision-trace.json"
LEDGER = ROOT / "docs/discovery/checker/ledger.json"
CATALOG = ROOT / "docs/evaluation/checker-acceptance-catalog.json"

KINDS = {"CONFLICT", "MISSING_COVERAGE", "UNRESOLVED_CONTRACT", "REVIEW_REQUIRED"}


def verify_trace(trace, ledger, catalog, spec_text):
    errors = []
    if not isinstance(trace, dict):
        return {"status": "INVALID", "errors": ["trace must be an object"]}
    if trace.get("schema") != "checker-decision-trace/v1":
        errors.append("unsupported trace schema")
    if trace.get("status") != "PROPOSED_UNREVIEWED":
        errors.append("trace must not claim owner acceptance")
    if trace.get("semantic_review") != "NOT_PERFORMED":
        errors.append("trace must not claim independent semantic review")
    if catalog.get("status") != "PROPOSED_NOT_OWNER_ACCEPTED":
        errors.append("candidate catalog status is not proposed")
    accepted = {
        item.get("id") for item in ledger.get("decisions", [])
        if isinstance(item, dict) and item.get("status") == "ACCEPTED"
    }
    cases = {
        case.get("id"): case for case in catalog.get("cases", [])
        if isinstance(case, dict)
    }
    pairs = set()
    current_requirement = None
    for line in spec_text.splitlines():
        if line.startswith("### Requirement: "):
            current_requirement = line[len("### Requirement: "):]
        elif line.startswith("#### Scenario: ") and current_requirement:
            pairs.add((current_requirement, line[len("#### Scenario: "):]))
    entries = trace.get("entries")
    if not isinstance(entries, list):
        entries = []
        errors.append("entries must be list")
    found = set()
    gap_count = 0
    link_count = 0
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("trace entry must be object")
            continue
        ident = entry.get("decision_id")
        if not isinstance(ident, str) or not re.fullmatch(r"D-[0-9]{3,}", ident):
            errors.append("invalid trace decision ID " + str(ident))
            continue
        if ident in found:
            errors.append("duplicate trace decision " + ident)
        found.add(ident)
        if ident not in accepted:
            errors.append("trace includes non-accepted decision " + ident)
        links, gaps = entry.get("links"), entry.get("gaps")
        if not isinstance(links, list) or not isinstance(gaps, list):
            errors.append(ident + ": links and gaps must be lists")
            continue
        if not links and not gaps:
            errors.append(ident + ": decision has neither links nor declared gaps")
        if len(links) != len({(x.get("requirement"), x.get("case_id"))
                              for x in links if isinstance(x, dict)}):
            errors.append(ident + ": duplicate candidate link")
        for link in links:
            if not isinstance(link, dict):
                errors.append(ident + ": link must be object")
                continue
            link_count += 1
            requirement, case_id = link.get("requirement"), link.get("case_id")
            case = cases.get(case_id)
            if case is None:
                errors.append(ident + ": unknown CHK case " + str(case_id))
            elif case.get("requirement") != requirement:
                errors.append(ident + ": CHK case does not belong to requirement " + str(requirement))
            elif (requirement, case.get("scenario")) not in pairs:
                errors.append(ident + ": CHK case scenario missing from candidate spec")
        for gap in gaps:
            gap_count += 1
            if (not isinstance(gap, dict) or gap.get("kind") not in KINDS
                    or not isinstance(gap.get("description"), str)
                    or len(gap["description"].strip()) < 25
                    or not isinstance(gap.get("next_action"), str)
                    or len(gap["next_action"].strip()) < 20):
                errors.append(ident + ": invalid or unactionable gap")
    for missing in sorted(accepted - found):
        errors.append("missing decision trace " + missing)
    return {
        "status": "INVALID" if errors else "VALID_WITH_OPEN_GAPS" if gap_count else "VALID_UNREVIEWED",
        "accepted_decisions": len(accepted),
        "traced_decisions": len(found & accepted),
        "candidate_links": link_count,
        "declared_gaps": gap_count,
        "semantics_verified": False,
        "owner_accepted_spec": False,
        "implementation_executed": False,
        "errors": errors,
    }


def main():
    try:
        trace = json.loads(TRACE.read_text(encoding="utf-8"))
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        result = verify_trace(
            trace, ledger, catalog, (ROOT / catalog["spec"]).read_text(encoding="utf-8")
        )
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result = {"status": "INVALID", "errors": [str(exc)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["status"] == "INVALID" else 0


if __name__ == "__main__":
    sys.exit(main())
