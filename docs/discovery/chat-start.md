# ChatGPT starting instructions — Checker discovery pilot

Use this prompt in a **new ordinary ChatGPT chat** with GitHub connected. Do not assume ChatGPT automatically loads files or Skills.

> Continue the Checker **requirements discovery pilot** from branch `experiment/iterative-discovery-protocol` and its Draft PR (NOT main). Read the branch's `AGENTS.md`, `docs/discovery/protocol.md`, `docs/discovery/checker/ledger.json`, latest round report and `docs/scenario/owner-problem-brief.md`. Reconstruct the exact last committed checkpoint, current frontier and unresolved decisions. Follow the protocol without skipping prepublication of questions, explicit owner review, validation, or GitHub commit. Ask 3–7 dependency-ready questions in one batch; I will answer by microphone. Normalize answers and show the package for my confirmation **before** saving any as approved. Record new/replaced/cancelled questions and reasons. After confirmation, checkpoint the entire round in one commit, validate, and only then ask the next round. Do not present proposed OpenSpec details as accepted, do not solve owner decisions yourself, and never modify main. If a tool/write/checkpoint fails, STOP and say BLOCKED.

First invocation: there is **no agreed interview yet**. If the ledger is empty, derive a small first frontier from the owner brief, persist questions in this branch, and then ask them.

For inspection at any time, request: **"Покажи активную очередь, текущий раунд, последнее подтверждение и несохранённые изменения"**. For a semantic disagreement: **"Покажи источник решения, исходную формулировку и Example Mapping контрпример"**.

Do not copy this prompt into the main branch as accepted procedure before the pilot passes. The pilot is the experiment, not a proof of its own effectiveness.
