"""Invariant tests for decision -> candidate requirement -> CHK audit trace."""
import copy
import unittest
from tools.check_decision_trace import verify_trace

SPEC = """### Requirement: Proposed input
#### Scenario: Valid
### Requirement: Proposed result
#### Scenario: Ordered
"""
CATALOG = {
    "status": "PROPOSED_NOT_OWNER_ACCEPTED",
    "cases": [
        {"id": "CHK-001", "requirement": "Proposed input", "scenario": "Valid"},
        {"id": "CHK-002", "requirement": "Proposed result", "scenario": "Ordered"},
    ],
}
LEDGER = {"decisions": [
    {"id": "D-001", "status": "ACCEPTED"},
    {"id": "D-002", "status": "ACCEPTED"},
]}
GAP = {
    "kind": "MISSING_COVERAGE",
    "description": "The candidate has no scenario covering the approved domain rule.",
    "next_action": "Write a distinct requirement and independently reviewed case.",
}
TRACE = {
    "schema": "checker-decision-trace/v1",
    "status": "PROPOSED_UNREVIEWED",
    "semantic_review": "NOT_PERFORMED",
    "entries": [
        {"decision_id": "D-001", "links": [
            {"requirement": "Proposed input", "case_id": "CHK-001"}
        ], "gaps": []},
        {"decision_id": "D-002", "links": [], "gaps": [GAP]},
    ],
}


class DecisionTraceTests(unittest.TestCase):
    def result(self, data=None, ledger=None, catalog=None, spec=SPEC):
        return verify_trace(
            copy.deepcopy(TRACE if data is None else data),
            copy.deepcopy(LEDGER if ledger is None else ledger),
            copy.deepcopy(CATALOG if catalog is None else catalog),
            spec,
        )

    def rejected(self, data, message):
        result = self.result(data)
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn(message, " / ".join(result["errors"]))

    def test_valid_trace_with_explicit_gap_does_not_claim_semantic_pass(self):
        r = self.result()
        self.assertEqual(r["status"], "VALID_WITH_OPEN_GAPS")
        self.assertEqual(r["declared_gaps"], 1)
        self.assertIs(r["semantics_verified"], False)
        self.assertIs(r["owner_accepted_spec"], False)

    def test_new_accepted_decision_requires_trace(self):
        ledger = copy.deepcopy(LEDGER)
        ledger["decisions"].append({"id": "D-003", "status": "ACCEPTED"})
        self.assertIn("missing decision trace D-003", self.result(ledger=ledger)["errors"])

    def test_duplicate_decision_mapping_fails(self):
        x = copy.deepcopy(TRACE)
        x["entries"].append(copy.deepcopy(x["entries"][0]))
        self.rejected(x, "duplicate trace decision D-001")

    def test_unaccepted_decision_cannot_be_traced_as_accepted(self):
        x = copy.deepcopy(TRACE)
        x["entries"][1]["decision_id"] = "D-999"
        self.rejected(x, "non-accepted decision D-999")

    def test_link_must_reference_actual_catalog_case(self):
        x = copy.deepcopy(TRACE)
        x["entries"][0]["links"][0]["case_id"] = "CHK-999"
        self.rejected(x, "unknown CHK case CHK-999")

    def test_case_must_belong_to_named_spec_requirement(self):
        x = copy.deepcopy(TRACE)
        x["entries"][0]["links"][0]["requirement"] = "Proposed result"
        self.rejected(x, "does not belong to requirement")

    def test_case_scenario_must_exist_in_spec(self):
        x = copy.deepcopy(TRACE)
        self.assertIn(
            "scenario missing from candidate spec",
            " / ".join(self.result(x, spec="### Requirement: Proposed result\n#### Scenario: Ordered\n")["errors"])
        )

    def test_gaps_must_be_actionable(self):
        x = copy.deepcopy(TRACE)
        x["entries"][1]["gaps"][0]["next_action"] = ""
        self.rejected(x, "invalid or unactionable gap")

    def test_decision_cannot_be_silently_unmapped(self):
        x = copy.deepcopy(TRACE)
        x["entries"][1]["gaps"] = []
        self.rejected(x, "neither links nor declared gaps")

    def test_claiming_owner_acceptance_or_independent_review_fails(self):
        x = copy.deepcopy(TRACE)
        x["status"] = "OWNER_ACCEPTED"
        x["semantic_review"] = "PASS"
        self.rejected(x, "trace must not claim owner acceptance")
        self.rejected(x, "trace must not claim independent semantic review")


if __name__ == "__main__":
    unittest.main()
