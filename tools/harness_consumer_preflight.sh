#!/usr/bin/env bash
# TASK-004: read-only routing preflight for the pinned Harness consumer.
# Does not invoke any LLM, accept Checker semantics, or mutate Harness/project Git.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
PIN="$(python3 - "$ROOT/tooling/versions.yaml" <<'PY'
from pathlib import Path
import re, sys
data=Path(sys.argv[1]).read_text(encoding="utf-8")
section=re.search(r"(?ms)^  harness:\n(.*?)(?=^  [a-z_]+:|\Z)", data)
if not section: raise SystemExit("Missing harness source pin")
match=re.search(r"(?m)^    revision: ([0-9a-f]{40})$", section.group(1))
if not match: raise SystemExit("Missing pinned Harness SHA")
print(match.group(1))
PY
)"
CHECKOUT="$CACHE/sources/harness-$PIN"
PYTHON="$CACHE/venvs/harness-smoke/bin/python"
[[ -d "$CHECKOUT/.git" && -x "$PYTHON" ]] || {
  echo "Pinned Harness checkout or venv missing. First run: make harness-smoke" >&2
  exit 2
}
actual="$(git -C "$CHECKOUT" rev-parse HEAD)"
[[ "$actual" == "$PIN" ]] || {
  echo "Pinned Harness checkout changed: $actual != $PIN" >&2
  exit 3
}
[[ -z "$(git -C "$CHECKOUT" status --porcelain --untracked-files=no)" ]] || {
  echo "Pinned Harness checkout has modifications; refusing source-derived routing." >&2
  exit 3
}
mkdir -p "$CACHE/runs"
RUN="$(mktemp -d "$CACHE/runs/harness-consumer-routing.XXXXXX")"
export PYTHONPATH="$CHECKOUT/src"
declare -A OPS=(
  [bootstrap]=project-bootstrap-reconcile
  [profile]=design-profile
  [pipeline]=decision-pipeline
)
for label in bootstrap profile pipeline; do
  echo "Route operation: ${OPS[$label]}"
  "$PYTHON" -m harness.application.skill_router operation \
    --surface consumer --operation "${OPS[$label]}" --root "$CHECKOUT" \
    > "$RUN/op-$label.json"
done
for kind in problem-evidence product-requirements verification-strategy test-design implementation-design; do
  echo "Route artifact: $kind"
  "$PYTHON" -m harness.application.skill_router artifact \
    --knowledge-kind "$kind" --root "$CHECKOUT" \
    > "$RUN/artifact-$kind.json"
done
"$PYTHON" - "$RUN" "$PIN" "$CHECKOUT" <<'PY'
from pathlib import Path
import json,sys
run,pin,root=Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3])
expected={
    "op-bootstrap.json": ("operation","project-bootstrap-reconcile"),
    "op-profile.json": ("operation","design-profile"),
    "op-pipeline.json": ("operation","decision-pipeline"),
}
expected.update({
    f"artifact-{kind}.json": ("artifact-production",kind)
    for kind in ("problem-evidence","product-requirements","verification-strategy","test-design","implementation-design")
})
routed=[]
for filename,(route_class,key) in expected.items():
    data=json.loads((run/filename).read_text(encoding="utf-8"))
    if data.get("route_class")!=route_class or data.get("route_key")!=key:
        raise SystemExit(f"Unexpected route in {filename}: {data}")
    if data.get("surface")!="consumer":
        raise SystemExit(f"Non-consumer route in {filename}")
    skill=data.get("skill")
    if not isinstance(skill,str) or not skill.endswith("/SKILL.md"):
        raise SystemExit(f"Missing skill path for {filename}")
    target=(root/skill).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise SystemExit(f"Missing/out-of-root skill for {filename}: {skill}")
    routed.append({"key":key,"skill":skill})
summary={
    "status":"ROUTING_PREFLIGHT_PASS_ONLY",
    "harness_sha":pin,
    "checked_routes":routed,
    "checker_problem_accepted":False,
    "harness_workflow_executed":False,
    "consumer_closure_verified":False,
    "model_calls":0,
}
(run/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,ensure_ascii=False))
PY
printf "Local routing evidence: %s\n" "$RUN"
