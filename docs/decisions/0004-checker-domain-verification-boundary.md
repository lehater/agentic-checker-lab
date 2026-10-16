# ADR-0004 — scoped Domain/Verification production contracts

Статус: ACCEPTED в пределах делегирования PDEC-CHECKER-005; предметная семантика
не принимается этим ADR. Дата: 2026-10-16.

В Engineering Graph добавляются только DOMAIN-USE-CASE-DESIGN и VERIFICATION-DESIGN
с first-slice capabilities checker.domain-use-case и checker.verification-strategy.
Каждая непосредственно зависит от checker.requirements. Технический Consumer
объединяет их для проверки этого решения; он не является implementation Consumer.

Accepted Strategic Domain ownership отсутствует. Его нельзя моделировать фиктивным
provider: Q-DV-001 сохраняет недостающую предпосылку. Отсутствующий matching contract
и oracle отражены Q-DV-002. Verification может независимо проектировать проверки
принятых Product facts, но неполная стратегия не допускается в CURRENT.

Следствие: оба направления могут быть честно BLOCKED; новые canonical providers
и lifecycle assertions не создаются. Когда появятся реальные принятые upstream
providers, dependencies уточняются по содержанию и admission выполняется заново.
Это минимальное расширение, без полной инвентаризации Authorities и без выбора
программной архитектуры. Принятые problem/requirements identities сохраняются.
