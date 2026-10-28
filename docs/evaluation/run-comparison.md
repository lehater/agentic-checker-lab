# Offline process and model comparison — NOT a model router

The evaluator at ../../tools/compare_runs.py accepts manually collected, independently verified E2E run records, or synthetic fixtures used only to test its policy logic.

Minimum requirements for a *measured* comparison:
- Same accepted specification SHA, frozen independent oracle SHA, declared budget ID and environment ID.
- At least two actual observed repetitions per arm.
- Every outcome independently verified against the same acceptance and architecture checks.
- Complete elapsed seconds per run. Known failures block; unknown checks are inconclusive.
- Report model/config hash, class and run identifiers; token totals may be UNKNOWN (null), never converted to zero.

A candidate efficiency winner is selected only from complete observed experiments; confidence remains NOT_STATISTICALLY_ESTABLISHED until a proper study. No automatic cloud/local routing, cost, token/quota or quality gain is inferred.

Fixture runs always report SIMULATED_ONLY and cannot generate a real recommendation. Use:

    python3 tools/compare_runs.py --input /path/to/verified-run-records.json --minimum-per-arm 2 --minimum-gain 0.05

The minimum-gain threshold is an explicit operator decision, not a scientifically measured constant. Report all blocked or incomplete runs.

**Local executor responsibilities:** collect the genuine Codex and CoderMind run outcomes, independently execute accepted oracle, record session+model+budget metadata, and obtain owner permission before adaptive routing. Never run an unverified experiment from GitHub Actions with subscription credentials.
