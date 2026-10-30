# D4 scoped independent re-review — Checker L1 (new frozen candidate)

**Status:** `AUTHOR_REPAIRS_PREPARED / D4_ORIGINAL_VERDICT_REVISE / INDEPENDENT_RE_REVIEW_NOT_RUN`. **Date:** 2026-10-30.  
**Candidate repair branch base:** [D3 PR #58](https://github.com/lehater/agentic-checker-lab/pull/58) head `9e73c76a87a853d4dde8b0ace51d057d0cd85997`.  
**Proposed repaired baseline commit:** `27bda5bfc36cea79725a17f524bdcb99099868ac` (immutable commit; packet itself is a later docs-only commit).  
**Original outside review:** [Independent D4 PR #60](https://github.com/lehater/agentic-checker-lab/pull/60), source review Git blob `1463bd7f9e9833e8392d3eb1dc5493d3881bd981`. Its `REVISE` verdict and `PARTIAL` source-integrity statement are historically accurate, **never overwritten** by this author's follow-up.

## 1. Reproducible source baseline and integrity evidence

This package intentionally spans three immutable histories: accepted `main` process authority, unmerged PR #51 L1 scope/spec ancestry, and candidate D3/repair. The historical Q/D ledger is from unmerged Discovery PR #48. Use the commit/blob identifiers below, **not moving branch tips**. All file contents below were retrieved from GitHub and their Git blob SHA-1 independently recalculated as `SHA1("blob " + UTF8_byte_length + NUL + exact_UTF8_file_bytes)`; resulting values were compared both to the expected blob and to GitHub's contents API SHA. **17/17 matched.** This establishes exact UTF-8 source-file consistency at author follow-up, not an independent sign-off on meanings or owner approvals.

| Input / role | Immutable pinned source | Verified Git blob SHA-1 |
| --- | --- | --- |
| Original owner brief | [source](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/scenario/owner-problem-brief.md) | `0061b6f982c015785b59cad4b1b8c9fb95478617` |
| Engineering Policy | [source](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/policy.md) | `3eac8b241f843ae25ca6239e82960e4e353ba1c0` |
| Architecture gate | [source](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/architecture-contract.json) | `77a078b87f21c246b190e831b2d8f6c4068b8b22` |
| D2 process/checklist | [source](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/project/design-stack.md) | `015a85b6117c9be2fa38bb2a35a80cae81609b12` |
| Historical Q/D ledger | [source](https://github.com/lehater/agentic-checker-lab/blob/experiment/iterative-discovery-protocol/docs/discovery/checker/ledger.json) | `6e25f5249416579d27462e2f54b26925339ee251` |
| Scope approval record | [source](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-l1-owner-review.md) | `aa76e72e231460b05df617cc3dd60417430fe2c3` |
| Original candidate spec | [source](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) | `f67756fbf24f92a194fd802b78a18e6f2151e3e4` |
| Original reviewed D3 design | [source](https://github.com/lehater/agentic-checker-lab/blob/9e73c76a87a853d4dde8b0ace51d057d0cd85997/openspec/changes/checker-v1-baseline/design.md) | `1973d0ee197a51aeb8c3ba328fa79687a4cf7e02` |
| Original D4 handoff | [source](https://github.com/lehater/agentic-checker-lab/blob/9e73c76a87a853d4dde8b0ace51d057d0cd85997/docs/design/checker-l1-d4-review-packet.md) | `990b17a585f246d19993414f70bbe986e23df5dc` |
| Independent D4 REVISE report | [source](https://github.com/lehater/agentic-checker-lab/blob/febf1364d72baa650cb40056ee28acd21990bbcc/docs/reviews/checker-l1-d4-independent-review-2026-10-30.md) | `1463bd7f9e9833e8392d3eb1dc5493d3881bd981` |
| Revised candidate spec | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) | `789d0579a7b355883a25d5dc79a4dbcdb9d1516b` |
| Revised CLI/wire contract | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/docs/evaluation/checker-v1-contract-proposal.md) | `ea4cfa963945202d174c9fd571181e68cafcb204` |
| Revised input JSON Schema | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/docs/evaluation/checker-v1-input.schema.json) | `4f7bc98fd97435b1f32cbbe0d4b52ef9c671e456` |
| Revised public input validator | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/tools/validate_checker_l1_input.py) | `76bfa8669f615dc1bc9f27ef1619e725d312ca08` |
| Revised public grammar tests | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/tests/test_checker_l1_input_contract.py) | `7c4163fae148a5c5b985854b62818edc6f631943` |
| Public NOT_RUN acceptance ideas | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/docs/evaluation/checker-acceptance-catalog.json) | `89bf8411dbeb90f2a325f16db29f84a33b3ad85a` |
| Revised D3 design | [source](https://github.com/lehater/agentic-checker-lab/blob/27bda5bfc36cea79725a17f524bdcb99099868ac/openspec/changes/checker-v1-baseline/design.md) | `f5cca431b6641343d2eb5546efea28903c574af8` |

**Reproduction:** fetch each immutable path, compute `git hash-object <file>` on exact bytes or use `git rev-parse <commit>:<path>` with a local repository; compare hashes in this table. The historical ledger **was decoded** for this author-side follow-up and matches the recorded blob. Reviewers shall independently validate whichever sources they consume; this author-side verification must not be misreported as the original D4 evaluator's work.

**Uploaded review artifact integrity:** the supplied `.patch` is a one-file addition containing the exact Markdown review bytes. Uploaded Markdown SHA-256 `dcee67b2dd8d93ebe7f1c8d9864d6f1116fe6acd3131aa5378c64318d0dde260`; Git blob `1463bd7f9e9833e8392d3eb1dc5493d3881bd981` in PR #60 agrees with locally computed Git blob hash. Original report remains read-only evidence, not a GitHub-authenticated reviewer submission.

## 2. Exact repair differences to challenge

| Independent finding | Repaired candidate and responsibility | Required counterexample/review |
| --- | --- | --- |
| **D4-F01 P1** | `last_success_at` accepts UTC `Z` and `+00:00` (seconds required, optional fraction); output serializes same instant as canonical `Z`. Outer adapter validates; application retains ACL-specific instant. | Feed same instant in both spellings; compare output provenance, reject `+01:00` as outside synthetic UTC grammar. Does this align with approved owner meaning without inventing a new one? |
| **D4-F02 P1** | Strict JSON parser rejects `NaN/Infinity` tokens; recursive `extra` walk rejects `float('inf')` from syntactically valid `1e400`; outer output must serialize strict JSON (`allow_nan=False` example). | Nested `extra` nonfinite values and unsupported mandatory fields; no false success/partial stdout. Public tests are authored grammar checks, not independent oracle. |
| **D4-F03 P2** | Relevant named ACL input must supply **at least one** preselected placement; empty placements cause explicit input error; FW with no ACL and ACL with zero matched rows remain valid, separate states. | Assess if this is a justified engineer-delegated integrity rule or a material change to owner semantics. Escalate to owner if required, do not silently approve. |
| **D4-F04 P2** | Parsing/typed boundary owns detached, transitively immutable nested evidence; output projection cannot alias/mutate input-owned `extra`. | Mutate nested input dictionary after typed request construction and before result serialization: should be unable to alter already validated evidence. No framework/class hierarchy added. |
| **D4-F05 P2** | Outer parser handles `InputDecodeError`/`InputContractError` before `check`; `application.check(ValidatedCheckRequest)` returns `EvidenceIntegrityError` for cross-object concerns; domain matches valid values. | Inconsistent IDs vs malformed IP vs unknown mandatory rule: which exact layer owns each failure and what reaches CLI? |
| **D4-F06 P3** | This re-review checklist labels `DS-C05a/b/c` for wildcard/errors, cardinality and provenance, respectively, while retaining parent DS-C05. | Each subcase separately recorded so a single PASS cannot hide untested conditions. |

**Scope guard:** D-002 route computation, D-003 real placement selection, D-006 durable snapshot management and D-008 collector failure remain **deferred**. No production FW, generated Checker, independent held-out acceptance oracle or model run. All 16 public CHK-001..016 are still `NOT_RUN`.

## 3. Independent review protocol (D2 DS-C01..10)

1. **DS-C01:** exact spec revision/source authority, owner O vs engineer C vs deferred F; ensure every new rule (including nonempty placements) is tagged as engineering candidate.
2. **DS-C02/03:** pure domain matcher, application orchestration and inward dependencies; mark source architecture as `NOT_RUN` because no Checker implementation exists.
3. **DS-C04:** single ownership of FW/ACL grouping, original row occurrence identity and nested `extra` immutable evidence.
4. **DS-C05a:** port `any`, UTC timestamp grammar, strict JSON success/error semantics and unsupported mandatory predicates.
5. **DS-C05b:** no FW, zero ACL, named ACL zero match, missing snapshot and empty placements; all distinguishable.
6. **DS-C05c:** per-ACL timestamp from last-success synthetic input; actual collector failure remains out of L1.
7. **DS-C06:** no speculative ports/repositories/DI/services, SOLID and YAGNI judgment.
8. **DS-C07:** implementable typed input/output/error boundaries with no invented behavior; explicitly check parser vs application errors.
9. **DS-C08:** cover the 16 public CHK ideas and deferred D obligations; do not use public catalog as hidden oracle.
10. **DS-C09/10:** separate reviewer identity and context, exact inputs, P0–P3 findings, any unresolved P0/P1, verdict; distinguish owner-scope record, candidate spec, review, oracle custody, local preflight and implementation authorization.

## 4. Required new review outcome

Produce a **separate, immutable** written result keyed by the **revised** design and spec blobs, recording reviewer identity/role, independence basis, sources and verified hashes, scope, `DS-C01..10` + `DS-C05a/b/c` status, and a disposition for each D4-F01..F06: `RESOLVED | STILL_OPEN | REGRESSION | INCONCLUSIVE` with source-linked counterexample for any remaining material conflict. Record new findings separately as `P0..P3`. Verdict must be `APPROVE|REVISE|INCONCLUSIVE` with explicit confidence limits; do not pre-fill an approval. If any product meaning is undecidable, ask the product owner **only** for the specific new decision.

**Reviewer separation:** a new independent reviewer reads only this immutable packet, its pinned authorities and the *prior independent findings* (not this repair author's transcript or self-evaluation). The author-produced fix table above is a review target, **not** evidence of correctness. Any change of spec/design/validator after this freeze requires new hashes and scoped re-review.

**Stop gate:** D4 remains `REVISE` until an actual separate re-review approves corrected content. D5 separately requires accepted spec and design, privately frozen independently authored held-out oracle, local operator preflight, and an explicitly bounded implementation authorization. The current PR is not that authorization.
