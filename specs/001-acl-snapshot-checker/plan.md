# Implementation Plan: ACL Snapshot Checker

**Branch:** `experiment/spec-kit-checker-v1` | **Date:** 2026-10-16 | **Spec:** [spec.md](spec.md)

**Input:** Исходная постановка `docs/scenario/owner-problem-brief.md` → [spec.md](spec.md); варианты и решения в [research.md](research.md).

## Summary
Разработать небольшой offline CLI, который принимает один синтетический набор с параметрами потока, ссылками на релевантные ACL и снимками правил; валидирует данные; применяет ограниченный IPv4/protocol/port matching ко всем правилам; возвращает детерминированный JSON со всеми совпадениями, группировкой и порядком. Ни вывод о доступности, ни сеть, ни parsing vendor ACL не входят в объем.

## Technical Context
**Language/Version:** Python 3.12+.
**Primary Dependencies:** Python stdlib: json, ipaddress, pathlib, argparse; внешних runtime-зависимостей нет.
**Storage:** Локальный JSON fixture; постоянного хранилища нет.
**Testing:** `unittest` (acceptance и проверки граничных условий).
**Target Platform:** локальный CLI Linux/Windows/macOS при наличии Python.
**Project Type:** CLI с детерминированным JSON-входом/выходом.
**Performance Goals:** Ограниченный синтетический fixture; формальный SLA не задан владельцем.
**Constraints:** offline, без реальных устройств, без произвольного vendor ACL, без end-to-end verdict.
**Scale/Scope:** один query за запуск, конечный список устройств/ACL, простая синтетическая IPv4-семантика.

## Constitution Check
| Gate | Pre-design | Post-design | Основание |
|---|---|---|---|
| Источник — только owner brief | PASS | PASS | spec и research ссылаются только на него |
| Не навязывать реализацию на стадии specify | PASS | PASS | выбор Python и JSON находится здесь |
| Все совпадения, порядок, принадлежность | PASS | PASS | FR-005..008, contracts/cli.md |
| Нет итогового verdict | PASS | PASS | FR-009, output schema |
| Синтетический вертикальный срез | PASS | PASS | fixture contract, quickstart |
| Остановка до tasks/RPG/codegen | PASS | PASS | файлов tasks/source code нет |

## Architecture / Responsibility
- **Input adapter**: read one dataset, reject invalid or unsupported constructs before interpretation.
- **Domain matching**: pure predicate on IPv4 source/destination, transport protocol and inclusive source/destination port intervals. Rule `action` does not influence predicate or iteration.
- **Use-case orchestration**: iterate relevant pairs in input order; resolve unique snapshots; scan every rule in snapshot order; keep every matching result.
- **Reporting adapter**: serialize grouped JSON and summarize observed matches, preserving placements; never infer global permission.
- **CLI boundary**: parse positional path; stdout carries success JSON, stderr diagnostic, consistent exit codes.

**Direction of dependency:** adapters depend on use-case/domain contract; domain predicate independent of filesystem, serialization and CLI. Implementation file/class names are intentionally *not prescribed* for RPG.

## Project Structure

### Documentation (this feature)
```text
specs/001-acl-snapshot-checker/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── cli.md
│   └── dataset.schema.json
├── quickstart.md
└── checklists/
    ├── requirements.md
    └── acl-integrity.md
```

### Source Code (future RPG realization; non-prescriptive)
```text
src/                  # domain matching / use case / adapters
tests/                # independent behavior and contract tests
```

**Structure Decision:** single CLI executable boundary and pure matching core. RPG determines exact source layout.

## Downstream handoff to RPG
**Authoritative inputs for generation:** [spec.md](spec.md), [data-model.md](data-model.md), [contracts/cli.md](contracts/cli.md), [contracts/dataset.schema.json](contracts/dataset.schema.json), [quickstart.md](quickstart.md), this plan and research decisions.

**Fixed interfaces:** dataset shape, defined matcher semantics, JSON output grouping, error behavior. 
**RPG freedom:** code layout, classes, function names, internal algorithms, development task breakdown.
**Required pre-code review:** inspect generated RPG for source/destination address and port checks, range inclusivity, no-short-circuit, CLI contract, output absence of verdict.

## Complexity Tracking
No constitutional violations or framework-specific infrastructure justified.
