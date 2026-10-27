# OpenSpec baseline — candidate for review

The official OpenSpec [setup documentation](https://github.com/Fission-AI/OpenSpec/blob/main/docs-lab/start/setup.md) and [spec-driven schema](https://openspec.dev/docs/schemas/spec-driven) define `openspec/config.yaml` and `openspec/changes/<name>/` with `proposal.md`, delta specs, design and tasks.

An initial proposed change is at `openspec/changes/checker-v1-baseline/`. It exists so that direct Codex and CoderMind can consume **the same frozen input after acceptance**. The historical PR #27 remains an empirical reference, not the new authority.

## Validation/approval before model runs

1. In a disposable clone with a supported pinned OpenSpec CLI, run `openspec init --tools none` and inspect any created/modified files; do not overwrite reviewed project context.
2. Run `openspec validate checker-v1-baseline --strict`; if invalid, repair artifacts in a PR.
3. Review whether the selected synthetic matching semantics and CLI are truly within owner-delegated boundaries. Do not declare accepted automatically.
4. Freeze the accepted delta, architecture policy and independent tests with checksums **before** giving either model the input.
5. Follow the [experiment design](../project/experiment-design.md) for matched A/B runs, telemetry and evidence.

**Current status:** manually drafted OpenSpec-format artifacts; no CLI execution, validated OpenSpec version, generated tool skills, accepted domain scope, or model evaluation yet. No Harness.
