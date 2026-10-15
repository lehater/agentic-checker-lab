# P1: first forward RPG from synthetic requirements

Status: **PREPARED / NOT RUN IN UBUNTU**.

This stage deliberately verifies **requirements → feature specification → feature tree → skeleton → initial RPG**, not the existing-code RPG encoder, full Phase 2 or Checker code generation.

Source of truth for this probe: [synthetic requirements](../../tooling/fixtures/rpg-synthetic/requirements.md), which are *not* accepted Checker requirements. CoderMind reference: [forward pipeline and commands](https://github.com/microsoft/RPG-ZeroRepo/blob/3303a222eaec42c6a178bddd46ad63d9026ab8fa/CoderMind/docs/commands.md).

## Staged commands

Run from branch `tooling/task-003-synthetic-rpg`:

```bash
make check
make cmind-rpg-init
make cmind-rpg-status
```

The init stage uses the already installed **pinned PR #96** candidate, creates a synthetic workspace outside the repository (`~/.cache/agentic-checker-lab/runs/rpg-synthetic-v1/workspace`), copies the test specification and **does not call a model**. It does not initialize Git, MCP or any RPG.

After inspecting readiness, run **only when ready to consume real Codex model usage** (multiple calls, no guaranteed spending limit):

```bash
make cmind-rpg-phase1
make cmind-rpg-status
```

This runs `feature_spec.py --docs <synthetic-docs>` and the feature construction orchestrator with a limited review/refactor iteration budget. Inspect the actual produced feature tree; **do not assume quality or complete semantics because the script exited zero**.

Only after inspecting Phase 1:

```bash
make cmind-rpg-skeleton
make cmind-rpg-status
```

This runs `build_skeleton.py --max-iterations 2` and `check_skeleton.py`; the former should create `rpg.json`. Test verifies JSON parses and CoderMind's skeleton checker succeeds, **not** that architecture/coverage is correct. Scripts preserve logs/stdout/stderr in the synthetic run directory and use CoderMind's authoritative `~/.cmind/workspaces/<workspace-id>/data` storage. Any failed stage stops; no uncontrolled retry/force.

To prepare graph artifacts for repository evidence (modifies only the current task branch working tree):

```bash
make cmind-rpg-export
```

The explicit export creates `experiments/runs/rpg-synthetic-v1` with five JSON files and a SHA256 manifest; it **does not commit or push**. Review generated content, privacy and scope before committing the result in this task branch. For reproducibility, keep the PR #96 source SHA, original requirements checksum, and export hashes. The developer must separately assess generated nodes, relationships, required behavior and unforeseen extra features; a parseable graph is not a verified graph.

**Security:** no sandbox bypass allowed; scripts run only on an isolated test workspace; no real network device data, no Checker implementation, no Git hooks. Model calls are made *only* when the phase1/skeleton targets are explicitly launched. The user-installed global Codex configuration is not overridden.

**Completion criterion:** operator-reported working forward RPG, structural validation, saved artifacts for review, and explicit caveats. Full interfaces/tasks/code generation belongs to a later, separately gated phase.
