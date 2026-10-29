# Mutation v2 — post-unblinding results (2026-10-29)

**Status:** COMPLETED_4_OF_4; TARGET_DETECTED_2_OF_2; METHOD_NOT_VALIDATED.

The four independent reviewer reports were received before the hidden case mapping was opened. The private manifest was verified: every case file SHA-256 matched; within each domain the mutation changed exactly one normative statement. Review isolation remained `BLINDING_UNVERIFIED`.

| Case | Domain | Role after unblinding | Target result | Owner / contradiction / engineering findings | Reviewer stop |
|---|---|---|---|---|---|
| **X7Q4** | Checker | unchanged control | N/A | 0 / 0 / 2 | SUFFICIENT_WITH_KNOWN_GAPS |
| **V6L3** | Checker | contradiction: R07 excludes empty-match ACL but R12 retains every relevant ACL | **Found, correctly SOURCE_CONTRADICTION** | 1 / 1 / 2 | INSUFFICIENT |
| **P2N8** | Shared Rooms (fictional) | deletion: R05 no longer limits cancellation to creator | **Found, correctly OWNER_UNRESOLVED** | 5 / 0 / 0 | INSUFFICIENT |
| **H9B5** | Shared Rooms (fictional) | unchanged control | N/A | 3 / 1 / 0 | INSUFFICIENT |

**Scores:** both seeded defects detected (2/2), both correctly triaged (2/2). This is descriptive, not a statistically valid recall/precision estimate. Three `INSUFFICIENT` verdicts alone do not measure target detection. Number of all recorded issues: 15; owner nominations: 9; contradiction nominations: 2; engineering notes: 4.

## Critical control-quality caveat

H9B5, the **unchanged** fictional booking baseline, contains plausible latent ambiguities. In particular R05 requires a non-creator's cancellation to produce an access error; R12 requires an already-cancelled booking to produce an “already cancelled” message. Both can apply to a non-creator cancelling a cancelled booking. The reviewer correctly raised the unresolved priority/security meaning; do not automatically call this a false positive. It also flagged unknown employee on creation, another employee's access to booking history, and past-date creation. The benchmark did not prevalidate its fictional clean control as exhaustively specified; thus false-positive specificity **cannot be measured** by treating any H9B5 findings as errors.

An additional discrepancy exists on Checker controls: X7Q4 regarded a never-successful ACL snapshot as an engineer-presentational choice, whereas V6L3 treated it as a user-observable authority gap. The targeted mutation test does **not** validate stable classification of this unrelated ambiguity.

## Conclusion and next proposed test

Authority Gate v2 detected and correctly classified **both** planted changes across two domains, an encouraging result. It is **not yet a validated methodology**: controls were not fully independently verified, only two mutation targets were tested, the review model/effort and truly independent isolation were unverified, and owner effort was not measured.

The next corpus should use a demonstrably complete *clean negative control*, separately score unseeded latent issues, include fresh deletion/contradiction/ambiguity/engineering-delegation variants, and evaluate evidence for the class labels. Test on a different domain or independent reviewer set. Freeze a v3 key and scoring prior to launch. Do not silently retrofit the completed v2 cases.

**Evidence:** full original evaluator reports and private operator key are preserved in ChatGPT Library `/Projects/Checker-Discovery/Experiments/Mutation-v2/`. This public report excludes verbatim transcripts and hidden-case manifests. No Checker ledger, Fast D, OpenSpec, code, oracle or `main` changes.
