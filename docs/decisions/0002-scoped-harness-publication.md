# ADR-0002 — scoped direct Harness publication

Status: ACCEPTED within delegated TASK-004 technical scope, 2026-10-16.

Context: PDEC-CHECKER-002 authorizes strict admission and coherent publication of checker.problem, but does not adopt the historical five-Capability candidate graph. No canonical Harness realization existed.

Decision: use the pinned Consumer Pack direct-file publication API with `.harness/project-publication.yaml` as the sole coordinated Core/evaluation/lifecycle/failure snapshot and `.harness/engineering-graph.yaml` as its minimal production contract. Reuse PDEC-CHECKER-001 as the project-native Problem Evidence artifact. The sole consumer CHECKER-PROBLEM-ADMISSION selects Discovery admission, not implementation. Subject CHECKER-PROBLEM is an evaluation scope, not a product inventory.

Alternatives: adopting the full candidate graph would exceed delegation; separate component writes would violate atomic visibility; a database/adapter would add unnecessary infrastructure.

Consequences: publication uses validated baseline, CURRENT terminal validation and atomic CAS. Read models consume one read-back revision. Other Authorities, subject inventory and implementation coverage remain unresolved. No domain model or Checker architecture changes. Reproduction is provided by experiments/runs/harness-current-v1/execute.py; replay validates an existing equal publication without replacing it.

Sources: PDEC-CHECKER-001/002; pinned Harness docs/design/project-publication-v0.md and routed bootstrap/problem-evidence skills.
