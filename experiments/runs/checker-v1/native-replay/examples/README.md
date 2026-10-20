# Приём запроса

Минимальный пример с крайними значениями IPv4 и портов:

```sh
python3 -m checker --input examples/boundary_request.json --format json
```

Ожидаемый документ записан в `boundary_expected.json`. UDP-поток от
`0.0.0.0:0` к `255.255.255.255:65535` совпадает с обоими правилами:
сначала `z-deny`, затем `a-permit`. `/0` включает весь IPv4, `/32` — один адрес;
deny не останавливает поиск. Сравнить документы можно из Python:

```python
import json
from pathlib import Path
from examples.cli_usage import capture_report

code, output, diagnostic = capture_report(Path('examples/boundary_request.json'))
expected = json.loads(Path('examples/boundary_expected.json').read_text(encoding='utf-8'))
assert (code, diagnostic) == (0, '')
assert json.loads(output) == expected
```

Полная композиция проверки документа в памяти и сериализации JSON:

```python
from examples.contract_usage import report_document
from src.acl_checker.input.types import ExpectedInputFailure

try:
    report_json = report_document(document)  # разобранный входной JSON v1
except ExpectedInputFailure as error:
    print(f'Checker error: {error.reason}')
else:
    print(report_json, end='')
```

Пример проверяет весь документ до исследования и возвращает строку отчёта,
не печатая её. Ошибка не заменяется пустой успешной группой.

Пример захвата полного результата CLI без запуска дочернего процесса:

```python
from pathlib import Path
from examples.cli_usage import capture_report

code, report, diagnostic = capture_report(Path('examples/input_request.json'))
assert code == 0 and diagnostic == ''
print(report, end='')

code, text, diagnostic = capture_report(Path('examples/input_request.json'), 'text')
assert code == 0 and diagnostic == ''
print(text, end='')
```

При ожидаемой ошибке функция возвращает код 2, пустой отчёт и диагностику
`Checker error: ...` в третьем элементе. Файл читается без изменений.

Из корня репозитория публичный CLI читает локальный синтетический пример:

```sh
python3 -m checker --input examples/input_request.json --format json
```

`fw-a/outside` содержит оба совпадения в порядке `z-deny`, `a-permit`.
`fw-a/inside` и `fw-b/global` получают `NO_MATCH`; нерелевантный снимок
не включается. Общий permit/deny verdict не вычисляется.

Для вызова из Python:

```python
import json
from pathlib import Path

from examples.input_usage import check_document, check_file
from src.acl_checker.input.types import ExpectedInputFailure

path = Path('examples/input_request.json')
try:
    groups = check_file(path)
    same_groups = check_document(json.loads(path.read_text(encoding='utf-8')))
    assert same_groups == groups
except ExpectedInputFailure as error:
    print(f'Checker error: {error.reason}')
```

Оба API сначала проверяют весь документ, включая неиспользуемые снимки.
Неверные данные и отсутствие обязательного снимка вызывают
`ExpectedInputFailure`; частичный успешный отчёт не возвращается.

## Исследование совпадений ACL

`domain_usage.py` показывает `matches` и полный вызов `check` с локальными
источниками для заранее проверенных значений:

```python
from examples.domain_usage import investigate_saved_acl

groups = investigate_saved_acl()
assert groups[0]['status'] == 'MATCHES'
assert [rule['id'] for rule in groups[0]['rules']] == ['z-deny', 'a-permit']
```

Оба правила сохраняются вместе с action и исходными предикатами.
`deny` не останавливает поиск. Это сохранённые свидетельства без общего verdict.
Внешний ввод требует `validate_document`; доменное API принимает проверенные
значения. Отсутствие снимка у внедрённого источника вызывает
`ExpectedApplicationFailure`, а не `NO_MATCH`.

## Отбор и получение снимков ACL

`application_usage.py` показывает два варианта композиции для заранее
проверенных значений: получение полных снимков через `sources` и `evidence`
и полный отчёт через `check`. Например, после проверки документа:

```python
from examples.application_usage import investigate_snapshots, select_snapshots
from src.acl_checker.application.types import ExpectedApplicationFailure
from src.acl_checker.input.validation import validate_document

validate_document(document)  # document — разобранный JSON v1
try:
    snapshots = select_snapshots(
        document['flow'], document['relevance'], document['snapshots'],
    )
    groups = investigate_snapshots(
        document['flow'], document['relevance'], document['snapshots'],
    )
except ExpectedApplicationFailure as error:
    print(f'Checker error: {error.reason}')
```

Повторные пары обрабатываются один раз в порядке первого появления.
Отбор возвращает полные снимки, включая несовпавшие правила; отчёт содержит
только совпавшие правила и сохраняет группы `NO_MATCH`. Отсутствующий снимок
прерывает запрос без частичного результата. Источники локальны для вызова.
