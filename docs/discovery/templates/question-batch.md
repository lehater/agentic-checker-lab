# Discovery — Fast question batch (template)

Task/branch: `<task>` · source brief: `<link@sha>` · checkpoint: `<sha or NOT_COMMITTED>`  
Round: `R-xxx` · status: `PREPARED | ASKED | REVIEWED | CLOSED`  
Owner decision authority: `<role>`

## Why this round

Goal and boundary (1–3 sentences). Existing accepted decisions used, with links: `D-...@`. Which earlier questions are NOT repeated and why?

## Questions (usually 3–7, fewer if justified)

### Q-001 · <one independent decision>

- **Scenario / consequence:** <specific user-observable difference>
- **A:** <behavior>
- **B:** <behavior>
- **Source and authority:** <exact brief/previous D reference>; <OWNER_UNRESOLVED reasoning>
- **Dependencies:** <none or preceding Q IDs>
- **Recommendation (optional):** <clearly labelled, not owner approval>
- **Answer:** `PENDING`
- **Status:** `PREPARED`

[Repeat only for materially independent, dependency-ready questions. Never ask about source facts already settled.]

## Owner answers and batch confirmation (fill after interview)

| Q ID | Owner's answer, preserving critical qualifiers | Candidate D ID | Status |
| --- | --- | --- | --- |
| Q-001 | | D-001 | PROPOSED |

Positive example: ...  
Negative/counterexample: ...  
Conflicts, deferrals and rejected suggestions: ...

**Owner confirmation of normalized batch:** `PENDING / EXPLICITLY_CONFIRMED / CORRECTION_REQUIRED`  
Evidence link/date: ...  
Commit SHA after approval: ...

**Stop rule:** If explicit confirmation or successful checkpoint is missing, do not label any candidate D ACCEPTED or advance the dependent frontier.
