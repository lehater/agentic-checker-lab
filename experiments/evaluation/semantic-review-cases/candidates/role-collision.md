# Candidate: use-case ownership drift without a bad import

Status: PROPOSED test candidate.

1. The project places all application orchestration inside domain/rules.py because that file already owns matching.
2. The same function reads relevant ACL snapshots, deduplicates providers, decides error semantics and constructs presentation groups.
3. No code from domain imports application or CLI. All imports point inward or use the standard library.
4. The file structure therefore appears valid to an import-direction checker, but the source of responsibilities is not the accepted layered design.
5. Domain now handles use-case execution as well as pure matching.
