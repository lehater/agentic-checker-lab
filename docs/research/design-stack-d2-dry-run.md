# D2 dry-run: one synthetic design handoff, not implementation

**Type:** docs-only *desk trace* of the selected [minimal design stack](../project/design-stack.md). **2026-10-29.**
**Result:** `PAPER_TRACE_PASS / REVIEW_NOT_RUN / BEHAVIOR_NOT_RUN`. It tests whether a new executor can follow the proposed artifact handoff; it does not establish product correctness, approved Checker architecture, independent review or process efficiency.

## Source and provenance (GitHub only)

| Source | Exact evidence | Authority |
| --- | --- | --- |
| [Owner problem brief](../scenario/owner-problem-brief.md) | Main blob `0061b6f982c015785b59cad4b1b8c9fb95478617`: return **all** saved matching ACL rows, keep original snapshot order, show actions; never synthesize global E2E permit/deny. | Problem statement; not detailed engineering design |
| [Candidate OpenSpec Checker query](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) | Blob `f67756fbf24f92a194fd802b78a18e6f2151e3e4`, requirement `Complete stored-rule matching`, scenario `Multiple matching actions`. | **PROPOSED / Draft PR #51**, not main |
| [Candidate owner review packet](https://github.com/lehater/agentic-checker-lab/blob/59e2dd1968d20b76030e9deb8a0acd42b894627e/docs/evaluation/checker-l1-owner-review.md) | Owner scope/semantics approval reported in PR #51, with synthetic limitations and pending oracle/review. | Approval evidence in Draft PR, not frozen main spec |
| [Engineering policy](../engineering/policy.md) | AR-01..05 and semantic SOLID/KISS/YAGNI. | Accepted main policy |

**Isolation of example:** use only scenario "two different matching actions, preserve both and order, no global verdict". This scenario already occurs in owner brief and candidate spec. Do not add new owner-facing behavior, release CLI flags, invent a hidden oracle or infer actual live traffic.

## Step 1 — specification → a bounded design hypothesis

**Conceptual input:** a directed query, one *already identified relevant* firewall/ACL and an ordered synthetic snapshot with two supported matching rules (one permit and one deny). Relevance source and exact input grammar are separately proposed in PR #51, not established by this desk trace.

**Expected observable property (from source):** output contains **both row occurrences** in stored order and includes each original action; no global permit/deny. This is a paraphrase of existing requirements, **not** a newly authored independent expected-result fixture.

**Candidate responsibilities (engineering, not product authority):**

| Layer | Proposed responsibility | Input → output | Dependency direction |
| --- | --- | --- | --- |
| Domain | Evaluate a supported rule predicate against the requested flow, retaining an original row occurrence identity. | Flow + saved rule → match/no-match or explicit unsupported-predicate error | No dependency on JSON, CLI, files, networks |
| Application | Coordinate one flow query over *provided relevant* ACL snapshots; keep all matched rows, order and action. | Flow + preselected ACL/snapshot evidence → hierarchical result or missing-evidence failure | Depends inward on domain and small abstract evidence access contract only if necessary |
| Outer adapter | Parse/validate local synthetic JSON, supply snapshot/relevance records, serialize output/errors. | JSON/file → typed input; typed result → JSON/error | Inward dependency on application/domain contract |
| Composition | Wire the one-shot command to concrete adapters. | CLI arguments → request execution and process exit | Outer only |

**Design alternative:** for the tiny synthetic slice, avoid a generalized repository hierarchy or asynchronous service. A function or simple immutable data bundle can provide the snapshots; introduce a port only if isolation/replacement actually needs it. No persistence, real network route inference, event bus, factory or outbox is justified by the selected scenario.

**Unresolved and not guessed:** exact return/error types, snapshot absence behavior, mandatory predicate grammar, duplicate row identity, output field names and all other Checker scenarios require the full reconciled L1 spec/design (D3). This exercise does not choose them.

## Step 2 — request for independent design review (prepared, NOT executed)

A separately appointed reviewer should receive **only** the source refs/blob SHA above, design hypothesis above and [policy](../engineering/policy.md), with a bounded read-only instruction. The authoring chat/transcript, private oracle fixtures and any generated Checker code are not inputs.

| Checklist | Question to independent reviewer | Desk self-check (not review verdict) |
| --- | --- | --- |
| DS-C01/C08 | Does each observable output map to exact scenario(s), and would tasks independently verify action and order without inventing a global verdict? | Trace supplied to original brief + proposed scenario; executable acceptance **NOT_RUN** |
| DS-C02/C03 | Is predicate matching correctly isolated from I/O? Does application coordinate order and evidence, or is domain now orchestrating? | Candidate division recorded; no import graph or implementation exists |
| DS-C04 | Does a rule occurrence remain distinct even when two rows have identical text? | **NOT EVALUATED**: other scenario outside this example |
| DS-C05 | Does missing evidence stay distinct from zero matches? | **NOT EVALUATED**: full L1 needed; not inferred from this isolated example |
| DS-C06/C07 | Are generalized repository/ports/events unjustified for this sample? | Alternative documented; actual reviewer still needed |
| DS-C09 | Who is reviewer, what independently authored verdict, and exact design hash? | `reviewer=NOT_ASSIGNED`, `verdict=NOT_RUN`; no fake independent sign-off |
| DS-C10 | Is the held-out oracle frozen and local preflight verified? | **NO**; gates remain outside D2 |

**Finding disposition:** no independent findings exist. An independent reviewer must create a separate written report with severity and source reference. If source disagreements affect observed behavior, return them to the owner; do not repair by changing the spec silently.

## Step 3 — proposed trace to future tasks (no tasks committed to OpenSpec)

| Draft task (not actionable implementation) | Design ownership | Source behavior | Independent gate |
| --- | --- | --- | --- |
| T-EX-01: define a minimal flow/rule occurrence representation | Domain | Original brief / complete matching | D3 detailed typed contract before code |
| T-EX-02: implement supported predicate evaluation | Domain | `Complete stored-rule matching` | Real tests fixed independently before code |
| T-EX-03: coordinate collection of all matching saved occurrences without sorting or first-match exit | Application | `Multiple matching actions` | Same source scenarios and snapshot order |
| T-EX-04: adapt synthetic evidence and output | Outer adapter | Return action/order, no global verdict | Separate output/CLI error contract |
| T-EX-05: validate architecture and run independent acceptance | Independent verifier | AR-01..05 + selected scenario | D4 and D5 prerequisites first |

**Important:** these are *handoff illustrations*, not an approved `tasks.md`, real model run or codegen authorization. The real D3 design may assign different modules, provided AR-01..05 and approved behavior are preserved.

## Exit evidence and explicit limits

| D2 question | Observation | Result |
| --- | --- | --- |
| One canonical artifact schema? | [Existing `openspec/config.yaml`](../../openspec/config.yaml) says `spec-driven`; no schema changed | **PASS (source configuration)** |
| Can source → proposed responsibility → task be traced without additional tools? | Tables above name original brief, candidate spec blob and policy | **PASS (paper trace)** |
| Are owner meanings kept distinct from engineering assumptions? | Each source tagged problem, proposal or hypothesis; non-goals and open decisions stated | **PASS (paper trace)** |
| Is independent design review complete? | No second person/model context executed; review request only | **NOT_RUN** (D4) |
| Did pinned OpenSpec CLI, code, oracle or runtime tests execute for this paper case? | No; repository CI on the PR is only structural | **NOT_RUN** |
| Does the added checklist measurably improve outcomes over unmodified OpenSpec? | No matched independent run or latency/quality comparison | **UNKNOWN** |

**Decision from this bounded desk trace:** the minimal selected *candidate* is sufficient to prepare D3 without installing a new framework. Its independent quality and outcome improvement remain unproven; revisit only after an actual D4 review reveals a repeatable gap.

**Next:** after review/merge of D2, draft D3 **candidate** Checker design from a precisely pinned reconciled L1 spec; do not claim fully accepted semantics from Draft PR #51. Then independent D4 review and separate D5 oracle/operator gates.
