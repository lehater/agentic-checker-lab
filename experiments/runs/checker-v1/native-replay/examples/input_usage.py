"""Композиция input API с приложением; без печати и изменения данных."""

from pathlib import Path

from src.acl_checker.application.types import ReportGroups
from src.acl_checker.domain.application.check import check
from src.acl_checker.input.document import load_request_document
from src.acl_checker.input.validation import validate_document


def check_file(path: Path) -> ReportGroups:
    """Прочитать UTF-8 JSON; ExpectedInputFailure передать вызывающему коду."""
    invocation = load_request_document(path)
    return check(invocation.flow, invocation.relevance, invocation.snapshot)


def check_document(document: object) -> ReportGroups:
    """Проверить уже разобранный документ и исследовать все релевантные ACL."""
    invocation = validate_document(document)
    return check(invocation.flow, invocation.relevance, invocation.snapshot)
