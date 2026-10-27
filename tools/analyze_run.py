#!/usr/bin/env python3
"""Offline, read-only CoderMind/Codex run telemetry summarizer.

No LLM calls. Does NOT infer token totals from elapsed time or character count.
Use --expected-turns only when externally verified to make completeness claims.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

STAGE = re.compile(r"^[✓✔]\s+([a-z_]+)\s+done in\s+([\d.]+)s", re.M)
TOTAL = re.compile(r"Plan complete in\s+([\d.]+)s")
STRUCTURED = re.compile(r"LLM structured call successful")
REVIEW = re.compile(r"\[InterfaceReviewer\] Review iteration\s+(\d+)/(\d+)")


def parse_plan(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    stage_seconds: dict[str, float] = {}
    attempts: Counter[str] = Counter()
    for name, duration in STAGE.findall(text):
        stage_seconds[name] = round(stage_seconds.get(name, 0) + float(duration), 3)
        attempts[name] += 1
    totals = TOTAL.findall(text)
    warnings = sum(1 for line in text.splitlines() if "WARNING" in line)
    errors = sum(1 for line in text.splitlines() if "ERROR" in line)
    iterations = [int(x) for x, _ in REVIEW.findall(text)]
    return {
        "stage_seconds": stage_seconds,
        "stage_attempts": dict(attempts),
        "total_seconds": float(totals[-1]) if totals else None,
        "total_seconds_source": "CoderMind stdout" if totals else "UNKNOWN",
        "structured_llm_success_lines": len(STRUCTURED.findall(text)),
        "interface_review_iterations_logged": max(iterations) if iterations else None,
        "warning_lines": warnings,
        "error_lines": errors,
    }


def parse_trajectories(paths: list[Path]) -> dict:
    interactions = 0
    successful = 0
    durations: list[float] = []
    for path in paths:
        obj = json.loads(path.read_text(encoding="utf-8"))
        steps = obj.get("steps", [])
        if not isinstance(steps, list):
            raise ValueError(f"{path}: trajectory steps must be a list")
        for step in steps:
            for call in step.get("llm_interactions", []):
                interactions += 1
                if call.get("success"):
                    successful += 1
                if isinstance(call.get("duration_seconds"), (int, float)):
                    durations.append(float(call["duration_seconds"]))
    return {
        "trajectory_recorded_interactions": interactions,
        "trajectory_successful_interactions": successful,
        "trajectory_llm_duration_seconds": round(sum(durations), 3) if durations else None,
    }


def _int_or_none(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def parse_codex(paths: list[Path], expected_turns: int | None) -> dict:
    completed: list[dict] = []
    invalid_json = 0
    for path in paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            if not isinstance(event, dict):
                invalid_json += 1
                continue
            if event.get("type") == "turn.completed":
                completed.append(event.get("usage") if isinstance(event.get("usage"), dict) else {})
    fields = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
    metrics: dict[str, int | None] = {}
    for field in fields:
        vals = [_int_or_none(event.get(field)) for event in completed]
        metrics[field] = sum(vals) if vals and all(v is not None for v in vals) else None

    usable = sum(1 for event in completed if _int_or_none(event.get("input_tokens")) is not None
                 and _int_or_none(event.get("output_tokens")) is not None)
    if not completed or usable == 0:
        status = "UNKNOWN"
    elif expected_turns is not None and len(completed) == expected_turns and usable == len(completed):
        status = "COMPLETE_WITH_DECLARED_EXPECTATION"
    else:
        status = "PARTIAL"

    return {
        "usage_status": status,
        "observed_completed_turns": len(completed),
        "turns_with_input_and_output_usage": usable,
        "expected_turns": expected_turns,
        **metrics,
        "total_input_plus_output_tokens": (
            metrics["input_tokens"] + metrics["output_tokens"]
            if metrics["input_tokens"] is not None and metrics["output_tokens"] is not None else None
        ),
        "cost_usd": None,
        "cost_note": "Subscription/API billing not measured; cached tokens are a subset of input and must not be added twice.",
        "note": "No automatic guarantee that all Codex invocations of this run were exported."
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-id", required=True)
    p.add_argument("--plan-log", type=Path, action="append", default=[])
    p.add_argument("--codex-jsonl", type=Path, action="append", default=[])
    p.add_argument("--trajectory", type=Path, action="append", default=[])
    p.add_argument("--expected-turns", type=int, help="Externally verified count of Codex turns, never guessed")
    p.add_argument("--output", type=Path, help="Write result to file instead of stdout")
    args = p.parse_args()
    if not (args.plan_log or args.codex_jsonl or args.trajectory):
        p.error("provide at least one --plan-log, --codex-jsonl or --trajectory")
    if args.expected_turns is not None and args.expected_turns <= 0:
        p.error("--expected-turns must be positive")
    try:
        plan_reports = [parse_plan(path) for path in args.plan_log]
        trajectory = parse_trajectories(args.trajectory) if args.trajectory else None
        llm = parse_codex(args.codex_jsonl, args.expected_turns)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        p.exit(2, f"telemetry input error: {exc}\n")
    report = {
        "schema": "checker-lab/telemetry/v1",
        "run_id": args.run_id,
        "plan_logs": [str(path) for path in args.plan_log],
        "coder_mind_plans": plan_reports,
        "trajectory": trajectory,
        "codex_jsonl": [str(path) for path in args.codex_jsonl],
        "llm": llm,
        "scope": "Observed local artifacts only; no live calls or correctness/architecture verdict.",
    }
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
