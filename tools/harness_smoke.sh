#!/usr/bin/env bash
# P1/TASK-002: deterministic Harness integration smoke on Ubuntu.
# Does not alter the checker source, merge branches or commit generated files.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if ! command -v python3 >/dev/null; then
  echo "ERROR: python3 required (Harness: Python >=3.10)." >&2
  exit 2
fi
if ! command -v uv >/dev/null; then
  echo "ERROR: uv is required. See tooling/README.md (do not install without reviewing)." >&2
  exit 2
fi
if ! command -v git >/dev/null; then
  echo "ERROR: git required." >&2
  exit 2
fi

# Pin is read only from the existing canonical tooling declaration.
PIN="$(python3 - "$ROOT/tooling/versions.yaml" <<'PY'
import pathlib, re, sys
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
section = re.search(r"(?ms)^  harness:\n(.*?)(?=^  [a-z_]+:|\Z)", text)
if not section:
    raise SystemExit("Cannot locate harness source pin")
match = re.search(r"(?m)^    revision: ([0-9a-f]{40})$", section.group(1))
if not match:
    raise SystemExit("Missing 40-character Harness SHA")
print(match.group(1))
PY
)"

CACHE="${CHECKER_LAB_TOOL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/agentic-checker-lab}"
CHECKOUT="$CACHE/sources/harness-$PIN"
VENV="$CACHE/venvs/harness-smoke"
mkdir -p "$(dirname "$CHECKOUT")" "$CACHE/venvs" "$CACHE/runs"

if [[ ! -d "$CHECKOUT/.git" ]]; then
  git clone --quiet https://github.com/lehater/harness.git "$CHECKOUT"
fi
git -C "$CHECKOUT" -c advice.detachedHead=false checkout --quiet --detach "$PIN"
ACTUAL="$(git -C "$CHECKOUT" rev-parse HEAD)"
if [[ "$ACTUAL" != "$PIN" ]]; then
  echo "ERROR: Harness checkout does not match pinned revision" >&2
  exit 3
fi

uv venv --python python3 "$VENV"
uv pip install --quiet --python "$VENV/bin/python" "PyYAML==6.0.3"
PYTHON="$VENV/bin/python"
export PYTHONPATH="$CHECKOUT/src"
RUN="$(mktemp -d "$CACHE/runs/harness-smoke.XXXXXX")"
GRAPH="$ROOT/tooling/fixtures/harness-smoke/engineering-graph.yaml"
CORE="$ROOT/tooling/fixtures/harness-smoke/core.yaml"

"$PYTHON" -m harness.project_model.engineering_graph validate "$GRAPH" >"$RUN/validate.json"
"$PYTHON" -m harness.project_model.engineering_graph profile "$GRAPH" TOOLCHAIN-SMOKE >"$RUN/profile.json"
"$PYTHON" -m harness.project_model.engineering_graph evaluate "$GRAPH" TOOLCHAIN-SMOKE "$CORE" >"$RUN/evaluate.json"
"$PYTHON" -m harness.application.graph_doctor "$GRAPH" \
  --core-model "$CORE" --target TOOLCHAIN-SMOKE --source-root "$ROOT" --json >"$RUN/doctor.json"

"$PYTHON" - "$RUN" "$PIN" <<'PY'
import json
from pathlib import Path
import sys
run, pin = Path(sys.argv[1]), sys.argv[2]
load = lambda name: json.loads((run / name).read_text())
validated = load("validate.json")
evaluated = load("evaluate.json")
doctor = load("doctor.json")
if validated.get("valid") is not True:
    raise SystemExit("FAIL: Harness graph validation")
if evaluated.get("status") != "READY":
    raise SystemExit(f"FAIL: expected READY, got {evaluated.get('status')!r}")
if evaluated.get("implementation_consumer") is not False:
    raise SystemExit("FAIL: smoke graph falsely classified as implementation authorization")
created = {item["capability"] for item in evaluated["create"]}
if created != {"checker-lab.smoke.verification"}:
    raise SystemExit(f"FAIL: unexpected CREATE set: {created!r}")
if not evaluated.get("satisfied"):
    raise SystemExit("FAIL: synthetic problem evidence not satisfied")
if doctor.get("summary", {}).get("ERROR") != 0:
    raise SystemExit(f"FAIL: Graph Doctor errors: {doctor.get('findings')!r}")
summary = {
    "status": "PASS",
    "scope": "synthetic-toolchain-only",
    "harness_sha": pin,
    "evaluation_status": evaluated["status"],
    "create_capabilities": sorted(created),
    "doctor_errors": doctor["summary"]["ERROR"],
    "source_of_truth": "tooling/versions.yaml",
    "checker_implemented": False,
}
(run / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
PY
printf '\nOutput artifacts: %s\n' "$RUN"
printf 'NOTE: This is only a local toolchain smoke test. Capture the run evidence in the TASK-002 PR.\n'
