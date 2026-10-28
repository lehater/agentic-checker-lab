#!/usr/bin/env python3
"""Compare independent, bounded E2E run records without inventing model quality.

Returns simulation-only output for synthetic fixtures; never recommends routing
without complete measured acceptance and comparable budgets/inputs.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import statistics

VALID_CHECKS = {"PASS", "FAIL", "UNKNOWN"}


def compare(data: dict, minimum_per_arm: int = 2, minimum_gain: float = 0.0) -> dict:
    if data.get("schema") != "checker-lab/run-comparison/v1":
        raise ValueError("unsupported comparison schema")
    if minimum_per_arm < 2 or not 0 <= minimum_gain < 1:
        raise ValueError("repetition count must be >=2 and minimum gain in [0,1)")
    runs = data.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("no run records")
    seen, keys, groups = set(), set(), defaultdict(list)
    missing = []
    for r in runs:
        if not isinstance(r, dict):
            raise ValueError("non-object run record")
        ident = r.get("run_id")
        if not isinstance(ident, str) or not ident or ident in seen:
            raise ValueError("missing or duplicated run id")
        seen.add(ident)
        for name in ("arm", "spec_sha", "oracle_sha", "budget_id", "environment_id", "model_config_sha"):
            if not isinstance(r.get(name), str) or not r[name]:
                raise ValueError(f"{ident}: missing immutable context {name}")
        if r.get("record_class") not in {"fixture", "observed"}:
            raise ValueError(f"{ident}: record class must be fixture or observed")
        if r.get("quality") not in VALID_CHECKS or r.get("architecture") not in VALID_CHECKS:
            raise ValueError(f"{ident}: invalid independent check status")
        if r.get("verified_by") not in {"independent-tests", "not-verified"}:
            raise ValueError(f"{ident}: verification provenance required")
        elapsed = r.get("elapsed_seconds")
        if elapsed is not None and (type(elapsed) not in (int, float) or elapsed <= 0):
            raise ValueError(f"{ident}: invalid elapsed time")
        if r.get("verified_by") != "independent-tests" and (
                r["quality"] == "PASS" or r["architecture"] == "PASS"):
            raise ValueError(f"{ident}: unverified positive gate")
        for fld in ("input_tokens", "output_tokens"):
            val = r.get(fld)
            if val is not None and (type(val) is not int or val < 0):
                raise ValueError(f"{ident}: invalid {fld}")
        keys.add((r["spec_sha"], r["oracle_sha"], r["budget_id"], r["environment_id"]))
        groups[r["arm"]].append(r)
        if elapsed is None or "UNKNOWN" in (r["quality"], r["architecture"]):
            missing.append(ident)
    if len(groups) < 2:
        raise ValueError("at least two arms required")
    comparable = len(keys) == 1
    sample = {arm: {"runs": len(items),
                    "median_seconds": statistics.median([r["elapsed_seconds"] for r in items])
                    if all(r["elapsed_seconds"] is not None for r in items) else None,
                    "quality_passed": sum(r["quality"] == "PASS" for r in items),
                    "architecture_passed": sum(r["architecture"] == "PASS" for r in items)}
              for arm, items in sorted(groups.items())}
    all_observed = all(r["record_class"] == "observed" for r in runs)
    all_complete = all(r["elapsed_seconds"] is not None and
                       r["verified_by"] == "independent-tests" and
                       r["quality"] != "UNKNOWN" and
                       r["architecture"] != "UNKNOWN" for r in runs)
    enough = all(len(group) >= minimum_per_arm for group in groups.values())
    any_failure = any(r["quality"] == "FAIL" or r["architecture"] == "FAIL" for r in runs)
    winner = None
    reason = "Insufficient independent runtime evidence for routing/optimization"
    status = "INCONCLUSIVE"
    if not comparable:
        reason = "Different specification, oracle, budget or environment; comparison invalid"
    elif any_failure:
        status = "NO_GO"
        reason = "At least one candidate failed frozen quality or architecture checks"
    elif not enough:
        reason = "Too few comparable repetitions per arm"
    elif not all_complete:
        reason = "Measured time or independently verified checks are incomplete"
    elif not all_observed:
        status = "SIMULATED_ONLY"
        reason = "Fixture data demonstrate policy, not live model performance"
    else:
        sorted_arms = sorted(sample, key=lambda arm: sample[arm]["median_seconds"])
        best, second = sorted_arms[:2]
        gain = (sample[second]["median_seconds"] - sample[best]["median_seconds"]) / sample[second]["median_seconds"]
        status = "MEASURED_COMPARISON"
        reason = "Quality gates passed; compared median times at declared identical context"
        if gain > minimum_gain:
            winner = best
        else:
            reason += "; gain is below declared minimum"
    return {"schema": "checker-lab/comparison-result/v1", "status": status,
            "routing_candidate": winner, "confidence": "NOT_STATISTICALLY_ESTABLISHED",
            "comparable_context": comparable, "all_observed": all_observed,
            "all_complete": all_complete, "minimum_per_arm": minimum_per_arm,
            "minimum_gain": minimum_gain, "arms": sample, "reason": reason,
            "token_cost_verified": False,
            "note": "No billing/quota inference, no live routing; independent repetition and paired analysis are still required."}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--minimum-per-arm", type=int, default=2)
    p.add_argument("--minimum-gain", type=float, default=0.0)
    args = p.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = compare(data, args.minimum_per_arm, args.minimum_gain)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] in {"SIMULATED_ONLY", "MEASURED_COMPARISON"} else 1
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "INVALID", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
