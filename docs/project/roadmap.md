# Roadmap — post-Harness experimental method

**Owner-directed method (2026-10-28); phase completion must be supported by actual evidence.** The source of completion evidence is [state](current-state.yaml). Historical TASK-001..009 remain in git history; this roadmap supersedes their forward sequence.

| ID | Small deliverable | Acceptance gate |
| --- | --- | --- |
| S0 | Method reset, navigation, scopes, Engineering Policy; preserve PR #27 | Docs/links CI PASS; no active Harness instruction |
| S1 | Architecture validation against archived CoderMind skeleton and source import graph | Known domain/application violation fails; legitimate inward layout passes; stdlib CI PASS |
| S2 | CoderMind/Codex telemetry with normalized run schema | One reproducible offline log parser, zero tokens never equated to unknown; live token counts explicitly unverified until live probe |
| S3 | Freeze Checker task/specifications/independent oracle; evaluate OpenSpec minimal workflow | Same accepted inputs for all candidates; actual OpenSpec version and export validated before implementation |
| S4 | Controlled direct Codex vs CoderMind run with bounded budget | Architecture + independent tests, wall-clock, tokens or UNKNOWN, retries, interventions and hashes recorded |
| S5 | Optimize selected bottleneck(s) (no-op reviews, excessive context/iterations, semantic drift) | Measured improved quality-adjusted duration/usage without regressions on frozen cases |
| S6 | Adaptive model router: deterministic first for mechanical work, local/cloud by observed quality, speed and quota | A/B evidence and safe fallback; no hypothetical savings or forced local-first |
| S7 | Requirements change-impact and transfer to second task | Before/after trace, independent regression and evidence-based GO/NO-GO |

## Параллельный подготовительный трек: проектирование Agentic SDLC

**[DS-01..DS-06 — канонический план стека Design](agentic-sdlc-design-stack-plan.md).** DS-01 — ближайшая небольшая задача: аудит исходников готовых расширений OpenSpec (Intent-Driven, DDD Skills, Anvil), без их установки и без генерации Checker. DS-02 — минимальная обоснованная конфигурация OpenSpec; DS-03/04 — проект Checker и независимый Architecture Review. DS-05 синхронизируется с существующим L1/S3 (независимый oracle и preflight), DS-06 — с S4 (контролируемый Direct vs RPG); **это детализация этапов, не новая конкурирующая дорожная карта**. Подготовительное проектирование не снимает существующих blockers и не означает принятия PR #51.

One task, branch, PR and bounded proof at a time. Code execution/LLM calls are **never** implied by a documentation-only PR. Do not bypass architectural checks or rewrite fixed oracles after seeing implementation. An open PR remains a proposal until reviewed/merged.

GitHub CI covers S0 method, S1 architecture regression, S2 offline telemetry, OpenSpec CLI validation, proposed acceptance scenario trace and offline comparison. Live run results are not verified. The remaining L1–L5 local-executor steps are listed in [handoff](local-executor-handoff.md).
