# Access assessment — As-Is vertical slice v0

**Status:** Product Python path and historical SQL bodies observed; historical business interpretation separately author-confirmed in sibling SSSR_XLAM sources. Not a runtime test or To-Be architecture.

Scope: `GET /check/access/` (the same `Tools.urls` are also included under other URL prefixes). Code baseline: `891d751d50d85a260544c43e776dc51496bdd8db`. Primary evidence OBS-003, OBS-007, OBS-012, OBS-013, OBS-016.

## Observed request and processing path

| Step | Code / presentation | Observation |
| --- | --- | --- |
| 1 | [`NetView/urls.py`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/NetView/urls.py) and [`Tools/urls.py`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/Tools/urls.py) | `/check/` includes Tools routes; `/access/` maps to `check_access`. |
| 2 | [`Tools/views.py::check_access`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/Tools/views.py) | Unauthenticated requests redirect to Django Admin login. Authenticated GET without parameters renders defaults. |
| 3 | [`Tools/forms.py::CheckAccessForm`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/Tools/forms.py) | GET query validates source IP, destination IP, protocol (`tcp`, `udp`, `icmp`) and integer source/destination ports (0..65535). |
| 4 | [`Tools/views.py::has_rights_to_check`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/Tools/views.py) | Optional `mse_check` asks for live checking. Permission is determined by superuser status, specific admin-group ancestry or a Django group ID. Unprivileged requests stay on the DB-derived path. |
| 5 | [`checker.py::DevicesOnPath.run`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/SoS/dev_parsing/dev_checker/checker_types/checker.py) | SQL call `ProductTest.dbo.FindFirewallMain` determines candidate path-device rows; `dbo.FindACLMatch` receives those rows as filters; `GetZni` and `dbo.IPInfo4` retrieve additional records. |
| 6 | [`checker.py::get_trace`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/SoS/dev_parsing/dev_checker/checker_types/checker.py) | Only when live check is permitted and no more than **10** path devices are found does it invoke `DevicesPollingNew` and attach per-device results/errors. |
| 7 | [`Tools/views.py`](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/Tools/views.py) and [template](https://github.com/lehater/product/blob/891d751d50d85a260544c43e776dc51496bdd8db/templates/views/check_access.html) | View renders separate tables for firewalls, ACL matches, ZnI records, source/destination metadata; live results are displayed in firewall rows. |

## Observed result structure

| Result | Where produced | UI column/meaning observable |
| --- | --- | --- |
| Path firewalls | `FindFirewallMain` query and per-device mapping | Name, type, role, status, IP, ingress/egress interface, admin, owner, result/details |
| Policy matches | `FindACLMatch` | ACL name, rule number, action, protocol, source/destination, ports, hit count, zones, rule ID, last update |
| ZnI | `GetZni` | Number, action, protocol, endpoints, ports, description, editor, date |
| Address metadata | `IPInfo4(source/destination)` | Group, owner, site, admin, description, editor, date |
| Additional devices (S-Terra) | `sterra_res = []` in checker | No content shown from the current Python path |

The source does **not** establish that the screen computes one canonical final "allowed / blocked" judgment. It displays multiple evidence sets that may require interpretation by a human.

## Data/knowledge boundaries

1. **UI/input** — HTTP view and validation. Ownership: existing Django presentation.
2. **Topology and policy query** — SQL stored procedures and functions. The relevant `FindFirewallMain` and `FindACLMatch` definitions are available in the pinned sibling SSSR_XLAM SQL sources, allowing explicit tracing of candidate and ACL-match semantics. Their transitive SQL dependencies and deployed version require further verification.
3. **Live collection** — device dispatcher, polling and vendor-specific checker logic; runs only with extra permission and device-count limit.
4. **Presentation assembly** — positional DB result structures converted into tables, with equipment errors and ad-hoc result normalization.

These are **As-Is integration boundaries**, not proposed bounded contexts.

## Branches and edge cases visible in source

- No authentication -> login redirect, no result tables.
- Invalid GET form -> empty/initializing page branch; no verified domain-level rejection semantics.
- No extra live-check permission -> DB-derived result, with a permission warning attached to device results when present.
- Optional live check and more than ten path devices -> no live polling in the `get_trace` path; no explicit product-level response to this condition is established.
- Individual polling errors -> attached per-device error strings where available.
- `icmp` request -> port parameters are replaced with sentinel values before database invocation; meaning of the sentinel is not established.
- Device result shape uses iteration/positional column mapping from database rows; maintainability risk, **not evidence that current UI is necessarily broken**.

## Key discoveries and open semantics

- The sibling SSSR author-confirmed SCN-006 **is an operator evidence/explanation scenario**, not a generic Boolean access-decision service.
- The source distinguishes a **stored/cached route-policy analysis** from an **optional online device check**. They may disagree; no normative reconciliation rule was found.
- A check involving several firewalls is rendered as several rows. The program does not demonstrate a formal aggregation principle over all possible paths.
- Stored procedures contain material domain logic. Primary SQL bodies are now located and partially traced in the SSSR repo; deeper transitive SQL and deployed versions still warrant inspection.
- Whether a ZnI record is approval authority, a historical change log or just supporting context is unknown.

Questions: [Q-003/Q-004/Q-012](open-questions.md). The historical scenario is documented in the sibling [SCN-006 requirements](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/docs/legacy/requirements/SCN-006-traffic-check.md). Future-scope behavior and deployed data contracts remain separate questions.

## SQL logic now directly observable in SSSR_XLAM

Pinned sibling revision `d1abb6fac6b4147e28abce9c934ceffbba25570f`:

- [`FindFirewallMain.sql`](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/artifacts/sql/used/FindFirewallMain.sql): chooses the candidate system universe, builds host tuple and NAT representations, calls `GetDOP`, and adds NAT-derived placements only if source/destination routing and interface joins corroborate them. Returns logical system plus interface metadata.
- [`FindACLMatch.sql`](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/artifacts/sql/used/FindACLMatch.sql): resolves numeric IPv4 ranges, matching service ranges and normalized `A_Rule3`/ACL policy structures; constrains to relevant placement interface/ACL information; orders rows by hostname, ACL and rule number. Matching rows contain both actions (not limited to permit).
- [`SCN-006 requirement reconstruction`](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/docs/legacy/requirements/SCN-006-traffic-check.md): explicitly records author-confirmed interpretation: matched permit/deny ACL evidence shown in order; no-match remains evidence, **not inferred implicit deny**. Vendor live diagnostics stay a distinct evidence layer.

**Do not re-infer application policy semantics from SQL alone**: the SSSR documents already record user intent and an author correction. The SSSR `docs/legacy/scenarios.md` overview contains older implicit-deny wording; use the more specific corrected SCN-006 requirements when reconciling.

Not verified here: complete `GetDOP`/NAT procedure call graph; dynamic installation schema/version; production run output. Further source review should target those rather than repeat the resolved operator-purpose question.
