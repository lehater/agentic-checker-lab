#!/usr/bin/env python3
"""One-time scoped Checker reconciliation after Harness #224.

Recomputes the canonical publication with the official Harness CAS boundary.
No fabricated provider, semantic admission, or Question resolution identity.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / ".harness/harness-binding.json"
revision = json.loads(BINDING.read_text())["source"]["revision"]
pack = Path.home() / ".cache/harness/v1" / revision
if not pack.exists():
    subprocess.run(["python3", str(ROOT / ".harness/harnessw.py"), "sync"], cwd=ROOT, check=True)
assert pack.exists(), f"Missing pinned Harness Consumer Pack: {revision}"
sys.path.insert(0, str(pack / "src"))

from harness.application.project_publication import (
    prepare_reconciliation_publication,
    publish_project_publication,
    read_project_publication,
)
from harness.project_model.engineering_graph import validate_engineering_graph
from harness.assurance.capability_lifecycle import lifecycle_states
from harness.project_model.engineering_graph import validate_realization

def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def write(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8")

gpath = ROOT / ".harness/engineering-graph.yaml"
ppath = ROOT / ".harness/project-publication.yaml"
apath = ROOT / ".harness/authority-assessments.yaml"
spath = ROOT / "docs/scenario/checker-scope-reconciliation.yaml"
cpath = ROOT / "docs/project/current-state.yaml"

graph = load(gpath)
assert not any(a["id"] == "DOMAIN-STRATEGY" for a in graph["authorities"])
domain = next(a for a in graph["authorities"] if a["id"] == "DOMAIN-USE-CASE-DESIGN")
assert domain["produces"][0]["requires"] == ["checker.requirements"]
verification = next(a for a in graph["authorities"] if a["id"] == "VERIFICATION-DESIGN")
production = verification["produces"][0]
assert production["requires"] in (["checker.requirements"], ["checker.requirements", "checker.domain-use-case"])
production["requires"] = ["checker.requirements", "checker.domain-use-case"]
validate_engineering_graph(graph)

old = read_project_publication(ppath, graph=graph)
state = old["state"]
core = copy.deepcopy(state["core_model"])
questions = core["questions"]
assert [q["id"] for q in questions if q["id"].startswith("Q-DV-")] in (
    ["Q-DV-001", "Q-DV-002"], ["Q-DV-002"]
)
# Q-DV-001 was introduced solely by the invalid unconditional skill input.
# Delete this unsupported obligation from active truth; Git retains provenance.
core["questions"] = [q for q in questions if q["id"] != "Q-DV-001"]
q2 = next(q for q in core["questions"] if q["id"] == "Q-DV-002")
q2["text"] = (
    "Какие конкретные поддерживаемые ACL facts и match/non-match predicates "
    "применимы к входному IPv4 TCP/UDP потоку (оба адреса и оба порта), "
    "как интерпретируется известный порядок показываемых правил внутри context "
    "и где проходит граница unknown/unsupported фактов? Нужны независимо "
    "обоснованные положительные и отрицательные ожидаемые примеры. "
    "Syntax/masks, implicit deny, first-match, action priority, "
    "глобальный Permit/Deny и алгоритм не приняты."
)
assert set(q2["blocks_capabilities"]) == {
    "checker.domain-use-case", "checker.verification-strategy"
}
outcomes = {
    "checker.problem": "CURRENT",
    "checker.requirements": "CURRENT",
    "checker.domain-use-case": "BLOCKED",
    "checker.verification-strategy": "BLOCKED",
}
new = prepare_reconciliation_publication(
    graph=graph, current_publication=old, expected_revision=old["revision"],
    outcomes=outcomes, core_model=core,
    semantic_evaluations=state["semantic_evaluations"], lifecycle=state["lifecycle"],
    decision_failures=state["decision_failures"],
)
assert new["revision"] != old["revision"]
assert new["state"]["semantic_evaluations"] == state["semantic_evaluations"]
assert new["state"]["lifecycle"] == state["lifecycle"]
assert new["state"]["core_model"]["artifacts"] == state["core_model"]["artifacts"]
write(gpath, graph)
published = publish_project_publication(
    ppath, graph=graph, publication=new, expected_revision=old["revision"]
)
assert read_project_publication(ppath, graph=graph) == published

registry = load(apath)
for row in registry["assessments"]:
    aid = row["authority_id"]
    if aid == "DOMAIN-USE-CASE-DESIGN":
        row.update(
            applicability="REQUIRED",
            evidence=["docs/scenario/domain-verification-delegation.md",
                      ".harness/knowledge/checker-requirements.yaml",
                      "core:question:Q-DV-002"],
            rationale="Independent first-slice ACL behavior must be defined for verification; accepted matching meaning is still blocked.",
            depends_on_evidence=["PDEC-CHECKER-004", "PDEC-CHECKER-005", "Q-DV-002"],
            reopening_conditions=["first-slice behavior or accepted use-case consumer changes"],
        )
    elif aid == "VERIFICATION-DESIGN":
        row.update(
            applicability="REQUIRED",
            evidence=["docs/scenario/domain-verification-delegation.md",
                      ".harness/knowledge/checker-requirements.yaml",
                      "core:question:Q-DV-002"],
            rationale="Accepted first-slice requirements need independent verification; match-dependent evidence is blocked.",
            depends_on_evidence=["PDEC-CHECKER-004", "Q-DV-002"],
            reopening_conditions=["verification scope or accepted matching contracts change"],
        )
assert next(r for r in registry["assessments"] if r["authority_id"]=="DOMAIN-STRATEGY")["applicability"] == "UNASSESSED"
write(apath, registry)

scope = load(spath)
scope["open_design_questions"] = ["Q-DV-002"]
write(spath, scope)

current = load(cpath)
current["status"] = "P2_CHECKER_REQUIREMENTS_CURRENT_DOMAIN_MATCHING_BLOCKED"
current["verified"] = [
    "checker.problem CURRENT; original admission and lifecycle preserved",
    "checker.requirements CURRENT; 13 accepted first-slice obligations preserved",
    "checker.domain-use-case BLOCKED by Q-DV-002 (accepted matching semantics)",
    "checker.verification-strategy BLOCKED by Q-DV-002 (independent matching oracle)",
    "Q-DV-001 deleted as erroneous skill-derived prerequisite; no Domain Strategy provider invented",
    "Full product subject inventory and implementation are not accepted",
]
current["evidence"]["publication_revision"] = new["revision"]
write(cpath, current)

# Neither a missing Strategy nor a removed false Question implies acceptance.
model = validate_realization(graph, core)
assert all(x["id"] != "DOMAIN-STRATEGY" for x in graph["authorities"])
assert [q["id"] for q in core["questions"] if q["id"].startswith("Q-DV-")] == ["Q-DV-002"]
print(json.dumps({"old": old["revision"], "new": new["revision"], "outcomes": outcomes}))
