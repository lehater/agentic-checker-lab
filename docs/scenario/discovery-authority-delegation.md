# PDEC-CHECKER-002 — полномочия Discovery для `checker.problem`

**Статус: OWNER-AUTHORIZED, SCOPED TO TASK-004.** Дата фиксации: 2026-10-16.

## Основание решения

В продолжение подтверждённой постановки [PDEC-CHECKER-001](problem-framing-decision.md) владельцу был предложен следующий ограниченный набор полномочий: закрепить `DISCOVERY` за `checker.problem`, разрешить инженерному агенту содержательную проверку и строгую семантическую приёмку по контрактам Harness, с эскалацией существенных предметных противоречий и публикацией только согласованного проверенного состояния. Владелец ответил **«Продолжай»**.

Это подтверждение **делегирования на конкретную Capability**, а не отдельная подпись под ещё не созданным результатом Semantic Admission.

## Предоставленные полномочия

1. **Producer / semantic owner:** проект принимает назначение Authority `DISCOVERY` производителем знания вида `problem-evidence` для `checker.problem` в рамках TASK-004. Это разрешает проектную реализацию *этого соответствия* в Engineering Graph и оценку применимости DISCOVERY к данному scope; не принимает автоматически полный кандидатный граф из пяти Capabilities, остальных Authorities, Consumer scope или subject inventory.
2. **Semantic reviewer:** инженерному агенту делегируется выполнение реальной содержательной проверки Problem Evidence по официальному `problem-evidence` skill и pinned контрактам Harness. Агент вправе фиксировать `semantic_review.status: ACCEPTED` **только по результатам выполненных проверок** `source-discipline`, `authority-boundary`, `no-invention`, `evidence-not-solution`. Если факт или область полномочий не установлен, агент формирует Question и не подменяет review формальной отметкой.
3. **Admission и publication:** агент вправе вызвать штатный strict `semantic_admission`, подготовить согласованные Core CanonicalArtifact, Semantic Evaluation, Lifecycle и failure/Question state и выполнить атомарную Project Publication с CAS, **лишь если** реальные контракты, проверка и политика целевого проекта позволяют это. После доказанной публикации агент пересчитывает Decision Roadmap, Semantic Closure, Engineering Coverage и Project Frontier.
4. **Автономия:** агент вправе самостоятельно устранять технические препятствия исполнения внутри экспериментального репозитория и выбирать локальные обратимые технические действия. Существенные противоречия источников, изменения исходной постановки или решения, принадлежащие Product Requirements/Domain/Architecture, эскалируются соответствующему владельцу знания.

## Границы

- Принятый смысл проблемы ограничен [PDEC-CHECKER-001](problem-framing-decision.md); повторная постановка вопроса владельцу о нём не нужна.
- Эта запись не принимает offline/fixture-only scope, IPv4/IPv6 и match-алгоритм, live-device диагностику, UI/API, архитектуру, требования, независимый oracle или код Checker.
- Исторические SSSR и Product остаются source evidence, не принятыми каноническими prerequisite artifacts. Нельзя создавать фиктивные source authority, reviewer identity, acceptance ID, semantic evaluation, lifecycle либо publication revision.
- `UNASSESSED` других reference Authorities сохраняется как открытый вопрос reconciliation/coverage. Нельзя интерпретировать эту запись как утверждение `NOT_APPLICABLE` или полное закрытие Engineering Coverage.
- Разрешены изменения в `agentic-checker-lab` через отдельную ветку и PR согласно [governance](../project/governance.md). Не изменять `lehater/harness`, не запускать CoderMind/codegen, не обращаться к устройствам или секретам.
- `ACCEPTED` этой записи относится только к **управлению полномочиями**. `checker.problem` станет `CURRENT` исключительно после фактически успешной строгой семантической приёмки и согласованной публикации.

## Критерий следующего результата

**Успех:** опубликованный валидный project snapshot с Core provider `checker.problem`, `ACCEPTED` semantic evaluation и совпадающим Lifecycle `CURRENT`, после чего представлены действительные следующие действия Frontier.

**Отказ/блокировка:** воспроизводимый конкретный код ошибки/нарушенный контракт Harness и минимальный неразрешённый Question, без нового общего исследования и без выдуманной приёмки.
