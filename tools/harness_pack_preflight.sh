#!/usr/bin/env bash
# TASK-004: Pinned Harness Consumer Pack bootstrap and route/isolation preflight.
# Opt-in execution: may fetch the pinned Harness commit and install pinned PyYAML
# into a dedicated ~/.cache/harness bootstrap venv. No LLM or target Git edits.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
RUN_ROOT="$CACHE/runs"
mkdir -p "$RUN_ROOT"
RUN="$(mktemp -d "$RUN_ROOT/harness-consumer-pack.XXXXXX")"
echo "Routing evidence: $RUN"
python3 "$ROOT/.harness/harnessw.py" sync \
  --binding "$ROOT/.harness/harness-binding.json" \
  > "$RUN/sync.stdout" 2> "$RUN/sync.stderr" || {
    echo "Harness Consumer Pack sync failed. See $RUN/sync.stderr" >&2
    tail -n 40 "$RUN/sync.stderr" >&2
    exit 2
  }
PACK="$(tail -n 1 "$RUN/sync.stdout")"
[[ -d "$PACK" && -f "$PACK/harness-consumer-pack.yaml" ]] || {
  echo "Missing materialized pack directory: $PACK" >&2; exit 3
}
python3 - "$ROOT/.harness/harness-binding.json" "$PACK" <<'PY'
import json,sys
from pathlib import Path
pin=json.loads(Path(sys.argv[1]).read_text())["source"]["revision"]
pack=Path(sys.argv[2])
if pack.name!=pin or pack.parent.name!="v1":
    raise SystemExit(f"Unexpected pack version location: {pack}")
for rel in ("skills/maintainer-operation-registry-v0.yaml","skills/maintainer","tests"):
    if (pack/rel).exists():
        raise SystemExit(f"Forbidden maintainer/test surface present: {rel}")
PY
# Use the existing pinned lab Python venv, not any global Harness package.
PYTHON="$CACHE/venvs/harness-smoke/bin/python"
[[ -x "$PYTHON" ]] || {
    echo "Pinned lab Python environment missing; run make harness-smoke first." >&2
    exit 2
}
export PYTHONPATH="$PACK/src:$PACK"
pushd "$PACK" >/dev/null
"$PYTHON" -m harness.application.consumer_pack validate-pack "$PACK" \
  --revision "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["source"]["revision"])' "$ROOT/.harness/harness-binding.json")" \
  --consumer-api v1 > "$RUN/pack-validation.json"
for operation in project-bootstrap-reconcile design-profile decision-pipeline project-engineering-status; do
  echo "Consumer operation: $operation"
  "$PYTHON" -m harness.application.skill_router operation \
    --surface consumer --operation "$operation" --root "$PACK" \
    > "$RUN/operation-$operation.json"
done
for kind in problem-evidence product-requirements verification-strategy test-design implementation-design; do
  echo "Artifact route: $kind"
  "$PYTHON" -m harness.application.skill_router artifact \
    --knowledge-kind "$kind" --root "$PACK" \
    > "$RUN/artifact-$kind.json"
done
# Maintainer procedures must be physically absent, not just unused.
if "$PYTHON" -m harness.application.skill_router operation \
    --surface maintainer --operation harness-audit --root "$PACK" \
    > "$RUN/forbidden-route.stdout" 2> "$RUN/forbidden-route.stderr"; then
  echo "Maintainer route unexpectedly available in Consumer Pack!" >&2
  exit 4
fi
popd >/dev/null
python3 - "$RUN" "$PACK" "$ROOT/.harness/harness-binding.json" <<'PY'
import json,sys
from pathlib import Path
run,pack,binding=map(Path,sys.argv[1:])
pin=json.loads(binding.read_text())["source"]["revision"]
val=json.loads((run/"pack-validation.json").read_text())
if val!={"status":"VALID","consumer_api":"v1"}:
    raise SystemExit(f"Invalid Consumer Pack validation: {val}")
paths=[]
for prefix,keyfield,names in [
    ("operation","route_key",["project-bootstrap-reconcile","design-profile","decision-pipeline","project-engineering-status"]),
    ("artifact","route_key",["problem-evidence","product-requirements","verification-strategy","test-design","implementation-design"]),
]:
    for name in names:
        route=json.loads((run/f"{prefix}-{name}.json").read_text())
        if route.get(keyfield)!=name or route.get("surface")!="consumer":
            raise SystemExit(f"Unexpected route for {name}: {route}")
        contracts=route.get("instruction_contracts")
        if not isinstance(contracts,list) or not contracts:
            raise SystemExit(f"Missing instruction contracts on {name}")
        for path in [route.get("skill"),*contracts]:
            if not isinstance(path,str):
                raise SystemExit(f"Invalid route file path for {name}")
            resolved=(pack/path).resolve()
            if not resolved.is_relative_to(pack.resolve()) or not resolved.is_file():
                raise SystemExit(f"Route references missing/escaping file: {path}")
        paths.append(name)
report={
    "status":"CONSUMER_PACK_PREFLIGHT_PASS_ONLY",
    "consumer_api":"v1",
    "harness_sha":pin,
    "pack_path":str(pack),
    "routes_verified":paths,
    "maintainer_route_unavailable":True,
    "checker_problem_accepted":False,
    "agent_workflow_executed":False,
    "model_calls":0,
}
(run/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
PY
