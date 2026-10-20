"""Вызов полного локального CLI из Python с захватом результата."""

from io import StringIO
from pathlib import Path
from typing import Literal

from src.acl_checker.cli.main import main


def capture_report(
    path: Path, output_format: Literal['text', 'json'] = 'json',
) -> tuple[int, str, str]:
    """Вернуть код, отчёт и диагностику без завершения текущего процесса."""
    stdout, stderr = StringIO(), StringIO()
    code = main(
        ['--input', str(path), '--format', output_format],
        stdout=stdout, stderr=stderr,
    )
    return code, stdout.getvalue(), stderr.getvalue()
