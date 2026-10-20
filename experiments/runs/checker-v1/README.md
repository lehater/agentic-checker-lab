# Checker v1 — verified synthetic prototype

Date: 2026-10-20. Base: `origin/main` at `2bf23ce`.
Owner input: [problem brief](../../../docs/scenario/owner-problem-brief.md).
Product usage and limits: [Checker](../../../docs/checker/README.md).
The [2026-10-16 checkpoint](checkpoint.md) is historical; current results are below.

## Verified result

| Boundary | Actual evidence |
| --- | --- |
| Harness knowledge | 12 capabilities CURRENT; CHECKER-PROTOTYPE closure, coverage, roadmap and frontier COMPLETE; verification.json |
| Native generation | 30/30 tasks, 0 failed; native-codegen-status.json and native-codegen.stdout |
| Native final test | 197 passed, 0 failed/errors, imports/entrypoint/stub smoke PASS; native-final-test.json |
| Native review, unchanged upstream | FAIL after 10 iterations because visual guard unconditionally requires pages/screenshots for CLI; native-global-review-upstream.json |
| Native review, isolated local patch | PASS, 5/5 functional groups, post-pytest PASS, no stubs; native-global-review.json; ADR-0004 |
| Exported native suite | 197 passed in reconstructed temporary workspace against repository runtime; 2 runpy warnings from repeated module execution in generated tests; native-provenance.json |
| Independent oracle | 10 methods PASS, including 15 pre-code scenarios, strict failures, complete original rule/placement data and source substitution; TD-*-execution.json |
| Test Design realization | Both TD contracts ACCEPTED, every OP/OR covered; TD-*-conformance.json; missing-operation/failed-execution negatives rejected |
| Oracle sensitivity | Baseline passes; 6 semantic mutants detected; source unchanged; mutations.json |
| Trace | All four requirements bound to actual RPG feature IDs, existing function symbols, file hashes and independent contracts; traceability.json |
| Publication safety | Schema/currentness PASS; stale CAS, false acceptance identity and changed bridge input rejected; verification.json and bridge-verification.json |

Sources are copied without changes from native commit
`956fd748da803bfa3031a7acc9debc64e3b2bf22`; all runtime file hashes are in
native-provenance.json. Completion evidence is bound to current source/contracts,
checks and publication by completion.json and tools/check_checker_evidence.py.
Actual PR CI/owner review is a separate integration boundary; no automatic merge.

## Reproduction

From repository root with Python 3.10+, no third-party runtime packages:

```bash
python3 -m checker --input examples/checker-input.json
python3 -m checker --input examples/checker-input.json --format json
make check
```

`make check` runs documentation checks, independent unittest, baseline plus six
mutants in temporary source copies, and evidence-identity/accounting checks. No
model calls, Harness/CoderMind installation, private fixtures or caches are needed.
A clean checkout gate is recorded in clean-checkout.json when executed.
The same gate is wired to PR CI. Native 197-test replay is optional development
verification; see [snapshot instructions](native-replay/README.md).

Explicit pinned Harness verification: sync the Consumer Pack, route/read the
Consumer skill for the intended responsibility, then use verify.py for currentness,
schema, negative publication checks and complete closure; it writes derived run
outputs. Actual model-driven CoderMind execution remains separate from CI.

## Tool identities and review correction

Harness: `1c31054a8c4af223dc1bb003175c1fbe3f0538d6`.
CoderMind generation/final-test base: `3303a222eaec42c6a178bddd46ad63d9026ab8fa`.
Codex current observed version and source hashes: native-provenance.json.

The upstream review FAIL is retained. An explicit CLI review scope is implemented
by a two-file hash-checked patch in an isolated package copy, with the original
installation untouched. Eight regression checks cover CLI, strict visual/default,
pytest failure, stubs, unresolved functions and invalid scope. The actual patched
model-driven review took 75.8s and passed in one iteration. This is **not** a PASS
of unchanged upstream; see [ADR-0004](../../../docs/decisions/0004-cmind-cli-review.md),
cmind-review-patch-tests.json and the versioned patch/lock.

## Engineering history and limitations

Problem, requirements, bounded domain, verification/scenarios, architecture,
interface, policy, components, technical verification and Test Design were produced
in dependency order through strict admission and CAS publication/read-back.
Requirements schema initially failed for the managed envelope and was corrected
and re-admitted before downstream work. Four cohesive requirements own product
behavior; field/test facets were not promoted into separate requirements.

Architecture/component/implementation alternatives existed before preferred
candidates. This Harness pin has no registered decision-explorer route;
the decision-pipeline procedure owns FORM/REVIEW/CHOOSE. Decisions use scoped BROAD
engineering delegation and REQUEST_BOUND evidence, not attested isolation.

First feature construction: 335.2s; first five-stage plan: 1039.6s. Native structural
checks passed but semantic review rejected range/CLI/JSON drift (rpg-attempt-1).
Native feature edit claimed MODIFY but semantic inputs did not change; exact diff
is preserved. Ordinary scoped workspace AGENTS then bound accepted contracts to
native planning: all five stages completed in 1118.8s, review accepted candidate
input (rpg-context-1; ADR-0003). Autonomous native codegen completed in 46.1 min.
Realized RPG keeps all 50 planned feature identities/names; source locators/hashes
are checked rather than inferred from native success counters.

CHECKER-CODEGEN-INPUT separates accepted generation inputs from finished product
readiness; CHECKER-PROTOTYPE only became COMPLETE after actual executable evidence
and implementation admission. No readiness was inferred from tool installation.
Coverage is bounded to synthetic runtime: three specialized concerns are explicitly
inapplicable and two production governance concerns deferred with reasons.

Historical docs were read on an initially open archival branch before fetching the
clean restarted main. Writes started from current main; prior product admissions
were not reused. No blind comparison is claimed. Fixed scenarios precede code but
were visible to generation. Structural tests were refined to avoid constraining
private lookup scheduling; see checkpoint.md. Semantic expectations were unchanged.
No verified billing/token counters or complete clean model-toolchain rerun exists.
The CLI patch must be included in any future frozen comparison protocol.

## Remaining laboratory work

The synthetic prototype scope is verified. Main integration remains subject to PR
CI and owner review. Full production readiness is outside scope. P5 change-impact,
P6 controlled A/B/C/D comparison and P7 conclusions/replication remain separate
work; this pilot does not establish the comparative benefit of Harness + RPG.
