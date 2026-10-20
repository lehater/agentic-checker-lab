from __future__ import annotations

import sys

import src.acl_checker.cli.main as cli


def main() -> int:
    """Обеспечить запуск python3 -m checker, передав аргументы и стандартные потоки существующему CLI main. Вернуть его код завершения; модульный запуск завершает процесс этим кодом."""
    return cli.main(sys.argv[1:], stdout=sys.stdout, stderr=sys.stderr)


if __name__ == '__main__':
    raise SystemExit(main())
