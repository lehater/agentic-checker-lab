from __future__ import annotations
import ast
from pathlib import Path
from importlib.util import resolve_name


ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'src.acl_checker'
OUTER = (PREFIX + '.cli', PREFIX + '.input', PREFIX + '.application.sources',
         'checker', 'tests', 'harness', 'cmind', 'codermind')
SERVICES = set('socket ssl http urllib requests httpx aiohttp ftplib telnetlib '
               'paramiko netmiko napalm scrapli sqlite3 sqlalchemy psycopg psycopg2 '
               'pymongo redis flask fastapi django uvicorn gunicorn socketserver '
               'asyncio threading multiprocessing concurrent celery rq subprocess '
               'openai transformers torch'.split())
IO = set('json pathlib os sys io argparse pickle shelve shutil tempfile glob'.split())
DYNAMIC = {'__import__', 'importlib.import_module', 'importlib.__import__',
           'eval', 'exec', 'compile', 'builtins.eval', 'builtins.exec',
           'builtins.compile', 'builtins.__import__', 'runpy.run_module', 'runpy.run_path'}


def _sources() -> dict[str, ast.Module]:
    sources = {}
    for folder in ('src', 'checker'):
        for path in sorted((ROOT / folder).rglob('*.py')):
            parts = list(path.relative_to(ROOT).with_suffix('').parts)
            if parts[-1] == '__init__':
                parts.pop()
            sources['.'.join(parts)] = ast.parse(path.read_text(encoding='utf-8'))
    assert sources, 'Runtime sources missing'
    return sources


def _name(node: ast.AST | None, aliases: dict[str, str]) -> str:
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return _name(node.value, aliases) + '.' + node.attr
    return ''


def _imports(module: str, tree: ast.Module) -> tuple[set[str], dict[str, str]]:
    dependencies, aliases = set(), {}
    package = module if ROOT.joinpath(*module.split('.')).is_dir() else module.rpartition('.')[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                dependencies.add(item.name)
                aliases[item.asname or item.name.split('.')[0]] = item.name if item.asname else item.name.split('.')[0]
        elif isinstance(node, ast.ImportFrom):
            base = resolve_name('.' * node.level + (node.module or ''), package) if node.level else node.module or ''
            dependencies.add(base)
            for item in node.names:
                full = base + '.' + item.name
                dependencies.add(full)
                aliases[item.asname or item.name] = full
    # Resolve aliases without executing source, including broad exception aliases.
    for _ in range(len(list(ast.walk(tree)))):
        changed = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                value = _name(node.value, aliases)
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and value and aliases.get(target.id) != value:
                        aliases[target.id] = value
                        changed = True
        if not changed:
            break
    return dependencies, aliases


def _inner(module: str) -> bool:
    # sources contains concrete invocation-scoped adapters, despite its directory.
    return (module.startswith((PREFIX + '.domain', PREFIX + '.application'))
            and not module.startswith(PREFIX + '.application.sources'))


def _function(sources: dict[str, ast.Module], name: str) -> tuple[str, ast.FunctionDef]:
    found = [(m, n) for m, tree in sources.items() for n in tree.body
             if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(found) == 1, f'Expected one module-level {name}'
    return found[0]


def test_functional_boundaries() -> None:
    """Проверить разделение matching, orchestration и внешних адаптеров.

    Параметры отсутствуют; pytest вызывает тест напрямую. Возвращает None.
    Читает PythonSourceText как str и анализирует ast.parse: matches остаётся
    чистой операцией, check принимает flow и два узких callable, композиция,
    parsing и serialization находятся снаружи. Проверяет реальное размещение
    функций, включая вложенные каталоги, без требования конкретного алгоритма.
    При нарушении контракта поднимает AssertionError; файлы не изменяет.
    """
    sources = _sources()
    module, matching = _function(sources, 'matches')
    check_module, check = _function(sources, 'check')
    assert module.startswith(PREFIX + '.domain.') and _inner(check_module)
    for function, parameters in ((matching, ['flow', 'rule']),
                                 (check, ['flow', 'relevance', 'snapshot'])):
        assert [a.arg for a in function.args.posonlyargs + function.args.args] == parameters
        assert not function.args.vararg and not function.args.kwarg
        assert not function.args.kwonlyargs and not function.args.defaults
        assert not function.decorator_list
        assert not any(isinstance(n, (ast.Global, ast.Nonlocal, ast.Await,
                                     ast.Yield, ast.YieldFrom)) for n in ast.walk(function))
    assert matching.returns is not None and ast.unparse(matching.returns) == 'bool'
    for source in ('relevance', 'snapshot'):
        assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == source for n in ast.walk(check))
    types = sources[PREFIX + '.application.types']
    for alias in ('RelevanceSource', 'SnapshotSource'):
        value = next(n.value for n in types.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == alias for t in n.targets))
        assert isinstance(value, ast.Subscript) and ast.unparse(value.value).endswith('Callable')
        assert isinstance(value.slice, ast.Tuple)
        assert isinstance(value.slice.elts[0], ast.List) and len(value.slice.elts[0].elts) == 2
    for name in ('validate_document', 'load_request_document', 'parse_invocation',
                 'render_text_report', 'render_json_report',
                 'create_relevance_provider', 'create_snapshot_provider'):
        assert not _inner(_function(sources, name)[0]), name
    _, aliases = _imports(module, sources[module])
    for node in ast.walk(matching):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)):
            targets = node.targets if isinstance(node, (ast.Assign, ast.Delete)) else [node.target]
            for target in targets:
                root = target
                while isinstance(root, (ast.Subscript, ast.Attribute)):
                    root = root.value
                assert not (root is not target and _name(root, aliases) in {'flow', 'rule'})
        if isinstance(node, ast.Call):
            name = _name(node.func, aliases)
            assert name not in {'print', 'input', 'open', 'setattr', 'delattr'}
            assert not any(name.startswith(p + '.') and name.rsplit('.', 1)[-1]
                           in {'update', 'clear', 'pop', 'append', 'extend', 'sort', 'remove'}
                           for p in ('flow', 'rule'))

def test_inward_imports() -> None:
    """Проверить направленность прямых и транзитивных внутренних импортов.

    Параметры отсутствуют; вызывается pytest, возвращает None. Исходники
    domain и application читаются как str и разбираются через ast.parse.
    Проверяет абсолютные и относительные импорты, включая re-export пути:
    внутреннее ядро не зависит от CLI, validation, concrete adapters, JSON,
    filesystem, networking, Harness или CoderMind. Application использует
    domain и собственные контракты источников. Динамический обход запрета
    также считается нарушением; допустимые чистые библиотеки не запрещаются.
    Несоответствие выражается AssertionError, а не изменением исходников.
    """
    sources = _sources()
    # Fixed probes exercise relative/re-export resolution and dynamic aliases
    # without importing or executing the candidate source.
    dependencies, aliases = _imports(PREFIX + '.domain.matching', ast.parse(
        'from ..cli import rendering as output\n'
        'import importlib as loader\nload = loader.import_module\n'))
    assert PREFIX + '.cli.rendering' in dependencies
    assert aliases['load'] == 'importlib.import_module'
    pure, _ = _imports(PREFIX + '.domain.matching', ast.parse(
        'from ipaddress import IPv4Network\nfrom functools import reduce\n'))
    assert not any(d.split('.')[0] in IO | SERVICES for d in pure)
    for start in sources:
        if not _inner(start):
            continue
        pending, seen = [start], set()
        while pending:
            module = pending.pop()
            if module in seen:
                continue
            seen.add(module)
            assert not any(module == p or module.startswith(p + '.') for p in OUTER), (start, module)
            assert module.split('.')[0] not in IO | SERVICES, (start, module)
            if module not in sources:
                continue
            dependencies, aliases = _imports(module, sources[module])
            pending.extend(dependencies)
            for dependency in dependencies:
                parts = dependency.split('.')
                pending.extend('.'.join(parts[:i]) for i in range(1, len(parts))
                               if '.'.join(parts[:i]) in sources)
            for node in ast.walk(sources[module]):
                if isinstance(node, ast.Call):
                    name = _name(node.func, aliases)
                    assert name not in DYNAMIC | {'open', 'print', 'input'}, (module, name)
                    if name in {'getattr', 'builtins.getattr'} and node.args:
                        assert _name(node.args[0], aliases) not in {'builtins', 'importlib', 'sys'}

def test_bounded_runtime_scope() -> None:
    """Проверить статические ограничения runtime принятого прототипа.

    Параметры отсутствуют; pytest получает None либо AssertionError.
    Анализирует runtime-исходники, исключая тестовые subprocess и временные
    файлы: нет сетевых вызовов, серверов, БД, workers, исполнения входных
    значений, записи снимков или глобального изменяемого кеша. Источники
    замыкают данные одного запроса, обработка синхронная. Проверка AST
    дополняется динамическими integration и CLI тестами и не заявляется
    доказательством отсутствия любого возможного побочного эффекта.
    """
    # Runtime roots deliberately exclude test subprocesses and temporary files.
    for module, tree in _sources().items():
        dependencies, aliases = _imports(module, tree)
        assert not any(d.split('.')[0] in SERVICES for d in dependencies), module
        for node in ast.walk(tree):
            assert not isinstance(node, (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor,
                                         ast.AsyncWith, ast.Global, ast.Nonlocal)), module
            if isinstance(node, ast.Call):
                name = _name(node.func, aliases)
                assert name not in DYNAMIC | {'os.system', 'os.popen'}, (module, name)
                assert name.rsplit('.', 1)[-1] not in {'write_text', 'write_bytes',
                       'unlink', 'rename', 'mkdir', 'rmdir', 'touch', 'dump', 'save_snapshot'}, (module, name)
                if name in {'open', 'builtins.open', 'io.open'} or name.endswith('.open'):
                    modes = [k.value for k in node.keywords if k.arg == 'mode']
                    if len(node.args) > 1:
                        modes.append(node.args[1])
                    assert all(isinstance(m, ast.Constant) and isinstance(m.value, str)
                               and not set(m.value) & set('wax+') for m in modes), module
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                assert not any(_name(d.func if isinstance(d, ast.Call) else d, aliases)
                               in {'functools.cache', 'functools.lru_cache'}
                               for d in node.decorator_list), module
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                assert not isinstance(node.value, (ast.List, ast.Dict, ast.Set,
                           ast.ListComp, ast.DictComp, ast.SetComp)), module
                if isinstance(node.value, ast.Call):
                    assert _name(node.value.func, aliases) not in {'list', 'dict', 'set',
                           'collections.defaultdict', 'collections.OrderedDict'}, module

def test_exception_handling_scope() -> None:
    """Проверить узкие границы перехвата ожидаемых отказов.

    Параметры отсутствуют; вызывается pytest, возвращает None.
    Анализирует обработчики runtime: запрещены bare except и blanket
    Exception/BaseException, включая алиасы, кортежи и подавляющие контексты.
    Ожидаемые ошибки чтения, декодирования, JSON и проверки преобразуются
    на соответствующей внешней границе; application не заменяет отказ
    пустым результатом, NO_MATCH, retry или fallback. Нарушения вызывают
    AssertionError; propagation programmer errors проверяется также динамически.
    """
    allowed = {
        PREFIX + '.input.document': {'OSError', 'UnicodeDecodeError', 'ValueError', 'json.JSONDecodeError'},
        PREFIX + '.input.validation': {'ValueError', 'ipaddress.AddressValueError', 'ipaddress.NetmaskValueError'},
        PREFIX + '.application.sources': {'KeyError'},
        PREFIX + '.cli.main': {PREFIX + '.input.types.ExpectedInputFailure',
                              PREFIX + '.application.types.ExpectedApplicationFailure'},
    }
    for module, tree in _sources().items():
        _, aliases = _imports(module, tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                assert node.type is not None, (module, 'bare except')
                types = node.type.elts if isinstance(node.type, ast.Tuple) else [node.type]
                names = {_name(t, aliases).removeprefix('builtins.') for t in types}
                assert names <= allowed.get(module, set()), (module, names)
                assert any(isinstance(n, ast.Raise) for n in ast.walk(node)) or (
                    module == PREFIX + '.cli.main' and any(
                        isinstance(n, ast.Return) and isinstance(n.value, ast.Constant)
                        and n.value.value == 2 for n in ast.walk(node))), module
            if isinstance(node, (ast.With, ast.AsyncWith)):
                for item in node.items:
                    context = item.context_expr
                    if isinstance(context, ast.Call):
                        assert _name(context.func, aliases) != 'contextlib.suppress', module
