from __future__ import annotations
import json
from pathlib import Path

from src.acl_checker.input.types import ExpectedInputFailure, ValidatedInvocation
from src.acl_checker.input.validation import validate_document


def load_request_document(path: Path) -> ValidatedInvocation:
    """Прочитать локальный JSON-файл и вернуть проверенный запрос.

    Args:
        path: Явный путь входного файла из обязательного CLI --input.
            Относительный путь разрешается относительно рабочего каталога.
            Значение '-' не означает stdin; неявного источника ввода нет.

    Returns:
        ValidatedInvocation: Результат validate_document после чтения UTF-8
            и разбора JSON; готов для внешнего вызова check с его тремя полями.

    Raises:
        ExpectedInputFailure: Ошибка чтения OSError, некорректный UTF-8,
            ошибка разбора JSON или отказ validate_document. reason содержит
            понятную причину; исходная причина сохраняется через chaining.
            Нестандартные JSON-константы NaN и Infinity отвергаются.

    Файл открывается только для чтения. Значения не исполняются; сетевые
    запросы, запись файлов и чтение stdin не выполняются. Проверка схемы
    полностью делегируется validate_document. Перехватываются только
    ожидаемые ошибки границы; blanket except Exception запрещён.
    Функция не печатает и не завершает процесс: внешний CLI преобразует
    ExpectedInputFailure в exit 2, пустой stdout и stderr
    'Checker error: <reason>'.
    """
    try:
        content = path.read_text(encoding='utf-8')
    except OSError as error:
        raise ExpectedInputFailure(f'Cannot read {path}: {error}') from error
    except UnicodeDecodeError as error:
        raise ExpectedInputFailure(f'Invalid UTF-8 in {path}: {error}') from error

    def reject_constant(value: str) -> None:
        raise ValueError(f'Nonstandard JSON constant {value}')

    try:
        document = json.loads(content, parse_constant=reject_constant)
    except ValueError as error:
        raise ExpectedInputFailure(f'Invalid JSON in {path}: {error}') from error

    return validate_document(document)
