# ADR-0003 — bounded Product Requirements production

Статус: ACCEPTED в границах PDEC-CHECKER-003; 2026-10-16.

Контекст: после CURRENT checker.problem PDEC-CHECKER-003 принимает отдельную границу PRODUCT-REQUIREMENTS и непосредственное производство checker.requirements. Существующий технический Discovery Consumer не задаёт product scope.

Решение: добавить ровно PRODUCT-REQUIREMENTS → checker.requirements (product-requirements), requires: checker.problem. Новый CHECKER-REQUIREMENTS-ADMISSION выбирает эту engineering closure и не объявляется полным implementation Consumer. Discovery production, provider и acceptance остаются неизменными. Существенные Product Questions адресуются PRODUCT-REQUIREMENTS и блокируют только checker.requirements.

Используется существующая direct-file Project Publication из ADR-0002: terminal BLOCKED публикует Core Questions и неизменные accepted evaluation/lifecycle/failure components одним проверенным CAS snapshot. Неуспешный semantic admission остаётся evidence попытки, не становится canonical provider evaluation. Для CURRENT нужны будущая успешная admission и matching lifecycle; Questions нельзя закрывать строковым ответом без предусмотренной Core resolution identity.

Альтернативы: слияние Product с DISCOVERY стирает принятые границы; полный пятиузловой кандидатный граф выходит за делегирование; отдельная публикация Core Questions нарушает согласованность snapshot.

Последствия: граница Product явная и проверяемая, scope completeness по-прежнему не доказана. Домен, архитектура Checker, runtime, oracle и код не проектируются. Проверки: до Questions новая Capability READY/CREATE, после публикации Core Questions — BLOCKED; checker.problem CURRENT в обоих случаях. Воспроизведение: experiments/runs/harness-requirements-v1/produce.py.

Источники: PDEC-CHECKER-001/002/003; pinned Harness routed product-requirements и project-bootstrap-reconcile; docs/design/project-publication-v0.md из закреплённого Pack.
