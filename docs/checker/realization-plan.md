# Implementation Design — candidate, admission pending

Основания: REQ-CHECKER-101..104, DOM-1/2, ARCH-1, IF-1, COMP-1, POL-1,
TD-BEHAVIOR и TD-BOUNDARIES. Варианты сформированы и проверены до этого candidate:
[exploration](../../experiments/runs/checker-v1/implementation-options.yaml).

Выбор инженерного агента в рамках поручения владельца: один небольшой вертикальный
slice с независимым oracle до кода; Python package `checker`, внешний composition
root `checker.__main__`, отдельные domain/application/input adapter функции;
runtime standard library, без сетевых зависимостей. `unittest` для независимой
приёмки; CoderMind может использовать pytest как dev tool, не runtime dependency.

RPG/CoderMind получает только принятые Harness contracts и frozen expected cases
через bridge manifest. Порядок: feature construct → plan (все 5 стадий) → проверка
RPG на semantic drift → code generation по штатным scripts → перенос проверенного
source в task branch → независимая CLI и dependency проверка. Tool-generated tests
не заменяют oracle. Обновлять accepted requirements/ожидания из-за output запрещено.
Private helper names/representations остаются свободой генерации в рамках COMP-1.

Снимки — input fixtures, не миграция базы. Нет совместимости с историческим Checker
или production rollout. Откат — обычный revert task change; deployment/merge не
выполняется этим планом. Ручное тестирование полезно дополнительно, но не заменяет
версионированный `make check` в PR CI. Отдельный benchmark не нужен: нет SLA.

Обязательные completion evidence: независимые CLI сценарии и error cases PASS,
source substitution/no mutation и deterministic import boundary checks PASS,
Harness test-realization conformance ACCEPTED для каждой OP/OR obligation,
полный актуальный Harness closure и coverage, действительные RPG artifacts и
checksums, provenance до source/tests. До этого данный кандидат **не CURRENT**.

Validation execution review: только быстрые детерминированные suites на synthetic
входе, один общий trigger PR/push main, без selective execution или model calls в CI.
`make check` — воспроизводимый authoritative gate; локально та же команда.
Model-driven tool work — отдельные явные запуски, результаты экспортируются, а не
повторяются недетерминированно на каждом PR. Структурные правила проверяются AST,
schema/semantic tooling — pinned Harness при явном запуске с отдельным evidence.
Runtime dependency inventory: Python stdlib only; CoderMind/Harness остаются dev
инструментами с pin. Увеличение dependency footprint требует пересмотра решения.
