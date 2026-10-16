# Checker — первый принятый срез

- [Проблема владельца](problem-framing-decision.md) — `checker.problem CURRENT`.
- [Решение о границах первой версии](first-slice-product-decision.md) — PDEC-CHECKER-004.
- [Канонические Product Requirements](../../.harness/knowledge/checker-requirements.yaml) — **13 действующих требований**, `checker.requirements CURRENT`.
- [Делегирование Domain и Verification](domain-verification-delegation.md) — PDEC-CHECKER-005.

Обязательное поведение: исследовать заданный IPv4 TCP/UDP поток, используя предоставленные policy contexts и сохранённые снимки ACL; показывать подходящие правила в известном порядке, источник и ограничения достоверности. Не выводить необоснованный общесистемный Permit/Deny.

**Открыто:** Q-DV-002 — конкретная ACL matching-семантика и независимый oracle. `checker.domain-use-case` и `checker.verification-strategy` — **BLOCKED**. Q-DV-001 исключён как ошибочная обязательная предпосылка skill; отдельная Domain Strategy не требуется для выбранного first slice, а общепроектная применимость остаётся UNASSESSED. Полнота всего Checker и subject inventory не подтверждена.

Для состояния приёмки использовать [Project Publication](../../.harness/project-publication.yaml), а не прежние отчёты. Историю изменений брать из Git.
