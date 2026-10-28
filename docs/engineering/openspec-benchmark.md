# OpenSpec baseline — mechanically validated, subject to owner review

The [official OpenSpec CLI reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md) defines the spec-driven layout and strict validation. The proposed change lives at [checker-v1-baseline](../../openspec/changes/checker-v1-baseline/proposal.md).

## Verified in GitHub CI

- OpenSpec CLI: pinned official npm release **1.14.3**, installed in GitHub Actions under Node.js 22.
- Command: `openspec validate checker-v1-baseline --strict --json --no-interactive`
- Evidence: [GitHub Actions #40605882242](https://github.com/lehater/agentic-checker-lab/actions/runs/40605882242), **success**.
- CI uses `OPENSPEC_TELEMETRY=0` and no model credentials or LLM calls.
- Validates structure and expected OpenSpec artifacts **only**; does not accept product semantics or prove Codex tooling integration.

## Next approval gates

1. Review the concrete proposed IPv4/CIDR/range/CLI subset against the [owner's original problem](../scenario/owner-problem-brief.md).
2. Mark accepted or resolve unanswered product/domain decisions before publishing one frozen input for A/B agents.
3. Check Codex/OpenSpec interactive tooling and CoderMind consumers in a bounded E2E (cannot be proven by CLI validation alone).
4. Freeze independent oracles, architecture policy and task budget hashes before model runs.

Do not run `openspec init` against the working repository in CI: it may change project files and is not necessary for read-only validation.
