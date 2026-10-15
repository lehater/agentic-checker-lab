#!/usr/bin/env bash
# Staged synthetic forward RPG probe. Model calls are opt-in.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ACTION="${1:-status}"
case "$ACTION" in init|phase1|skeleton|status|export) ;; *) echo "Unknown action: $ACTION" >&2; exit 2;; esac
if [[ -n "${CMIND_CODEX_BYPASS_SANDBOX:-}" ]]; then
  echo "Unset CMIND_CODEX_BYPASS_SANDBOX before proceeding." >&2; exit 2
fi
CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
VENV="$CACHE/venvs/cmind-codex-pr96"
CMIND="$VENV/bin/cmind"
PY="$VENV/bin/python"
RUN="$CACHE/runs/rpg-synthetic-v1"
WORK="$RUN/workspace"
FIXTURE="$ROOT/tooling/fixtures/rpg-synthetic/requirements.md"
[[ -x "$CMIND" && -x "$PY" ]] || { echo "First run make cmind-codex-smoke" >&2; exit 2; }
PIN="$(python3 - "$ROOT/tooling/versions.yaml" <<'PYCODE'
from pathlib import Path
import re,sys
s=Path(sys.argv[1]).read_text()
m=re.search(r'(?ms)^  rpg_codex_pr96_candidate:\n(.*?)(?=^  [a-z_]+:|\Z)',s)
if not m: raise SystemExit("Missing candidate source")
r=re.search(r'(?m)^    revision: ([0-9a-f]{40})$',m.group(1))
if not r: raise SystemExit("Missing candidate revision")
print(r.group(1))
PYCODE
)"
"$PY" - "$PIN" <<'PYCODE'
import json,sys
from importlib.metadata import distribution
d=distribution("cmind-cli")
src=json.loads(d.read_text("direct_url.json") or "{}").get("vcs_info",{}).get("commit_id")
if src!=sys.argv[1]: raise SystemExit("CoderMind installed SHA disagrees with candidate pin")
PYCODE
DATA="$("$PY" - "$WORK" <<'PYCODE'
from cmind_cli._storage import workspace_data_dir
from pathlib import Path
import sys
print(workspace_data_dir(Path(sys.argv[1])))
PYCODE
)"
if [[ "$ACTION" == "status" ]]; then
  "$PY" - "$WORK" "$DATA" <<'PYCODE'
import json,sys
from pathlib import Path
w,d=map(Path,sys.argv[1:])
print(json.dumps({"workspace":str(w),"data_dir":str(d),
 "initialized":(w/".cmind/config.toml").is_file(),
 "files":{n:(d/(n+".json")).is_file() for n in
 ("feature_spec","feature_build","feature_tree","skeleton","rpg")}},indent=2))
PYCODE
  exit 0
fi
mkdir -p "$RUN"
step() {
  label="$1"; shift
  echo "Running: $label"
  if "$@" >"$RUN/$label.stdout" 2>"$RUN/$label.stderr"; then
    tail -n 12 "$RUN/$label.stdout" || true
  else
    echo "FAILED: $label" >&2
    tail -n 35 "$RUN/$label.stderr" >&2 || true
    tail -n 12 "$RUN/$label.stdout" >&2 || true
    echo "Local evidence: $RUN" >&2
    exit 1
  fi
}
initialize() {
  if [[ -f "$WORK/.cmind/config.toml" ]]; then
    cmp -s "$FIXTURE" "$WORK/docs/requirements.md" || {
      echo "Fixture changed since init; stop and inspect." >&2; exit 3;
    }
    return
  fi
  [[ ! -e "$WORK" ]] || { echo "Incomplete existing workspace: $WORK" >&2; exit 3; }
  (cd "$RUN"; step init "$CMIND" init workspace --ai codex --script sh --no-git --no-mcp --no-encode --ignore-agent-tools)
  mkdir -p "$WORK/docs"
  cp "$FIXTURE" "$WORK/docs/requirements.md"
}
initialize
if [[ "$ACTION" == "init" ]]; then echo "INITIALIZED_NO_MODEL_CALLS: $WORK"; exit 0; fi
export PATH="$VENV/bin:$PATH"
export CMIND_AI_CLI_CMD="codex exec"
if [[ "$ACTION" == "phase1" ]]; then
  (cd "$WORK"; step feature-spec cmind script feature_spec.py --docs "$WORK/docs")
  (cd "$WORK"; step feature-construct cmind script feature_construct.py --review-max-iterations 1 --max-iter-refactor 3)
  [[ -s "$DATA/feature_tree.json" ]] || { echo "Missing feature_tree.json" >&2; exit 4; }
  echo "PHASE1_COMPLETE: $DATA"
elif [[ "$ACTION" == "skeleton" ]]; then
  [[ -s "$DATA/feature_tree.json" ]] || { echo "First run phase1." >&2; exit 4; }
  if [[ ! -s "$DATA/rpg.json" || ! -s "$DATA/skeleton.json" ]]; then
    (cd "$WORK"; step build-skeleton cmind script build_skeleton.py --max-iterations 2)
  fi
  (cd "$WORK"; step check-skeleton cmind script check_skeleton.py)
  "$PY" - "$DATA/rpg.json" <<'PYCODE'
import json,sys
from pathlib import Path
f=Path(sys.argv[1]); j=json.loads(f.read_text(encoding="utf-8"))
if not isinstance(j,dict) or not j: raise SystemExit("RPG JSON is invalid/empty")
print("INITIAL_RPG_JSON_VALID:",f,"bytes:",f.stat().st_size)
PYCODE
elif [[ "$ACTION" == "export" ]]; then
  [[ "$(git -C "$ROOT" branch --show-current)" != "main" ]] || {
    echo "Do not export in main." >&2; exit 5;
  }
  DEST="$ROOT/experiments/runs/rpg-synthetic-v1"
  [[ ! -e "$DEST" ]] || { echo "Export exists, refusing overwrite: $DEST" >&2; exit 5; }
  for n in feature_spec feature_build feature_tree skeleton rpg; do
    [[ -s "$DATA/$n.json" ]] || { echo "Missing $n.json; no partial export." >&2; exit 4; }
  done
  mkdir -p "$DEST"
  for n in feature_spec feature_build feature_tree skeleton rpg; do cp "$DATA/$n.json" "$DEST/"; done
  "$PY" - "$DEST" "$PIN" "$FIXTURE" "$(git -C "$ROOT" rev-parse HEAD)" <<'PYCODE'
import hashlib,json,sys
from pathlib import Path
d,pin,fixture,sha=Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3]),sys.argv[4]
files=sorted(d.glob("*.json"))
for f in files: json.loads(f.read_text(encoding="utf-8"))
manifest={"schema":"synthetic-forward-rpg/v1","status":"EXPORTED_UNREVIEWED",
 "cmind_revision":pin,"repository_revision_at_export":sha,
 "fixture_sha256":hashlib.sha256(fixture.read_bytes()).hexdigest(),
 "files":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(d/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print("EXPORTED_FOR_REVIEW:",d)
PYCODE
  echo "Inspect generated JSON before git add/commit/push; no automatic Git operations."
fi
