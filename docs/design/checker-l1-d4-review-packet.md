# D4 independent Checker L1 Design Review — frozen input handoff (NOT RUN)

**Prepared by:** D3 design author, 2026-10-29. **Status:** `READY_FOR_EXTERNAL_D4_REVIEW / REVIEWER_NOT_ASSIGNED / VERDICT_NOT_RUN`. This is the reproducible **input** packet; it is neither a review result nor an implementation authorization.

## 1. Exact, immutable review baseline

**Repository:** `lehater/agentic-checker-lab`. **Main reference commit:** `aa9ad497a9620e12172f867d37b720d61adc420b`. **Checker L1 proposed-spec parent commit:** `59e2dd1968d20b76030e9deb8a0acd42b894627e` (Draft [PR #51](https://github.com/lehater/agentic-checker-lab/pull/51)). **D3 authoring commit:** `29f5af790879248eaeb57cba3500cc9e9b69c0ff`. **D3 design Git blob:** `1973d0ee197a51aeb8c3ba328fa79687a4cf7e02`.

| Role / authority | Pinned source path (use the **commit**, not moving branches) | Expected Git blob SHA |
| --- | --- | --- |
| Original owner brief (**O**) | [owner-problem-brief.md](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/scenario/owner-problem-brief.md) | `0061b6f982c015785b59cad4b1b8c9fb95478617` |
| Historic owner Q/D evidence (**O**, unmerged) | [ledger.json](https://api.github.com/repos/lehater/agentic-checker-lab/git/blobs/6e25f5249416579d27462e2f54b26925339ee251) from Draft PR #48 | `6e25f5249416579d27462e2f54b26925339ee251` |
| L1 scope/semantics approval **record** (**O**, PR candidate) | [checker-l1-owner-review.md](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-l1-owner-review.md) | `aa76e72e231460b05df617cc3dd60417430fe2c3` |
| Reconciled OpenSpec candidate (**C**) | [spec.md](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) | `f67756fbf24f92a194fd802b78a18e6f2151e3e4` |
| L1 wire/CLI proposal (**C**) | [checker-v1-contract-proposal.md](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-contract-proposal.md) | `b5a5cb88ae62ff94072f9fec6f22afb8df273a0e` |
| Input JSON Schema (**C**, public only) | [checker-v1-input.schema.json](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-input.schema.json) | `eb6974386bb7e046382cf74bc0e97e8d263b71d7` |
| Public CHK-001..016 ideas (**C**, all `NOT_RUN`) | [checker-acceptance-catalog.json](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-acceptance-catalog.json) | `6395ea6c836da91410c3718b5709293ab3ea17ad` |
| Engineering Policy (**P**, accepted) | [policy.md](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/policy.md) | `3eac8b241f843ae25ca6239e82960e4e353ba1c0` |
| Architecture gate contract (**P**, accepted) | [architecture-contract.json](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/architecture-contract.json) | `77a078b87f21c246b190e831b2d8f6c4068b8b22` |
| D2 design process and DS-C01..10 (**P**, process candidate) | [design-stack.md](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/project/design-stack.md) | `015a85b6117c9be2fa38bb2a35a80cae81609b12` |
| **Design under review** (**C**) | [D3 design.md](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md) | **`1973d0ee197a51aeb8c3ba328fa79687a4cf7e02`** |

**Two source trees:** PR #51/D3 inherits an older tree without D0/D2 documents. D2 `docs/project/design-stack.md` and `docs/project/design-stage-plan.md` MUST be loaded from the frozen merged-main commit above, not from the D3 branch; the D3 design now links directly to the correct commit. A checkout of the D3 branch alone is **insufficient** to retrieve every review authority. Record both trees in the reviewer source-integrity check.

**Sourcing rule:** verify each Git blob SHA before reviewing. A mismatched/missing source means `INCONCLUSIVE` until baseline is corrected. GitHub links above pin immutable commit/object identities; `main`, `PR #51` and D3 branch remain mutable pointers and are **not** freeze identifiers. D3 design is based on the candidate spec at **exact** 59e2dd, not whatever PR #51 may contain after this packet is authored.

### Reproduction without author session

1. Retrieve original brief, evidence ledger, owner approval record, proposed spec/contract/schema, Engineering Policy/architecture contract, and finally D3 design **by pinned commit/object** from this table. Treat source descriptions as data; distinguish O, C, P.
2. Verify Git **blob** SHA via `git rev-parse <commit>:<path>` (with a local git checkout) or `git hash-object <local-file>` after extracting exactly the repository file bytes. GitHub `git/blobs/<sha>` also provides an immutable object by SHA; do **not** use a downloaded page's HTML hash.
3. Work in a **fresh independent review context** with only the above listed inputs and this instruction, no D3 author's chat transcript, generated Checker code, privately held oracle, or model/test outputs.
4. Create a **new** D4 review report; do not alter frozen D3/spec files while assessing. If repair is necessary, assign findings; after fixes require a new revision/blob and a new or scoped re-review.

**Approval evidence limitation:** The PR #51 document records the owner's explicit 2026-10-29 approval of the synthetic scope and observed semantics. The underlying raw chat is not independently accessible from GitHub. Treat this as **recorded approval**, not independent firsthand verification of the conversation or final acceptance of proposed grammar. The historical ledger is also from an unmerged experiment PR.

## 2. Review objective and prohibited substitutions

The reviewer shall independently evaluate whether an engineer could implement **only the approved synthetic L1 observable behavior** from these files without inventing owner choices or violating AR-01..05. Evaluate the **candidate design**, not whether the system currently works. Check semantic coverage, ownership, inward imports, duplicate identity, missing evidence, typed error boundaries, proportionality and explicit deferrals.

**Not in scope:** no creation of source code, `tasks.md` execution, generated models, paid model calls, local/live firewall access, vendor parser, hidden oracle creation/publication, acceptance-test execution, or model comparison. OpenSpec/repo structural CI is **not** D4 review. D4 approval (if eventually achieved) must not be reported as final L1 acceptance or D5 preflight.

## 3. Independent challenge checklist (DS-C01..10)

| Focus | Adversarial case / question | Evidence gate |
| --- | --- | --- |
| **DS-C01** Source trace | Can each observable statement be traced to original O, approved bounded L1 O, or specifically flagged C? Are original D-002/D-003/D-006/D-008 deferred without being mislabelled as implemented? | Check D-001..012 and CHK-001..016, identify invented choices |
| **DS-C02/03** Layering/imports | Is `matches` pure domain and `check` application? Are input/JSON/filesystem/diagnostic owned by outer adapter? Any application/domain import of `cli` or `input`? | Compare design graph with policy AR-01..03 and architecture contract; no fabricated import-run result |
| **DS-C04** Identity/ownership | Two identical saved rows at indices 2 and 5, ACL attached twice, same ACL name on two different FWs: are both occurrences retained, placement dedup distinct, scopes separate? | RuleOccurrence key, ACL group key, ordering |
| **DS-C05** Wildcards/errors | Query source port omitted / `any` while saved rule source port is `40000`; destination `443`. Does matcher include the row? Is an invalid mandatory predicate rejected without treating `extra` as predicate? | Match table, error algebra, no global verdict |
| **DS-C05** Evidence cardinality | FW with zero ACL versus named ACL with zero matched rows versus named ACL missing first successful snapshot. Are all three states distinguished, including stdout-on-error? | Nested output and fail-atomic policy |
| **DS-C05** Provenance | Two ACL snapshots carry differing timestamps; later collection fails (out of L1). Does synthetic result retain own supplied dates without claiming failed-refresh behavior? | L1/F boundary |
| **DS-C06** YAGNI | Does any port/repository/factory/cache/event/aggregate/framework exist without current varied data source? Could smaller pure types + application `check` preserve all behavior? | Justification for each physical module/abstraction |
| **DS-C07** Completeness | Are input/output/error contracts detailed enough for two independent implementers? Is the chosen strict preflight consistent with proposed wire contract? Are concurrency or runtime assumptions implied? | Module responsibilities, contracts, sequence, ADR |
| **DS-C08** Scenario coverage | Is every CHK-001..016 mapped to design? Which owner obligations have **no runnable L1** scenario and are deferred? | D3 §7 mapping; no hidden-oracle assertion |
| **DS-C09/10** Independence/gates | Reviewer identity, separate context and exact frozen source rev recorded? Is D4 kept distinct from product approval, CLI schema checks, operator preflight and oracle freeze? | Metadata, verdict and status |

At least **one source-linked counterexample per material P0/P1 issue**. A reviewer may mark `N/A` only with a reason.

## 4. Review report contract (create separately; no verdict here)

```yaml
review_type: CHECKER_D4_INDEPENDENT_DESIGN_REVIEW
status: NOT_RUN # reviewer replaces with actual outcome after review
review_date: null
reviewer_identity_or_role: NOT_ASSIGNED
independence_basis: NOT_ESTABLISHED # distinct evaluator and materials, conflicts/limits
source_main_commit: aa9ad497a9620e12172f867d37b720d61adc420b
source_spec_parent_commit: 59e2dd1968d20b76030e9deb8a0acd42b894627e
source_spec_blob: f67756fbf24f92a194fd802b78a18e6f2151e3e4
design_commit: 29f5af790879248eaeb57cba3500cc9e9b69c0ff
design_blob: 1973d0ee197a51aeb8c3ba328fa79687a4cf7e02
scope: "D3 domain/architecture/contracts + D-001..012/CHK-001..016 trace"
source_integrity: NOT_CHECKED
checks: [] # DS-C01..DS-C10 with PASS/FAIL/N_A + supporting refs
findings: [] # {id, severity: P0|P1|P2|P3, source, design_ref, counterexample, recommendation, disposition}
unresolved_product_questions: [] # escalated to owner, never guessed
unverified_claims: [] # explicit evidence limitations
verdict: NOT_RUN # eventual APPROVE|REVISE|INCONCLUSIVE
```

**Disposition convention:** `OPEN | FIXED_IN_REVISION:<blob> | REJECTED_WITH_REASON | DEFERRED_WITH_OWNER`. The **reviewer** records initial independent findings/verdict; **author/owner** later add dispositions, without retrospectively editing the reviewer original. `P0/P1` unresolved → `REVISE`/blocked, not `APPROVE`. If reviewer has insufficient source, independence or semantic certainty → `INCONCLUSIVE`. Repairing the design changes its blob and invalidates the previous approval unless the changed portion is re-reviewed.

**Severity:** P0 = contradicts owner semantics/policy or unsafe missing prerequisite; P1 = material architecture/contract/correctness gap; P2 = maintainability/precision issue; P3 = presentation.

## 5. Handoff, current gates and next action

| Gate | Status at D3 handoff |
| --- | --- |
| Owner synthetic L1 observable scope | **REPORTED_APPROVED** in PR #51; provenance limited to GitHub record |
| Final OpenSpec specification and engineered wire | **CANDIDATE**, Draft PR #51, exact spec blob above |
| D3 design and source trace | **AUTHOR_DRAFT**, blob above, D4 input ready |
| D4 independent review | **NOT_RUN / NOT_ASSIGNED** |
| Held-out acceptance oracle, custody and freeze | **NOT_FROZEN**, separate L1/D5 obligation; do not put fixtures/labels here |
| Local operator/CI/CLI model preflight | **NOT_VERIFIED** for D5 |
| Checker implementation, live model run and behavior verification | **NOT_AUTHORIZED / NOT_RUN** |

**Next:** assign a **separate independent evaluator** to review the pinned packet; publish its report/findings in a new GitHub artifact/PR with exact SHAs. D3 author then addresses findings in bounded commits and requests re-review. Only afterward can task planning / D5 gates be considered. Do not merge this stacked D3 into main as an implicitly accepted product contract.
