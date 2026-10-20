"""Проверки справки и диагностики CLI без запуска подпроцессов."""

import json
from io import StringIO

import pytest

from src.acl_checker.cli.main import main


def test_help_provides_copyable_examples_and_format_descriptions():
    stdout, stderr = StringIO(), StringIO()

    assert main(['--help'], stdout=stdout, stderr=stderr) == 0

    help_text = stdout.getvalue()
    assert 'python3 -m checker --input request.json\n' in help_text
    assert 'python3 -m checker --input request.json --format json\n' in help_text
    assert 'text — группы ACL и полные правила' in help_text
    assert 'json — документ v1 для автоматизации' in help_text
    assert stderr.getvalue() == ''


@pytest.mark.parametrize('arguments', [[], ['--input'], ['--format', 'yaml']])
def test_argument_errors_point_to_help_without_printing_a_report(arguments):
    stdout, stderr = StringIO(), StringIO()

    assert main(arguments, stdout=stdout, stderr=stderr) == 2

    assert stdout.getvalue() == ''
    assert stderr.getvalue().startswith('Checker error: ')
    assert 'python3 -m checker --help' in stderr.getvalue()
    assert len(stderr.getvalue().splitlines()) == 1


@pytest.mark.parametrize('relevance, snapshots, expected', [
    ([], [], 'Нет релевантных ACL (synthetic source).\n'),
    ([{'device': 'fw', 'acl': 'outside'}],
     [{'device': 'fw', 'acl': 'outside', 'placements': [], 'rules': []}],
     'fw / outside — NO_MATCH\nplacements: []\n'),
])
def test_basic_command_displays_explicit_empty_states(tmp_path, relevance, snapshots, expected):
    # Сохраняем точные строки контракта: отсутствие совпадений не означает deny.
    path = tmp_path / 'request.json'
    path.write_text(json.dumps({
        'version': 1,
        'flow': {'source': '10.0.0.1', 'destination': '192.0.2.1',
                 'protocol': 'tcp', 'source_port': 0, 'destination_port': 65535},
        'relevance': relevance, 'snapshots': snapshots,
    }), encoding='utf-8')
    stdout, stderr = StringIO(), StringIO()

    assert main(['--input', str(path)], stdout=stdout, stderr=stderr) == 0

    assert stdout.getvalue() == expected
    assert stderr.getvalue() == ''
