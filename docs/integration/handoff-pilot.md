# Harness → CoderMind: контрольный handoff (экспериментальное предложение)

Статус: **HYPOTHESIS / NOT IMPLEMENTED**. Это не API Microsoft и не новая Harness Core сущность. См. [ADR-0002](../decisions/0002-harness-cmind-boundary.md) и [аудит](../research/methodology-integration-audit-2026-10.md).

## Исходный ownership

- Project-owned accepted canonical artifacts (возможно `.harness/knowledge/**`, возможно проектные форматы) содержат принятые обязательства и решения.
- Harness/агент выводят применимый scope, проверяют ownership, completeness, questions, verification dispositions и кодинговый handoff.
- `CoderMind feature_spec.json`, `feature_tree.json`, RPG и код — предложения/реализация, а не новый авторитетный Requirements/Architecture реестр.
- Передача может использовать текстовые docs, `--input-text` или другой импорт. **Не утверждать, что CoderMind понимает Harness schemas без адаптера.**

## Минимальная воспроизводимая поставка входа

Это **содержательный контракт пакета**, не жёсткая новый YAML/JSON schema до compatibility spike.

| Поле / ссылка | Источник | Инвариант |
| --- | --- | --- |
| `source_revision` и `source_hashes` | Canonical project Git | Нельзя читать произвольный изменяющийся HEAD или неизвестные незакреплённые данные |
| `consumer` / `scope` | Engineering Graph + Harness Project Frontier | Выбранный Consumer и только его проверенная closure |
| `requirements`, `source_refs`, `non_goals` | Принятые Product Requirements | Устойчивые ID, отрицательные ограничения, provenance, нет неподтверждённых правил |
| `design_constraints` / `implementation_freedoms` | Принятые Domain/Application/Architecture/Interface/Implementation Design | Запрещено принимать решения вне разрешённой свободы |
| `verification_dispositions` / `test_contracts` | Принятые Verification/Test Design | TEST/ANALYSIS/INSPECTION/DEMONSTRATION; независимый oracle хранится отдельно |
| `question_status` / `closure_evidence` | Актуальные Harness read-models | При blocking Question или незавершённой applicable closure handoff запрещён |
| `pin` / `execution_policy` | Лаборатория | SHA Harness/CoderMind/агента, разрешённые I/O и Git операция; ограничить token/cost |

**Никакой файл/проекция из этого пакета сама по себе не предоставляет новую Capability.**

## Пилот совместимости: фальсифицируемые проверки

1. **Positive, synthetic:** создать маленькую принятую спецификацию и scope через agent-driven Harness, зафиксировать исходные версии и Test Design. Получить CoderMind `feature_spec` и RPG в scratch, проверить покрытие каждого требования, отрицательных ограничений и допустимых решений.
2. **Missing/changed source:** убрать обязательный REQ либо изменить SHA после компиляции handoff. Пайплайн должен остановиться с доказуемым несоответствием; не восстанавливать значение через догадку LLM.
3. **Injected conflict:** спровоцировать предложение дополнительного поведения/несогласованной архитектуры. Результат — quarantined proposal и Question/owner review, а не silently ACCEPTED или изменение canonical truth.
4. **Design constraint:** передать принятое ограничение пакетов/порта, убедиться, что build_skeleton/interfaces не противоречат ему; иначе STOP, не автоматический override.
5. **Git isolation:** запуск CoderMind `run_batch` и `rpg_edit` только в изолированном disposable repo, проверить отсутствие push/merge/commit в лаборатории, hooks/self-upgrade/agent privileges; clean tree and diff after run.
6. **Traceability:** реальный снимок RPG должен иметь проверяемое соответствие REQ→feature→code/test либо отдельную однонаправленную *derived* link projection. Простого совпадения текстовых имён недостаточно.
7. **Cost and reproducibility:** исходники, scripts/model/prompt pins, runs/log policy, расход и статусы записываются без приватных логов в Git.

## Процедура передачи

```text
Harness project frontier / applicable engineering coverage
  → accepted semantic/verification/design closure
  → immutable project-owned handoff projection
  → isolated CoderMind feature specification/planning
  → reconciliation with accepted semantics and allowed freedoms
  → conflict: Question, return to owning Authority (no codegen)
  → pass: guarded codegen in scratch Git
  → independent oracle & provenance audit
  → reviewed PR
```

На первой итерации **не реализуем генератор полного RPG из Harness**. Сначала проверяем, возможно ли штатное потребление принятого корпуса CoderMind без потери смысла. Adapter выбирается по фактическим failures, а не по предпочтению формата.
