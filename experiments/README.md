# Archive экспериментальных прогонов

[Checker v1](runs/checker-v1/README.md): реальный Harness → RPG/CoderMind → код → независимые проверки. Срез для оценки владельцем сохранён в [checkpoint](runs/checker-v1/checkpoint.md); актуальное состояние — [current-state](../docs/project/current-state.yaml). Не маркировать будущие файлы PASS без исполнения.

Будущий layout: experiments/runs/<run-id>/manifest.yaml + sanitized logs + model/tool/source refs + versioned RPG/engineering graph snapshots (если применимы) + oracle results + raw normalized metrics + analysis. Для больших выходов использовать внешнее хранилище только при явном решении с checksum/immutable pointer; запрещено выкладывать токены, приватные устройства и реальные production данные.

Режимы A/B/C/D и процедура сравнения: [protocol](../docs/project/experiment-design.md). Pilot runs не могут автоматически становиться сравнительными доказательствами.
