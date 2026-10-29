# Authority Gate v0.1 — decision classification

Use for **every candidate owner question** and every consequential alternative raised in Quality Gate/Deep. Goal: ask the owner **only** for a material product decision that cannot be answered from the current source or a valid delegation. The reviewer must not create an answer by preference.

## Candidate evidence (minimum)

1. **Scenario:** concrete input, state, actor, and exact MVP boundary.
2. **Two observable outcomes:** A vs B. If they are equivalent for the user/acceptance tests, this is probably implementation detail.
3. **Authority:** exact source excerpt, approved D/Q, and/or explicit delegation that governs the choice. Link to stable version/commit, not an unsupported summary.
4. **Consequence:** which test or user action changes, severity and why it matters **now**.
5. **Disposition:** class, proof, next action, reviewer confidence/unknowns.

## Classes and burden control

| Class | When it is justified | Action |
| --- | --- | --- |
| \`SETTLED\` | Exact approved requirement already selects an outcome | Link D/quote and a test; **do not ask** |
| \`DERIVED_FROM_SOURCE\` | Accepted sources **entail** one behavior and rule out the alternative; show proof and falsifying counterexample | Record the derivation/test; **do not ask** |
| \`ENGINEERING_DELEGATED\` | A **specific applicable** source explicitly assigns the choice to engineering | Record contract obligation; **do not ask** |
| \`OWNER_UNRESOLVED\` | In-scope, material distinct observable outcomes; no accepted rule, proof or applicable delegation | Include **once** in next independent owner batch |
| \`SOURCE_CONTRADICTION\` | Two current normative requirements require incompatible outcomes for the **same** scenario | Cite both; ask owner for precedence/meaning if product semantics, not merely formatting |
| \`DEFERRED_OUT_OF_SCOPE\` | Explicit MVP boundary excludes the case, with effect documented | Preserve as future scope; **do not ask** |
| \`EVIDENCE_ONLY\` | Missing raw transcript, original approval artifact or runtime evidence **without** a content gap | Disclose limitation; request proof only if required for acceptance |
| \`NEEDS_PROOF\` | Unclear authority/scope or missing support for proposed derivation | Seek source/independent review; do not turn directly into owner question |

**Two anti-errors:**
- "This is the normal/default way" **does not prove** \`DERIVED_FROM_SOURCE\`. A supported conclusion must rule out the alternative. Conversely, ambiguity does not automatically make every UX detail an owner question.
- Delegation of *ACL predicate syntax* does **not** delegate the meaning of an omitted **user query field**. Delegation of a UI format does **not** delegate who can view other users' data.

## Five-step classification decision

1. Is the scenario **within the accepted MVP** and does A vs B materially affect observable meaning? If no, justify \`DEFERRED_OUT_OF_SCOPE\`, trivial or engineering output.
2. Is a source-backed accepted rule already enough? If yes, \`SETTLED\` (with exact citation).
3. Does a demonstrable implication rule out an alternative? If yes, \`DERIVED_FROM_SOURCE\` (show the inference).
4. Is the **same decision** explicitly delegated? If yes, \`ENGINEERING_DELEGATED\` (cite the relevant sentence).
5. Otherwise \`OWNER_UNRESOLVED\`, \`SOURCE_CONTRADICTION\` or \`NEEDS_PROOF\`; do not hide uncertainty by calling it complete.

For \`SOURCE_CONTRADICTION\`, do not silently prefer the later-numbered rule, the stricter rule or a guessed "security-first" precedence. A product-policy conflict must be resolved by its proper authority.

## Stop criteria

- **No critical unresolved owner-authority question and no unresolved normative conflict** within agreed scope.
- Material matrix cells have cited rule, derivation, delegation or explicit deferral.
- At least one deliberate negative/weak-coverage challenge, not only re-confirmation of known cases.
- Owner-approved normalized meanings and trace to spec obligations; gaps/statuses explicit.
- Distinguish content sufficiency from missing proof of historic approval; don't re-interview merely to recreate a transcript.

If any fail, report \`NEEDS_OWNER_DECISIONS\` or \`BLOCKED_EVIDENCE\`; never silently "pass" the gate. \`READY_FOR_SPEC_REVIEW\` is not spec/oracle/implementation approval.

## Empirical basis and limitation

This is a proposed operational safeguard. In Checker mutation v1, reviewers discovered 1 of 3 planted defects; in two-domain v2, 2 of 2 were found and categorized, but the unmodified fictional booking control still contained plausible genuine ambiguities. Neither study validates general accuracy or a measured cost improvement. Improve the gate only on documented subsequent failures rather than creating automatic loops.
