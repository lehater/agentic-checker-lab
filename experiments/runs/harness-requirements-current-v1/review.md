# Semantic Review — продолжение checker.requirements

Решение: **ACCEPTED для первого slice PDEC-CHECKER-004**. Выполнено действующим инженерным агентом по PDEC-CHECKER-003. Не независимая человеческая подпись и не доказательство runtime behavior. Рассмотрены существующий кандидат REQ-CHECKER-001..007, прежние review/admission, реальные опубликованные Q-PR-001/002 и новое owner product decision. Исторический research не повторялся.

## Полнота принятого product decision

| Принятый смысл / источник | Требования / disposition |
| --- | --- |
| PDEC-001: placements, ACL, порядок, credibility | Исходные statements REQ-CHECKER-001..004 сохранены дословно; acceptance criteria уточнены новым решением |
| PDEC-001/004: universal verdict NOT_REQUIRED, no-match и matching rule не доказывают effective verdict | REQ-CHECKER-005..007 сохранены; критерии уточняют complete/no-data/unknown cases и не запрещают все scoped interpretations |
| PDEC-004 Q-PR-001.1: source/destination IPv4, TCP/UDP, соответствующие ports | REQ-CHECKER-008..011; четыре независимо теряемых входных аспекта |
| Q-PR-001.2: предоставленные релевантные contexts/placements, нет обязанности самостоятельного route discovery | REQ-CHECKER-012 и критерии 001; ограничение auto route также в non_goals |
| Q-PR-001.3: предоставленные stored ACL snapshots, known order внутри context, context и происхождение | REQ-CHECKER-013/014/015, уточнённые критерии 002/003. Произвольная ACL syntax, порядок между независимыми contexts или all-covering сверх принятой формулировки не вводятся |
| Q-PR-001.4: независимая проверяемость поддерживаемых совпадений; алгоритм/legacy не oracle | REQ-CHECKER-028, критерий 002; expected examples должны приходить из независимого контракта. Реальные matching test cases не выдуманы в этом review |
| Q-PR-001.5: live devices, ICMP, IPv6, route discovery, NAT вне первой версии | Явные non_goals; это граница поддерживаемого slice, не утверждение о поведении reject/ignore неподдерживаемых входов и не запрет будущего расширения |
| Q-PR-001.5: CLI/API, architecture, data model, runtime не приняты | downstream_open_decisions, без нового требования или Authority |
| Q-PR-002.1: confirmed/uncertain, provenance каждого source, known date, known completeness, неизвестные metadata explicit unknown | Критерий 004, REQ-CHECKER-015..019; origin unknown включён в критерий 015. Не подставлять выдуманные значения |
| Q-PR-002.2: partial explainable result допустим с видимыми limits/unestablished facts; не маскировать как полный | REQ-CHECKER-020..022. «Допустим» не заменён обязанностью всегда возвращать partial или обязательной failure policy |
| Q-PR-002.3: complete snapshot no-match отличается от missing data и unknown completeness | REQ-CHECKER-023/024, отрицательное ограничение 006 |
| Q-PR-002.4: stale только с подтверждённым основанием, нет TTL, unknown date не current | REQ-CHECKER-025..027; пример external classification — пример основания, не обязательная новая интеграция |
| Q-PR-002.5: universal Permit/Deny не обязателен | Дубликат 005, без нового ID |
| Governance/provenance PDEC-003/004 | Полномочия и принятые product choices; PDEC-004 — прямое evidence original Product assertions, не фиктивный accepted prerequisite artifact |

Новая provenance не меняет checker.problem: старые семь intent statements derived_from реальных DISCOVERY atoms принятого prerequisite. Новые product requirements — оригинальные PRODUCT-REQUIREMENTS assertions по прямому owner decision, source_refs указывают PDEC-004. Поле source_refs является evidence, а не обходом canonical-reference boundary. Исторические SSSR/Product не используются как принятая новая спецификация.

## Обязательные semantic checks

- **source-discipline — PASS:** все 28 REQ имеют непустые source_refs, существующие 001..007 сохраняют ID/statement и прежние ссылки; каждое новое обязательство отображено на принятое решение выше. Нет нормативного утверждения из исторического алгоритма или runtime.
- **authority-boundary — PASS:** Product принимает только observable first-slice input/result/constraints; DISCOVERY не меняется. Новые Domain/Architecture/Verification Authorities не назначаются.
- **no-invention — PASS:** нет ACL algorithm/syntax, TTL, UI/API, нового universal Permit/Deny. Принята предоставленная информация, но не произвольный формат её хранения. Исключения первой версии не расширены на весь будущий продукт.
- **observable-product-level — PASS:** требования разделяют входы, наблюдаемые результаты и допустимость partial. Acceptance criteria описывают независимые условия различения complete no-match/missing snapshot/unknown completeness, known/unknown metadata, внутри-context order и отсутствие ложных verdicts. Это product acceptance contract, не реализация и не выполненный oracle.
- **no-downstream-design-promotion — PASS:** конкретные ACL semantics и независимые expected match examples потребуются перед реализацией поддерживаемого matching. Их будущая конкретизация прямо разрешена PDEC-004 и сохранена как downstream_open_decisions; она не является новым Product blocker или разрешением агенту выбрать алгоритм. Первое slice product решение не требует законченного downstream дизайна для CURRENT Product Requirements.

Существенных новых продуктовых противоречий не обнаружено. Q-PR-001/002 содержательно отвечены PDEC-004; исходные записи сохраняются и разрешаются Core.resolve_question через новый принятый CHECKER-REQUIREMENTS artifact, acceptance_id admission и supersedes_acceptance_id ABSENT (у этого artifact ранее не было принятой identity). Прежняя REJECTED attempt identity не является superseded acceptance.

Стадия разрешения — только предложенный in-memory snapshot, до admission ничего не публикуется. Caller/integration владеет семантической валидностью Core identities; atomic publish разрешён только после ACCEPTED admission той же identity и terminal validation CURRENT для обеих Capabilities. Никакого ручного удаления blockers, подмены answer_from или обновления Discovery acceptance нет.

Полнота этого review ограничена всеми принятыми statements PDEC-004 первого slice. Subject-obligation inventory, concern completeness всего Checker, precise Domain matching contract и независимый oracle не объявлены завершёнными.
