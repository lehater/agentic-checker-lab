#!/usr/bin/env python3
"""Independent read-only checks for Checker domain applicability reconciliation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
load = lambda p: yaml.safe_load((ROOT / p).read_text(encoding="utf-8"))

pub = load(".harness/project-publication.yaml")
graph = load(".harness/engineering-graph.yaml")
registry = load(".harness/authority-assessments.yaml")
scope = load("docs/scenario/checker-scope-reconciliation.yaml")
binding = json.loads((ROOT / ".harness/harness-binding.json").read_text())

assert pub["kind"] == "harness-project-publication"
recomputed = "sha256:" + hashlib.sha256(json.dumps(
    {"parent_revision": pub["parent_revision"], "state": pub["state"]},
    sort_keys=True, separators=(",", ":"), ensure_ascii=False,
).encode("utf-8")).hexdigest()
assert pub["revision"] == recomputed, "CAS publication revision mismatch"
assert binding["source"]["revision"] == "1c31054a8c4af223dc1bb003175c1fbe3f0538d6"
assert not any(a["id"] == "DOMAIN-STRATEGY" for a in graph["authorities"])
by_authority = {a["id"]: a for a in graph["authorities"]}
assert by_authority["DOMAIN-USE-CASE-DESIGN"]["produces"][0]["requires"] == ["checker.requirements"]
assert by_authority["VERIFICATION-DESIGN"]["produces"][0]["requires"] == [
    "checker.requirements", "checker.domain-use-case"
]
assess = {x["authority_id"]: x["applicability"] for x in registry["assessments"]}
assert assess["DOMAIN-STRATEGY"] == "UNASSESSED", assess
assert assess["DOMAIN-USE-CASE-DESIGN"] == "REQUIRED", assess
assert assess["VERIFICATION-DESIGN"] == "REQUIRED", assess
core = pub["state"]["core_model"]
questions = {q["id"]: q for q in core["questions"]}
assert "Q-DV-001" not in questions, questions
assert "Q-DV-002" in questions, questions
assert questions["Q-DV-002"].get("resolution") is None
assert set(questions["Q-DV-002"]["blocks_capabilities"]) == {
    "checker.domain-use-case", "checker.verification-strategy"
}
assert scope["open_design_questions"] == ["Q-DV-002"]
assert len(load(".harness/knowledge/checker-requirements.yaml")["content"]["requirements"]) == 13
assert {x["capability"] for x in pub["state"]["lifecycle"]["providers"]} == {
    "checker.problem", "checker.requirements"
}, "fabricated downstream CURRENT"
assert {x["capability"] for x in pub["state"]["semantic_evaluations"]["semantic_evaluations"]} == {
    "checker.problem", "checker.requirements"
}, "fabricated downstream Semantic Admission"
assert len(core["artifacts"]) == 2, "unexpected canonical provider"
assert all(q.get("resolution") is not None for k,q in questions.items() if k.startswith("Q-PR-"))
print("Checker Domain Strategy applicability reconciliation PASS")
