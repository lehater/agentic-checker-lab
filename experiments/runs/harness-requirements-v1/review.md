# Product Requirements — source disposition и содержательный review

Выполнено действующим инженерным агентом по PDEC-CHECKER-003, не независимая человеческая подпись. Итоговый Semantic Review: **REJECTED для всего checker.requirements**, с сохранением source-supported intent subset. Причина — не отсутствие полномочий и не техническая схема, а недостаточность подтверждённого наблюдаемого product scope и критериев принятия свидетельств.

## Source-by-source disposition

| Источник / утверждение | Класс | Disposition |
| --- | --- | --- |
| PDEC-001: оператор объяснимо исследует поток | Нормативное основание / цель | purpose; не придумывать отдельный обязательный use-case artifact |
| PDEC-001: релевантные placements | Нормативное основание | REQ-CHECKER-001; критерий релевантности/поддерживаемый scope Q-PR-001 |
| PDEC-001: подходящие сохранённые ACL | Нормативное основание | REQ-CHECKER-002; не повышать автоматически до every covering rule; supported matching scope Q-PR-001 |
| PDEC-001: порядок обработки | Нормативное основание | REQ-CHECKER-003; не выдумывать глобальный порядок несвязанных policy contexts |
| PDEC-001: достоверность источников | Нормативное основание с существенной неизвестностью | REQ-CHECKER-004; наблюдаемый результат при недостатке свидетельств Q-PR-002 |
| PDEC-001: отсутствие обязательного универсального verdict | NOT_REQUIRED | REQ-CHECKER-005; не превращать в абсолютный запрет scoped diagnostics |
| PDEC-001: no-match не равен DENY/ALLOW | Нормативная отрицательная граница | REQ-CHECKER-006; отдельный формат no-match output не принят |
| PDEC-001: наличие подходящего правила не доказывает общесистемный effective verdict | Нормативная отрицательная граница | REQ-CHECKER-007 |
| PDEC-001: IPv4/IPv6, ports, scope, freshness/completeness | Неизвестности | Q-PR-001/002; отсутствие решения не трактуется как NOT_REQUIRED |
| PDEC-002/003 | Контекст governance | Полномочия и допустимый production contract; не product behavior и не semantic prerequisites |
| Reconciliation Q-REC-001 | Контекст, закрытый owner gate | Закрыт PDEC-003; повторного согласования нет |
| Reconciliation Q-REC-002 | Неизвестность | Уточнён до Q-PR-001 и Q-PR-002; inventory не объявлен полным |
| Стратегия / roadmap | Контекст | Самостоятельный Checker, лабораторная методика; не спецификация runtime или UI |
| scenario README: proposed fixture/IPv4/CLI/API slice | Историческое исследовательское предложение | Не принимается в target scope; Q-PR-001 |
| SCN-006 REQ-034, RULE-021 | Исторический пример | Tuple, IPv4, source-port/default/ICMP не принимаются автоматически; Q-PR-001 |
| SCN-006 REQ-035, SCN-002 dependency | Исторический пример / downstream | Не принимать every placement, routing/correction/NAT алгоритм; observable relevance scope Q-PR-001, алгоритм вне Product |
| SCN-006 REQ-036, RULE-018/019 | Исторический пример / частичное дублирование owner evidence | Порядок поддержан PDEC-001; all rules/actions/fields не принимаются дополнительно |
| SCN-006 REQ-037, RULE-020 | Исторический пример / частичное дублирование | Отрицательная граница принята только по PDEC-001; explicit no-match output и политика unknown остаются Q-PR-002 |
| SCN-006 REQ-038 | Исторический контекст | ZnI/address metadata не включены как функции |
| SCN-006 REQ-039, RULE-022 | Исторический пример | Live diagnostics не обязательны и не разрешены этим циклом; нельзя выводить ни target live support, ни offline-only |
| SCN-006 REQ-040, SCN-004 dependency | Исторический пример / неизвестность | Last-known vs live evidence помогает сформулировать Q-PR-002; timestamps/thresholds не добавлены как требования |
| Product As-Is: URL/auth/form/DB/polling/rendering и branches | Исторический пример / downstream | SQL/Django, groups, 10-device limit, tables, API shape и runtime не принимаются |
| Product As-Is: result fields/ZnI/IP metadata, transitive SQL/deployed version | Контекст / неизвестность / downstream | Источник не является target oracle или product requirement; новая историческая разведка не нужна |
| Точные matching algorithms, domain entities/invariants, storage, architecture, interface | Downstream-решения | Не исполняются; вопрос о поддерживаемом поведении не решается выбором алгоритма |
| Конфликт accepted owner sources | Противоречие | Не обнаружен. Исторические более сильные формулировки не равны accepted To-Be и не требуют повторного решения owner intent |

## Semantic checks

- source-discipline: PASS для семи выделенных intent rows. Каждый ссылается на принятый checker.problem; SSSR/Product не подменяют canonical prerequisite.
- authority-boundary: PASS. PRODUCT-REQUIREMENTS действует по PDEC-003; других Authority не назначает.
- no-invention: PASS для subset и отрицательных границ. Пробелы сохранены как реальные Questions, не заполнены default scope.
- observable-product-level: **INCOMPLETE для всего артефакта**. Высокоуровневые acceptance clauses проверяют поддержанные ограничения, но не определяют минимальный поддерживаемый набор входов/релевантных свидетельств и результат при недостатке данных. Переименовать это в полный product intent contract без решения Q-PR-001/002 означало бы скрыто принять ограничение scope. Критерии в кандидате — спецификация частичных проверок, не выполненные runtime tests и не независимый oracle.
- no-downstream-design-promotion: PASS. Не выбраны API/CLI, архитектура, алгоритмы или fixture-only режим.

REQ-CHECKER-001..007 сохраняют нормативные утверждения, непосредственно подтверждённые owner framing. Статус ACCEPTED у строк означает только индивидуально рассмотренный нормативный intent в schema product-requirements/v1 (схема допускает лишь ACCEPTED/RETIRED). Он не означает ACCEPTED artifact admission: кандидат помечен CANDIDATE_BLOCKED_NOT_CORE_PROVIDER, весь review REJECTED, provider не регистрируется. Эти ID зарезервированы и не должны переиспользоваться для другого смысла.

Ни один положительный acceptance identity, lifecycle row или provider для checker.requirements не создаётся. Strict API получает заранее вычисленный идентификатор **реальной попытки**, возвращает его только в REJECTED admission; это не действующий acceptance identity.

Минимальные вопросы: Q-PR-001 (поддерживаемый product slice / observable input и matching/relevance boundary) и Q-PR-002 (наблюдаемые условия приёмки evidence credibility/partial results). Владелец может подтвердить узкий первый slice; не требуется решить всю будущую систему, выбрать архитектуру или алгоритмы. После ответов — доработка того же requirements candidate, CREATE, новый содержательный review/strict admission. Предыдущее checker.problem не требует пересоздания.
