"""Полный JSON-отчёт из недоверенного документа в памяти."""

from src.acl_checker.cli.rendering import render_json_report
from src.acl_checker.domain.application.check import check
from src.acl_checker.input.validation import validate_document


def report_document(document: object) -> str:
    """Проверить v1, исследовать снимки и сериализовать все группы.

    ExpectedInputFailure передаётся вызывающему коду; ошибочный документ
    не превращается в пустой успешный отчёт. Ввод не изменяется.
    """
    invocation = validate_document(document)
    groups = check(invocation.flow, invocation.relevance, invocation.snapshot)
    return render_json_report(groups)
