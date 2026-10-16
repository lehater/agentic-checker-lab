# PDEC-CHECKER-005 — делегирование Domain Use-Case Design и Verification Design для первого slice Checker

**Статус: OWNER-AUTHORIZED, SCOPED; PRODUCTION AND ADMISSION PENDING.** Дата: 2026-10-16.

## Основание

После принятия `checker.problem CURRENT` и `checker.requirements CURRENT` в PR #20 владелец получил предложение делегировать две ограниченные инженерные области:

1. **Domain-Use-Case Design** — поддерживаемая семантика сопоставления IPv4 TCP/UDP потока с сохранёнными ACL-правилами, порядок обработки и границы неопределённости.
2. **Verification Design** — независимые проверочные примеры совпадений, несовпадений, порядка и неполных источников с трассировкой к принятым требованиям.

На прямой запрос подтвердить обе области владелец ответил **«Да, подтверждаю»**.

Это **делегирование права выполнять реальную работу в данных границах**, не принятие новой ACL-семантики, стратегии домена, test oracle или acceptance result.

## Разрешённые работы

### DOMAIN-USE-CASE-DESIGN

- Authority `DOMAIN-USE-CASE-DESIGN` авторизована для **конкретного first-slice поведения**, следующего из `checker.requirements` и PDEC-CHECKER-004.
- Агенту разрешено определить минимальную непосредственно необходимую Capability с knowledge kind `domain-use-case`, обоснованный production contract и **только непосредственные** accepted dependencies, не подставляя исторический граф целиком.
- При успешном подтверждении применимости и prerequisite contracts агент вправе выполнить официальный routed `domain-use-case` skill, substantive Semantic Review, strict admission, lifecycle/CAS publication и read-back.
- Описать в доменных терминах: что значит поддерживаемый match/non-match для принятого набора flow/snapshot facts; scope/порядок внутри одного policy context; отличие rule action от универсального verdict; и no-match, incomplete, missing или unknown evidence.
- **Важный контракт Harness:** pinned `domain-use-case` skill требует *accepted Strategic Domain ownership*. В проекте пока нет принятой `DOMAIN-STRATEGY` Capability. Агент должен проверить реальную достаточность предпосылок и не выдавать ссылки на каталог, проектное делегирование или Product Requirements за автоматически принятое стратегическое владение. Если оно действительно необходимо и отсутствует — создать **один узкий предметный Authority/ownership Question**, не выдумывая Strategy provider и не проводя ложный admission.
- Не выбирать aggregates, tactical model, schema, data storage, маршрутизацию, ACL implementation algorithm, API, транспорт, платформу или architecture.

### VERIFICATION-DESIGN

- Authority `VERIFICATION-DESIGN` авторизована разработать ограниченный `verification-strategy` для принятого first slice; при удовлетворении штатных предпосылок — `acceptance-scenarios` с независимыми входами и ожидаемыми результатами.
- Обязательна прослеживаемость к **всем `REQ-CHECKER-001..028`**, либо явная честная disposition для тех проверок, которые требуют ещё не принятого доменного контракта.
- Отдельно проверить matched/non-matched rule, known within-context order, complete no-match vs missing snapshot vs unknown completeness, known/unknown source metadata, partial explainable results, no invented TTL, no universal Permit/Deny.
- **Независимый oracle** должен быть выведен из принятых Product/Domain semantic contracts и независимо заданных expected cases. Генерация ожиданий по собственному алгоритму агента/наследуемой SQL-логике и последующее тестирование того же алгоритма не являются независимыми evidence.
- По pinned `verification-strategy` skill evidence план должен быть конкретным; по `acceptance-scenarios` skill допустимы только сценарии, ожидаемые результаты которых определены принятыми upstream contracts. Если нет утверждённого matching contract — подготовить неоспоримые сценарии и зафиксировать **адресный Question о конкретной недостающей семантике** вместо фабрикации проверок.
- Разрешены соответствующие agent semantic review, strict admission и coherent atomic CAS publication **только после успешной проверки** настоящих production/source/knowledge/decision contracts.

## Границы делегирования

- Принятые upstream: `checker.problem` и `checker.requirements` для PDEC-CHECKER-004. Их смысл, Core identities и Lifecycle нельзя менять только ради обхода новой стадии.
- Это решение **не** утверждает применимость/контент `DOMAIN-STRATEGY`, `TACTICAL-DOMAIN-DESIGN`, `SYSTEM-ARCHITECTURE`, `TEST-DESIGN`, `IMPLEMENTATION-DESIGN` и иных Authorities, не внедряет `NOT_APPLICABLE` и не принимает полный Checker subject inventory.
- Утверждённая первая версия ограничена IPv4 TCP/UDP, предоставленными policy contexts/placements и сохранёнными ACL snapshots. Нет live-device access, route discovery, NAT или универсального системного Permit/Deny как обязательного результата.
- Разрешение строить **семантический контракт** не разрешает произвольно решать, например, ACL implicit deny/default, конкретный wildcard/mask/syntax, first-match vs all-match, rule action priority, порядок между контекстами, обработку отсутствующей metadata: каждое не заданное upstream решение должно быть либо обосновано принятым независимым источником, либо эскалировано соответствующему владельцу. Не считать historical SSSR/Product To-Be acceptance.
- Не подменять Verification Design предметным Product/Domain authority и не называть выполнение synthetic fixture действительным независимым runtime oracle без утверждённых ожидаемых значений.
- Не изменять `lehater/harness`, не запускать CoderMind, генерацию кода Checker, операции с реальными устройствами, не выбирать язык, UI/API, storage или системную архитектуру.
- Использовать один focused execution branch/PR, краткие воспроизводимые evidence и действующие pinned Consumer Pack instructions/skills; запрещено готовить ещё один общий research-only PR как замену предметному результату.

## Критерий завершения

**Успех:** принятые `CURRENT` domain-use-case и verification artifacts в том объёме, где prerequisites и независимые семантические ожидания действительно установлены, с честным first-slice coverage и конкретным следующим шагом.

**Действительный BLOCKED:** воспроизводимое нарушение конкретного prerequisite (например, отсутствующее accepted Strategic Domain ownership), недостающий узкий доменный факт либо oracle, оформленный минимальным адресным Question; ранее принятые `checker.problem` и `checker.requirements` остаются CURRENT. Отсутствие доказательства нельзя скрывать новым default или объявлением всего проекта COMPLETE.
