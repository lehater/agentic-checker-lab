# Checker L1 D4 — second repair, third scoped independent checkpoint

**Author-prepared candidate; NOT a reviewer verdict.** Prepared on 2026-10-30 in response to [independent PR #62 REVISE](https://github.com/lehater/agentic-checker-lab/pull/62). Repaired sources pinned at commit `dd71bdd540882435935f105899b6456f0d8bd24f`; this handoff file may be committed later without modifying those source blobs.

**Gate:** `D4_SECOND_INDEPENDENT_VERDICT=REVISE` / `AUTHOR_REPAIR_PROPOSED` / `INDEPENDENT_SCOPED_REVIEW_NOT_RUN` / `D5_BLOCKED`.

## 1. Exact review inputs, including immutable ledger

**Immutable historical ledger:** [GitHub Git blob object `6e25f5249416579d27462e2f54b26925339ee251`](https://api.github.com/repos/lehater/agentic-checker-lab/git/blobs/6e25f5249416579d27462e2f54b26925339ee251). Retrieve via GitHub Git Blobs API; base64-decode its `content`, then hash exact bytes. **Do not** follow a mutable `experiment/iterative-discovery-protocol` branch URL as evidence of this blob. The owner's real chat approval is not independently verifiable here; use the pinned GitHub approval record without overstating it.

| Source | Immutable source URL | Expected Git blob |
| --- | --- | --- |
| Owner brief | [exact file](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/scenario/owner-problem-brief.md) | `0061b6f982c015785b59cad4b1b8c9fb95478617` |
| Engineering Policy | [exact file](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/policy.md) | `3eac8b241f843ae25ca6239e82960e4e353ba1c0` |
| Architecture contract | [exact file](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/architecture-contract.json) | `77a078b87f21c246b190e831b2d8f6c4068b8b22` |
| D2 process stack | [exact file](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/project/design-stack.md) | `015a85b6117c9be2fa38bb2a35a80cae81609b12` |
| Owner L1 approval record | [exact file](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-l1-owner-review.md) | `aa76e72e231460b05df617cc3dd60417430fe2c3` |
| First D4 report (PR #60) | [exact file](https://github.com/lehater/agentic-checker-lab/blob/febf1364d72baa650cb40056ee28acd21990bbcc/docs/reviews/checker-l1-d4-independent-review-2026-10-30.md) | `1463bd7f9e9833e8392d3eb1dc5493d3881bd981` |
| Second D4 REVISE report (PR #62) | [exact file](https://github.com/lehater/agentic-checker-lab/blob/2de514604cc1ef7e05f0843de1bd6c89bd6344a2/docs/reviews/checker-l1-d4-independent-rereview-2026-10-30.md) | `3839ca672068cae2d4157f8f970ca64173b4f00f` |
| Prior candidate and packet | [exact file](https://github.com/lehater/agentic-checker-lab/blob/e8c35a0e29f678f217282c18b5caad20339c3978/docs/design/checker-l1-d4-rereview-packet-20261030.md) | `c5fd49966b15edb02f52c97d40f6ed06c3b18053` |
| Repaired spec | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) | `a592b86532dcda65bc858c1255e368a792e56ff7` |
| Repaired design | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/openspec/changes/checker-v1-baseline/design.md) | `98f5542fceea4c0d285114809fb8a0e58c5bcb18` |
| Repaired wire contract | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/docs/evaluation/checker-v1-contract-proposal.md) | `b8410c3f826fb6c71c229bc1d9e082e1a83c92a1` |
| Repaired JSON Schema | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/docs/evaluation/checker-v1-input.schema.json) | `c3698737d78aacc73e7593a00f9a8b40aef0326c` |
| Repaired public validator | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/tools/validate_checker_l1_input.py) | `c151ef1cfe3631be378f2dbf568e6fd530a7fa61` |
| Repaired public tests | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/tests/test_checker_l1_input_contract.py) | `ef3f025fe09d0d25b3f96f5c1f68146768d410bd` |
| Public acceptance idea catalog (all NOT_RUN) | [exact file](https://github.com/lehater/agentic-checker-lab/blob/dd71bdd540882435935f105899b6456f0d8bd24f/docs/evaluation/checker-acceptance-catalog.json) | `8e0d56c8f18c06793dc6c325c6f4907d539ff1c8` |

**Source verification obligation:** Independently check Git blob identity using `git rev-parse <commit>:<path>` (or `git hash-object` on exact raw file bytes); for the ledger use the immutable blob-object ID. Read and verify the relevant content. These hashes are author-recorded expectations, not claims that the separate reviewer already verified them. If verification is impossible, state `PARTIAL` rather than adopting an author's integrity assertion. Historical review reports remain unchanged.

## 2. Targeted findings for a single bounded re-review

| Review item | Author repair to challenge | Decisive inspection / adversarial input |
| --- | --- | --- |
| **F05 / P2** | Only input adapter checks local nonempty `placements` and constructs `NonEmptyArray<Placement>`; `application.check` handles cross-object identities and emits `EvidenceIntegrityError`, never a placement-cardinality error | Inspect D3 §4/5, typed error variants and public validator. Ensure no duplicate owner remains |
| **N01 / P2** | Validate UTC RFC3339 text; normalize `+00:00` by replacing suffix with `Z` rather than formatting through microsecond-limited `datetime` | `2026-10-29T08:00:00.12345678901234567890+00:00` must be represented exactly as `...12345678901234567890Z` |
| **N02 / P1** | Lossless decimal JSON values in opaque `extra`: parse JSON decimals with exact representation, preserve all accepted digits, emit strict numeric tokens without float conversion or quoting; reject `NaN/Infinity` and `1e400` under explicit proposed `adjusted_exponent <= 308` bound | `0.1234567890123456789012345` remains a numeric value with exact source decimal representation; `1e308` allowed; `1e400` rejected. No Checker output implementation exists; test whether the **contract** is implementable and sufficiently unambiguous |
| **N03 / P2** | JSON Schema explicitly described as insufficient structural gate; public strict parser + semantic validator is normative input gate | A schema-only PASS for UTC `+01:00` or lexical port `443.0` is not L1 validity; validator rejects both |
| **N04 / P2** | CHK-006/009/013/016 include explicit `public_edge_variants` and CHK-017/018/019 map the three added OpenSpec scenarios one-to-one; every public case remains `NOT_RUN`. Cover empty placements, strict-JSON error/no success stdout, exact extra decimal output, UTC suffix equivalence and fractional precision | Verify every new publicly observable candidate behavior is mapped and none is misrepresented as executed or held-out |
| **N05 / P2** | This packet links ledger via immutable Git blob-object URL | Compare URL to expected blob; no mutable branch link is required to reproduce the source |

## 3. Stop criteria and authority boundary

Preserve these original constraints: pure five-dimensional directed rule matching, query `any` as unconstrained dimension, all matching occurrences in snapshot order, FW→ACL→row hierarchy, per-ACL provenance, no first-match verdict; owner O vs engineer C vs deferred F remain separate. D-002 actual route inference, D-003 live placement selection, D-006 durable snapshot lifecycle and D-008 refresh failure behavior remain **deferred**.

**No codegen or model comparison.** Public input grammar/serialization-boundary checks are allowed but are not Checker implementation tests, independent behavioral oracle or product acceptance. Never treat a CI green badge as D4 semantic approval.

Issue one **independently authored** concise result with finding-specific `RESOLVED|STILL_OPEN|REGRESSION|INCONCLUSIVE`, any new P0–P3, a source-integrity evidence row and `APPROVE|REVISE|INCONCLUSIVE`. Do not expand the scope to repeat unaffected D-001..012 design review unless an actual regression is found.

**Convergence rule:** for any new P2/P3, report its concrete safety/correctness impact and propose a bounded disposition; do not generate indefinite review cycles over cosmetic or hypothetical edge cases. Any unresolved P0/P1 blocks D4; P2 may remain open only if explicitly accepted as documented engineering debt that does not undermine the immutable L1 contract. Approval here would still **not** authorize D5 until spec owner acceptance, private held-out oracle and operator preflight are separately resolved.
