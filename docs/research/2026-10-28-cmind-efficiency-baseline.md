# CoderMind efficiency baseline: archived Checker run

**Source:** [PR #27](https://github.com/lehater/agentic-checker-lab/pull/27), immutable repo evidence from 2026-10-16–20. This is a **retrospective observation**, not a new run or an equal-input controlled comparison.

| Stage | First RPG plan | Replanned after semantic drift |
| --- | ---: | ---: |
| Skeleton | 118.7 s | 146.8 s |
| Data flow | 94.4 s | 122.9 s |
| Base classes | 57.2 s | 62.6 s |
| Design interfaces | **640.3 s** | **634.4 s** |
| Tasks | 128.0 s | 151.1 s |
| Total | **1039.6 s** | **1118.8 s** |

Design interfaces accounts for ~61.6% / ~56.7% of planning elapsed time. Plan totals include overhead and do not necessarily equal the sum of stage timers. First plan was semantically rejected: port range, CLI and report contract drift. Second plan corrected those but still located `check()` under `domain/application`. Historical code generation subsequently required ~46.1 minutes, and upstream global review wasted 10 iterations on a screenshot requirement in a CLI application. The isolated review patch resolved that specific issue, not the architecture issue.

**Tokens/cost:** the frozen CoderMind manifest has `model_cost: null`, and the pinned CLI LLM adapter's `last_usage` returns zero placeholders. Do **not** interpret zero as zero consumption. Timing alone cannot establish tokens, API cost or subscription quota.

## Proposed measurement

`tools/analyze_run.py` parses CoderMind plan stdout, optional CoderMind trajectory summaries and independently captured Codex `turn.completed` JSONL events. It records token fields as `null/UNKNOWN` unless real usage is present, then `PARTIAL` until an externally verified expected number of turns is supplied. Cached tokens are a subset of input tokens; never double count. The offline parser is intentionally separate from modifying CoderMind/Codex's actual execution wrapper.

Example (using existing local log when available):

```sh
python3 tools/analyze_run.py --run-id baseline-1 \
  --plan-log /path/to/plan.stdout \
  --codex-jsonl /path/to/sanitized-codex.jsonl \
  --output /tmp/observation.json
```

Do not commit raw prompts/session files without privacy review. Record model/version/host metadata outside the parser and align all turns to a fixed run/task/stage before claiming precise stage-level token attribution.

## Highest-value next tests

1. Validate the RPG skeleton before spending ~10 minutes in interface design.
2. Instrument actual Codex CLI invocations with structured event capture (requires local environment) and correlate stage/task IDs.
3. Apply a bounded retry/review stop policy and compare objective quality against baseline.
4. Compare direct Codex with CoderMind under a common accepted specification before deciding if RPG has marginal value.
