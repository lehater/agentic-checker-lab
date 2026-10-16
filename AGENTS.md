# Spec Kit Checker experiment — branch-specific instructions

This file applies to `experiment/spec-kit-checker-v1` only. The original repository instructions remain unchanged on `main`.

## Task
Use the owner's original problem statement at `docs/scenario/owner-problem-brief.md` to prepare engineering artifacts by the GitHub Spec Kit workflow. Produce specifications, clarification notes, quality checklists, a plan, research, data model, interface contracts, and an implementation validation guide. Stop **before** tasks, RPG planning, or code generation.

## Isolation
- Do not use Harness tools, .harness state, previous Checker designs, prior RPG files, implementation or test solutions as feature input.
- Work only under `specs/001-acl-snapshot-checker/`, `.specify/`, and `experiments/runs/spec-kit-checker-v1/`.
- The source brief is the only product input; unresolved choices must be documented as assumptions or questions, not falsely attributed to the owner.
- Do not access real network appliances. Use synthetic data only.
- Preserve provenance, experimental limitations and any operator interventions.

## Experimental integrity
This branch was prepared from main at 2bf23ce. The initial artifacts here are produced in a ChatGPT session by directly following upstream Spec Kit command templates; the official `specify` CLI and autonomous coding-agent integration were not executed. This is a **non-blind, adapted Spec Kit process**, not a controlled A/B benchmark. Do not report it otherwise.
