# P1 — Независимый аудит первого синтетического RPG

Статус: **PASS WITH LIMITATIONS** (2026-10-16). Это принятие узкого эксперимента по генерации *начального* графа, а не подтверждение правильности программы или оптимальности архитектуры.

## Источники и контроль целостности

- [Исходные требования](../../tooling/fixtures/rpg-synthetic/requirements.md), идентификаторы R-SYN-01..06.
- Экспортированный комплект: [feature_spec.json](../../experiments/runs/rpg-synthetic-v1/feature_spec.json), [feature_build.json](../../experiments/runs/rpg-synthetic-v1/feature_build.json), [feature_tree.json](../../experiments/runs/rpg-synthetic-v1/feature_tree.json), [skeleton.json](../../experiments/runs/rpg-synthetic-v1/skeleton.json), [rpg.json](../../experiments/runs/rpg-synthetic-v1/rpg.json), [manifest.json](../../experiments/runs/rpg-synthetic-v1/manifest.json).
- Первоначальный экспорт отправлен в Git коммитом `b20a93b7377471fc553298128b613ee38726f8b9`. Инструмент: Microsoft RPG-ZeroRepo [PR #96](https://github.com/microsoft/RPG-ZeroRepo/pull/96), pinned SHA `3303a222eaec42c6a178bddd46ad63d9026ab8fa`.
- Все 5 JSON непосредственно прочитаны из GitHub и проверены: независимо вычисленные SHA-256 **5/5 совпадают с манифестом**; SHA-256 исходных требований также совпадает.
- `repository_revision_at_export=6448295...` — исходный коммит *до* включения результатов экспорта в Git. `status=EXPORTED_UNREVIEWED` в неизменяемом манифесте относится ко времени выгрузки, а не к текущей оценке.

## Структура графа и сквозное сопоставление

| Объект | Независимо установлено |
| --- | --- |
| Узлы RPG, уникальные ID | 31, без повторений |
| Типы узлов | `repo=1`, `functional_area=3`, `feature_group=9`, `feature=18` |
| Иерархия containment | Через вложенные `children` (30 отношений родитель–потомок) |
| Явные семантические рёбра | **0** (`edges=[]`) |
| Листья Feature Tree → RPG | **18/18**, имена сопоставлены, пропусков/добавлений нет |
| Листья RPG → назначения skeleton | **18/18**, каждый лист имеет `meta.path` |
| Файлы в skeleton | 9: четыре функциональных модуля и пять `__init__.py` |
| Содержательные `meta.description` / `meta.content` у 18 листьев RPG | **0/18** в каждом поле |

Контракт структуры RPG распознаётся: корень, области, группы и листья; отсутствуют незнакомые назначения или повторяющиеся feature-имена. Однако file-узлы **не входят** в `rpg.json`: путь файла — свойство листа, дерево будущих файлов находится в `skeleton.json`. Вызовы функций, интерфейсы, нетривиальные зависимости и реальный код пока не созданы.

## Покрытие намерения шести исходных требований

| Требование | Смысл восстановлен в совокупности артефактов | Узлы первого RPG |
| --- | --- | --- |
| R-SYN-01: ровно один локальный путь | Разбор пути, проверка числа аргументов, чтение локального файла | `parse input file path`, `validate argument count`, `read local file bytes`, `verify local file isolation` |
| R-SYN-02: последовательности ASCII-букв и lowercase | Полный смысл присутствует в описаниях Feature Tree | `extract ascii words`, `lowercase recognized words` |
| R-SYN-03: точный JSON, частоты, сортировка | Подсчёт слов, частот, сортировка и сериализация | `calculate total words`, `count normalized occurrences`, `construct count result`, `sort frequency keys`, `serialize deterministic result` |
| R-SYN-04: пустой вход и отсутствие слов | Представлен **в описании** `construct count result`, не отдельной негативной проверкой | `construct count result` |
| R-SYN-05: ошибки чтения/UTF-8 → ненулевой exit, stderr, stdout пустой | Все части присутствуют в Feature Tree | `decode utf8 content`, `return nonzero exit status`, `write input error message`, `suppress failure stdout` |
| R-SYN-06: Python 3.12, stdlib, повторяемость | Точка входа, ограничения библиотек, детерминированная сериализация | `execute python312 cli`, `verify standard library dependencies`, `serialize deterministic result` |

**6/6 узнаваемы как проектные намерения**, если анализировать несколько артефактов вместе. Это **не равно** 100%-ной автоматической трассируемости RPG и не подтверждает исполнение требований: в графе отсутствуют R-SYN/FT IDs и почти все поясняющие тексты. В `feature_build.json` LLM сообщил `coverage_percentage=100`, а в `feature_tree.json` `assigned_leaf_count=18`; это внутренние метрики процесса, не независимый oracle.

## Значимые проблемы

1. **Потеря семантики при переходе в RPG:** узлы сохраняют имена и пути, но не объяснения, rationale и provenance. Для Harness↔RPG нужны явные typed links `requirement → capability → RPG node → file/code entity → test`, а не сопоставление по строковым именам.
2. **Промежуточность графа:** отсутствие non-containment рёбер на данном этапе не является ошибкой синтаксиса, но делает `rpg.json` недостаточным для планирования зависимостей и оценки влияния. `build_data_flow`, `design_interfaces` и остальные стадии Phase 2 ещё не запускались.
3. **Смешение проверки ограничений и runtime-логики:** `verify local file isolation` и `verify standard library dependencies` попали в список функций приложения, назначенных `input.py` и `main.py`. Скорее это архитектурные constraints и тестовые obligations; владелец должен определяться на следующих этапах.
4. **Гранулярность:** четыре смысловых модуля и пять `__init__.py` на маленький CLI могут оказаться избыточными, хотя три функциональные области разделены разумно. Данных для решения об оптимальности ещё недостаточно.
5. **Нет независимых поведенческих тестов:** реальные примеры word-count, ошибки UTF-8 и формат stdout ещё не исполнялись — исходного кода приложения пока нет.

Быстрый поиск по пяти экспортам не выявил строк, похожих на email, домашние абсолютные пути или типичные API-токены; это **не** формальный секрет-скан и не его замена.

## Решение и границы завершения P1

**Принять TASK-003 как воспроизводимый proof-of-concept:** связка CoderMind PR #96 + Codex действительно построила начальное RPG из независимых требований и сохранила артефакты с проверенными хешами. Не трактовать как готовность генерации Checker, полноту архитектурной модели, корректность программы или завершение всей CoderMind Phase 2.

PR #96 остаётся **экспериментальным закреплённым кандидатом**, а основной pin `rpg_zerorepo=a4e6966...` не меняется автоматически. Upstream PR ещё не объединён, отдельно существуют вопросы execution authority, рассмотренные в PR #99.

Следующий основной шаг — [TASK-004/P2](../project/roadmap.md): принять смысл, границы и независимые oracle для Checker. В P3/P4 заранее спроектировать мост требований, capability, RPG и проверок; лишь затем строить полноценный граф и код.
