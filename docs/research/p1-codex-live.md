# P1 — Codex via CoderMind: one actual model call

Status: **LIVE LLM CLIENT PASS — user-reported Ubuntu run, 2026-10-16; RPG NOT_TESTED**.

Purpose: close the gap between the structural `CodexSessionManager` test and actual model execution. This task does **not** attempt Checker requirements, RPG creation or agent code generation.

After [PR #96 structural PASS](p1-codex-pr96.md), the operator may run:

```bash
git switch tooling/task-003-codex-live-contract
make check
make cmind-codex-live
```

**This command invokes the real Codex model and may consume usage.** It makes one explicitly requested `LLMClient.generate` call with `max_retries=1`, a simple read-only prompt and a timeout; other subprocess stages do not call the model. Do not run in documentation CI. It uses the already installed PR #96 venv and verifies SHA provenance; **no reinstall/auto-upgrade**. It creates a new temporary `cmind init ... --ai codex --no-git --no-mcp --no-encode --ignore-agent-tools` workspace outside the repository and confirms the actual installed CoderMind LLM client uses `CodexSessionManager`, then checks that the returned token is exact.

Outputs, run details and errors are written to `~/.cache/agentic-checker-lab/runs/codex-live.XXXXXX/`. Logs can contain model session details; review and redact before committing. Sandbox bypass `CMIND_CODEX_BYPASS_SANDBOX` is rejected. Do not change Codex's own global auth/settings to work around a failure without inspecting it.

Success: `LIVE_LLM_CLIENT_PASS_RPG_NOT_TESTED`, expected exact response, preserved repo, pinned SHA. Failure: record the actual CLI stderr (e.g. invalid option/authentication/sandbox), not substitute a direct Codex call; the wrapper itself is under test. After PASS, use **another task** to create and serialize a tiny real RPG in a fresh workspace, independently validate it and decide when to promote PR #96 to the canonical tool pin.

Important: `codex exec ... --help` passing during the structural probe does not guarantee all flags work in an actual invocation. A failure here is valuable diagnostic evidence; it does not retroactively invalidate the earlier structural results.

## Результат испытания (2026-10-16)

Владелец проекта передал следующий вывод реального запуска `make cmind-codex-live` на своей Ubuntu:

```json
{
  "status": "LIVE_LLM_CLIENT_PASS_RPG_NOT_TESTED",
  "cmind_sha": "3303a222eaec42c6a178bddd46ad63d9026ab8fa",
  "codex_session_manager": "PASS",
  "single_cli_call": true,
  "model_output_matches": true,
  "rpg_generation": "NOT_TESTED",
  "checker_implemented": false
}
```

Путь к локальному evidence: `/home/alex/.cache/agentic-checker-lab/runs/codex-live.Vzhj33/`. Скрипт подтвердил точное совпадение возвращённого токена. Полный набор локальных stdout/stderr, число токенов и стоимость не получены в этой переписке. Это **operator-reported evidence**, не независимый запуск с нашей стороны.

Таким образом, принятый PR #96 адаптер доказал не только наличие CLI и передачу prompt, но и реальный путь `CoderMind LLMClient → CodexSessionManager → codex exec → ответ модели`. В результате не создавался RPG и не реализован Checker. Следующий проверяемый вопрос — графовая генерация и экспорт.
