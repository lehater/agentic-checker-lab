# L1 — scope review and owner decision record

Status: **AWAITING_OWNER_DECISIONS**, not accepted requirements. Tracks [issue #32](https://github.com/lehater/agentic-checker-lab/issues/32).

## Source comparison

The [owner brief](../scenario/owner-problem-brief.md) requires all matching stored rules, device/ACL grouping, snapshot order, preserved actions and no global verdict. Synthetic snapshots and supplied relevance are permitted for the prototype. These requirements are retained in the [candidate specification](../../openspec/changes/checker-v1-baseline/specs/checker-query/spec.md).

The following choices narrow or extend that brief and still require explicit owner decisions:

| Decision | Candidate | Owner decision |
| --- | --- | --- |
| Predicates | IPv4 exact addresses/canonical CIDR; rule protocols tcp/udp/any; both ports use inclusive ranges 0..65535 | PENDING |
| Interface | One local UTF-8 JSON document with one TCP/UDP flow; versioned JSON report | PENDING |
| Relevance | Supplied ordered device/ACL pairs, deduplicated by both keys in first-seen order | PENDING |
| Failure | Missing or invalid relevant snapshot fails whole query; nonzero exit, diagnostic stderr, no partial successful stdout | PENDING |
| Evidence | Preserve placements and original matching rule fields; MATCHES or NO_MATCH per group | PENDING |

Approval of these choices alone will not freeze a complete wire contract. The candidate does not yet define exact JSON field names, version discriminator, placement representation, error codes or a CLI invocation. Empty relevance, duplicate snapshot identities, permitted action values and treatment of malformed non-relevant snapshots also need explicit resolution. Record proposed resolutions in requirements/design/catalog together for review before generating accepted fixtures. Do not infer acceptance from this worksheet.

## Independent oracle gate

The existing [catalog](../evaluation/checker-acceptance-catalog.json) covers ten proposed scenarios; its prose is not executable accepted fixtures. An independent custodian must be identified to prepare/review the hidden oracle outside implementation-agent access. Public examples cannot be called held out. After scope and wire-contract decisions, record approved spec, architecture and oracle hashes with custodian evidence before codegen. No accepted oracle hash exists at this stage.

## Observed local preflight — 2026-10-28

- Accepted main and fetched origin/main: `23fb14db473635b8ad2dfbb8121a581a9c42eafa`; fast-forward update reported already up to date.
- `make check`: PASS, including requirement trace, archived RPG rejection/corrected-layout regression and offline comparison checks. Catalog acceptance remains false; implementation execution remains false.
- `command -v openspec`: absent from current PATH; local strict validation and workflow integration NOT_RUN. Existing GitHub structural validation remains verified and is not repeated as missing work.
- `node --version`: `v18.19.1`; CI uses Node 22 and OpenSpec 1.14.3. No installation or destructive initialization performed.
- `codex --version`: `codex-cli 0.163.0`; CLI emitted a read-only PATH-alias warning. Version observation does not verify authentication, model access or OpenSpec integration.
- No model-driven command, quota experiment or live device operation performed.

L1 remains incomplete. L2–L5 remain gated by the handoff dependencies. Next action: owner decisions and independent oracle custody, then a reviewed concrete contract and frozen fixtures. Runtime setup can be checked without model calls, but cannot satisfy the acceptance gate.
