# Roadmap — post-Harness experimental method

**Owner-directed method (2026-10-28); phase completion must be supported by actual evidence.** The source of completion evidence is [state](current-state.yaml). Historical TASK-001..009 remain in git history; this roadmap supersedes their forward sequence.

| ID | Small deliverable | Acceptance gate |
| --- | --- | --- |
| S0 | Method reset, navigation, scopes, Engineering Policy; preserve PR #27 | Docs/links CI PASS; no active Harness instruction |
| S1 | Architecture validation against archived CoderMind skeleton and source import graph | Known domain/application violation fails; legitimate inward layout passes; stdlib CI PASS |
| S2 | CoderMind/Codex telemetry with normalized run schema | One reproducible offline log parser, zero tokens never equated to unknown; live token counts explicitly unverified until live probe |
| S3 | Freeze Checker task/specifications/independent oracle; evaluate OpenSpec minimal workflow | Same accepted inputs for all candidates; actual OpenSpec version and export validated before implementation |
| **S3D** | **Design-stage integration and review**: [recoverable plan](design-stage-plan.md) (D1 audit → D2 minimum stack → D3 Checker design → D4 independent review; parallel to L1 where safe) | Evidence-based tool selection, traceable design, independent design review; no model codegen before frozen spec/design/oracle and local preflight |
| S4 | Controlled direct Codex vs CoderMind run with bounded budget | Architecture + independent tests, wall-clock, tokens or UNKNOWN, retries, interventions and hashes recorded |
| S5 | Optimize selected bottleneck(s) (no-op reviews, excessive context/iterations, semantic drift) | Measured improved quality-adjusted duration/usage without regressions on frozen cases |
| S6 | Adaptive model router: deterministic first for mechanical work, local/cloud by observed quality, speed and quota | A/B evidence and safe fallback; no hypothetical savings or forced local-first |
| S7 | Requirements change-impact and transfer to second task | Before/after trace, independent regression and evidence-based GO/NO-GO |

One task, branch, PR and bounded proof at a time. Code execution/LLM calls are **never** implied by a documentation-only PR. Do not bypass architectural checks or rewrite fixed oracles after seeing implementation. An open PR remains a proposal until reviewed/merged.

GitHub CI covers S0 method, S1 architecture regression, S2 offline telemetry, OpenSpec CLI validation, proposed acceptance scenario trace and offline comparison. Live run results are not verified. The remaining L1–L5 local-executor steps are listed in [handoff](local-executor-handoff.md). Parallel **S3D** design-stage work is detailed in the [recoverable OpenSpec design-stage plan](design-stage-plan.md); the immediate documentation task is its D1 source audit, not Checker codegen.
