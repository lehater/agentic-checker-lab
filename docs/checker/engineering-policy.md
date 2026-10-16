# Engineering Policy — Checker prototype

Потребители: реализация и её review. Основание: пользовательские KISS/SOLID/Clean
Architecture правила и ARCH-1 / IF-1. Одна ответственность на модуль: matching,
use case, внешняя serialization/validation. Чистое ядро не импортирует CLI,
файловые или сетевые адаптеры. Внешние источники передаются use case как узкие
callables: relevance(source,destination) и snapshot(device,acl). Не создавать
абстракцию, класс, repository или wrapper без текущей причины для подстановки.

Ожидаемые ошибки границ переводятся в понятный CLI отказ с пустым stdout,
без превращения missing/invalid в NO_MATCH. Ошибка программиста не должна
подавляться общим `except Exception`. Данные не исполняются; только JSON parsing.
Снимки и query не мутируются. Нет текущей причины для БД, CQRS, event bus,
DI framework, конкурентного shared state или production dependency.

Автоматическая проверка зависимости внутренних модулей и public acceptance
scenarios обязательна до готовности. Случаи и expected значения фиксируются
до реализации, изменения expectations требуют upstream обоснования.
