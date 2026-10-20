# Component Design — Checker

Основание: ARCH-1, IF-1, DOM-1/2, POL-1. До candidate рассмотрены варианты
[exploration](../../experiments/runs/checker-v1/components-options.yaml).

- Domain: `matches(flow, rule) -> bool`, чистая конъюнкция DOM-1; принимает
  проверенные значения, не читает источник и не выбирает verdict. Адрес/порт
  представляется обычным значением, не service/entity с lifecycle.
- Application: `check(flow, relevance, snapshot) -> report groups`. Контракты
  relevance(src,dst) -> пары и snapshot(device,acl) -> snapshot принадлежат
  потребляющему use case. Дедупликация пар, обход правил в порядке снимка,
  сохранение context/placements/rule facts, NO_MATCH — согласно DOM-2.
  Missing snapshot вызывает ожидаемый отказ, без частичного success.
- Outer input adapter: parsing и проверка IF-1. Функции synthetic providers
  замыкают валидированные данные конкретного запроса; не используют глобальный
  mutable cache. Один adapter может реализовать оба source contracts.
- Outer CLI/composition: выбирает text/json, связывает adapters/use case,
  переводит ожидаемые ошибки в exit 2. Domain/application не импортируют CLI,
  JSON loader, filesystem, networking или Harness/CoderMind.

Выбраны функции и callables: class lifetime здесь не несёт смысла. Provider
objects также допустимы технически, но добавляют конструкцию без текущей
пользы. Global cache потребовал бы invalidation и согласования снимков; для
read-only одного запроса выгоднее значения invocation. Приватные функции,
внутренние value representations и детали алгоритма coding свободен выбрать,
сохранив public контракты и dependency direction.

Контроль: AST/import analysis внутренних модулей, public CLI tests и подмена
source callable в integration test. SRP проверяется независимостью matching
от input parsing; DIP — переданными функциями; KISS — отсутствием service
framework и лишних wrapper classes. Изменение protocol или источника не должно
требовать изменения predicate, изменение predicate не должно менять CLI parser
за пределами документированной схемы.
