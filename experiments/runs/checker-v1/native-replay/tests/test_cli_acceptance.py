from __future__ import annotations
from collections.abc import Sequence
from pathlib import Path
import subprocess
import os
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
BASE = {
    'version': 1,
    'flow': {'source': '10.0.0.1', 'destination': '192.0.2.10',
             'protocol': 'tcp', 'source_port': 50000, 'destination_port': 443},
    'relevance': [{'device': 'fw-a', 'acl': 'outside'},
                  {'device': 'fw-a', 'acl': 'inside'},
                  {'device': 'fw-b', 'acl': 'global'},
                  {'device': 'fw-a', 'acl': 'outside'}],
    'snapshots': [
        {'device': 'fw-a', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'}],
         'rules': [
             {'id': 'z-deny', 'source': '10.0.0.0/24',
              'destination': '192.0.2.10/32', 'protocol': 'tcp',
              'source_ports': [50000, 50000], 'destination_ports': [443, 443], 'action': 'deny'},
             {'id': 'a-permit', 'source': '0.0.0.0/0',
              'destination': '192.0.2.0/24', 'protocol': 'any',
              'source_ports': [0, 65535], 'destination_ports': [440, 450], 'action': 'permit'},
             {'id': 'wrong-source', 'source': '10.0.1.0/24',
              'destination': '0.0.0.0/0', 'protocol': 'any',
              'source_ports': [0, 65535], 'destination_ports': [0, 65535], 'action': 'permit'}]},
        {'device': 'fw-a', 'acl': 'inside',
         'placements': [{'interface': 'lan0', 'direction': 'out'}], 'rules': []},
        {'device': 'fw-b', 'acl': 'global', 'placements': [{'global': True}],
         'rules': [{'id': 'udp-only', 'source': '0.0.0.0/0',
                    'destination': '0.0.0.0/0', 'protocol': 'udp',
                    'source_ports': [0, 65535], 'destination_ports': [0, 65535], 'action': 'permit'}]},
        {'device': 'irrelevant', 'acl': 'unused', 'placements': [], 'rules': []}],
}
# Fixed rule indices below are pre-code expectations, never product calculations.
EXPECTED = {'version': 1, 'groups': [
    {'device': 'fw-a', 'acl': 'outside',
     'placements': [{'interface': 'wan0', 'direction': 'in'}],
     'status': 'MATCHES', 'rules': deepcopy(BASE['snapshots'][0]['rules'][:2])},
    {'device': 'fw-a', 'acl': 'inside',
     'placements': [{'interface': 'lan0', 'direction': 'out'}], 'status': 'NO_MATCH', 'rules': []},
    {'device': 'fw-b', 'acl': 'global', 'placements': [{'global': True}],
     'status': 'NO_MATCH', 'rules': []}]}


def run_isolated_cli(argv: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Запустить публичный CLI в отдельном локальном процессе для теста.

    Args:
        argv: Аргументы после 'python3 -m checker', включая явный --input
            для обычного запуска; отрицательные тесты могут его опустить.
        cwd: Рабочий каталог, позволяющий проверить публичный пакет checker
            без Harness/CoderMind и неявных development bootstrap hooks.
    Returns:
        subprocess.CompletedProcess[str]: args, returncode, stdout и stderr;
            ненулевой код возвращается как наблюдение, а не исключение.
    Вызывается приёмочными тестами этого файла. Использует subprocess.run
    с shell=False, capture_output, text, check=False, закрытым stdin и
    конечным тестовым timeout без требования к продуктовой производительности.
    Не импортирует matching, validation, check или rendering для вычисления oracle.
    """
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('PYTHON')}
    environment.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run(
        ['python3', '-m', 'checker', *argv], cwd=cwd, env=environment,
        shell=False, stdin=subprocess.DEVNULL, capture_output=True,
        text=True, encoding='utf-8', check=False, timeout=10,
    )

from pathlib import Path
from tempfile import TemporaryDirectory


def test_cli_exit_behavior() -> None:
    """Проверить публичные коды завершения и разделение потоков CLI.

    Параметры отсутствуют; вызывается pytest, возвращает None.
    Через run_isolated_cli проверяет успех и help: exit 0, пустой stderr;
    help работает без --input и описывает публичную команду и scope.
    Ошибки аргументов, формата, отсутствующий --input, файл, malformed JSON,
    invalid shape, unsupported predicates и missing snapshot дают exit 2,
    строго пустой stdout и 'Checker error: <непустая причина>' в stderr.
    Покрывает отрицательные фиксированные сценарии, NaN/Infinity и поздний
    отказ без частичного отчёта. '-' проверяется как путь, без stdin fallback.
    Байты входных файлов сравниваются до и после запуска в обоих форматах.
    """
    with TemporaryDirectory() as directory:
        path = Path(directory) / 'input.json'
        original = json.dumps(BASE).encode()
        path.write_bytes(original)
        for format_name in ('text', 'json'):
            result = run_isolated_cli(['--input', str(path), '--format', format_name], ROOT)
            assert (result.returncode, result.stderr) == (0, '')
            assert result.stdout
            assert path.read_bytes() == original
        result = run_isolated_cli(['--help'], ROOT)
        assert (result.returncode, result.stderr) == (0, '')
        assert 'python3 -m checker --input PATH [--format text|json]' in result.stdout
        invalid = [[], {}, {'version': 1}]
        for field, value in [('source', '::1'), ('source_port', 65536),
                             ('destination_port', -1), ('source_port', True),
                             ('destination_port', None)]:
            document = deepcopy(BASE)
            document['flow'][field] = value
            invalid.append(document)
        for field in ('source_port', 'destination_port'):
            document = deepcopy(BASE)
            del document['flow'][field]
            invalid.append(document)
        for field, value in [('negate', True), ('source', '10.0.0.1/24'),
                             ('source_ports', 50000), ('source_ports', [2, 1]),
                             ('destination_ports', [False, 443]), ('protocol', 'icmp')]:
            document = deepcopy(BASE)
            document['snapshots'][0]['rules'][0][field] = value
            invalid.append(document)
        for index in (0, 2):  # SC-MISSING and late failure after valid groups.
            document = deepcopy(BASE)
            del document['snapshots'][index]
            invalid.append(document)
        for version in (2, True):
            document = deepcopy(BASE)
            document['version'] = version
            invalid.append(document)
        document = deepcopy(BASE)
        document['relevance_records'] = []
        invalid.append(document)
        payloads = [json.dumps(item).encode() for item in invalid]
        payloads.extend([b'{', b'NaN', b'Infinity', b'-Infinity', b'\xff'])
        for format_name in ('text', 'json'):
            for argv in ([], ['--input'], ['--unknown'],
                         ['--input', str(path), '--format', 'yaml'],
                         ['--input', str(Path(directory) / 'missing.json')],
                         ['--input', directory], ['--input', '-']):
                # Keep invalid format last so argparse cannot override it.
                result = run_isolated_cli(['--format', format_name, *argv], ROOT)
                assert result.returncode == 2, (argv, result)
                assert result.stdout == ''
                assert result.stderr.startswith('Checker error: ')
                assert result.stderr.removeprefix('Checker error: ').strip()
                assert len(result.stderr.splitlines()) == 1
            for payload in payloads:
                path.write_bytes(payload)
                result = run_isolated_cli(['--input', str(path), '--format', format_name], ROOT)
                assert result.returncode == 2, (payload, result)
                assert result.stdout == ''
                assert result.stderr.startswith('Checker error: ')
                assert result.stderr.removeprefix('Checker error: ').strip()
                assert len(result.stderr.splitlines()) == 1
                assert path.read_bytes() == payload

import json
from pathlib import Path
from tempfile import TemporaryDirectory


def test_exact_evidence_groups() -> None:
    """Выполнить все успешные pre-code сценарии через JSON CLI.

    Параметры отсутствуют; pytest получает None либо AssertionError.
    run_isolated_cli запускается отдельно для каждого фиксированного случая
    из принятого сценарного контракта; production helpers не строят expected.
    После json.loads сравниваются точные группы, первые уникальные пары,
    статусы, полные исходные правила, IDs/actions, порядок и placements.
    SC-ALL требует z-deny перед a-permit и две явные NO_MATCH группы;
    покрываются UDP, обе адресные границы, несовпадения и портовые границы.
    Дополнительные фиксированные случаи проверяют пустой relevance и пустые
    placements. Нерелевантный снимок отсутствует в отчёте, совпадения после
    первого сохранены. Исходные файлы остаются неизменными.
    """
    cases = [({}, [0, 1], []), ({'protocol': 'udp'}, [1], [0]),
             ({'source': '10.0.0.0'}, [0, 1], []),
             ({'source': '10.0.0.255'}, [0, 1], []),
             ({'source': '10.0.2.1'}, [1], []),
             ({'destination': '198.51.100.10'}, [], []),
             ({'source_port': 49999}, [1], []), ({'source_port': 50001}, [1], []),
             ({'destination_port': 440}, [1], []),
             ({'destination_port': 450}, [1], []),
             ({'destination_port': 451}, [], [])]
    with TemporaryDirectory() as directory:
        path = Path(directory) / 'scenario.json'
        for changes, outside, global_rules in cases:
            document, expected = deepcopy(BASE), deepcopy(EXPECTED)
            document['flow'].update(changes)
            document['snapshots'].reverse()
            for group_index, snapshot_index, indices in ((0, 0, outside), (2, 2, global_rules)):
                group = expected['groups'][group_index]
                group['rules'] = [deepcopy(BASE['snapshots'][snapshot_index]['rules'][i]) for i in indices]
                group['status'] = 'MATCHES' if indices else 'NO_MATCH'
            original = json.dumps(document).encode()
            path.write_bytes(original)
            result = run_isolated_cli(['--input', str(path), '--format', 'json'], ROOT)
            assert (result.returncode, result.stderr) == (0, ''), changes
            assert json.loads(result.stdout) == expected, changes
            assert path.read_bytes() == original

import json
from pathlib import Path
from tempfile import TemporaryDirectory


def test_evidence_interpretation_limits() -> None:
    """Проверить допустимые выводы публичного отчёта и help.

    Параметры отсутствуют; вызывается pytest, возвращает None.
    Запускает через run_isolated_cli text/json и help с фиксированными
    смешанными permit/deny, NO_MATCH, пустыми placements и переставленным
    relevance. Проверяет отсутствие общего verdict и выдуманных implicit
    deny правил; порядок отражает предоставленные пары, а не найденный путь.
    Help описывает synthetic saved evidence без обещаний live truth,
    freshness/SLA или сетевых привязок. Текст не превращает NO_MATCH в deny
    и пустые placements в утверждение об отсутствии реальных привязок.
    JSON проверяется структурно, без запрета слова verdict внутри входных ID.
    """
    document, expected = deepcopy(BASE), deepcopy(EXPECTED)
    document['snapshots'][0]['placements'] = []
    document['snapshots'][0]['rules'][0]['id'] = 'verdict-is-an-input-id'
    document['relevance'] = [BASE['relevance'][2], BASE['relevance'][0],
                             BASE['relevance'][1], BASE['relevance'][2]]
    expected['groups'][0]['placements'] = []
    expected['groups'][0]['rules'][0]['id'] = 'verdict-is-an-input-id'
    expected['groups'] = [expected['groups'][2], expected['groups'][0], expected['groups'][1]]
    with TemporaryDirectory() as directory:
        path = Path(directory) / 'evidence.json'
        original = json.dumps(document).encode()
        path.write_bytes(original)
        for format_name in ('text', 'json'):
            result = run_isolated_cli(['--input', str(path), '--format', format_name], ROOT)
            assert (result.returncode, result.stderr) == (0, '')
            if format_name == 'json':
                assert json.loads(result.stdout) == expected
            else:
                lines = result.stdout.splitlines()
                assert lines[:4] == ['fw-b / global — NO_MATCH', 'placements: [{"global": true}]',
                                     'fw-a / outside — MATCHES', 'placements: []']
                assert [json.loads(line) for line in lines[4:6]] == expected['groups'][1]['rules']
                assert lines[6:] == ['fw-a / inside — NO_MATCH',
                                      'placements: [{"interface": "lan0", "direction": "out"}]']
            assert path.read_bytes() == original
    result = run_isolated_cli(['--help'], ROOT)
    assert (result.returncode, result.stderr) == (0, '')
    help_text = ' '.join(result.stdout.split())
    for phrase in ('synthetic', 'сохранённые правила', 'без live truth',
                   'не означает сетевой путь', 'не доказывает отсутствие привязок',
                   'NO_MATCH не означает deny', 'implicit deny не создаётся', 'SLA/TTL не заявлены'):
        assert phrase in help_text

import json
from pathlib import Path
from tempfile import TemporaryDirectory


def test_public_output_formats() -> None:
    """Проверить точную публичную схему JSON и содержание text.

    Параметры отсутствуют; pytest получает None либо AssertionError.
    Через run_isolated_cli проверяет default text, явный text и json.
    JSON содержит ровно version=1 и groups; каждая группа содержит ровно
    device, acl, placements, status, rules. Проверяются типы, полные поля
    правил и статусы MATCHES/NO_MATCH без matches/device_id/acl_id замен.
    Text содержит 'device / acl — status', 'placements: <JSON>' и строки
    со всеми полями каждого правила; default совпадает с явным text.
    Для пустого relevance ожидается ровно
    'Нет релевантных ACL (synthetic source).\n', а JSON имеет пустой groups.
    Успех означает exit 0 и пустой stderr; expected не берётся из rendering.
    """
    with TemporaryDirectory() as directory:
        path = Path(directory) / 'formats.json'
        for empty in (False, True):
            document = deepcopy(BASE)
            if empty:
                document['relevance'] = []
            original = json.dumps(document).encode()
            path.write_bytes(original)
            outputs = []
            for arguments in ([], ['--format', 'text'], ['--format', 'json']):
                result = run_isolated_cli(['--input', str(path), *arguments], ROOT)
                assert (result.returncode, result.stderr) == (0, '')
                outputs.append(result.stdout)
                assert path.read_bytes() == original
            assert outputs[0] == outputs[1]
            report = json.loads(outputs[2])
            assert report == ({'version': 1, 'groups': []} if empty else EXPECTED)
            assert set(report) == {'version', 'groups'}
            assert type(report['version']) is int
            if empty:
                assert outputs[0] == 'Нет релевантных ACL (synthetic source).\n'
                continue
            expected_lines = []
            for group in EXPECTED['groups']:
                expected_lines.extend([f"{group['device']} / {group['acl']} — {group['status']}",
                                       'placements: ' + json.dumps(group['placements'])])
                expected_lines.extend(json.dumps(rule) for rule in group['rules'])
            assert outputs[0] == '\n'.join(expected_lines) + '\n'
            for group in report['groups']:
                assert set(group) == {'device', 'acl', 'placements', 'status', 'rules'}
                assert isinstance(group['device'], str)
                assert isinstance(group['acl'], str)
                assert isinstance(group['placements'], list)
                assert isinstance(group['rules'], list)
