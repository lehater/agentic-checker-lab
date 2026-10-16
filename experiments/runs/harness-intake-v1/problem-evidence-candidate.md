# Problem Evidence — Checker

**DRAFT — NOT SEMANTICALLY ACCEPTED**

Кандидат для `checker.problem`, subject `CHECKER-OFFLINE-CANDIDATE`, кандидатная Authority `DISCOVERY`. Основание производства: фактические `target-evaluation.stdout` (CREATE) и `agent-routing.stdout` (problem-evidence). Это не Core provider и не Project Publication.

## Проблема, актор и желаемый исход

Сетевому администратору/оператору нужно понять, какие сведения о конкретном потоке доступны и насколько им можно доверять. Одного непрозрачного ответа allow/deny недостаточно для объяснения релевантных мест применения политики, сохранённых правил и ограничений данных.

Желаемый исход: оператор может проследить связь traffic tuple → релевантные placements → все covering stored rules в порядке политики, увидеть no-match как отдельный факт, происхождение и свежесть свидетельств. При наличии допустимой live diagnostics её результаты представлены отдельно. Это описание потребности, не принятый контракт нового продукта.

## Свидетельства и пределы утверждений

Все пути ниже заданы от корня репозитория. Immutable provenance: `tooling/fixtures/checker-intake/README.md`.

| Класс | Локальный источник / исходный раздел | Поддерживаемое утверждение |
| --- | --- | --- |
| author-confirmed historical | `tooling/fixtures/checker-intake/sssr-scn-006.md`, Purpose; REQ-034 | Историческая потребность администратора в объяснении конкретного host-to-host tuple; IP, protocol, ports where applicable. Историческая реализация IPv4 не определяет новый API. |
| author-confirmed historical | Там же, REQ-035; Shared dependency on SCN-002 | Релевантные placements используют общий routing/correction контекст. Полный алгоритм и production routing этим снимком не доказаны. |
| author-confirmed historical | Там же, REQ-036; RULE-019 | Все covering stored permit/deny правила сохраняют policy order; не вычисляется универсальный effective verdict. |
| author-confirmed historical | Там же, REQ-037; RULE-018/020 | Relevant ≠ match ≠ permit; no-match не означает deny или выбранный blocking point. |
| author-confirmed historical | Там же, REQ-039/040; RULE-022 | Stored snapshots — last-known, optional live vendor diagnostics — отдельное свидетельство. |
| observed legacy | `tooling/fixtures/checker-intake/product-access-as-is.md`, Observed request and processing path; Observed result structure | Python/SQL/UI показывали отдельные группы path/policy/context/live данных. Это наблюдение исходников, не runtime или deployed-data проверка. |
| observed legacy | Там же, Branches and edge cases visible in source; SQL logic now directly observable in SSSR_XLAM | Permissions, предел 10 устройств одного live пути, ICMP sentinel и SQL процедуры — исторические технические детали, не требования новой системы. |
| new proposed scope | `docs/scenario/README.md`, Предполагаемый минимальный вертикальный срез; Вне первой задачи | Offline fixture providers и небольшой CLI/API — гипотеза лаборатории, не историческое поведение и не принятие target scope. |
| unknown | SSSR, To-Be audit notes; Product, Key discoveries and open semantics; `questions.md` | Target actor/success criterion, полнота placements, freshness policy, match/protocol scope, делегирование и oracle требуют решения владельцев. |

SSSR snapshot: commit `d1abb6fac6b4147e28abce9c934ceffbba25570f`, blob `c434c0e7b0fe43561d4b7a543688f3ced9a9c619`. Product snapshot: commit `759fcd7b773b12144a14f4a990cfba11bddc3527`, blob `220d37864a6bbd4e111a62eaa43c16320a38e32d`; описывает code baseline `891d751d50d85a260544c43e776dc51496bdd8db`.

## Ограничения этого пилота

Только discovery и кандидатное обрамление проблемы. Нет принятия требований, проектирования архитектуры, реализации, тестового oracle, production access или device interactions. Offline fixture не доказывает полноту реального маршрута. UNKNOWN не равен пустой политике. SQL, Django layout, vendor commands, sentinel ports и historical permissions не повышаются до target требований.

Все последующие продуктовые, доменные и технические решения остаются открыты в `questions.md`. Черновик не зарегистрирован: шаг acceptance/registration skill сознательно не выполнен по явному ограничению оператора.
