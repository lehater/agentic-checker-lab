# Исторический Checker — смысловые сведения

Статус: **SOURCE-DERIVED**, не новая принятая спецификация.

Источники:
- https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/docs/legacy/requirements/SCN-006-traffic-check.md
- https://github.com/lehater/product/blob/759fcd7b773b12144a14f4a990cfba11bddc3527/docs/discovery/access-assessment-as-is.md

По автором подтверждённому SCN-006 оператор проверяет одну конкретную IPv4 tuple, видит все релевантные firewall/policy placements, все stored ACL rules, покрывающие tuple, **в policy order** с Permit и Deny, дополнительные контекстные сведения и, если устройство/права поддерживают, отдельно живой vendor diagnostic.

- REQ-034 — source/destination IP, protocol, source/destination port где применимо.
- REQ-035 — релевантные firewall placements из общей routing/correction модели.
- REQ-036 — все covering ACL rules, порядок и действия.
- REQ-037 — no-match остаётся evidence, не универсальный allow/deny.
- REQ-038 — optional diagnostic metadata не меняет смысл matching.
- REQ-039 — live packet-tracer evidence отдельным слоем.
- REQ-040 — stored snapshots/route evidence/live evidence различаются по свежести и происхождению.

RULE-018..022: relevance != permission; ordering matters; no-match uninterpreted; source port carried but исторически редко ограничивался; stored ≠ live.

Непроверенные аспекты: deployed SQL/коды вендоров, все NAT/route сценарии, полнота snapshots, source-port defaults, способ согласования разнородных evidence. Эти вопросы нельзя заполнять придуманными требованиями.

Product Django и SQL процедуры не являются целевой архитектурой. Fixture-based first slice — **новое ограничение проекта**, подлежащее отдельному принятому требованиям P2.
