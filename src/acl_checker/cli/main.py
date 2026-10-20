from __future__ import annotations
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import TextIO

from src.acl_checker.domain.application.check import check
from src.acl_checker.application.types import ExpectedApplicationFailure
from src.acl_checker.cli.rendering import render_json_report, render_text_report
from src.acl_checker.input.document import load_request_document
from src.acl_checker.input.types import ExpectedInputFailure


@dataclass(frozen=True)
class CliOptions:
    input_path: Path
    format: str


class _InvocationParser(ArgumentParser):
    def error(self, message: str) -> None:
        raise ExpectedInputFailure(
            f'{message}. Справка: python3 -m checker --help'
        )


def parse_invocation(argv: Sequence[str], stdout: TextIO) -> CliOptions | None:
    """Разобрать параметры либо вывести справку для main.

    Args:
        argv: Аргументы без имени программы. Поддерживаются --input PATH,
            --format text|json и -h/--help; формат по умолчанию text.
        stdout: TextIO для справки; обычный разбор ничего не печатает.

    Returns:
        CliOptions | None: Параметры запуска либо None после справки.
        Справка не требует --input, не загружает файл и означает exit 0.

    Raises:
        ExpectedInputFailure: Отсутствующий --input, неизвестный аргумент,
            неверный формат или другой отказ разбора. Диагностику печатает
            main; парсер не завершает процесс и не пишет в stderr.

    Использует ArgumentParser с переводом ошибок разбора в указанный отказ,
    без стандартного error-exit. Значение '-' является именем файла,
    stdin не подразумевается. Path не проверяется чтением на этом этапе.
    Справка показывает 'python3 -m checker --input PATH [--format text|json]'
    и объясняет локальный synthetic scope: IPv4 TCP/UDP, оба порта,
    все совпавшие сохранённые правила, отсутствие live truth и общего
    verdict. Порядок релевантности не означает сетевой путь; placements
    описывают только предоставленные сведения; SLA/TTL не заявлены.
    """
    parser = _InvocationParser(
        prog='python3 -m checker',
        usage='python3 -m checker --input PATH [--format text|json]',
        add_help=False,
        allow_abbrev=False,
        formatter_class=RawDescriptionHelpFormatter,
        description=(
            'Локальный synthetic Checker: IPv4 TCP/UDP, оба порта обязательны '
            '(0..65535). Показывает все совпавшие сохранённые правила, '
            'без live truth и общего end-to-end verdict.'
        ),
        epilog=(
            'Релевантность synthetic: порядок ACL не означает сетевой путь. '
            'placements содержат только предоставленные сведения; пустой список '
            'не доказывает отсутствие привязок в сети. NO_MATCH не означает deny; '
            'implicit deny не создаётся. Свежесть, SLA/TTL не заявлены. '
            'Только локальные данные, без обращения к устройствам и сети.\n\n'
            'Форматы:\n'
            '  text — группы ACL и полные правила (по умолчанию)\n'
            '  json — документ v1 для автоматизации\n\n'
            'Примеры (request.json — ваш входной файл):\n'
            '  python3 -m checker --input request.json\n'
            '  python3 -m checker --input request.json --format json\n'
            '\nКоды завершения: 0 — отчёт или справка; 2 — ошибка запроса.'
        ),
    )
    parser.add_argument('-h', '--help', action='store_true', help='показать справку')
    parser.add_argument('--input', type=Path, metavar='PATH',
                        help="обязательный локальный JSON UTF-8 файл; '-' — имя файла")
    parser.add_argument('--format', choices=('text', 'json'), default='text',
                        help='формат отчёта (по умолчанию text)')
    options = parser.parse_args(argv)
    if options.help:
        parser.print_help(file=stdout)
        return None
    if options.input is None:
        parser.error('the following arguments are required: --input')
    return CliOptions(input_path=options.input, format=options.format)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Выполнить один локальный запрос и вернуть код публичного CLI.

    Args:
        argv: Аргументы без имени программы; None использует sys.argv[1:].
        stdout: Поток успешного отчёта или справки; None использует sys.stdout.
        stderr: Поток диагностики; None использует sys.stderr.

    Returns:
        int: 0 после отчёта или справки; 2 при ExpectedInputFailure либо
            ExpectedApplicationFailure. Функция сама не завершает процесс.

    Вызывается публичным checker/__main__.py через SystemExit(main()).
    Последовательно вызывает parse_invocation, load_request_document,
    check(invocation.flow, invocation.relevance, invocation.snapshot)
    и выбранный render_text_report либо render_json_report.
    Источники уже созданы валидатором; повторная композиция не требуется.

    Успешный отчёт полностью вычисляется и сериализуется до записи stdout.
    При ожидаемом отказе stdout пуст, stderr получает ровно
    'Checker error: <reason>\n'; частичный отчёт не публикуется.
    Причина выводится одной строкой с экранированием встроенных CR/LF.
    Не перехватывает blanket Exception и не подавляет ошибки программиста.

    Код завершения и записи в потоки вместе с argv дают внешним приёмочным
    тестам ProcessObservation; CLI не импортирует проверочные структуры.
    Не изменяет входные данные, не сохраняет результаты и не обращается
    к сети. JSON-успех не содержит текстовых пояснений.
    """
    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    arguments = sys.argv[1:] if argv is None else argv
    try:
        options = parse_invocation(arguments, output)
        if options is None:
            return 0
        invocation = load_request_document(options.input_path)
        groups = check(invocation.flow, invocation.relevance, invocation.snapshot)
        render = render_json_report if options.format == 'json' else render_text_report
        report = render(groups)
    except (ExpectedInputFailure, ExpectedApplicationFailure) as error:
        reason = error.reason.replace('\r', '\\r').replace('\n', '\\n')
        errors.write(f'Checker error: {reason}\n')
        return 2
    output.write(report)
    return 0
