# D4 independent design review — Checker L1 (PR #58)

```yaml
review_type: CHECKER_D4_INDEPENDENT_DESIGN_REVIEW
status: COMPLETED_WITH_LIMITATIONS
review_date: 2026-10-30
reviewer_identity_or_role: "External read-only D4 assessment by ChatGPT (GPT-6); unauthenticated GitHub reviewer"
independence_basis: "Fresh context; reviewed GitHub-published frozen packet and pinned sources; did not use D3 author transcript, previous conversations, author's conclusions, model results or generated Checker"
source_main_commit: aa9ad497a9620e12172f867d37b720d61adc420b
source_spec_parent_commit: 59e2dd1968d20b76030e9deb8a0acd42b894627e
source_spec_blob: f67756fbf24f92a194fd802b78a18e6f2151e3e4
design_commit: 29f5af790879248eaeb57cba3500cc9e9b69c0ff
design_blob: 1973d0ee197a51aeb8c3ba328fa79687a4cf7e02
packet_commit: 9e73c76a87a853d4dde8b0ace51d057d0cd85997
packet_blob_recorded: 990b17a585f246d19993414f70bbe986e23df5dc
scope: "D3 domain / architecture / input-output-error contract, D-001..D-012, CHK-001..CHK-016, AR-01..05 and YAGNI"
source_integrity: "PARTIAL: immutable GitHub commit/raw paths read; expected blob hashes are packet-recorded but NOT independently recomputed against file bytes; historic ledger SHA endpoint accessible but contents were not decoded"
verdict: REVISE
```

## Review authority and limits

The sole evidence source is GitHub. I read [PR #58](https://github.com/lehater/agentic-checker-lab/pull/58), its [frozen packet](https://github.com/lehater/agentic-checker-lab/blob/9e73c76a87a853d4dde8b0ace51d057d0cd85997/docs/design/checker-l1-d4-review-packet.md), the [design under review](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md), the [original brief](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/scenario/owner-problem-brief.md), [recorded owner approval/scope](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-l1-owner-review.md), [candidate spec](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md), [wire/CLI proposal](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-contract-proposal.md), [JSON Schema](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-input.schema.json), [public validator](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/tools/validate_checker_l1_input.py), [its tests](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/tests/test_checker_l1_input_contract.py), [CHK catalog](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-acceptance-catalog.json), [Engineering Policy](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/policy.md), [architecture contract](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/architecture-contract.json), and [D2 process stack](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/project/design-stack.md). The packet's historic [D-001..12 ledger blob](https://api.github.com/repos/lehater/agentic-checker-lab/git/blobs/6e25f5249416579d27462e2f54b26925339ee251) was linked but not independently decoded; hence its historical approval evidence is *recorded*, not witnessed. No inference from author self-checks was used as review evidence.

**Source integrity limitation:** The immutable commit-path contents were inspected, but Git blob SHA equality was not independently established with `git hash-object`/tree API. Before treating this report as a completed formally sourced D4 gate, a GitHub-capable reviewer should verify the packet's expected Git blobs against exact bytes, including the ledger. This limitation does **not** remove the two concrete contradictions below. It does prohibit claims of full independently proved input integrity or final product acceptance.

**Prohibitions observed:** No code generation, Checker execution, model comparison, model calls, tests, network devices, hidden oracle, or generated implementation were run. All counterexamples are *reasoned review cases*, not observed runtime outputs. No code/spec/design file was modified.

## Findings (all dispositions initially `OPEN`)

### D4-F01 — P1 — UTC RFC3339 contract is narrower in public validator

- **Source:** [wire proposal, UTC row](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-contract-proposal.md#L128-L131); [schema, `format: date-time`](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-input.schema.json#L178-L182); [validator, `timestamp()`](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/tools/validate_checker_l1_input.py#L59-L67).
- **Design:** [D3 §4 `UtcInstant`, InputContractError, echo provenance](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L79-L110).
- **Counterexample:** In the wire example, replace the sole `last_success_at` with `"2026-10-29T08:00:00+00:00"`. It denotes UTC in RFC3339. The published validator's regular expression accepts only a literal `Z`, so the validator's intended accept/reject differs from the broader contract. No runtime test was performed.
- **Impact:** Two implementers can disagree about valid evidence; per-ACL timestamp provenance is either rejected or silently normalized based on undocumented adapter choice. Acceptance scenarios CHK-016/009 do not resolve the discrepancy.
- **Recommendation:** Either (a) explicitly narrow the *candidate* wire/schema/design to `Z`-only and seek approval of that narrowing, or (b) admit RFC3339 offsets whose value is UTC and define preservation or normalization to a single output grammar. Pin matching public negative/positive cases in the contract suite. Do not silently update validator alone.
- **Disposition:** `OPEN`.

### D4-F02 — P1 — Strict JSON boundary is not enforced for opaque `extra`

- **Source:** [wire contract, JSON-only/opaque `extra`](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-contract-proposal.md#L130-L139); [schema `extra` object](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-input.schema.json#L292-L296); [validator `rule()`](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/tools/validate_checker_l1_input.py#L83-L95) and [default `json.loads`](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/tools/validate_checker_l1_input.py#L163-L170).
- **Design:** [D3 §2 I-07 and §4 `OriginalValidatedRule`/`extra` echo](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L26-L36); [D3 §4–5 outer JSON success](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L91-L116).
- **Counterexample:** Replace a rule's `"extra": {"note": "text"}` with `"extra": {"note": NaN}` inside otherwise valid input. `NaN` is not a JSON value, but Python `json.loads` without `parse_constant` rejects neither `NaN` nor `Infinity` by default; `rule()` only tests that `extra` is a dict. A second corner case is syntactically valid JSON `"extra":{"x":1e400}` producing a non-finite Python value. Echoing that value via a permissive serializer can break strict JSON output. This is a source-derived prediction, not an execution result.
- **Impact:** `InputDecodeError` versus successful response is not unambiguous; output may cease to be strict JSON or mutate opaque evidence semantics, contrary to fail-atomic, JSON-only rules (AR-04).
- **Recommendation:** At the outer parser boundary reject non-JSON constants (`parse_constant`), reject non-finite decoded values including large exponents, recursively constrain `extra` to JSON-compatible finite values, and guarantee strict output serialization. Add public contract cases, without creating a hidden acceptance oracle.
- **Disposition:** `OPEN`.

### D4-F03 — P2 — Zero placements on a named “relevant ACL” is undefined

- **Source:** [candidate requirement for supplied relevant placements](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md#L31-L41); [schema `placements` array without `minItems`](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-v1-input.schema.json#L103-L118); [validator allows empty list](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/tools/validate_checker_l1_input.py#L124-L134).
- **Design:** [D3 `RelevantACL` and I-03/I-04](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L22-L35).
- **Counterexample:** `{"id":"fw-a","acls":[{"id":"WEB_IN","placements":[]}]}` with a valid corresponding snapshot and matching rule satisfies current shape/preflight. The output can label `WEB_IN` relevant, but has no ingress, egress or global placement evidence. There is no defined “relevant by selection but placement unknown” state.
- **Recommendation:** Decide and document whether `placements:[]` is legal *evidence* for a named relevant ACL; if illegal, constrain schema/validator/application preflight; if legal, define explicit meaning and a CHK case so it cannot be mistaken for a missing relevant attachment. Escalate observable meaning to owner if needed rather than guessing.
- **Disposition:** `OPEN` (scope/semantics question).

### D4-F04 — P2 — Immutability / input isolation of `OriginalValidatedRule` is underspecified

- **Source:** [spec, no mutation of supplied evidence](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md#L53-L60); [D3 immutable DTOs and raw `extra`](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L51-L63); [D3 §4](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L74-L91).
- **Counterexample:** A frozen `RuleOccurrence` holds `extra={"schedule":{"active":true}}`; a caller mutates the nested `schedule.active` dictionary after `CheckRequest` construction. Without deep-copy/readonly handling, the same report could change without a change in the request identity.
- **Recommendation:** State whether parsing owns a detached immutable/deep-copied JSON tree, and ensure the projection does not mutate input. Use a plain one-shot deep copy at boundary if sufficient; do **not** add repositories or persistence solely for this.
- **Disposition:** `OPEN`.

### D4-F05 — P2 — Error-type ownership and propagation should be explicit

- **Source/design:** [D3 `check(...) -> Result<CheckReport, CheckError>`](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L81-L110), [D3 input vs application responsibility table](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L51-L63).
- **Counterexample:** A malformed `flow.src_ip` is rejected before a `CheckRequest` exists. One implementer may return it as a `CheckError` from `check`, another as `InputContractError` only from the adapter; both can meet CLI stderr but cannot implement the same declared typed API. `UnsupportedMandatoryMatcher` is likewise assigned to “input/domain construction”.
- **Recommendation:** Specify the error union *per layer*: outer decode/shape and domain value construction before `check`; `check` only receives valid typed request and returns evidence integrity errors (and other explicitly enumerated application errors). Keep the CLI nonzero/stderr mapping in outer adapter. No framework needed.
- **Disposition:** `OPEN`.

### D4-F06 — P3 — DS-C05 is repeated without stable sub-identifiers

- **Source:** [D4 packet checklist](https://github.com/lehater/agentic-checker-lab/blob/9e73c76a87a853d4dde8b0ace51d057d0cd85997/docs/design/checker-l1-d4-review-packet.md#L205-L217).
- **Counterexample:** The checklist repeats `DS-C05` for wildcard/error, evidence cardinality and provenance. A single `DS-C05: PASS` would not reveal which of three reviews was performed.
- **Recommendation:** Name subcases `DS-C05a/b/c` while retaining the canonical `DS-C05` umbrella; record each in the report. This does not require a second schema.
- **Disposition:** `OPEN`.

**Severity rollup:** `P0=0`, `P1=2`, `P2=3`, `P3=1`. There is no verified P0 contradiction in the pinned design. P1 findings are source-derived contract contradictions, not claims about Checker runtime.

## Requirements and scenario trace

| D decision | Assessment from owner brief / approval record / candidate spec to D3 | CHK public ideas |
| --- | --- | --- |
| D-001 | COVERED (synthetic directed five-field query; IPv4/CLI = candidate C) | 001,002,010 |
| D-002 | F: actual route/relevance computation deferred; supplied FW only | 005,015 only synthetic handoff |
| D-003 | F: actual applicable placement selection deferred; supplied placements only | 005,008 |
| D-004 | COVERED: pure five-dimensional predicate; `extra` display-only | 004,009,013 |
| D-005 | COVERED: every occurrence, permit + deny, snapshot index and order | 003,008,014 |
| D-006 | PARTIAL: one supplied last-success timestamp per ACL; storage/lifecycle F | 016 only synthetic timestamps |
| D-007 | COVERED: zero-ACL FW vs zero matches distinct | 007,015 |
| D-008 | F: collector failure, retry, preservation and logging absent | no runnable L1 case |
| D-009 | COVERED: required directed IPs/TCP-UDP, omitted/`any` ports | 001,002,011 |
| D-010 | COVERED: key `(FW,ACL)`, placement dedup not rule dedup | 005,008,014 |
| D-011 | COVERED: no reverse-flow inference | 012 |
| D-012 | COVERED: FW → ACL/placement → matched rows, even empty children | 007,008,015 |

Trace reference: [D3 §7](https://github.com/lehater/agentic-checker-lab/blob/29f5af790879248eaeb57cba3500cc9e9b69c0ff/openspec/changes/checker-v1-baseline/design.md#L126-L146) versus [original brief](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/scenario/owner-problem-brief.md#L176-L189), [recorded D disposition](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-l1-owner-review.md#L9-L33), [candidate spec](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md), and [public CHK catalog](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-acceptance-catalog.json). Every CHK-001..016 is mapped; **all are NOT_RUN and not an oracle**. Deferrals are not marked “implemented”. The historical ledger contents and original chat were not independently verified.

## Domain, layering, policy and YAGNI adjudication

- **Positive design properties:** `FlowQuery` distinguishes unconstrained *query filter* `Any` from saved-rule `any`; five supported dimensions are conjunctive. `RuleOccurrence` is keyed by `(FW, ACL, snapshot_index)`; equal row text at different indices survives. Repeated ACL placements consolidate into a single FW-local ACL; identical ACL name across FWs remains distinct. `ACLReport` timestamps belong to the individual saved snapshot, not the FW. Missing snapshot is not a zero-match report, and no global permit/deny verdict or implicit deny is invented. These satisfy the observable owner meaning **at design level only**.
- **AR-01 / AR-02 / AR-03:** `domain.matches` is pure and separate from `application.check`; JSON/path/diagnostics are outer adapters. The proposed physical paths and symbol names agree with [architecture-contract.json](https://github.com/lehater/agentic-checker-lab/blob/aa9ad497a9620e12172f867d37b720d61adc420b/docs/engineering/architecture-contract.json). No generated source exists to establish actual dependency imports or cycles; design-level PASS is **not** source-architecture gate PASS.
- **AR-04 / AR-05:** preflight rejects missing/duplicate/orphan snapshots and unsupported mandatory predicates before producing a partial success; valid zero-match remains distinct. However F01/F02 violate the intended consistency of the proposed grammar/validator, so boundary review **FAIL**. Structural CI and public grammar regression are not semantic test evidence.
- **SOLID, KISS, YAGNI:** pure domain matcher + one application use case + thin outer adapters is proportional. No generic `IRepository`, cache, DI container, collector, domain events, outbox, API server or framework proposed. No YAGNI violation requiring deletion was found; F04/F05 call for clarification, **not** more architecture.

## DS-C01..10 checklist outcome

| Check | Assessment | Evidence/qualification |
| --- | --- | --- |
| DS-C01 | PASS_WITH_SOURCE_LIMIT | D-001..12 and CHK-001..16 traced, O/C/F distinct; historical ledger not decoded, owner approval is a GitHub record |
| DS-C02 | PASS_DESIGN_ONLY | Matcher/value semantics do not depend on CLI/JSON/files |
| DS-C03 | PASS_DESIGN_ONLY | Inward arrow map; cannot claim tested imports/cycles without code |
| DS-C04 | PASS_WITH_ISSUE | FW/ACL/row identity and ownership coherent; F03/F04 need clarification |
| DS-C05a | FAIL | UTC grammar F01; JSON `extra` F02; query `any` logic itself passes paper review |
| DS-C05b | PASS_WITH_ISSUE | Empty FW / zero match / missing snapshot distinguished; empty placements F03 open |
| DS-C05c | PASS_WITH_SOURCE_LIMIT | Per-ACL timestamps preserved; no future collector claim |
| DS-C06 | PASS | No speculative ports/repositories/frameworks |
| DS-C07 | FAIL | Concrete wire inconsistencies F01/F02; layer error boundary F05 |
| DS-C08 | PASS_DESIGN_ONLY | All 16 CHK ideas traced, explicit D-008 future-only; none run |
| DS-C09 | PARTIAL | Reviewer role/context and pinned refs recorded; cryptographic blob verification and third-party identity proof unavailable; no GitHub PR published |
| DS-C10 | PASS | Scope approval ≠ candidate spec ≠ design review ≠ oracle/preflight ≠ implementation permission |

## Unresolved owner/product questions and gate disposition

1. Is a supplied *relevant named ACL* with `placements:[]` valid meaning, or an incomplete placement fact to reject? See F03. No assumption is imposed here.
2. If `Z`-only timestamps are intended, this is a **contract change**, not a de facto already-approved owner fact. See F01.

**Independent content verdict: `REVISE`.** Resolve P1 F01/F02, adjudicate P2 issues, freeze corrected candidate spec/contract/validator/design together, and request scoped re-review of changed hashes. Keep PR #51/#58 candidate and D5 codegen gate blocked. **Additional formal source-integrity gate:** independently verify all packet blob SHAs, including the historical ledger; until done, this review is not proof of a fully verified D4 source baseline. The source-access limitation and absence of an authenticated GitHub write identity also mean this document is a *local review artifact*, **not** a published separate GitHub PR or a final authorization.
