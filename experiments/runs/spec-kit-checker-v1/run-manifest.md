# Spec Kit Checker engineering preparation — run manifest

**Status:** `ARTIFACTS_PRODUCED_NOT_INDEPENDENTLY_VALIDATED`
**Date:** 2026-10-16
**Repository:** `lehater/agentic-checker-lab`
**Branch:** `experiment/spec-kit-checker-v1`
**Base commit:** `2bf23ce08512eda92684d09e3c46958d4b6ab3cc`
**Only owner input:** `docs/scenario/owner-problem-brief.md`.
**Spec Kit upstream reference:** `github/spec-kit@f6e72bc8523de8ec8368129cbdea78d45f27cef8`.

## Provenance and actual execution
This ChatGPT session retrieved and followed the upstream Spec Kit command definitions `templates/commands/specify.md`, `clarify.md`, `plan.md`, `checklist.md` and templates `spec-template.md`, `plan-template.md`, `checklist-template.md`.

**Not performed:** `specify init`, installation or launch of the official CLI, actual `/speckit.*` slash-command dispatch into a coding-agent integration, automatic extension hooks, autonomous background coding-agent execution, Spec Kit tool telemetry or independent blind evaluation.

**Equivalent work performed in-chat:** specification authoring, explicit assumptions/clarification log, own spec quality checklist, Phase 0 research with recorded choices, Phase 1 model/contracts/quickstart and reviewer-owned checklist generation. The official script-generated scaffold was recreated manually.

**Why not blind:** The assistant conducting this adaptation previously reviewed the Harness Checker results in the same conversation. The new artifacts do not copy those documents, but cognitive contamination cannot be excluded. This run cannot establish comparative superiority, objective token cost, or an unbiased baseline.

## Protocol
1. Start from original `main` before Harness-produced knowledge.
2. Override AGENTS on this isolated branch to prohibit reading `.harness/` and prior Checker outputs as product input.
3. Use original owner brief only for product requirements; distinguish plan decisions.
4. Stop before task breakdown, RPG, code generation.
5. Do not modify `main` or `feat/checker-problem-evidence`.

## Outputs
- `.specify/memory/constitution.md`, `.specify/feature.json`
- `specs/001-acl-snapshot-checker/spec.md`
- `specs/001-acl-snapshot-checker/checklists/requirements.md` (author self-check)
- `specs/001-acl-snapshot-checker/checklists/acl-integrity.md` (reviewer-only, unchecked)
- `specs/001-acl-snapshot-checker/plan.md`, `research.md`, `data-model.md`
- `specs/001-acl-snapshot-checker/contracts/cli.md`, `dataset.schema.json`
- `specs/001-acl-snapshot-checker/quickstart.md`
- `experiments/runs/spec-kit-checker-v1/clarification-log.md`, this manifest

## Checks and limits
- Structural review of artifact content: completed in-session.
- JSON Schema parse: generated from valid serialized JSON object, not validated against a real JSON Schema engine in this branch.
- Independent specification checklist: pending (all unchecked).
- Runtime code tests / RPG validation: not applicable; no code generated.
- Model API cost, token usage, elapsed time: **UNKNOWN**.
- Owner approval of A-03, A-04, A-05: **NOT OBTAINED**.
- Branch comparison with Harness: **NOT PERFORMED**.

## Suggested next stage
Have a **fresh, independent coding agent** on this branch run the real pinned Spec Kit CLI/agent commands from the original owner brief under an explicit token/time budget, then compare resulting artifacts against this preparation and the Harness baseline using an independently established oracle. Do not use this in-chat adaptation as an unbiased Spec Kit sample.
