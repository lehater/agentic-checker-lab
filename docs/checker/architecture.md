# System Architecture — синтетический Checker

Источники: REQ-CHECKER-101..104, DOM-1/2; [ADR](../decisions/0002-checker-prototype-boundaries.md).
До выбора сформирован [набор альтернатив](../../experiments/runs/checker-v1/architecture-options.yaml).

Один локальный процесс обслуживает один запрос: внешний адаптер валидирует ввод,
application запрашивает релевантные пары и снимки через переданные функции,
domain выполняет чистое сопоставление, внешний адаптер представляет отчёт.
Domain не знает файлов, CLI, Harness, CoderMind или источника релевантности.
Application зависит от domain и собственных контрактов источников;
инфраструктура зависит от этих внутренних контрактов. Композиция находится снаружи.
Релевантность не смешивается с matching. Снимки и поток не изменяются.

Выбор по предварительно рассмотренным альтернативам:
один процесс и deployable уменьшают эксплуатационную сложность синтетического
прототипа; сервис технически возможен, но не даёт пользы текущему потребителю.
Прямые синхронные вызовы проще очереди для немедленного отчёта.
Предоставленные снимки достаточны как evidence, импортируемая БД не требуется.
Inward зависимости обязательны по Clean Architecture; outward вариант отвергнут.
Отказ изолирован запросом; workers возможны, но добавляют координацию без требования.
Нет fallback, retry и частичного успешного отчёта при неверных данных.

## Architecture driver closure

| Concern | State | Основание/решение |
| --- | --- | --- |
| execution-mode | RESOLVED | Один диагностический запрос оператора, REQ-101; prototype по постановке |
| consumers | RESOLVED | Оператор и независимый приёмочный запуск, REQ-101/103 |
| load-volume-frequency | DEFERRED | Только небольшие синтетические данные; числовых целей нет, не меняет topology текущего slice |
| latency-freshness | DEFERRED | Нет SLA/TTL; показываются сохранённые сведения, не live truth |
| availability | NOT_APPLICABLE | Нет непрерывного сервиса в заявленном прототипе |
| recovery-durability | NOT_APPLICABLE | Read-only запрос; повторный запуск из тех же снимков, сохранять результат не требуется |
| growth-horizon | DEFERRED | Production network отдельно; синтетический slice не обосновывает distribution |
| deployment-environment | RESOLVED | Локальный прототип, допускаемый заданием; машинный runtime выбирает Implementation |
| concurrency | NOT_APPLICABLE | Нет общего изменяемого состояния и взаимодействующих записей |
| integration-boundaries | RESOLVED | Имитация релевантности и предоставленные снимки, REQ-102/103 |
| persistence-history | NOT_APPLICABLE | Нет обязанности вести промышленное хранилище/историю; постановка |
| security-trust-boundary | RESOLVED | Только локальные synthetic данные; внешние значения валидируются; devices/secrets отсутствуют |

Проверка структуры должна запрещать импорты CLI/файловых адаптеров во внутренние
модули. Реализация должна запускаться без Harness/CoderMind. Изменение live
источников, concurrent writes, service consumers, размеров или SLA открывает
driver closure и topology заново. HTTP, очереди, БД, routing и vendor parser
в текущую реализацию не входят.
