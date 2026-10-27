# Success criteria — current research

**Owner-directed proposed revision (2026-10-28).** Define comparison budgets/thresholds before model experiments, not after.

| ID | Objective | Independent evidence |
| --- | --- | --- |
| K-01 | One accepted and bounded Checker specification, explicit unknowns | Human-reviewed source, requirements, domain, design and negative scenarios |
| K-02 | Clean Architecture remains intact through RPG and codegen | Static dependency/role test rejects historical domain/application defect; valid graph/code passes |
| K-03 | SOLID/KISS/YAGNI do not regress into needless abstraction | Reviewed responsibilities, alternatives, justified components; record additions and overrides |
| K-04 | Product semantics not silently overridden by a model | Conflict case, frozen oracle and documented decision trail |
| K-05 | Correct Checker outcome | Critical independent cases PASS; no invented verdict, device operations or unsupported source |
| K-06 | Observable efficiency | Per-stage duration, tokens if verified, retries, quality failures, human edits; missing telemetry reported UNKNOWN |
| K-07 | Method comparison: same specs → direct Codex vs RPG/CoderMind+Codex | Source SHA, frozen model/config/budget, same oracle, comparable runs |
| K-08 | Local/cloud selection does not degrade quality or time | Controlled comparison of time-to-verified-result and quota consumption |
| K-09 | Repeatable specification change and portability | Before/after impact + independent tests on Checker and one separate task |

No success claims from green generated tests, volume of RPG artifacts or an LLM self-assessed review alone. Historical Harness-centered criteria are superseded for new experiments; historical evidence stays available in git history/PR #27.

**GO:** quality gates met, improved efficiency/traceability proven in controlled scope. **CONDITIONAL GO:** usable with bounded fixes. **NO-GO:** critical drift, unacceptable cost/time or no proven marginal benefit. **INCONCLUSIVE/BLOCKED:** insufficient evidence/tool access.
