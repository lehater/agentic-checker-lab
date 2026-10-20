import importlib
import runpy
import sys
from io import StringIO
from unittest.mock import patch

import pytest


@pytest.mark.parametrize('argv, exit_code', [
    (['--input', 'request.json', '--format', 'json'], 0),
    ([], 2),
])
def test_main_delegates_arguments_streams_and_exit_code(monkeypatch, argv, exit_code):
    entrypoint = importlib.import_module('checker.__main__')
    stdout, stderr = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'argv', ['checker', *argv])
    monkeypatch.setattr(sys, 'stdout', stdout)
    monkeypatch.setattr(sys, 'stderr', stderr)
    with patch('src.acl_checker.cli.main.main', autospec=True,
               return_value=exit_code) as cli_main:
        assert entrypoint.main() == exit_code
    cli_main.assert_called_once_with(argv, stdout=stdout, stderr=stderr)
    assert stdout.getvalue() == stderr.getvalue() == ''
    assert sys.argv == ['checker', *argv]


def test_main_propagates_cli_programming_error():
    entrypoint = importlib.import_module('checker.__main__')
    error = RuntimeError('CLI bug')
    with patch('src.acl_checker.cli.main.main', autospec=True,
               side_effect=error) as cli_main:
        with pytest.raises(RuntimeError) as failure:
            entrypoint.main()
    assert failure.value is error
    cli_main.assert_called_once()


@pytest.mark.parametrize('exit_code', [0, 2])
def test_module_execution_exits_with_cli_code(monkeypatch, exit_code):
    stdout, stderr = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'argv', ['checker', '--help'])
    monkeypatch.setattr(sys, 'stdout', stdout)
    monkeypatch.setattr(sys, 'stderr', stderr)
    # Run in-process: only the CLI boundary is replaced, not the entrypoint.
    with patch('src.acl_checker.cli.main.main', autospec=True,
               return_value=exit_code) as cli_main:
        with pytest.raises(SystemExit) as failure:
            runpy.run_module('checker', run_name='__main__')
    assert failure.value.code == exit_code
    cli_main.assert_called_once_with(['--help'], stdout=stdout, stderr=stderr)
