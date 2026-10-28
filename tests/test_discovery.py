import copy
import json
import tempfile
import unittest
from pathlib import Path
from tools.check_discovery import verify


class DiscoveryLedgerTests(unittest.TestCase):
    def setUp(self):
        self.seed = json.loads((Path(__file__).resolve().parent.parent / "docs/discovery/checker/ledger.json").read_text(encoding="utf-8"))

    def test_initial_seed_is_valid(self):
        self.assertEqual(verify(self.seed), [])

    def prepared(self):
        data = copy.deepcopy(self.seed)
        data.update(status="IN_PROGRESS", checkpoint=1)
        data["questions"] = [{"id": "Q-001", "text": "Что считать совпадением?", "status": "OPEN", "created_round": "R-001", "depends_on": [], "source": "brief"}]
        data["rounds"] = [{"id": "R-001", "status": "PREPARED", "question_ids": ["Q-001"], "owner_confirmation": None}]
        return data

    def test_prepared_round_is_valid(self):
        self.assertEqual(verify(self.prepared()), [])

    def test_answer_without_approval_fails(self):
        data = self.prepared()
        data["questions"][0].update(status="ANSWERED", answer={"normalized": "Все правила", "approval": "PROPOSED"})
        self.assertTrue(any("ANSWERED needs" in e for e in verify(data)))

    def test_duplicate_and_missing_dependency_fail(self):
        data = self.prepared()
        data["questions"].append(copy.deepcopy(data["questions"][0]))
        data["questions"][0]["depends_on"] = ["Q-999"]
        errors = verify(data)
        self.assertTrue(any("Duplicate ID" in e for e in errors))
        self.assertTrue(any("prerequisite" in e for e in errors))

    def test_superseded_requires_reason_and_replacement(self):
        data = self.prepared()
        data["questions"][0]["status"] = "SUPERSEDED"
        errors = verify(data)
        self.assertTrue(any("successor" in e for e in errors))
        self.assertTrue(any("reason" in e for e in errors))

    def test_closed_requires_owner_confirm_and_round_file(self):
        data = self.prepared()
        data["rounds"][0]["status"] = "CLOSED"
        self.assertTrue(any("owner_confirmation" in e for e in verify(data)))
        data["rounds"][0]["owner_confirmation"] = "owner reviewed normalized meaning"
        self.assertTrue(any("report missing" in e for e in verify(data)))

    def test_decision_cannot_cite_unapproved_question(self):
        data = self.prepared()
        data["decisions"] = [{"id": "D-001", "text": "Show all", "status": "ACCEPTED", "source_questions": ["Q-001"], "owner_confirmation": "owner approved"}]
        self.assertTrue(any("unapproved" in e for e in verify(data)))

    def test_ready_for_spec_rejects_open_items(self):
        data = self.prepared()
        data["status"] = "READY_FOR_SPEC"
        self.assertTrue(any("Cannot be READY_FOR_SPEC" in e for e in verify(data)))


if __name__ == "__main__":
    unittest.main()
