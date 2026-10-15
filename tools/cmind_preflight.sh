#!/usr/bin/env bash
# Isolated CoderMind preflight: no Checker codegen and no changes to this repo.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for cmd in python3 uv git; do
  command -v "$cmd" >/dev/null || { echo "Missing $cmd" >&2; exit 2; }
done
PIN="$(python3 - "$ROOT/tooling/versions.yaml" <<'PY'
import pathlib,re,sys
s=pathlib.Path(sys.argv[1]).read_text()
m=re.search(r"(?ms)^  rpg_zerorepo:\n(.*?)(?=^  [a-z_]+:|\Z)",s)
if not m: raise SystemExit("missing rpg_zerorepo source")
n=re.search(r"(?m)^    revision: ([0-9a-f]{40})$",m.group(1))
if not n: raise SystemExit("missing 40-character revision")
print(n.group(1))
PY
)"
CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
VENV="$CACHE/venvs/cmind-preflight"
mkdir -p "$CACHE/venvs" "$CACHE/runs"
if [[ -f "$VENV/pyvenv.cfg" && -x "$VENV/bin/python" ]]; then
  echo "Reusing CoderMind environment: $VENV"
elif [[ -e "$VENV" ]]; then
  echo "Incomplete venv at $VENV; inspect manually" >&2; exit 2
else
  uv venv --python python3.12 "$VENV"
fi
RUN="$(mktemp -d "$CACHE/runs/cmind-preflight.XXXXXX")"
trap 'status=$?; if ((status)); then echo "FAILED exit=$status; diagnostic files: '"$RUN"'" >&2; fi' EXIT
run() {
  label="$1"; shift
  echo "Running: $label"
  if ! "$@" >"$RUN/$label.stdout" 2>"$RUN/$label.stderr"; then
    echo "FAIL: $label" >&2
    tail -n 50 "$RUN/$label.stderr" >&2 || true
    tail -n 30 "$RUN/$label.stdout" >&2 || true
    return 1
  fi
}
run install uv pip install --quiet --python "$VENV/bin/python" \
  "git+https://github.com/microsoft/RPG-ZeroRepo.git@$PIN#subdirectory=CoderMind"
run provenance "$VENV/bin/python" - "$PIN" <<'PY'
import json,sys
from importlib.metadata import distribution
d=distribution("cmind-cli")
meta=json.loads(d.read_text("direct_url.json") or "{}")
actual=meta.get("vcs_info",{}).get("commit_id")
if actual != sys.argv[1]: raise SystemExit(f"Pinned SHA mismatch: {actual}")
print(json.dumps({"package":d.metadata["Name"],"version":d.version,"source_sha":actual}))
PY
run version "$VENV/bin/cmind" version
run scripts "$VENV/bin/cmind" script --list
# Scratch workspace only. Explicitly skip code encoding, MCP, git, and agent requirements.
run init bash -c 'cd "$1"; "$2" init cmind-fixture --ai claude --script sh --no-git --no-mcp --no-encode --ignore-agent-tools' \
  _ "$RUN" "$VENV/bin/cmind"
"$VENV/bin/python" - "$RUN" "$PIN" <<'PY'
from pathlib import Path
import json,sys
run=Path(sys.argv[1])
config=run/"cmind-fixture"/".cmind"/"config.toml"
if not config.is_file(): raise SystemExit("No scratch config.toml created")
summary={"status":"PREFLIGHT_PASS_AGENT_NOT_VERIFIED","source_sha":sys.argv[2],
         "scratch_config":True,"agent_auth":"NOT_TESTED",
         "rpg_generation":"NOT_TESTED","checker_implemented":False}
(run/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
PY
for name in claude copilot codex; do
  if command -v "$name" >/dev/null; then echo "$name: present (authentication unknown)"; else echo "$name: absent"; fi
done
"$VENV/bin/cmind" check >"$RUN/check.stdout" 2>"$RUN/check.stderr" || true
echo "CoderMind environment check saved: $RUN/check.stdout"
echo "Evidence: $RUN"
