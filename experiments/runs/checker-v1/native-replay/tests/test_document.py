import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.acl_checker.input.document import load_request_document
from src.acl_checker.input.types import ExpectedInputFailure, ValidatedInvocation


def test_load_valid_utf8_document_without_side_effects(tmp_path, capsys):
    value = {
        'version': 1,
        'flow': {'source': '10.0.0.1', 'destination': '192.0.2.10',
                 'protocol': 'tcp', 'source_port': 0, 'destination_port': 65535},
        'relevance': [{'device': 'экран', 'acl': 'outside'}],
        'snapshots': [{'device': 'экран', 'acl': 'outside',
                       'placements': [], 'rules': []}],
    }
    path = tmp_path / 'request.json'
    content = json.dumps(value, ensure_ascii=False).encode('utf-8')
    path.write_bytes(content)

    result = load_request_document(path)

    assert isinstance(result, ValidatedInvocation)
    assert result.flow == value['flow']
    assert result.relevance('10.0.0.1', '192.0.2.10') == value['relevance']
    assert result.snapshot('экран', 'outside') == value['snapshots'][0]
    assert path.read_bytes() == content
    assert capsys.readouterr() == ('', '')


def test_relative_paths_and_dash_are_local_filenames(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for name in ('request.json', '-'):
        Path(name).write_text('["данные", 1, null]', encoding='utf-8')
        with patch('src.acl_checker.input.document.validate_document',
                   autospec=True) as validator:
            result = load_request_document(Path(name))
        validator.assert_called_once_with(['данные', 1, None])
        assert result is validator.return_value


def test_read_errors_keep_original_cause(tmp_path):
    for path in (tmp_path / 'missing.json', tmp_path):
        with pytest.raises(ExpectedInputFailure) as failure:
            load_request_document(path)
        assert isinstance(failure.value.__cause__, OSError)
        assert str(path) in failure.value.reason


def test_invalid_utf8_is_rejected(tmp_path):
    path = tmp_path / 'invalid.json'
    path.write_bytes(b'{"value": "\xff"}')
    with pytest.raises(ExpectedInputFailure) as failure:
        load_request_document(path)
    assert isinstance(failure.value.__cause__, UnicodeDecodeError)
    assert 'utf-8' in failure.value.reason.lower()


def test_malformed_json_keeps_parse_cause(tmp_path):
    path = tmp_path / 'broken.json'
    path.write_text('{"version":', encoding='utf-8')
    with pytest.raises(ExpectedInputFailure) as failure:
        load_request_document(path)
    assert isinstance(failure.value.__cause__, json.JSONDecodeError)
    assert 'json' in failure.value.reason.lower()


def test_nonstandard_constants_are_rejected_before_validation(tmp_path):
    path = tmp_path / 'constant.json'
    for constant in ('NaN', 'Infinity', '-Infinity'):
        path.write_text('{"value": ' + constant + '}', encoding='utf-8')
        with patch('src.acl_checker.input.document.validate_document',
                   autospec=True) as validator:
            with pytest.raises(ExpectedInputFailure) as failure:
                load_request_document(path)
        validator.assert_not_called()
        assert isinstance(failure.value.__cause__, ValueError)
        assert constant in failure.value.reason


def test_validator_failures_propagate_unchanged(tmp_path):
    path = tmp_path / 'request.json'
    path.write_text('null', encoding='utf-8')
    for error in (ExpectedInputFailure('schema rejected'), ValueError('bug')):
        with patch('src.acl_checker.input.document.validate_document',
                   autospec=True, side_effect=error) as validator:
            with pytest.raises(type(error)) as failure:
                load_request_document(path)
        validator.assert_called_once_with(None)
        assert failure.value is error
