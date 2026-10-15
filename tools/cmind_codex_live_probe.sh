#!/usr/bin/env bash
# Operator-initiated one-call CoderMind -> Codex compatibility test.
# May incur model usage. No RPG/codegen; isolated synthetic workspace only.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -n "${CMIND_CODEX_BYPASS_SANDBOX:-}" ]]; then
  echo "ERROR: CMIND_CODEX_BYPASS_SANDBOX must be unset" >&2
  exit 2
fi
for tool in python3 codex; do
  command -v "$tool" >/dev/null || { echo "Missing $tool" >&2; exit 2; }
done
CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
VENV="$CACHE/venvs/cmind-codex-pr96"
CMIND="$VENV/bin/cmind"
PYTHON="$VENV/bin/python"
if [[ ! -x "$CMIND" || ! -x "$PYTHON" ]]; then
  echo "Candidate preflight not installed. Run make cmind-codex-smoke first." >&2
  exit 2
fi
PIN="$(python3 - "$ROOT/tooling/versions.yaml" <<'PY'
import re,sys,pathlib
s=pathlib.Path(sys.argv[1]).read_text()
m=re.search(r"(?ms)^  rpg_codex_pr96_candidate:\n(.*?)(?=^  [a-z_]+:|\Z)",s)
if not m: raise SystemExit("candidate SHA not declared")
r=re.search(r"(?m)^    revision: ([0-9a-f]{40})$",m.group(1))
if not r: raise SystemExit("candidate SHA invalid")
print(r.group(1))
PY
)"
"$PYTHON" - "$PIN" <<'PY'
import json,sys
from importlib.metadata import distribution
d=distribution("cmind-cli")
src=json.loads(d.read_text("direct_url.json") or "{}").get("vcs_info",{}).get("commit_id")
if src!=sys.argv[1]: raise SystemExit(f"CoderMind SHA mismatch: {src!r}")
PY
mkdir -p "$CACHE/runs"
RUN="$(mktemp -d "$CACHE/runs/codex-live.XXXXXX")"
echo "Evidence directory: $RUN"
trap 'status=$?; if ((status)); then echo "Probe failed (exit $status), evidence in '"$RUN"'" >&2; fi' EXIT
(
  cd "$RUN"
  "$CMIND" init codex-live-fixture --ai codex --script sh --no-git --no-mcp --no-encode --ignore-agent-tools \
    >"$RUN/init.stdout" 2>"$RUN/init.stderr"
)
"$CMIND" script --where common/llm_client.py >"$RUN/llm-path.stdout"
LLM_PATH="$(cat "$RUN/llm-path.stdout")"
[[ -f "$LLM_PATH" ]] || { echo "Packaged CoderMind LLMClient missing" >&2; exit 3; }
codex --version >"$RUN/codex-version.stdout" 2>"$RUN/codex-version.stderr"

# Import the actual installed CoderMind LLM client. It must resolve a scratch
# workspace from cwd and pass the prompt through CodexSessionManager via stdin.
(
  cd "$RUN/codex-live-fixture"
  CMIND_AI_CLI_CMD="codex exec" \
    "$PYTHON" - "$LLM_PATH" "$RUN" "$PIN" <<'PY'
import json, pathlib, sys
script_path, output_dir, pin=pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2]),sys.argv[3]
sys.path.insert(0,str(script_path.parent.parent))
from common.llm_client import LLMClient
from common.session_manager import CodexSessionManager
client=LLMClient(tool="codex exec")
if not isinstance(client._session_manager,CodexSessionManager):
    raise SystemExit("CodexSessionManager not selected")
token="CHECKERLAB_CODEX_LIVE_OK"
prompt=(
    "This is a minimal read-only compatibility test. "
    "Do not use tools; do not read or change files. "
    f"Reply with EXACTLY this token on one line, nothing else: {token}"
)
response=client.generate(prompt,purpose="lab-compatibility",max_retries=1,timeout=120)
(output_dir/"model-response.txt").write_text(response+"\n",encoding="utf-8")
if response.strip()!=token:
    raise SystemExit(f"Unexpected model response; see {output_dir/'model-response.txt'}")
summary={
  "status":"LIVE_LLM_CLIENT_PASS_RPG_NOT_TESTED",
  "cmind_sha":pin,
  "codex_session_manager":"PASS",
  "single_cli_call":True,
  "model_output_matches":True,
  "rpg_generation":"NOT_TESTED",
  "checker_implemented":False
}
(output_dir/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
PY
) >"$RUN/live.stdout" 2>"$RUN/live.stderr" || {
  echo "Codex/CoderMind failed. Last errors:" >&2
  tail -n 35 "$RUN/live.stderr" >&2 || true
  echo "See $RUN for full local diagnostics." >&2
  exit 1
}
cat "$RUN/live.stdout"
echo "No RPG generated; no source files or Git hooks modified."
