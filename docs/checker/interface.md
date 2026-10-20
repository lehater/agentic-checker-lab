# Machine Interface Contract — Checker v1

Основания: REQ-CHECKER-101..104, DOM-1/2, ARCH-1.
Граница: локальная CLI `python3 -m checker --input <path> [--format text|json]`.
Текстовый отчёт по умолчанию даёт оператору видимый список групп и строк;
JSON нужен автоматизированной приёмке. HTTP и интерактивный UI не требуются.
`--help` объясняет поддержанный scope; входной файл — JSON UTF-8 объект.

Input v1:
- `version`: целое 1.
- `flow`: `source`, `destination` (IPv4 строки), `protocol` (`tcp`/`udp`),
  `source_port`, `destination_port` (целые 0..65535, bool не число).
- `relevance`: список `{device, acl}`; это synthetic результат источника
  релевантности для **данного** flow, а не универсальная карта реальной сети.
  Adapter отдаёт его приложению по двум IP запроса; повторяющиеся пары схлопываются
  с сохранением первого появления. Пустой список даёт пустой отчёт.
- `snapshots`: список `{device, acl, placements, rules}`; пара уникальна.
  `device`, `acl`, `id` правила и `action` — непустые строки; `action`
  поддерживает `permit` и `deny`.
- `placements`: список объектов `{interface: <nonempty>, direction: in|out}`
  либо `{global: true}`. Пустой список допустим как отсутствие предоставленных
  сведений о местах применения, а не вывод об отсутствии привязок в сети.
- Правило: `{id, source, destination, protocol, source_ports, destination_ports, action}`;
  source/destination — IPv4 host либо canonical CIDR, protocol — tcp/udp/any,
  ports — массив двух включительных целых границ. Нулевые host bits в CIDR
  обязательны. Порядок массива `rules` — порядок снимка, ID не сортируются.
  Все перечисленные поля обязательны; неизвестные поля на каждой границе
  отвергаются, чтобы не проигнорировать неподдержанный predicate.
- Все предоставленные снимки проверяются на корректность; релевантные пары должны
  иметь снимок. ID правил уникальны в пределах одного ACL. Дополнительные
  неиспользуемые корректные снимки не попадают в результат.

JSON success (stdout, exit 0): `{version: 1, groups: [...]}`.
Каждая группа: `{device, acl, placements, status: MATCHES|NO_MATCH, rules: [...]}`.
Правила выводятся со всеми исходными полями и action в порядке снимка.
Группы — в порядке первых уникальных relevance пар. Это serialization convention,
не заявление о порядке прохождения устройств. Поля общего verdict нет.

Text success: заголовок `device / acl — status`, строка `placements: <JSON>`
и затем по строке на правило, включая id/action и все поля predicates.
Пустой relevance выводит `Нет релевантных ACL (synthetic source).`

Ошибка чтения/JSON/валидации/отсутствующего снимка: exit 2, stdout пуст,
stderr содержит `Checker error: <понятная причина>`. Запрос не выдаёт успешный
частичный отчёт. Никаких сетевых запросов, записи снимков или исполнения
значений входного файла. Неизвестная версия отвергается. Совместимость за
пределами v1 не заявлена.
