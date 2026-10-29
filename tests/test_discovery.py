"""Contract tests for the experimental discovery ledger validator.

Fixtures model protocol states rather than copying today's working ledger.
The live ledger is validated separately by tools/check_discovery.py in make check.
These tests verify structural invariants, not semantic agreement or real consent.
"""
import copy
import tempfile
import unittest
from pathlib import Path

from tools.check_discovery import verify


def seed():
    """An independent, never-started discovery state."""
    return {
        "schema": "checker-discovery-ledger/v1",
        "status": "NOT_STARTED",
        "checkpoint": 0,
        "rounds": [],
        "questions": [],
        "decisions": [],
    }


def question(qid="Q-001", round_id="R-001", depends_on=None):
    return {
        "id": qid,
        "text": "Какой результат требуется оператору?",
        "source": "synthetic/owner-brief",
        "status": "OPEN",
        "created_round": round_id,
        "depends_on": [] if depends_on is None else depends_on,
    }


def prepared():
    """One published question, not answered or approved."""
    data = seed()
    data.update(status="IN_PROGRESS", checkpoint=1)
    data["questions"] = [question()]
    data["rounds"] = [{
        "id": "R-001",
        "status": "PREPARED",
        "question_ids": ["Q-001"],
        "owner_confirmation": None,
    }]
    return data


def approved_answer():
    return {
        "approval": "APPROVED",
        "normalized": "Показывать все найденные строки.",
        "owner_confirmation": "Owner explicitly approved normalized answer.",
    }


def decision(did="D-001", source_questions=None, status="ACCEPTED"):
    return {
        "id": did,
        "text": "Show every matching rule.",
        "source_questions": ["Q-001"] if source_questions is None else source_questions,
        "status": status,
        "owner_confirmation": (
            "Owner explicitly approved decision." if status == "ACCEPTED" else None
        ),
    }


class DiscoveryLedgerTests(unittest.TestCase):
    def setUp(self):
        # A missing round report must remain missing even when the real
        # repository already has a closed R-001 and rounds/001.md.
        sandbox = tempfile.TemporaryDirectory()
        self.addCleanup(sandbox.cleanup)
        self.root = Path(sandbox.name)

    def report(self, number="001"):
        target = self.root / "docs/discovery/checker/rounds" / f"{number}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Confirmed synthetic round\n", encoding="utf-8")
        return target

    def closed(self):
        data = prepared()
        data["rounds"][0].update(
            status="CLOSED",
            owner_confirmation="Owner explicitly approved round.",
        )
        data["questions"][0].update(status="ANSWERED", answer=approved_answer())
        self.report()
        return data

    def next_frontier(self):
        data = self.closed()
        data["checkpoint"] = 3
        data["rounds"].append({
            "id": "R-002",
            "status": "PREPARED",
            "question_ids": ["Q-002"],
            "owner_confirmation": None,
        })
        data["questions"].append(question("Q-002", "R-002", ["Q-001"]))
        return data

    def assert_valid(self, data):
        self.assertEqual(verify(data, root=self.root), [])

    def assert_rejected(self, data, expected):
        errors = verify(data, root=self.root)
        self.assertTrue(
            any(expected in error for error in errors),
            f"Expected rejection for {expected!r}, got: {errors}",
        )

    def test_independent_initial_state_is_valid(self):
        self.assert_valid(seed())

    def test_not_started_forbids_ledger_entries(self):
        data = seed()
        data["questions"].append(question())
        self.assert_rejected(data, "NOT_STARTED ledger must be empty")

    def test_prepared_frontier_is_valid_without_owner_approval(self):
        self.assert_valid(prepared())

    def test_closed_round_with_approved_answer_and_report_is_valid(self):
        self.assert_valid(self.closed())

    def test_next_round_can_depend_on_an_approved_previous_answer(self):
        self.assert_valid(self.next_frontier())

    def test_only_one_round_may_be_prepared(self):
        data = prepared()
        data["rounds"].append({
            "id": "R-002",
            "status": "PREPARED",
            "question_ids": ["Q-002"],
            "owner_confirmation": None,
        })
        data["questions"].append(question("Q-002", "R-002"))
        self.assert_rejected(data, "At most one round can be PREPARED")

    def test_prepared_round_must_be_last(self):
        data = prepared()
        data["rounds"].append({
            "id": "R-002",
            "status": "CLOSED",
            "question_ids": ["Q-002"],
            "owner_confirmation": "Owner approved second round.",
        })
        data["questions"].append(question("Q-002", "R-002"))
        self.report("002")
        self.assert_rejected(data, "Only the final round may be PREPARED")

    def test_prepared_round_cannot_claim_owner_confirmation(self):
        data = prepared()
        data["rounds"][0]["owner_confirmation"] = "Premature approval"
        self.assert_rejected(data, "PREPARED cannot have owner_confirmation")

    def test_prepared_questions_must_remain_open(self):
        data = prepared()
        data["questions"][0].update(status="DEFERRED", reason="Later")
        self.assert_rejected(data, "prepared question must be OPEN")

    def test_prepared_question_requires_answered_prerequisites(self):
        data = self.next_frontier()
        data["rounds"][-1]["question_ids"].append("Q-003")
        data["questions"].append(question("Q-003", "R-002", ["Q-002"]))
        self.assert_rejected(data, "depends on unanswered Q-002")

    def test_question_ids_are_unique_and_sequential(self):
        data = prepared()
        data["questions"].append(copy.deepcopy(data["questions"][0]))
        self.assert_rejected(data, "Duplicate ID Q-001")
        data = prepared()
        data["questions"][0]["id"] = "Q-002"
        self.assert_rejected(data, "Question IDs must be sequential")

    def test_question_prerequisites_must_exist(self):
        data = prepared()
        data["questions"][0]["depends_on"] = ["Q-999"]
        self.assert_rejected(data, "invalid prerequisite Q-999")

    def test_question_must_belong_to_its_round(self):
        data = prepared()
        data["questions"].append(question("Q-002", "R-001"))
        self.assert_rejected(data, "Q-002: not listed in its round")

    def test_answer_requires_normalization_and_owner_approval(self):
        data = self.closed()
        data["questions"][0]["answer"]["approval"] = "PROPOSED"
        self.assert_rejected(data, "ANSWERED needs normalized owner-approved answer")
        data = self.closed()
        data["questions"][0]["answer"]["owner_confirmation"] = ""
        self.assert_rejected(data, "ANSWERED needs normalized owner-approved answer")
        data = self.closed()
        data["questions"][0]["answer"]["normalized"] = ""
        self.assert_rejected(data, "ANSWERED needs normalized owner-approved answer")

    def test_open_question_cannot_carry_approved_answer(self):
        data = prepared()
        data["questions"][0]["answer"] = approved_answer()
        self.assert_rejected(data, "approved answer must be ANSWERED")

    def test_closed_round_requires_explicit_confirmation(self):
        data = self.closed()
        data["rounds"][0]["owner_confirmation"] = None
        self.assert_rejected(data, "CLOSED requires explicit owner_confirmation")

    def test_closed_round_requires_a_report_in_its_own_root(self):
        data = self.closed()
        self.assert_valid(data)
        (self.root / "docs/discovery/checker/rounds/001.md").unlink()
        self.assert_rejected(data, "closed round report missing")

    def test_closed_round_may_retain_unresolved_question(self):
        data = self.closed()
        data["questions"][0].update(status="OPEN", answer=None)
        # Partial approval does not silently convert an open question to ANSWERED.
        self.assert_valid(data)

    def test_accepted_decision_must_reference_approved_answer(self):
        data = prepared()
        data["decisions"].append(decision())
        self.assert_rejected(data, "accepted decision cites unapproved answer Q-001")

    def test_accepted_decision_requires_confirmation_and_valid_sources(self):
        data = self.closed()
        data["decisions"].append(decision())
        self.assert_valid(data)
        data["decisions"][0]["owner_confirmation"] = None
        self.assert_rejected(data, "ACCEPTED needs owner confirmation")
        data = self.closed()
        data["decisions"].append(decision(source_questions=["Q-999"]))
        self.assert_rejected(data, "unknown source question Q-999")

    def test_superseded_question_requires_successor_and_reason(self):
        data = self.next_frontier()
        old = data["questions"][0]
        old.update(status="SUPERSEDED", answer=None)
        self.assert_rejected(data, "SUPERSEDED needs successor Q IDs")
        self.assert_rejected(data, "needs a reason")
        old.update(superseded_by=["Q-002"], reason="Owner clarified the meaning.")
        # A later prepared Q can replace an earlier closed-round Q.
        self.assert_valid(data)

    def test_cancelled_question_requires_explanation(self):
        data = self.closed()
        data["questions"][0].update(status="CANCELLED", answer=None)
        self.assert_rejected(data, "needs a reason")
        data["questions"][0]["reason"] = "Out of scope."
        self.assert_valid(data)

    def test_superseded_decision_requires_replacement(self):
        data = self.closed()
        data["decisions"] = [
            decision("D-001", status="SUPERSEDED"),
            decision("D-002"),
        ]
        self.assert_rejected(data, "superseded decision requires replacement")
        data["decisions"][0]["superseded_by"] = "D-002"
        self.assert_valid(data)

    def test_ready_for_spec_rejects_open_or_prepared_items(self):
        data = prepared()
        data["status"] = "READY_FOR_SPEC"
        self.assert_rejected(data, "Cannot be READY_FOR_SPEC")


if __name__ == "__main__":
    unittest.main()
