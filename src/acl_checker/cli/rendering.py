from __future__ import annotations
import json

from src.acl_checker.application.types import ReportGroups


def render_text_report(groups: ReportGroups) -> str:
    """Сформировать полный текстовый отчёт для публикации через main.

    Args:
        groups: Проверенные группы приложения в порядке первых уникальных
            relevance-пар; правила и placements уже взяты из снимков.

    Returns:
        str: Отчёт с завершающим переводом строки. Для каждой группы:
            'device / acl — status', затем 'placements: <JSON>', затем
            по одной строке на правило со всеми исходными полями, включая
            id, action и обе пары включительных границ портов.
            Пустой список даёт ровно
            'Нет релевантных ACL (synthetic source).\n'.

    NO_MATCH выводится явно и не создаёт implicit deny. Пустые placements
    отображаются как [], без вывода об отсутствии реальных привязок.
    Порядок групп и правил сохраняется, аргумент не изменяется.
    Общий verdict, сетевой путь и live-состояние не вычисляются.
    Функция не пишет в потоки; json.dumps используется для JSON-фрагментов.
    """
    if not groups:
        return 'Нет релевантных ACL (synthetic source).\n'

    lines: list[str] = []
    for group in groups:
        lines.append(f"{group['device']} / {group['acl']} — {group['status']}")
        lines.append('placements: ' + json.dumps(group['placements'], ensure_ascii=False))
        lines.extend(json.dumps(rule, ensure_ascii=False) for rule in group['rules'])
    return '\n'.join(lines) + '\n'


def render_json_report(groups: ReportGroups) -> str:
    """Сериализовать успешный отчёт v1 для публикации через main.

    Args:
        groups: Проверенные группы приложения, включая полные исходные
            правила, placements и статусы MATCHES либо NO_MATCH.

    Returns:
        str: Один JSON-документ с завершающим переводом строки и ровно
            верхними полями version=1 и groups. Каждая группа содержит
            ровно device, acl, placements, status, rules.
            Пустой вход сериализуется с groups=[].

    Сохраняет все исходные значения правил, порядок групп, placements
    и правил. Не изменяет аргумент, не добавляет общий verdict, пояснения
    или синтетические правила и не пишет в потоки. Вызывает json.dumps.
    """
    return json.dumps({'version': 1, 'groups': groups}, ensure_ascii=False) + '\n'
