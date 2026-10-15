# Archive экспериментальных прогонов

**Реальных прогонов пока нет.** Не маркировать будущие файлы PASS без исполнения.

Будущий layout: experiments/runs/<run-id>/manifest.yaml + sanitized logs + model/tool/source refs + versioned RPG/engineering graph snapshots (если применимы) + oracle results + raw normalized metrics + analysis. Для больших выходов использовать внешнее хранилище только при явном решении с checksum/immutable pointer; запрещено выкладывать токены, приватные устройства и реальные production данные.

Режимы A/B/C/D и процедура сравнения: [protocol](../docs/project/experiment-design.md). Pilot runs не могут автоматически становиться сравнительными доказательствами.
