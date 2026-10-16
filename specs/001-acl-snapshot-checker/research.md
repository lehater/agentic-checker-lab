# Research — технические решения для синтетического Checker

**Дата:** 2026-10-16. **Статус:** решения планирования, не принятые владельцем продуктовые требования.

## R-01. Входные данные: один локальный JSON
**Decision:** Один файл содержит поток, список релевантных пар устройство/ACL и соответствующие snapshots.
**Rationale:** Один атомарный dataset даёт минимальный воспроизводимый end-to-end сценарий без сети и хранилища.
**Alternatives:** отдельные query/snapshots файлы (больше связности на CLI); REST API (лишняя инфраструктура); Python fixture objects (сложнее внешний контракт).

## R-02. Исполнение: Python 3.12+ stdlib CLI
**Decision:** Небольшое offline CLI `python -m acl_checker FIXTURE.json` со stdout JSON.
**Rationale:** Воспроизводимость и лёгкость независимой проверки без серверов и runtime-зависимостей.
**Alternatives:** веб-API (не нужен); библиотека без CLI (хуже пользовательский end-to-end сценарий); YAML (требуется parser).

## R-03. Минимальный поднабор ACL-предикатов
**Decision:** IPv4 host/CIDR или `any`; protocol `tcp` / `udp` / `any`; порты как включительные интервалы `[min,max]` от 0 до 65535; действие `permit`/`deny`.
**Rationale:** Поддерживает проверяемые host/prefix/any и boundary cases; нет двусмысленного vendor-specific языка.
**Alternatives:** ASN/address objects/service groups/vendor masks (за пределами MVP); готовые строки vendor ACL (неопределённая семантика).

## R-04. Релевантность и snapshots
**Decision:** Пары устройство/ACL подаются явно и могут содержать разные ACL на одном устройстве; snapshot уникален по (device_id,acl_id). При отсутствии снимка запрос отклоняется.
**Rationale:** Не смешивать неполные данные с доказанным отсутствием совпадений.
**Alternatives:** silently skip missing snapshot (ложно отрицательный результат); вычисление транзитного firewall по маршрутам (не входит в текущую задачу).

## R-05. Выходная модель
**Decision:** JSON, устройства и ACL в порядке первого появления во входном списке релевантности, каждое правило в порядке snapshot; include empty groups; `matched_rule_count` в summary; без агрегированного `verdict`.
**Rationale:** Отчёт детерминирован и полон, полезен при отсутствии совпадений.
**Alternatives:** только matching ACL в отчёте (теряет сведения о проверенных списках); текстовая таблица (хуже machine verification).

## R-06. Отрицательные сценарии
**Decision:** Валидация всего входа до генерации отчёта; диагностические ошибки в stderr, exit 2 для некорректного входа; отсутствие частичного stdout JSON.
**Rationale:** Не выдавать неполный анализ за корректный.
**Alternatives:** частичный отчёт с предупреждениями (необоснован для минимального среза).

## R-07. Тестирование
**Decision:** Независимые fixtures и проверки пяти полей, range boundaries, 2 ACL на устройстве, order, no-short-circuit, empty result, invalid/missing data, no verdict. Использовать stdlib unittest.
**Rationale:** Все основные свойства observable; отдельная семантическая верификация решения для Python-кода не требуется на этой стадии.
**Alternatives:** только snapshot-output сравнения (хрупкие); self-check генерирующего агента как единственный oracle (слабая независимость).

## R-08. Архитектурная граница
**Decision:** Отделить чтение и валидацию fixtures, чистый match predicate, orchestration «relevant pairs → snapshot → rules» и сериализацию отчёта. Конкретные классы и файлы — свобода downstream RPG.
**Rationale:** Сохраняет проверяемую предметную логику без преждевременного microservice/DDD каркаса.

## Открытые вопросы
A-03/A-04/A-05 из спецификации остаются временными проектными допущениями. Это не блокирует синтетический эксперимент, но не позволяет считать результаты production-требованиями.
