# TASK-004 — first-slice Domain / Verification Design

Дата: 2026-10-16. Base main: `b8779db`. Pin: `442db854c3a736a5e500b4a41664b80981b0d94c`.
Локальное рабочее дерево на старте было чистым. Одна ветка, один PR, без merge.

| Capability | Authority | Итог |
| --- | --- | --- |
| checker.problem | DISCOVERY | CURRENT, прежние identity/evaluation/lifecycle |
| checker.requirements | PRODUCT-REQUIREMENTS | CURRENT, REQ-CHECKER-001..028 без изменений |
| checker.domain-use-case | DOMAIN-USE-CASE-DESIGN | BLOCKED: Q-DV-001 и Q-DV-002 |
| checker.verification-strategy | VERIFICATION-DESIGN | BLOCKED: Q-DV-002, strict admission REJECTED |

Applicability двух новых Authorities — UNRESOLVED, а не REQUIRED по одному
делегированию. Реальные providers не зарегистрированы. DOMAIN-STRATEGY остаётся
UNASSESSED; её инвентаризация/производство не выполнялись.

[Минимальный доменный draft](domain-contract.md) фиксирует только принятые
Product facts: IPv4 TCP/UDP и оба порта, предоставленные contexts и snapshots,
известный порядок внутри context, принадлежность правил, no-match/missing/unknown,
metadata и partial/freshness boundaries, rule action ≠ universal verdict.
Новые predicates, syntax/masks, implicit deny, first-match/all-match и algorithm
не принимались. [ADR](../../../docs/decisions/0004-checker-domain-verification-boundary.md)
обосновывает минимальное расширение Engineering Graph и Questions.

[Verification candidate](verification-candidate.yaml) имеет восемь проверок с
явными disposition для всех 28 requirements, TEST method, конкретными evidence
requirements и независимыми upstream oracle sources. Это проверочный план, не
отчёт о выполнении Checker. Matching BLOCKED, порядок с independently matched
labels CONDITIONAL; остальные intents можно уточнять независимо.

[Восемь сценарных drafts](scenario-drafts.yaml): полное пустое множество правил,
missing snapshot, unknown completeness, известные metadata, неизвестные metadata,
partial/incomplete/missing, подтверждённая внешняя stale classification и старая
дата без TTL. Ожидания заданы из requirements до реализации; SQL и matcher не
использовались. Положительные/отрицательные непустые matching cases, TCP/UDP
predicate boundaries и matching-dependent order/action cases пока не готовы.
Drafts не означают accepted acceptance-scenarios Capability.

## Точные остановки routed skills

- [domain-use-case](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/domain-use-case/SKILL.md): input **“accepted Strategic Domain ownership for the selected scope”** отсутствует. Q-DV-001 адресован владельцу проекта через scoped DOMAIN-USE-CASE-DESIGN; нужен реальный принятый ownership provider. Domain admission не имитировался.
- [verification-strategy](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/verification-strategy/SKILL.md): stop **“a verification objective depends on upstream behavior or semantics that are not accepted”**. Q-DV-002 адресован DOMAIN-USE-CASE-DESIGN: минимальные поддерживаемые ACL facts/predicates, роль порядка, unknown/unsupported boundary и независимые expected match/non-match cases. Не требуется произвольно выбирать универсальный ACL язык.
- [acceptance-scenarios](https://github.com/lehater/harness/blob/442db854c3a736a5e500b4a41664b80981b0d94c/skills/artifacts/acceptance-scenarios/SKILL.md): **“Confirm Verification Strategy is accepted.”** Не выполнено; после проверки inputs skill не исполнялся как production/admission. Неоспоримые drafts сохранены для продолжения.

## Admission, публикация и воспроизводимость

[Semantic Review](review.md), [strict admission](semantic-admission.yaml),
[execution evidence](evidence.json), [verification](verification.json).
Schema VALID сама по себе не принимает семантику. Реальный strict evaluator
вернул REJECTED с SEMANTIC_REVIEW_REJECTED; lifecycle assertion отсутствует.
Отказ — ожидаемый инженерный исход, не отказ автоматического approval review.

Publication revision:
`sha256:f38832e09ce67f6713d26e1a06ab04d1af786d5cbd148e6e702181201c938334`.
Parent: `sha256:94bc167d0108b5b4b90dcea6cefd0af3f5ba5132091f0ee20756163127da9852`.
Официальные prepare/publish/read-back API атомарно сохраняют Core Questions
вместе с неизменёнными upstream acceptance/lifecycle, с проверкой CAS.

Decision Roadmap и Semantic Closure для нового scoped Consumer — BLOCKED.
Engineering Coverage неполон; Project Frontier — READY из-за дальнейших coverage
reconciliation actions, при двух BLOCKED design items. Это не готовность реализации
и не разрешение общей инвентаризации в этой задаче.

Из корня репозитория:

```sh
python3 .harness/harnessw.py sync
python3 experiments/runs/harness-domain-verification-v1/execute.py
python3 experiments/runs/harness-domain-verification-v1/verify.py
make check
```

Проверены два идентичных replay, стабильные байты публикации, неизменные upstream
providers/evaluations/lifecycle и Q-PR resolutions, coverage всех 28 requirements,
отсутствие фиктивного Strategic provider, отказ stale CAS и ложного CURRENT.
Source/skill SHA256 находятся в evidence. CoderMind, codegen, реальные устройства
и Checker tests не запускались. Следующий шаг: реальный scoped Strategic ownership,
затем domain matching contract + независимые labels, завершение стратегии,
review/strict admission и только затем acceptance-scenarios.
