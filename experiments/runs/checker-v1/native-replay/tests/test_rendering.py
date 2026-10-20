import json
from copy import deepcopy

import pytest

from src.acl_checker.cli.rendering import render_json_report, render_text_report


@pytest.fixture
def groups():
    rules = [
        {'id': identifier, 'source': '10.0.0.0/24',
         'destination': '192.0.2.10/32', 'protocol': 'any',
         'source_ports': [0, 65535], 'destination_ports': [440, 450],
         'action': action}
        for identifier, action in [('z-deny', 'deny'), ('a-permit', 'permit')]
    ]
    return [
        {'device': 'fw-б', 'acl': 'outside',
         'placements': [{'interface': 'wan0', 'direction': 'in'},
                        {'global': True}],
         'status': 'MATCHES', 'rules': rules},
        {'device': 'fw-a', 'acl': 'inside', 'placements': [],
         'status': 'NO_MATCH', 'rules': []},
    ]


def test_json_report_preserves_complete_ordered_groups(groups):
    result = render_json_report(groups)

    assert result.endswith('\n')
    assert json.loads(result) == {'version': 1, 'groups': groups}
    assert type(json.loads(result)['version']) is int


def test_text_report_has_headers_placements_and_complete_rule_lines(groups):
    lines = render_text_report(groups).splitlines()

    assert lines[0] == 'fw-б / outside — MATCHES'
    assert lines[1].startswith('placements: ')
    assert json.loads(lines[1].removeprefix('placements: ')) == groups[0]['placements']
    # Full JSON objects are the simplest unambiguous rule-line representation.
    assert [json.loads(line) for line in lines[2:4]] == groups[0]['rules']
    assert lines[4:] == ['fw-a / inside — NO_MATCH', 'placements: []']


def test_empty_reports():
    assert render_text_report([]) == 'Нет релевантных ACL (synthetic source).\n'
    assert json.loads(render_json_report([])) == {'version': 1, 'groups': []}
    assert render_json_report([]).endswith('\n')


@pytest.mark.parametrize('render', [render_text_report, render_json_report])
def test_rendering_is_repeatable_and_does_not_mutate_or_print(render, groups, capsys):
    before = deepcopy(groups)

    result = render(groups)

    assert result == render(groups)
    assert result.endswith('\n') and not result.endswith('\n\n')
    assert groups == before
    captured = capsys.readouterr()
    assert captured.out == captured.err == ''


@pytest.mark.parametrize('render', [render_text_report, render_json_report])
def test_serialization_error_propagates_without_partial_output(render, groups, capsys):
    # Invalid internal data is a programming error, not a NO_MATCH result.
    groups[1]['placements'] = [object()]

    with pytest.raises(TypeError):
        render(groups)

    captured = capsys.readouterr()
    assert captured.out == captured.err == ''
