# Round R-NNN — CHECKPOINT TEMPLATE (copy and fill)

- Prepared question commit: `<Git SHA>` (must predate asking)
- Close checkpoint commit: `<Git SHA>` (recorded by next round or PR comment; never guess)
- Status: PREPARED / INTERVIEWED / REVIEWED / CLOSED
- Source brief SHA: UNKNOWN until observed
- Interview instructions: `docs/discovery/protocol.md` v0.1
- Model/skill/prompt revision: UNKNOWN unless observed
- Owner confirmation: PENDING — MUST NOT mark decisions ACCEPTED before explicit confirmation

## Exact published questions
- Q-NNN — <persisted question text; do not retrospectively rewrite>

## Voice answers → proposed normalized statements
- Q-NNN: owner answer summary; critical verbatim nuance, if needed
- Normalized interpretation: <unambiguous>
- Status: PROPOSED / APPROVED / OPEN
- Meaning checks: rule + concrete example + counterexample as needed

## Owner review
- Summary presented: <what was shown>
- Owner response and timestamp if known: <explicit approval or corrections>
- Remaining uncertainties: <items>

## Changes in this checkpoint
- Created / answered / superseded / cancelled / deferred Q IDs + **why**
- Accepted / proposed / superseded D IDs + source Q IDs
- Conflicts / duplicate questions avoided / dependencies unlocked

## Measurement and retrospective evidence
- Number asked / answered / re-asked / corrected / new material questions
- Agent interpretation corrected by owner: <count and reason>
- Semantics lost, invented or recovered: <evidence>
- Agent runtime / owner waiting time: UNKNOWN unless measurable separately
- Measured input/output tokens: UNKNOWN unless directly observed
- Process problem / next hypothesis: <free text>

## Gate
- [ ] Owner explicitly approved normalized meaning (partial items still PROPOSED if not)
- [ ] `python3 tools/check_discovery.py` PASS
- [ ] Commit was created and branch advanced
- [ ] Only then next-round questions were presented
