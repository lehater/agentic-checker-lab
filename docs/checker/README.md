# Checker

Локальная утилита показывает все сохранённые ACL-правила, совпадающие с заданным
потоком, по устройствам и ACL. Порядок правил и их действия сохраняются.
Общий permit/deny verdict не вычисляется; NO_MATCH означает отсутствие совпадений
в предоставленных данных, а не запрет трафика.

Нужен Python 3.10 или новее. Установка пакетов для запуска не требуется.
Из корня репозитория:

```bash
python3 -m checker --input examples/checker-input.json
python3 -m checker --input examples/checker-input.json --format json
python3 -m checker --help
make check
```

Вход — локальный JSON UTF-8: поток, фиктивный ответ источника релевантности и
снимки ACL. [Пример](../../examples/checker-input.json) и [точный контракт](interface.md).
Поддерживаются IPv4, TCP/UDP, any для протокола правила, CIDR и включительные
диапазоны портов. Оба порта потока обязательны. Неизвестные поля, неподдерживаемые
значения и отсутствующие релевантные снимки дают отказ: код 2, пустой stdout,
диагностика в stderr. Успешный отчёт или справка возвращают код 0.

Источники синтетические; запросов к устройствам нет. Производственный сборщик,
маршрутизация, vendor-specific парсер, IPv6 и промышленное хранение вне этого среза.

## Инженерные основания

[Проблема](problem.md) · [Требования](../generated/checker/requirements.md) ·
[Домен](domain.md) · [Архитектура](architecture.md) · [Компоненты](components.md) ·
[Политика](engineering-policy.md) · [План и приёмка реализации](realization-plan.md) ·
[Независимые сценарии](scenarios.yaml) · [Результаты прогонов](../../experiments/runs/checker-v1/README.md).

Дополнительные 197 native-тестов CoderMind воспроизводятся по
[инструкции snapshot](../../experiments/runs/checker-v1/native-replay/README.md).
Они требуют dev-пакеты pytest; основной gate установки пакетов не требует.
