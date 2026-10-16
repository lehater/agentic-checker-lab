# Static handoff review — for independent verifier

**Reviewer:** generating assistant (not independent).
**Result:** candidate ready for external requirements review, **not approved for RPG**.

## Traceability matrix (pre-code)
| Requirement | Proposed verification evidence |
|---|---|
| FR-001 | Spec flow user story; JSON Schema flow shape; invalid fields tests |
| FR-002 | RelevantACL model and dataset contract |
| FR-003 | Missing snapshot error case in spec and quickstart |
| FR-004 | IPv4/prefix/protocol/port matching contract in data-model and research |
| FR-005 | Two matches with deny then permit in CLI example |
| FR-006 | Snapshot array ordering and output ordinal |
| FR-007 | Grouping output devices/acls |
| FR-008 | Match action preserved in output |
| FR-009 | Explicit prohibition of global verdict |
| FR-010 | Placement metadata defined in data model/schema/report |
| FR-011 | Offline synthetic fixture; no external IO |
| FR-012 | Restriction to declared predicate subset, fail on unsupported |
| FR-013 | Invalid input exit 2, no partial report |

## Findings
- **P1** Source problem permits design decisions but does not approve A-03/A-04/A-05; they remain provisional. These must not be misrepresented as owner-selected.
- **P1** No independent test of preservation of source meaning. Traceability links alone are insufficient.
- **P2** The proposed CLI and JSON shape are additional engineering decisions not specified by the owner; verify RPG preserves them if accepted.
- **P2** Structured JSON Schema cannot express all semantic constraints (CIDR parsing, port min<=max, uniqueness); enforce in runtime validation and acceptance checks.
- **P2** Custom checklist is intentionally unchecked pending a separate reviewer.
- **P2** The run was performed by an assistant already exposed to prior Harness results, not by an independently bootstrapped Spec Kit coding agent.

## Gate
`RPG_HANDOFF=NOT_APPROVED`. Required before handoff: independent review, explicit handling of provisional requirements and machine verification of contracts.
