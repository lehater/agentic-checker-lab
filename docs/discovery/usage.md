# Using Evidence-Gated Discovery

**This is a task-scoped operating aid**, not a ChatGPT auto-loaded skill and not a license to bypass the [project entrypoint](../../AGENTS.md).

## Start a new feature

1. Create a small task branch/Draft PR from the accepted `main`; read problem statement and approved D/Q. Do not copy historical Checker approval statuses from experimental PR #48.
2. Copy [ledger template](templates/decision-ledger.md) into the task's own work directory; link it from the PR. Preserve stable IDs for that task.
3. Start a chat with GitHub access and paste the invocation below. Read/verify live GitHub state **before** asking anything.
4. Use Fast question batches if needed; commit owner-reviewed decisions; run the compact Quality Gate; trigger Deep only if a recorded risk warrants it.
5. When the handoff says `READY_FOR_SPEC_REVIEW`, conduct a separate specification/acceptance review. For Checker specifically, existing L1 and oracle approval gates still apply.

### New-chat starter

> Work on this repository task's requirements only, on its existing task branch/PR (not main). Read AGENTS.md, docs/discovery/README.md, methodology.md and authority-gate.md, the task brief, any approved Q/D and latest GitHub checkpoint. First recover the exact open items and cite sources. If material owner decisions remain, prepare an independent batch of up to 3–7 questions with concrete alternative outcomes and Authority Gate classification, and persist the prepared frontier before asking. Do not repeat confirmed questions. Normalize the owner's answers for a **single batch confirmation**; only then commit accepted decisions. Run the compact Quality Gate; Deep only if documented risk. Report unresolved issues, evidence limitations, SHA and next safe action. Do not silently approve a candidate specification, change main, or execute models/code without the separately required project authorization. On tool failure, state BLOCKED.

### Resuming after a new chat

> Recover Discovery from GitHub only. Identify last accepted checkpoint, exact owner approvals, active Q/D, unresolved authority and planned next action. Do not use prior chat memory to manufacture missing approvals. Continue only the next permitted step under the repository methodology.

## Practical example

A change asks "filter saved ACL matching rules by a connection." Existing owner-approved behavior may already answer TCP/UDP and query direction; **link approved evidence**, do not re-ask. An unsupported ACL parser predicate is delegated to engineering if the source explicitly says so. A missing user port default with two distinct user-observable results **cannot** be downgraded to "engineering" solely because predicate syntax is delegated. Provide a scenario and run Authority Gate instead of inventing the default.

## Small acceptance checklist for the practice itself

- Task-specific Q/D recovered in a new chat from committed sources, not memory.
- One batch of nonduplicated decision-ready questions; explicit owner approval; commit with stable IDs.
- Quality Gate identifies at least one meaningful negative example and distinguishes `OWNER_UNRESOLVED` from `ENGINEERING_DELEGATED` with citations.
- Handoff does not claim OpenSpec/oracle acceptance or bypass outstanding L1.
- Reusable on the next real ambiguous feature; measure owner burden and corrections when available.

Success is a **reproducible handoff**, not a predetermined count of questions or three obligatory full-depth runs.
