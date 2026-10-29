# Launchers for isolated experiment sessions

**Operator warning:** this file belongs to the **planner**. Never share it wholesale with a participant; paste only the selected single-arm section below plus the exact bytes of [inputs/checker-brief.md](inputs/checker-brief.md). Do not paste project links, historical Q/D, competing prompts or [evaluation](EVALUATION.md). The participant's chat/workspace must not have prior project context. If ChatGPT retains memory and cannot isolate it, label the run `BLINDING_UNVERIFIED`. Native vs emulation is not interchangeable.

All prompts are in Russian to avoid language-dependent variation.

## Shared neutral header — prepend identically to A, B and C

> Вы участвуете в эксперименте по выявлению требований. Вам доступна только исходная постановка Checker, приложенная ниже. Не используйте другие чаты, сохранённую память, GitHub/репозиторий, прошлые ответы, веб-поиск или прежние спецификации Checker. Если это ограничение технически невозможно обеспечить, немедленно обозначьте это. Цель — выявить необходимые уточняющие вопросы и определить, когда Discovery достаточно полон для **небольшого синтетического MVP**, не разрабатывать продукт. Не пишите код и не создавайте архитектуру. Отделяйте предметные вопросы владельцу от инженерных решений, фактов исходной постановки и будущего scope. Не подменяйте отсутствие данных доказанным отрицательным ответом. При получении ответов сначала нормализуйте смысл и запросите явное подтверждение. Приоритет — значимость вопросов, не их количество. В начале укажите название модели, режим исполнения (NATIVE_SKILL / NATIVE_COMMAND / PROMPT_EMULATION) и ограничения изоляции, если известны.

Then attach **only** the entire body of `inputs/checker-brief.md` verbatim. For the first phase append: `ФАЗА P0: сформируйте первый доступный набор вопросов, но пока не отвечайте на них и не переходите к следующему раунду. Обоснуйте вопросы и их зависимости. Для окончания Discovery укажите проверяемый критерий, а не "вопросы закончились".` P1 begins only after P0 output is externally frozen.

## A — Matt Pocock Grill Me (native preferred)

**Native fidelity:** in a sandbox with `grill-me` and `grilling` installed, invoke `/grill-me`; use the [source-version references](README.md) to record active skill revision. Use the **native** decision tree and whole ready frontier; do not replace it with our coverage taxonomy. The skill wrapper is stateless; copy the full Q/answer history into the run record afterwards, not as hidden guidance.

**Single-arm prompt:**

> Используй именно метод `grill-me` / `grilling` (если этот skill реально доступен): построй дерево решений, спрашивай только вопросы с выполненными зависимостями, выводи весь текущий frontier за раунд и пересчитывай его после ответов. Факты, уже содержащиеся в задаче, не спрашивай у владельца; новые предметные решения не принимай самостоятельно. Остановись только при пустом frontier и подтверждённом общем понимании. Не запускай реализацию. Если настоящий skill недоступен, работай по этому описанию, но пометь результат `PROMPT_EMULATION`, не `NATIVE_SKILL`.

## B — GitHub Spec Kit Clarify (native preferred)

**Native fidelity:** use an initialized, empty **Spec Kit** feature workspace whose **active feature spec** contains only [inputs/spec-kit-neutral-seed.md](inputs/spec-kit-neutral-seed.md), not historical Checker OpenSpec. Verify the active spec path/prerequisites; run the real `/speckit.clarify`. Record Spec Kit version, paths, exact question count and edits made by clarify. A native clarify invocation asks **at most five, sequentially**; multiple invocations are permitted under the shared time budget. The neutral seed is only a spec-shaped transcription of the same brief. Do not silently create extra requirements in it before P0.

**Single-arm prompt:**

> Применяй `speckit.clarify` к предоставленной нейтральной спецификации Checker. Исследуй функциональную область, доменные сущности и состояния, пользовательские потоки, ошибки, зависимости, ограничения и проверяемость. Обнаруженные неясности ранжируй по влиянию и неопределённости. Уточняй по одному вопросу и сохраняй незакрытые области. Не переходи к `speckit.plan` или реализации. Если реальный Spec Kit недоступен, честно пометь исполнение `PROMPT_EMULATION`; соблюдай предел пяти вопросов на один имитируемый вызов и явно показывай непройденные категории в отчёте.

**Important P0 native distinction:** the official tool asks one question at a time and does not reveal its hidden future queue. Therefore **freeze only the first published question** in native B P0; do not force it to expose all five candidate questions, which would change the method. In cross-arm comparisons use `first published owner question` as an invariant P0 signal; first-five comparisons are available only after the user answers enough questions in P1.

## C — Combined coverage + frontier + counterexamples (experimental)

**Single-arm prompt:**

> Используй экспериментальную процедуру `coverage scan → owner-choice frontier → Example Mapping → completeness gate`. Сначала извлеки цели, способности, сущности, входы/выходы, состояния данных и исключения только из постановки. Для каждой значимой области проверь `нет / один / много / неизвестно / ошибочно` там, где это имеет смысл. Построй кандидаты в вопросы на основе неполного покрытия, негативных примеров, противоречий и непроверенных предположений. Отсей инженерные решения и дубли; предметные вопросы владельцу поставь в frontier с зависимостями и объяснением последствий. После ответа проверяй правила позитивным примером и контрпримером, снова сканируй покрытие. Заверши только когда критические предметные неопределённости разрешены или явно отсрочены, основные сценарии покрыты, а отдельная финальная проверка не обнаружила новых существенных owner-choice вопросов. Не считай ноль вопросов достаточным сам по себе; не придумывай дополнительные вопросы ради количества. Это `PROMPT_EMULATION` нового протокола, не работа готового сертифицированного skill.

## Common P1 continuation message (same for all)

> ФАЗА P1. Теперь можно задавать следующие вопросы по выбранной методике. Ответы даёт владелец. Не утверждай решения без явного подтверждения, не открывай исходники других прогонов. Каждый новый вопрос фиксируй с причиной и зависимостью. В конце выдай полную нормализованную спецификацию *только выявленных смыслов*, список неизвестного и отчёт о критерии остановки. Реализацию и формальную OpenSpec не начинай.

## What to freeze after each run

Record exactly: `run_id`, arm, native/emulation, source version, model/effort, isolation statement; P0 published question(s) and source rationale; P1 raw questions/owner answers and approvals; dependencies, owner-only vs engineering classification; new question triggers; original and corrected interpretations; unfinished issues; stopping reason and coverage snapshot; owner-active time; token data or `UNKNOWN`; failure/connector/tool incidents. Use [run record template](RUN_RECORD_TEMPLATE.md).

**Never send A/B/C prompts as a combined message to a participant.** Their presence in one chat is itself contamination.
