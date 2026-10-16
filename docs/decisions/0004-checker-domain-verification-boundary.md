# ADR-0004 — scoped Domain/Verification production contracts

Статус: ACCEPTED в пределах PDEC-CHECKER-005; предметная ACL-семантика не принята этим ADR. Дата: 2026-10-16.

В Engineering Graph объявлены две необходимые для first slice Authorities:
DOMAIN-USE-CASE-DESIGN и VERIFICATION-DESIGN с capabilities
`checker.domain-use-case` и `checker.verification-strategy`.

`checker.domain-use-case` непосредственно зависит от `checker.requirements`.
Самостоятельная стратегическая классификация subdomains, инвестиций или ownership
не потребляется выбранным Consumer, поэтому DOMAIN-STRATEGY не является
необходимым входным этапом. Это scoped-оценка: project-wide DOMAIN-STRATEGY
остаётся UNASSESSED, а не молча становится NOT_APPLICABLE.

`checker.verification-strategy` потребляет `checker.requirements`
и `checker.domain-use-case`: полный first-slice verification contract
зависит от независимо установленной семантики matching. Ранее
выделяемые проверки требований, не зависящие от matching, могут
проектироваться в черновиках отдельно без принятия всей Capability.

Исправление Harness #224 устранило безусловный input Strategic Domain
ownership из domain-use-case skill. Q-DV-001 являлся ошибочным
вопросом, возникшим из этого input, и удалён из активного Core
через новый атомарный CAS snapshot; историческая запись находится в Git.
Никакого фиктивного resolution/acceptance_id не создаётся.

Q-DV-002 остаётся реальным семантическим препятствием: принятые ACL
match/non-match predicates, роль порядка и независимо обоснованные
expected cases отсутствуют. Обе downstream Capabilities остаются BLOCKED,
без providers и lifecycle assertions. Existing `checker.problem` и
`checker.requirements` сохраняют CURRENT и прежние admission identities.

Это не реализация, не утверждение полного product subject inventory и не
принятие неизвестных ACL syntax/masks, implicit deny, first-match, verdict
или algorithm.
