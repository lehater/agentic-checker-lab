# Минимальный контракт first slice — upstream facts, не принятый Domain provider

Статус: BLOCKED. Основание: PDEC-CHECKER-004/005 и CURRENT checker.requirements.

Инициатор — оператор, исследующий поток. Вход: конкретные IPv4 source/destination,
TCP либо UDP, предоставленные source/destination ports; предоставленные policy
contexts/placements и связанные сохранённые ACL snapshots. Эти факты не определяют
синтаксис ACL или представление интерфейса.

Успех на уровне принятого Product: показать переданные релевантные placements,
подходящие сохранённые правила с принадлежностью context, сохранить известный
относительный порядок показываемых правил внутри context. Межконтекстный порядок
не установлен. Это не решение first-match/all-match и не правило приоритета action.

Match/non-match для непустого snapshot пока НЕ определён: нет нормативного
predicate contract для адресов/портов/protocol и допустимых ACL facts. Нельзя
превратить совпадение tuple по равенству в принятый ACL contract. Полный пустой
snapshot не содержит подходящих сохранённых правил независимо от predicate;
это наблюдение о множестве, а не выбор implicit deny.

No-match в полном известном snapshot отличается от missing snapshot и unknown
completeness. Incomplete не доказывает полноту отсутствия совпадений. Неизвестные
origin/date/completeness остаются неизвестными; известные сохраняются.
Частичный результат допустим с ограничениями и неустановленными фактами, но
возвращать его всегда не предписано. Stale требует подтверждённого основания;
TTL не задан, отсутствие даты не означает freshness.

Action сохранённого Permit/Deny правила — факт правила, а не доказанный
общесистемный effective verdict. Наличие или отсутствие подходящего правила
само по себе не даёт universal verdict. Универсальный Permit/Deny не является
обязательным результатом.

Отказы, неверный вход, syntax, masks/wildcards, defaults/implicit deny,
first-match/all-match, action priority и неоднозначный порядок не определены
этим draft. Алгоритмы, aggregates, API, storage и live devices не выбирались.

Q-DV-001: владелец проекта должен обеспечить accepted Strategic Domain ownership
для этого scope через надлежащий процесс DOMAIN-STRATEGY. Делегирование PDEC-005
не заменяет provider. До этого domain-use-case skill останавливается на inputs.

Q-DV-002: DOMAIN-USE-CASE-DESIGN после установления ownership должен принять
минимальный набор поддерживаемых ACL facts и predicates, значения match/non-match
для IPv4 TCP/UDP с обоими портами; определить роль порядка (отбор/остановка или
лишь сохранение порядка показа) и границы неподдерживаемых/неизвестных facts.
Приложить независимо размеченные match/non-match cases с основаниями из контракта.
Не требуется выбирать универсальный ACL язык или реализацию; произвольные defaults
не допускаются. Product meaning при необходимости эскалируется PRODUCT-REQUIREMENTS.
