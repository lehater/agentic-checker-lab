# Iterative Requirements Discovery — experimental operating protocol v0.1

**Status: EXPERIMENTAL / NOT ACCEPTED.** Applies only to the Checker discovery pilot branch and its Draft PR. It does not approve the current proposed Checker OpenSpec, acceptance oracle or any model-driven implementation. Owner approves domain meanings; an AI never silently approves them.

**Canonical source:** [owner problem brief](../scenario/owner-problem-brief.md); existing [candidate OpenSpec](../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md) is **PROPOSED**, not evidence of owner choices. The old L1 handoff remains blocked until owner decisions and independent oracle are approved.

## Entry and roles

- **ChatGPT = interviewer/editor:** read this protocol, `checker/ledger.json`, previous round notes, original brief, related project policy. Fetch GitHub branch *before every round*. Use IBIS issue/alternatives/reasons, the Matt Pocock `grilling` frontier principle and BABOK-style owner confirmation; do not pretend to have executed the original Skills runtime. Check facts in source/tools, ask owner only for real choices.
- **Owner = meaning authority:** answers orally/free-form, confirms the *normalized* summary; can reject, defer, amend, or explicitly leave open. Silence is not consent. A suggestion is not approval.
- **GitHub = durable state:** one experiment branch and one Draft PR; checkpoint commits are the durable boundary. Changes to main only in a separate explicit merge decision after pilot review and passing checks. Do not touch the separate L1 PR #47.
- **Independent reviewer** (later): check important normalized statements, concrete examples and OpenSpec against approved answers; mechanical validator does **not** prove semantic correctness.

## Non-negotiable round state machine

`NOT_STARTED → PREPARED → INTERVIEWED → REVIEWED → COMMITTED`; then prepare next round. `INTERVIEWED` and `REVIEWED` can be transient in ChatGPT, but **never continue the next round without a successful committed checkpoint**. If GitHub cannot be read/written, or owner confirmation is missing, report **BLOCKED**, present the pending summary and stop; do not rely on chat memory as a substitute.

### 0. Preflight (every new chat or resumed session)

1. Read project-root `AGENTS.md` **at the experiment branch**, this protocol, `checker/ledger.json` and the latest `checker/rounds/*.md`. Read the problem brief. Check live branch and Draft PR; **main is the accepted project baseline; pilot branch contains the unaccepted protocol/state**.
2. Reconstruct OPEN questions, prerequisites, answered questions, accepted decisions, unresolved conflicts, last checkpoint and next allowed action. Do not re-ask already settled questions. Report any inconsistency, missing links or conflicting approvals; repair through explicit review, not guesses.
3. Record source revision and interviewer instruction version; if model name/token usage/time not observable, use `UNKNOWN` / null. Do not invent precision or cost.

### 1. Prepare and publish the *frontier* (first checkpoint)

1. Research source facts, objectives, prior confirmed answers, glossary and dependencies; compare the draft OpenSpec only as a *candidate*, not accepted facts.
2. Draft **3–7** independent owner-choice questions, adjustable downward for complex cases. Each Q has an immutable ID, text, why it matters, dependencies, proposed option/recommendation clearly labelled, and source. Questions not yet ready remain open but *unasked*. Ordering is dependency-aware, not strict FIFO.
3. Search all prior questions and decisions for semantic duplicates. If a proposed question is answered already, do not ask; if its old form is insufficient, add a linked follow-up.
4. Commit newly prepared questions into `checker/ledger.json` with a `PREPARED` round and stable IDs **before** displaying them to the owner. A first-run seed can be committed with an empty ledger, but it is **not** the prepared-questions checkpoint.
5. Only after the commit succeeds, present the **exact persisted question texts and IDs**, preferably as one list for one voice reply. If the owner changes questions before answering, record a correction/replacement in a checkpoint before asking revised texts.

### 2. Interview and provisional interpretation

1. Owner answers freely by microphone; map each answer to question ID. Owner may introduce issues, reverse a previous choice, refuse a recommendation, or leave answers unresolved.
2. Normalize into unambiguous statements **without silently strengthening, omitting a negation, adding a contract, or treating advice as an owner decision**. Keep relevant short verbatim excerpts when a nuance would otherwise be lost; avoid unnecessary full audio/transcripts or private data (repo is public).
3. Generate: candidate answers, candidate decisions, new questions, superseded/cancelled/deferred items, dependencies, unresolved conflicts, Example Mapping rule+example+counterexample for critical meanings.
4. **Do not modify the persisted ledger as if these were approved** while the owner is reviewing: show the change summary first. An unfinished chat may retain provisional data but its persistence must be clearly marked `PROPOSED` if deliberately checkpointed early.

### 3. Owner confirmation — blocking gate

Present one reviewable summary with:
- per-Q normalized response and status (approved / correction needed / unresolved);
- proposed decisions and reasons, any changed/invalidated previous decisions;
- created/replaced/cancelled/deferred questions and why; next-round candidates;
- semantic-risk examples and conflicting interpretations;
- counts and optional process observations.

The owner can approve the package or individual items. **Only explicit approval makes an answer `APPROVED` / decision `ACCEPTED`**. Corrections must be incorporated and re-presented if substantial; an unapproved item remains OPEN/PROPOSED. Never infer approval from agreeing to a proposed default in the agent's own text.

### 4. Atomic logical checkpoint — then new frontier

In **one commit**, after approval:
1. Update every affected Question/Answer/Decision and its origins, reason codes and links in `checker/ledger.json`; preserve old Q IDs and history in round notes. Do not erase answered content.
2. Add `checker/rounds/NNN.md` containing exact asked IDs/text (or references to the immutable prepared Git SHA), normalized answers and approval evidence, question/decision changes, outstanding ambiguity, reviewer examples, process observations, config/model/prompt info, unknown metrics marked unknown.
3. Mark that round `CLOSED` and record explicit owner confirmation; update checkpoint number. **May** append prepared questions for round N+1 in same commit. Those questions are not sent until this commit succeeds.
4. Run `python3 tools/check_discovery.py` and repository checks; fix structural errors without changing owner meaning. Commit on pilot branch and update Draft PR. If checks/commit fail, remain BLOCKED.
5. Announce committed SHA, counts, unresolved issues and *then* ask next prepared frontier, if any. On resumed chat, read persisted checkpoint first; don't reconstruct a supposed commit from memory.

## Question / answer / decision policy

- A Q ID is never reused. Published substantive rewording => old Q `SUPERSEDED` + new Q ID referencing old; typographical correction may retain ID when meaning unchanged and change is disclosed. `CANCELLED` and `DEFERRED` preserve explanation. The earlier round record preserves what was asked.
- Partial answer => keep Q OPEN with candidate answer, or create a targeted follow-up Q linked to it. `ANSWERED` requires an explicit owner-approved normalized answer. A recommendation is not a decision.
- Significant decision changes => new D ID superseding old D; old D is `SUPERSEDED`, never silently overwritten. All accepted D items must cite approved source questions. Obvious facts from files are source evidence, not owner approval.
- A question with unresolved dependencies is not on the askable frontier. A replaced/answered/cancelled question is not asked again. An old answer that proves incomplete is a new *clarification*, not a repeated question.
- `ledger.json` = **current index**; `rounds/*.md` plus Git history = **audit trail**. Do not claim a strict append-only audit if a PR squash merge or Git rewriting can change history; preserve all history that matters in the round files.

## Completion and quality

**Discovery is COMPLETE only when:** no unresolved *critical* owner choices; owner approves scope/terminology/rules and critical example cases; every important D maps to OpenSpec requirement/scenario or explicitly deferred scope; no unexplained contradictions; independent review of meaning has been performed. Otherwise `INCOMPLETE` or `BLOCKED`, never PASS.

**Do not automatically generate or approve OpenSpec from interviewing.** After the discovery pilot, submit a separate reviewed change that maps approved D IDs to requirements and independent acceptance criteria. Check both trace completeness and *semantic agreement*, with owner and independent reviewer.

## What to measure (without gaming the counts)

Each round records why Qs were asked/changed, duplicates avoided, owner corrections of agent interpretation, new material issues, approval iterations, contradictory decisions, examples that exposed ambiguity, and evidence of lost meaning downstream. Capture model/skill/prompt version, actual elapsed times (separate owner waiting vs agent where observable) and measured tokens if available; otherwise `UNKNOWN`.

**Pilot review before main:** check skipped steps, failed checkpoints, semantic losses, unnecessary questions, repair effort, completeness of trace, and whether the overhead was worthwhile. The current draft is only a hypothesis. Do not merge into main or claim tested effectiveness before an actual complete interview, review and CI evidence.

## Useful conventions

Reason codes: `new_dependency`, `owner_clarification`, `ambiguous_question`, `duplicate`, `contradiction`, `out_of_scope`, `source_fact`, `agent_misinterpretation`, `other`. Include human explanation; code is secondary.

IDs: `R-001`, `Q-001`, `D-001` (never renumber). Checkpoint count increments for each successful saved round transition; **Git commit SHA is the authoritative checkpoint identity**, not the counter alone. A single commit may close round N and prepare N+1.
