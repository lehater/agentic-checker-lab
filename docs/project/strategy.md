# Strategy — Agentic Checker Lab

**Owner-directed reset, proposed for main via PR (2026-10-28).** Replaces the active Harness-based method, without deleting historical evidence.

## Mission

Разработать и независимо проверить воспроизводимую методику управляемой Agentic SDLC: постановка → требования → предметная модель и архитектура → проектирование реализации → код → проверка → изменение.

Проверять преимущество каждого дополнительного инструмента; **не использовать Harness в новых сценариях**. Checker — малый реалистичный тестовый продукт, методика — исследуемый результат.

## Method candidates

1. Accepted specifications, design decisions and oracle cases, ideally managed by **OpenSpec** once validated in a minimal consumer. Markdown/ADR remain usable while the integration is unverified.
2. **Direct Codex** implementation baseline.
3. Optional **Microsoft RPG-ZeroRepo / CoderMind**, consuming *the same accepted design*, producing a proposal for file graph/interfaces/tasks. Never overriding requirements or architectural constraints.
4. Independent architecture/behavior checks before code generation and after changes.
5. Trace per-stage time, API/CLI usage where measurable, retries, defects, manual intervention and outcome.
6. Improve workflow/prompts/model routing only against frozen evaluations and a fixed resource budget.

## Design policy

[Clean Architecture + SOLID + KISS + YAGNI](../engineering/policy.md). No extra capability, framework, service, interface, hierarchy, generalized adapter or validation bureaucracy without a current reason. Separate enforceable dependency rules from architectural judgments.

## Boundaries

- **Checker Lab** owns methodology, tests, reproducible model-run procedures, evidence and limited integration adapters.
- **AI Lab** provides independently deployable infrastructure on consumer demand; do not import the Checker methodology into its core.
- **CoderMind** is a replaceable experimental tool, not the source of product truth.
- **Harness experiments and PR #27** are preserved as historical evidence; do not automatically merge or delete them.
- No production devices, vendor parsers, network polling, credentials or implicit permit/deny claims.

## Research questions

RQ-01: Does accepted documentation preserve requirements and design through code and change?
RQ-02: Does CoderMind improve outcome versus direct Codex at equal inputs/budgets?
RQ-03: Can hard architecture checks detect generated structural violations before codegen?
RQ-04: Where are time, tokens and retries spent; which interventions improve efficiency?
RQ-05: Which model routing policy optimizes time-to-verified-result under actual quota constraints?
RQ-06: Does the improvement transfer to a second problem?

Historical strategy and its A/B/C/D Harness arms are superseded for new runs, not erased.
