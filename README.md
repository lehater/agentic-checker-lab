# Agentic Checker Lab

Исследовательский репозиторий для воспроизводимой проверки методики агентной разработки **от задачи до исполняемого приложения** с использованием [Harness](https://github.com/lehater/harness) и [Microsoft RPG-ZeroRepo / CoderMind](https://github.com/microsoft/RPG-ZeroRepo).

**Исследуемый продукт — методика разработки, а не модернизация SSSR, Product или NAPMS.** Минимальный диагностический Checker — экспериментальный пример. Исторические репозитории используются только как зафиксированные источники свидетельств и требований.

**Начало работы:** [карта документации](docs/README.md), [стратегия](docs/project/strategy.md), [текущее состояние](docs/project/current-state.yaml), [порядок разработки](docs/project/governance.md).

Текущее состояние: **P4 — синтетический Checker реализован и проверен**. Harness readiness COMPLETE; независимые тесты, native suite и мутационные проверки проходят. Приёмка и ограничения зафиксированы в [прогоне checker-v1](experiments/runs/checker-v1/README.md). Исследование change-impact и сравнение методик ещё впереди.

Ubuntu является целевой средой эксперимента. Само приложение Checker должно работать независимо от Harness и CoderMind.

Запуск (Python 3.10+, без установки пакетов):

```bash
python3 -m checker --input examples/checker-input.json
python3 -m checker --input examples/checker-input.json --format json
```

[Контракт и ограничения Checker](docs/checker/README.md).
Полная быстрая проверка репозитория и приложения после клонирования:

```bash
make check
```
