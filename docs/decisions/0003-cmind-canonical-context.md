# ADR-0003 — контекст принятых контрактов для стадий CoderMind

Статус: инженерное решение для bounded prototype; результат проверяется исполнением.
Дата: 2026-10-16.

Первый native pipeline структурно PASS, но нарушает DOM-1/IF-1: равенство портов
вместо диапазонов, stdin вместо обязательного пути, другой report envelope.
Native feature edit сообщает MODIFY, но сравнение relevant sections показывает
полный no-op. Повторная генерация с тем же semantic input сама по себе не ремонт.

Изолированный coding workspace получает обычный scoped AGENTS.md, предписывающий
модельным стадиям читать transferred canonical contracts и сохранять явно
перечисленные ограничения. CoderMind LLMClient использует workspace как cwd;
источники инструмента и pinned версии не меняются. Снимок instructions сохранён
в run evidence. Это дополнение интеграционного контекста, не новый владелец смысла.

Альтернативы: принять некорректный граф — нарушает upstream contracts;
исправлять ожидания под генератор — запрещено; менять CoderMind source pipeline
или писать новый planner — несоразмерно прототипу. Обычные project instructions
позволяют сохранить штатные scripts/checks и проверить достаточность контекста.

Второй force-run без действительного repair остановлен до передачи в кодирование;
новый force-run начинается со стабильным instruction snapshot. Даже успешные
native checks требуют отдельной сверки DOM/IF и независимых исполняемых проверок.
Если исправленный контекст не сохранит контракты, результат BLOCKED, а не кодирование
по противоречащему плану. Harness/CoderMind не входят в runtime Checker.

Consumer `CHECKER-CODEGEN-INPUT` потребляет принятые контракты для производства
кандидата кода. `CHECKER-PROTOTYPE` дополнительно требует implementation readiness
с фактическими tests/conformance. Готовность входов не равна готовности продукта;
проверка готового кода не может быть prerequisite его первоначального создания.
Оба профиля используют одну coverage policy и одни canonical providers; новой
предметной истины или отдельного workflow-state Core это не создаёт.
