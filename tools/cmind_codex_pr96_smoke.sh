#!/usr/bin/env bash
# TASK-003-CODEX-PR96: isolated, non-inferential compatibility probe.
# No Codex model calls, no code generation, no init in the lab repository.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for cmd in python3 uv git codex; do
  command -v "$cmd" >/dev/null 2>&1 || {
    printf 'ERROR: %s not available in PATH\n' "$cmd" >&2
    exit 2
  }
done
if [[ -n "${CMIND_CODEX_BYPASS_SANDBOX:-}" ]]; then
  echo "ERROR: CMIND_CODEX_BYPASS_SANDBOX is set. Unset it; unsafe bypass is not permitted in this experiment." >&2
  exit 2
fi

PIN="$(python3 - "$ROOT/tooling/versions.yaml" <<'PY'
import pathlib, re, sys
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
section = re.search(r"(?ms)^  rpg_codex_pr96_candidate:\n(.*?)(?=^  [a-z_]+:|\Z)", text)
if not section:
    raise SystemExit("Missing rpg_codex_pr96_candidate version pin")
match = re.search(r"(?m)^    revision: ([0-9a-f]{40})$", section.group(1))
if not match:
    raise SystemExit("Invalid pinned candidate revision")
print(match.group(1))
PY
)"

CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
VENV="$CACHE/venvs/cmind-codex-pr96"
mkdir -p "$CACHE/venvs" "$CACHE/runs"
if [[ -f "$VENV/pyvenv.cfg" && -x "$VENV/bin/python" ]]; then
  echo "Reusing Codex candidate environment: $VENV"
elif [[ -e "$VENV" ]]; then
  echo "ERROR: incomplete/corrupt candidate venv at $VENV; inspect it, no auto-delete." >&2
  exit 2
else
  uv venv --python python3.12 "$VENV"
fi

RUN="$(mktemp -d "$CACHE/runs/codex-pr96.XXXXXX")"
trap 'exit_code=$?; if (( exit_code )); then printf "FAIL (exit %s). Diagnostic files: %s\n" "$exit_code" "$RUN" >&2; fi' EXIT
echo "Evidence directory: $RUN"
run_step() {
  local label="$1"
  shift
  echo "Running: $label"
  if ! "$@" >"$RUN/$label.stdout" 2>"$RUN/$label.stderr"; then
    printf 'FAIL: %s, stderr:\n' "$label" >&2
    tail -n 50 "$RUN/$label.stderr" >&2 || true
    tail -n 30 "$RUN/$label.stdout" >&2 || true
    return 1
  fi
}

run_step install uv pip install --quiet --python "$VENV/bin/python" \
  "git+https://github.com/microsoft/RPG-ZeroRepo.git@$PIN#subdirectory=CoderMind"
run_step provenance "$VENV/bin/python" - "$PIN" <<'PY'
import json, sys
from importlib.metadata import distribution
dist = distribution("cmind-cli")
source = json.loads(dist.read_text("direct_url.json") or "{}")
actual = source.get("vcs_info", {}).get("commit_id")
if actual != sys.argv[1]:
    raise SystemExit(f"Git SHA mismatch: expected {sys.argv[1]}, installed {actual}")
print(json.dumps({"package":dist.metadata["Name"],"version":dist.version,"source_sha":actual}))
PY

export PATH="$VENV/bin:$PATH"
run_step codex-version codex --version
# --help parses actual permission flags, but does not call the model.
run_step codex-flags codex exec --approve-for-me --ephemeral --skip-git-repo-check --help
run_step cmind-version cmind version
run_step cmind-scripts cmind script --list

# The only initialized workspace is underneath this fresh per-run cache directory.
run_step init bash -c '
  cd "$1"
  cmind init codex-fixture --ai codex --script sh --no-git --no-encode --ignore-agent-tools
' _ "$RUN"
run_step active-backend bash -c 'cd "$1"; cmind config show' _ "$RUN/codex-fixture"
run_step session-path cmind script --where common/session_manager.py

run_step assertions "$VENV/bin/python" - "$RUN" "$PIN" <<'PY'
import json
import os
from pathlib import Path
import sys
import tomllib

run, pin = Path(sys.argv[1]), sys.argv[2]
workspace = run / "codex-fixture"
with (workspace / ".cmind" / "config.toml").open("rb") as f:
    cfg = tomllib.load(f)
if cfg["cmind"]["ai_cli_cmd"] != "codex exec":
    raise SystemExit("FAIL: active backend is not codex exec")
with (workspace / ".codex" / "config.toml").open("rb") as f:
    codex = tomllib.load(f)
mcp = codex["mcp_servers"]["rpg-tools"]
if mcp["command"] != "cmind-mcp":
    raise SystemExit("FAIL: Codex rpg-tools MCP registration incorrect")
skills = sorted((workspace / ".agents" / "skills").glob("cmind-*/SKILL.md"))
if len(skills) != 15:
    raise SystemExit(f"FAIL: expected 15 Codex skills, got {len(skills)}")
script_path = Path((run / "session-path.stdout").read_text().strip())
if not script_path.is_file():
    raise SystemExit("FAIL: missing packaged Codex session manager")
sys.path.insert(0, str(script_path.parent.parent))
from common.session_manager import CodexSessionManager, create_session_manager

# No subprocess, no model request: inspect generated arguments and prompt delivery.
manager = create_session_manager("codex", workspace)
with manager.trace("codex probe, do not execute", purpose="preflight") as context:
    if not isinstance(manager, CodexSessionManager):
        raise SystemExit("FAIL: CodexSessionManager not selected")
    if context.extra_args != ["--approve-for-me", "--ephemeral", "--skip-git-repo-check", "-"]:
        raise SystemExit(f"FAIL: unsafe/incorrect Codex arguments: {context.extra_args}")
    if context.stdin is None or context.stdin.read() != "codex probe, do not execute":
        raise SystemExit("FAIL: prompt is not delivered through stdin")
result = {
    "status": "STRUCTURAL_PASS_LIVE_AGENT_NOT_TESTED",
    "source_sha": pin,
    "skills": len(skills),
    "mcp_command": mcp["command"],
    "backend": cfg["cmind"]["ai_cli_cmd"],
    "codex_session_manager": "PASS",
    "codex_cli_flags": "PARSE_OK",
    "model_authentication": "NOT_TESTED",
    "full_rpg_generation": "NOT_TESTED",
    "checker_implemented": False,
}
(run / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
PY
cat "$RUN/summary.json"
echo "Complete. Local evidence: $RUN"
echo "No model invocation, no generated RPG and no changes to project hooks/source."
