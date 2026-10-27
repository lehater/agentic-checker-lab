#!/usr/bin/env python3
"""Zero-dependency architecture guard for Checker RPG skeletons and Python imports.

This checks *mechanically decidable* boundaries only. SOLID/KISS/YAGNI require
separate design review. No model calls, no dependency on CoderMind or Harness.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path, PurePosixPath
import sys

PACKAGE = "src.acl_checker"
INNER = {"domain", "application"}
OUTER = {"cli", "input", "inputs", "infrastructure", "adapters", "presentation"}
DOMAIN_FORBIDDEN = OUTER | {"application"}
APPLICATION_FORBIDDEN = OUTER


def _relative_parts(path: str) -> tuple[str, ...]:
    """Extract layout below the Checker package (not arbitrary outside paths)."""
    parts = PurePosixPath(path.replace("\\", "/")).parts
    if "acl_checker" not in parts:
        return ()
    return parts[parts.index("acl_checker") + 1:]


def _layout_errors(path: str) -> list[str]:
    parts = _relative_parts(path)
    if not parts:
        return []
    layer = parts[0]
    errors: list[str] = []
    if layer == "domain" and any(part in DOMAIN_FORBIDDEN for part in parts[1:-1]):
        errors.append(f"{path}: forbidden outer/application package nested inside domain")
    if layer == "application" and any(part in APPLICATION_FORBIDDEN for part in parts[1:-1]):
        errors.append(f"{path}: forbidden outer adapter nested inside application")
    if layer == "domain" and parts[-1] == "check.py":
        errors.append(f"{path}: Checker check() orchestration must live in application, not domain")
    return errors


def _iter_skeleton_files(node: object):
    if isinstance(node, list):
        for item in node:
            yield from _iter_skeleton_files(item)
    elif isinstance(node, dict):
        if node.get("type") == "file" and isinstance(node.get("path"), str):
            yield node["path"]
        for value in node.values():
            if isinstance(value, (dict, list)):
                yield from _iter_skeleton_files(value)


def check_skeleton(path: Path) -> tuple[list[str], int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    paths = list(dict.fromkeys(_iter_skeleton_files(data.get("root", data))))
    if not paths:
        return [f"{path}: no file paths in RPG skeleton"], 0
    errors: list[str] = []
    for item in paths:
        errors.extend(_layout_errors(item))
    return errors, len(paths)


def _module_name(rel: Path, prefix: str) -> str:
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join([prefix, *parts])


def _imports(node: ast.AST, module: str, is_init: bool):
    package = module if is_init else module.rsplit(".", 1)[0]
    for item in ast.walk(node):
        if isinstance(item, ast.Import):
            for alias in item.names:
                yield alias.name
        elif isinstance(item, ast.ImportFrom):
            if item.level:
                parts = package.split(".")
                keep = len(parts) - item.level + 1
                base = ".".join(parts[:max(0, keep)])
                target = ".".join(x for x in (base, item.module or "") if x)
            else:
                target = item.module or ""
            yield target
            for alias in item.names:
                if alias.name != "*":
                    yield target + "." + alias.name if target else alias.name


def _layer(module: str, prefix: str) -> str | None:
    if not module.startswith(prefix + "."):
        return None
    rest = module[len(prefix) + 1:].split(".")
    return rest[0] if rest else None


def check_source(root: Path, prefix: str) -> tuple[list[str], int]:
    if not root.is_dir():
        return [f"{root}: source directory not found"], 0
    modules: dict[str, tuple[Path, ast.AST]] = {}
    errors: list[str] = []
    for file in sorted(root.rglob("*.py")):
        rel = file.relative_to(root)
        name = _module_name(rel, prefix)
        errors.extend(_layout_errors(file.as_posix()))
        try:
            parsed = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"{file}: Python parse error: {exc}")
            continue
        if name in modules:
            errors.append(f"{file}: duplicate Python module {name}")
            continue
        modules[name] = (file, parsed)
        if rel.parts[0] == "domain":
            if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "check"
                   for n in parsed.body):
                errors.append(f"{file}: use-case function check() belongs in application")
        if rel.parts[0] != "domain":
            if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "matches"
                   for n in parsed.body):
                errors.append(f"{file}: rule predicate matches() belongs in domain")

    edges: dict[str, set[str]] = {name: set() for name in modules}
    for name, (file, parsed) in modules.items():
        origin = _layer(name, prefix)
        for imp in set(_imports(parsed, name, file.name == "__init__.py")):
            destination = _layer(imp, prefix)
            if (origin == "domain" and destination in DOMAIN_FORBIDDEN
                    or origin == "application" and destination in APPLICATION_FORBIDDEN):
                errors.append(f"{file}: forbidden {origin} -> {destination} import: {imp}")
            if imp in modules and imp != name:
                edges[name].add(imp)

    visited: set[str] = set()
    active: set[str] = set()

    def visit(name: str, stack: list[str]) -> None:
        if name in active:
            cycle = stack[stack.index(name):] + [name]
            errors.append("module import cycle: " + " -> ".join(cycle))
            return
        if name in visited:
            return
        active.add(name)
        for target in sorted(edges[name]):
            visit(target, stack + [target])
        active.remove(name)
        visited.add(name)

    for name in sorted(edges):
        visit(name, [name])
    return sorted(set(errors)), len(modules)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skeleton", type=Path, help="CoderMind skeleton.json: check before codegen")
    ap.add_argument("--source-root", type=Path, help="Python source package directory: check after codegen")
    ap.add_argument("--package-prefix", default=PACKAGE, help="Python import prefix (default: src.acl_checker)")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable report")
    args = ap.parse_args()
    if not args.skeleton and not args.source_root:
        ap.error("provide --skeleton and/or --source-root")
    errors: list[str] = []
    counts: dict[str, int] = {}
    try:
        if args.skeleton:
            result, counts["skeleton_files"] = check_skeleton(args.skeleton)
            errors.extend(result)
        if args.source_root:
            result, counts["source_modules"] = check_source(args.source_root, args.package_prefix)
            errors.extend(result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"invalid input: {exc}")
    report = {"status": "FAIL" if errors else "PASS", "checked": counts,
              "violations": sorted(set(errors))}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Architecture " + report["status"] + ": " + str(counts))
        for problem in report["violations"]:
            print(" - " + problem)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
