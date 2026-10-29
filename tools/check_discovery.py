#!/usr/bin/env python3
"""Offline structural guard for experimental Checker discovery ledger.

This cannot verify the owner's actual consent or semantic equivalence.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "docs/discovery/checker/ledger.json"
Q_STATES = {"OPEN", "ANSWERED", "SUPERSEDED", "CANCELLED", "DEFERRED"}
D_STATES = {"PROPOSED", "ACCEPTED", "SUPERSEDED", "REJECTED"}
R_STATES = {"PREPARED", "CLOSED"}


def verify(data, root=ROOT):
    errors = []

    def fail(msg):
        errors.append(msg)

    if not isinstance(data, dict):
        return ["Ledger must be an object"]
    if data.get("schema") != "checker-discovery-ledger/v1":
        fail("Incorrect schema")
    if data.get("status") not in {"NOT_STARTED", "IN_PROGRESS", "INCOMPLETE", "BLOCKED", "READY_FOR_SPEC"}:
        fail("Invalid discovery status")
    if type(data.get("checkpoint")) is not int or data["checkpoint"] < 0:
        fail("checkpoint must be a nonnegative integer")
    for field in ("rounds", "questions", "decisions"):
        if not isinstance(data.get(field), list):
            fail(field + " must be a list")
    if errors:
        return errors

    rounds = data["rounds"]
    questions = data["questions"]
    decisions = data["decisions"]

    def index(items, prefix):
        found = {}
        for item in items:
            if not isinstance(item, dict):
                fail(prefix + " entry must be an object")
                continue
            ident = item.get("id")
            if not isinstance(ident, str) or not re.fullmatch(prefix + r"-[0-9]{3,}", ident):
                fail("Invalid " + prefix + " id: " + repr(ident))
                continue
            if ident in found:
                fail("Duplicate ID " + ident)
            found[ident] = item
        return found

    rr, qq, dd = index(rounds, "R"), index(questions, "Q"), index(decisions, "D")
    prepared = [r for r in rounds if isinstance(r, dict) and r.get("status") == "PREPARED"]
    if len(prepared) > 1:
        fail("At most one round can be PREPARED")
    if prepared and rounds[-1] is not prepared[0]:
        fail("Only the final round may be PREPARED")
    if any(int(rid.split("-")[1]) != i + 1 for i, rid in enumerate(rr)):
        fail("Round IDs must be sequential")
    if any(int(qid.split("-")[1]) != i + 1 for i, qid in enumerate(qq)):
        fail("Question IDs must be sequential")
    if data["status"] == "NOT_STARTED" and (rounds or questions or decisions or data["checkpoint"]):
        fail("NOT_STARTED ledger must be empty with checkpoint zero")
    if data["status"] != "NOT_STARTED" and not rounds:
        fail("Active discovery needs a round")
    if data["status"] == "READY_FOR_SPEC" and (prepared or any(q.get("status") == "OPEN" for q in questions)):
        fail("Cannot be READY_FOR_SPEC with prepared or open questions")

    for r in rounds:
        if not isinstance(r, dict):
            continue
        rid, state = r.get("id"), r.get("status")
        if state not in R_STATES:
            fail(str(rid) + ": invalid round status")
        ids = r.get("question_ids")
        if not isinstance(ids, list) or not ids:
            fail(str(rid) + ": question_ids must be nonempty list")
            continue
        if len(set(map(str, ids))) != len(ids):
            fail(str(rid) + ": duplicate question IDs")
        for qid in ids:
            if qid not in qq:
                fail(str(rid) + ": unknown question " + str(qid))
            elif qq[qid].get("created_round") != rid:
                fail(str(rid) + ": question " + str(qid) + " wrong created_round")
        if state == "CLOSED":
            if not isinstance(r.get("owner_confirmation"), str) or not r["owner_confirmation"].strip():
                fail(str(rid) + ": CLOSED requires explicit owner_confirmation evidence")
            expected = root / "docs/discovery/checker/rounds" / (str(rid).split("-")[-1] + ".md")
            if not expected.is_file():
                fail(str(rid) + ": closed round report missing: " + str(expected))
        if state == "CLOSED" and "decision_ids" in r:
            accepted_ids = r["decision_ids"]
            if not isinstance(accepted_ids, list) or any(
                not isinstance(did, str) or not re.fullmatch(r"D-[0-9]{3,}", did)
                for did in accepted_ids
            ) or len(accepted_ids) != len(set(accepted_ids)):
                fail(str(rid) + ": decision_ids must be unique valid IDs")
            else:
                for did in accepted_ids:
                    if did not in dd:
                        fail(str(rid) + ": unknown accepted decision " + did)
                    elif dd[did].get("status") != "ACCEPTED":
                        fail(str(rid) + ": round references non-accepted decision " + did)
                if expected.is_file():
                    report_text = expected.read_text(encoding="utf-8")
                    section = re.search(
                        r"(?ms)^## Accepted decisions\s*\n(.*?)(?=^## |\Z)",
                        report_text,
                    )
                    reported_ids = re.findall(
                        r"(?m)^\s*[-*]\s+(?:\*\*)?(D-[0-9]+)(?:\*\*)?\s*(?=←|\()",
                        section.group(1) if section else "",
                    )
                    if len(reported_ids) != len(set(reported_ids)) or set(reported_ids) != set(accepted_ids):
                        fail(str(rid) + ": round report decision IDs do not match ledger")
        elif r.get("owner_confirmation"):
            fail(str(rid) + ": PREPARED cannot have owner_confirmation")
    for qid, q in qq.items():
        state = q.get("status")
        if state not in Q_STATES:
            fail(qid + ": invalid question status")
        if not str(q.get("source") or "").strip():
            fail(qid + ": source missing")
        if not isinstance(q.get("text"), str) or not q["text"].strip():
            fail(qid + ": text missing")
        if q.get("created_round") not in rr:
            fail(qid + ": invalid created_round")
        deps = q.get("depends_on", [])
        if not isinstance(deps, list):
            fail(qid + ": depends_on must be list")
            deps = []
        for dep in deps:
            if dep not in qq or dep == qid:
                fail(qid + ": invalid prerequisite " + str(dep))
        if q.get("created_round") in rr and rr[q["created_round"]].get("status") == "PREPARED":
            if state != "OPEN":
                fail(qid + ": prepared question must be OPEN")
            for dep in deps:
                if dep in qq and qq[dep].get("status") != "ANSWERED":
                    fail(qid + ": prepared question depends on unanswered " + str(dep))
        if state == "SUPERSEDED":
            to = q.get("superseded_by", [])
            if not isinstance(to, list) or not to or any(x not in qq or x == qid for x in to):
                fail(qid + ": SUPERSEDED needs successor Q IDs")
        if state in {"SUPERSEDED", "CANCELLED", "DEFERRED"} and not str(q.get("reason") or "").strip():
            fail(qid + ": closed/deferred question needs a reason")
        answer = q.get("answer")
        if state == "ANSWERED":
            if not isinstance(answer, dict) or answer.get("approval") != "APPROVED" or not str(answer.get("normalized") or "").strip() or not str(answer.get("owner_confirmation") or "").strip():
                fail(qid + ": ANSWERED needs normalized owner-approved answer and confirmation")
        if isinstance(answer, dict) and answer.get("approval") == "APPROVED" and state != "ANSWERED":
            fail(qid + ": approved answer must be ANSWERED")
    for did, d in dd.items():
        state = d.get("status")
        if state not in D_STATES:
            fail(did + ": invalid decision status")
        if not isinstance(d.get("text"), str) or not d["text"].strip():
            fail(did + ": decision text missing")
        sources = d.get("source_questions")
        if not isinstance(sources, list) or not sources:
            fail(did + ": source_questions must be nonempty list")
            continue
        for qid in sources:
            if qid not in qq:
                fail(did + ": unknown source question " + str(qid))
            elif state == "ACCEPTED" and qq[qid].get("status") != "ANSWERED":
                fail(did + ": accepted decision cites unapproved answer " + str(qid))
        if state == "ACCEPTED" and not str(d.get("owner_confirmation") or "").strip():
            fail(did + ": ACCEPTED needs owner confirmation")
        if state == "SUPERSEDED" and d.get("superseded_by") not in dd:
            fail(did + ": superseded decision requires replacement D")
    for qid, q in qq.items():
        if q.get("created_round") in rr and qid not in rr[q["created_round"]].get("question_ids", []):
            fail(qid + ": not listed in its round")
    return errors


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = verify(data)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print("DISCOVERY FAIL:", error, file=sys.stderr)
        return 1
    print("DISCOVERY STRUCTURAL CHECK: PASS (not semantic/owner validation)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
