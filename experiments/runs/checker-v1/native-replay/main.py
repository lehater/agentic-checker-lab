#!/usr/bin/env python3
"""acl-checker — исследование сохранённых ACL для одного IPv4-потока.

Запуск из чистого checkout без установки пакета:
    python3 main.py --input examples/input_request.json
    python3 main.py --input examples/input_request.json --format json
    python3 main.py --help

Обязательный --input, форматы, справка и диагностика предоставляются
существующим CLI. Канонический запуск: python3 -m checker.
"""

from collections.abc import Sequence

from src.acl_checker.cli.main import main as cli_main


def main(argv: Sequence[str] | None = None) -> int:
    """Передать аргументы CLI и вернуть его код: 0 — успех, 2 — отказ."""
    return cli_main(argv)


if __name__ == '__main__':
    raise SystemExit(main())
