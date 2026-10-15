# Synthetic RPG input — deterministic word counter

Status: **TOOLING FIXTURE**, not Checker requirements. This test does not authorize implementing Checker.

Build a small independent Python 3.12 CLI called `word-count-lab` that reads a local UTF-8 plain-text file and prints one JSON object to stdout.

## Observable behavior

- **R-SYN-01**: Accept one positional input file path. Only local files; no network, database, GUI, services or device interactions.
- **R-SYN-02**: Recognize words as non-empty contiguous sequences of ASCII letters A-Z/a-z. Convert recognized words to lowercase. All other characters are separators.
- **R-SYN-03**: Emit a JSON object with exactly `total` (nonnegative integer) and `counts` (mapping from lowercase words to positive integer occurrences). Sort the mapping keys lexicographically for deterministic output.
- **R-SYN-04**: For empty input or input with no recognized words, return `{"total":0,"counts":{}}`.
- **R-SYN-05**: On missing/unreadable input file or invalid UTF-8, exit nonzero, emit an explanatory stderr message and no stdout JSON.
- **R-SYN-06**: Use only the Python standard library and provide a deterministic CLI entry point.

## Examples — independent acceptance expectations

- Input `Apple banana APPLE!` → `{"total":3,"counts":{"apple":2,"banana":1}}`.
- Input `123 _ --` → `{"total":0,"counts":{}}`.
- Input `A-b 42b` → `{"total":3,"counts":{"a":1,"b":2}}`.

This fixture is intentionally much smaller than Product/SSSR/NAPMS. Its purpose is to check whether CoderMind constructs a meaningful **forward RPG** from explicit accepted requirements, not to build Checker or recreate legacy.
