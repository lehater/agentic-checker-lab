# Iterative Requirements Discovery — pilot retrospective (draft)

**Date:** 2026-10-29  
**Status:** DRAFT / FOR OWNER REVIEW — not an accepted method, not an independently validated semantic result.  
**Scope:** `experiment/iterative-discovery-protocol`, [Draft PR #48](https://github.com/lehater/agentic-checker-lab/pull/48), two Checker discovery rounds.  
**Method baseline:** protocol v0.1 during interviews; v0.2 introduced after the initial pilot.  
**Authority:** owner problem brief, persisted ledger, round reports, Git commit history, CI and [read-only fresh-chat audit](https://github.com/lehater/agentic-checker-lab/pull/48#issuecomment-6490016712).

## 1. What the experiment set out to prove

The *method* under test is a durable owner-interview workflow: source facts → explicit, prepublished owner questions → free-form answers → normalized review → explicit owner confirmation → committed ledger/round report → recovery in a new chat. This is **Experiment A**.

Turning those decisions into an OpenSpec, acceptance catalog, architecture and a working Checker is **Experiment B**. Candidate spec work that followed the interviews supplies evidence of downstream semantic friction, but is **not** necessary to declare the elicitation workflow sound and must not be confused with pilot completion.

## 2. Evidence and verdicts

| Check | Evidence | Verdict / limit |
| --- | --- | --- |
| Question frontier committed before owner interview | [R-001 prepared `9ed8fa2`](https://github.com/lehater/agentic-checker-lab/commit/9ed8fa2c4a6a1761ccbb84c6e869ca4104e4d1a8), [R-002 prepared `9517152`](https://github.com/lehater/agentic-checker-lab/commit/9517152709104df945db82fe83885cce401e9751) | PASS (persisted question texts and IDs) |
| Explicit owner review before accepting meaning | R-001 and R-002 reports contain approved normalized answers, correction history and owner-confirmation records | PASS as recorded; raw voice/transcript is not independently available in GitHub |
| Atomic logical round closure | [R-001 close `bc2a3f0`](https://github.com/lehater/agentic-checker-lab/commit/bc2a3f089db72e13a096c9c0a8d99427372717b6), [R-002 close `b7e90a3`](https://github.com/lehater/agentic-checker-lab/commit/b7e90a33c48b31311abb4c572bb4484f0512888f) | Data written, but both initial closure commits FAILED repository CI; repaired later |
| Restart after chat switch | [Fresh-chat recovery audit](https://github.com/lehater/agentic-checker-lab/pull/48#issuecomment-6490016712) reconstructed checkpoint, 8 Qs, 11 Ds, open seams and commit history | PASS for *operational recovery*, not independent truth of original spoken answers |
| Structural regression / current state | [Latest repository CI](https://github.com/lehater/agentic-checker-lab/actions/runs/40833777166), [strict OpenSpec structure](https://github.com/lehater/agentic-checker-lab/actions/runs/40833777203) | PASS for structure; no Checker behavior/CHK executions |
| Independent semantic fidelity to primary owner statements | Original audio/transcript is not present in public repo; an author's later comparison is not an independent reviewer | NOT VERIFIED |
| Actual elapsed owner/agent time, waiting time, prompt tokens or cost | No trustworthy measurements recorded for the two rounds | UNKNOWN — not zero, not an efficiency PASS |
| Stable transfer to another domain/task | Only one Checker pilot, two rounds | NOT TESTED |

**State at review:** checkpoint 4, rounds R-001/R-002 CLOSED, 8 approved answers, 11 accepted decisions, no prepared R-003. Protocol and any downstream product specification remain experimental/unaccepted.

## 3. Checkpoint and repair history

| Role | Commit(s) | Observed consequence |
| --- | --- | --- |
| Initial protocol/CI bootstrap | `10d3dcc`, `ac1503a`, `ada46a2`, `28b9f8d` | Four setup commits before first published frontier |
| R-001 PREPARED / CLOSED | `9ed8fa2`, `bc2a3f0` | Two required logical state boundaries; initial close repo CI FAIL |
| R-001 repair | `fe3c289`, `726dda6` | Original test fixtures depended on mutable live ledger; first repair introduced another fixture issue; second passed |
| R-002 PREPARED / CLOSED | `9517152`, `b7e90a3` | Two required logical state boundaries; original close repo CI FAIL from malformed `D-09` |
| R-002 repair | `898bc3a` | Corrected ledger ID to `D-009`; report still had stale ID until later audit |
| Audit/tracing improvements (after interviews) | `4182d4b`, `6d4cdb6` | New validator had a misattached conditional; corrected after CI failure; retrospective process evidence, not another interview |
| Candidate specification work (Experiment B) | `65f6bef`, `e6925fa` | Semantic proposal and formatting correction; keep outside elicitation-efficiency counts |

Within the two actual interview rounds there were **four required checkpoint commits and three repair commits** (two R-001 test-fixture commits and one R-002 ID correction). Across the experimental branch up to `e6925fa`, 15 commits comprise setup (4), interview checkpoints (4), interview repair (3), audit/trace repair (2), and candidate-spec work (2). **Commit count is a reproducible activity count, not a measurement of elapsed time or model costs.**

For accurate historical evidence do **not** call original failed close checks PASS because a later head is green:

- R-001 initial close [repository run 40721865250 — FAILURE](https://github.com/lehater/agentic-checker-lab/actions/runs/40721865250); [repair run 40826390478 — SUCCESS](https://github.com/lehater/agentic-checker-lab/actions/runs/40826390478).
- R-002 initial close [repository run 40829507637 — FAILURE](https://github.com/lehater/agentic-checker-lab/actions/runs/40829507637); [repair run 40829573030 — SUCCESS](https://github.com/lehater/agentic-checker-lab/actions/runs/40829573030).

## 4. Observed method failures and successful protections

1. **Interview framing drift:** Q-001 originally suggested "flow checking", leading to an incorrect inference about actual traffic reachability. The owner clarified that Checker only searches recorded ACL-policy rules. The confirmation gate caught this before D-001 was approved.
2. **Biased option framing:** Q-003 proposed interpretations of unsupported additional ACL conditions that did not fit the owner's intended display-only treatment. Free-form answer plus explicit review corrected it.
3. **Source-port default was a real changed interpretation:** In R-002 initial owner answer, source port 65535 was suggested. During review, the owner explicitly corrected the intended meaning: both ports can be blank/`any` and default to `any`. The initial D-009 was only PROPOSED; persisted approved D-009 is the corrected version. This demonstrates the value of review **before** final approval.
4. **Question labels before publication:** The R-001 interview review used provisional Q-006/Q-007 labels that were never canonical; R-002 later assigned those IDs to new subjects. Avoid provisional public-looking IDs to prevent mistaken cross-reference.
5. **Preflight quality gap:** R-001 close failed because tests improperly derived synthetic test state from the live ledger. R-002 close failed because one accepted D ID was accidentally serialized as `D-09`; later the written round report still disagreed with the corrected ledger. These are **process/validation** defects, not reason to change owner semantics.
6. **Recovery coverage was narrower than semantic correctness:** A fresh chat successfully reconstructed recorded meanings, but could not prove fidelity to unavailable original voice. Do not report recovery PASS as independent semantic PASS.
7. **Scope drift after the pilot:** Work on candidate OpenSpec/CHK continued inside the same PR. It exposed useful conflicts (notably wildcard ports and additional ACL conditions), but blurred the boundary between evaluating the interview method and engineering the Checker product.

## 5. Recommended checkpoint policy for next trial (NOT YET APPROVED)

**Keep two durable *logical* boundaries.** Reduce physical commits through batching rather than dropping recovery guarantees.

- **PREPARED barrier:** persist exact question texts, immutable IDs, dependency and source context **before sending owner-choice questions**. Do not checkpoint each tentative draft or each answer.
- **CLOSED barrier:** after the owner explicitly approves normalized meanings, atomically persist all Q/A/D changes, round report, approval evidence and unresolved topics. Never persist proposals as ACCEPTED.
- **Batching:** if new questions are genuinely needed, prefer `CLOSED(R-N) + PREPARED(R-N+1)` **in one Git commit**. Thus two interview rounds could have used three checkpoint commits instead of four: `PREPARED(R-001)`, `CLOSED(R-001)+PREPARED(R-002)`, `CLOSED(R-002)`. This does not save owner review or validation work; it saves one separate write/CI cycle. Do not invent R-003 to exercise batching.
- **Optional provisional recovery:** for a long or interrupted interview, commit a snapshot explicitly marked PROPOSED/UNCONFIRMED, capturing a resumable frontier and explicit owner review still pending. It must never be counted as approval.
- **Stage checks before advancing a branch:** in an isolated complete candidate tree, run syntactic/ID/ref consistency checks, verify report IDs match the ledger, and ideally run the same tests as CI. Precommit validation should detect errors; CI on the committed tree remains the final gate. No state is declared verified before that gate passes.
- **No needless persistence:** brainstorming, question prioritization, clarifications within the same active session and proposed wording changes may stay transient until the next legitimate checkpoint, unless interruption or meaningful scope loss makes an explicitly provisional commit necessary.

### Process guards worth adopting

- Maintain **separate** `RECOVERY_OK`, `STRUCTURAL_OK`, `SEMANTIC_REVIEWED`, and `OWNER_ACCEPTED` outcomes. Never compress them into a single ambiguous PASS.
- Record short owner-origin excerpts, Example Mapping and a *counterexample* for each semantically risky decision, with privacy-conscious evidence/consent. A confirmation record without original evidence cannot prove audio fidelity.
- A new chat should be told to inspect the ledger and decide whether any novel owner-choice frontier exists; **do not automatically ask 3–7 questions after completion**. The current chat-start text needs this adjustment for a future revision.
- Version prompt and protocol at the start of each round; retain previous accepted statements and exact question texts even if an interpretation changes.
- Enforce invariant-driven tests with independent fixtures; never adjust a test's expected answer solely to fit the current ledger.
- Do not combine the method trial and product specification acceptance into the same success gate. Future separate product-engineering work should use an independently reviewed contract and separate PR/branch.

## 6. Proposed disposition / owner review

**Proposed conclusion:** The protocol has demonstrated persistence and recoverability in **one two-round pilot**. It has *not* established independent semantic fidelity, measured efficiency, or cross-domain transferability. Therefore classify as **OPERATIONAL PILOT PASS / METHOD VALIDATION INCOMPLETE**, not fully proven or ready for unconditional adoption in `main`.

**Recommended next steps in order:**

1. Owner reviews this retrospective and the proposed checkpoint policy; approve/amend recommendations separately from owner-approved Checker D-001..D-011.
2. Independently verify critical interpretations against primary owner evidence where possible, or explicitly record the evidence limit and run a small new *semantic review/confirmation* exercise (not an automatic new Q frontier).
3. If the process changes are approved, update the experiment's chat-start instructions and automated guards with invariant tests; validate a fresh-chat re-entry to the **post-interview** state (must not ask questions when no frontier exists).
4. Decide whether a second pilot on a different domain is necessary before moving a generalized method to `main`. Keep Checker OpenSpec work separate from this decision.

**No new R-003, no merge, no Checker implementation, no claim of independent semantic approval is authorized by this draft.**
